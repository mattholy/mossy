# -*- encoding: utf-8 -*-
'''
main.py
----
mossy main entry point.


@Time    :   2024/04/11 17:33:24
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

# FastAPI相关
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

# Python标准库
from pathlib import Path
from contextlib import asynccontextmanager

# mossy
from routers.api.router import router as api_router
from routers.wellknown.router import router as wellknown_router
from routers.nodeinfo.router import router as nodeinfo_router
from routers.setup.router import router as setup_router
from routers.oauth.router import router as oauth_router
from routers.public.router import router as public_router
from utils.logger import async_log_error_to_db, logger
from env import NODE_ID, BACKEND_URL, ALLOWED_ORIGINS
from utils.system.security import async_load_key_pair
from utils.init import init_node, ready
from utils.model.orm import NodeType

# 其它
import uuid
import time
from sqlalchemy.exc import ProgrammingError


@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_id = str(uuid.uuid4())
    private_key, public_key = await async_load_key_pair()
    init_node(public_key, NodeType.fastapi)
    logger.info(f"Starting FastAPI worker: {NODE_ID}: {worker_id}")
    app.state.node_id = NODE_ID
    app.state.worker_id = worker_id
    app.state.public_key = public_key
    app.state.private_key = private_key
    yield
    init_node(public_key, NodeType.fastapi, status=False)
    logger.warn(f"Stopping FastAPI worker: {NODE_ID}: {worker_id}")


# 创建FastAPI实例
app = FastAPI(lifespan=lifespan)


@app.get("/", name="Frontend Pages")
async def read_index(request: Request):
    index_path = Path("static/index.html")
    if not index_path.is_file():
        return PlainTextResponse(content=f"Backend server is running. Response from node {request.app.state.node_id} worker {request.app.state.worker_id}")
    return FileResponse(index_path)


@app.get("/test", name="Frontend Pages")
async def read_index():
    return PlainTextResponse('test_page')


@app.get("/favicon.ico", name="Frontend Pages")
async def fetch_favicon():
    return FileResponse("logo.png")

# 导入路由
app.include_router(api_router)
app.include_router(wellknown_router)
app.include_router(nodeinfo_router)
app.include_router(setup_router)
app.include_router(oauth_router)
app.include_router(public_router)

# 静态文件服务
app.mount("/", StaticFiles(directory="static"), name="Frontend Pages")

# 异常处理


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if (not isinstance(exc, (HTTPException, StarletteHTTPException))):
        raise exc
    handle_dict: dict[int, JSONResponse] = {
        400: JSONResponse(
            content={
                "status": "CLIENT_ERROR",
                "msg": "InvalidData",
                "payload": exc.detail
            },
            status_code=400,
        ),
        401: JSONResponse(
            content={
                "status": "CLIENT_ERROR",
                "msg": "InvalidToken",
                "payload": exc.detail
            },
            status_code=401,
        ),
        403: JSONResponse(
            content={
                "status": "CLIENT_ERROR",
                "msg": "PermissionDenied",
                "payload": exc.detail
            },
            status_code=403
        ),
        404: JSONResponse(
            content={
                "status": "CLIENT_ERROR",
                "msg": "EndpointNotExists",
                "payload": exc.detail
            },
            status_code=404,
        ),
        406: JSONResponse(
            content={
                "status": "CLIENT_ERROR",
                "msg": "RequestNotUnderstandable",
                "payload": exc.detail
            },
            status_code=406,
        ),
        410: JSONResponse(
            content={
                "status": "CLIENT_ERROR",
                "msg": "ResourceDeleted",
                "payload": exc.detail
            },
            status_code=406,
        ),
        503: JSONResponse(
            content={
                "status": "SERVER_ERROR",
                "msg": "ServiceUnavailable",
                "payload": exc.detail
            },
            status_code=503,
        ),
    }
    res: JSONResponse | None = handle_dict.get(exc.status_code)
    if res:
        return res
    else:
        raise exc

# 中间件


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f} ms"
    return response


@app.middleware("http")
async def internal_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.error(f"An error occurred when access {
                     request.url}: ", exc_info=True)
        exception_id = await async_log_error_to_db(
            exc, request.app.state.node_id, request.app.state.worker_id)
        return JSONResponse(
            content={
                "status": "SERVER_ERROR",
                "msg": "UnknownError",
                "payload": {
                    "exception_id": exception_id,
                    "instruction": 'Please contact the administrator with the exception_id.'
                }
            },
            status_code=500,
            headers={"X-Error": exception_id},
        )


@app.middleware("http")
async def check_server_ready(request: Request, call_next):
    if request.url.path in ['/', '/favicon.ico', '/setup/status', '/setup/init', '/docs', '/openapi.json'] or request.url.path.startswith('/assets'):
        return await call_next(request)
    else:
        if ready():
            return await call_next(request)
        else:
            return JSONResponse(
                content={
                    "status": "SERVER_ERROR",
                    "msg": "ServiceInitializing",
                    "payload": {
                        "instruction": f'This endpoint is not available now. The Server is not ready. Please finish setup.',
                        'setup_url': f'{BACKEND_URL}'
                    }
                },
                status_code=425,
            )


@app.middleware("http")
async def add_worker_info(request: Request, call_next):
    start_time = time.time()
    logger.debug('Incoming request with header: ' + str({key: value for key, value in request.headers.items()}) + ' body: ' + str(await request.body()))
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Total-Time"] = f"{process_time:.2f} ms"
    response.headers["X-Worker-ID"] = request.app.state.worker_id
    response.headers["X-Node-ID"] = request.app.state.node_id
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[ALLOWED_ORIGINS])
