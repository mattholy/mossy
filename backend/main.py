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
from utils.logger import async_log_error_to_db, logger
from env import NODE_ID, BACKEND_URL
from utils.system.security import async_load_key_pair
from utils.init import init_node, ready
from utils.model.orm import NodeType

# 其它
import uuid
from sqlalchemy.exc import ProgrammingError

worker_info_dict = {
    'node_id': NODE_ID
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_id = str(uuid.uuid4())
    worker_info_dict['worker_id'] = worker_id
    private_key, public_key = await async_load_key_pair()
    worker_info_dict['private_key'] = private_key
    worker_info_dict['public_key'] = public_key
    if ready():
        init_node(public_key, NodeType.fastapi)
    logger.info(f"Starting FastAPI worker: {
        worker_info_dict['node_id']}: {worker_id}")
    yield
    if ready():
        init_node(public_key, NodeType.fastapi, status=False)
    logger.error(f"Stopping FastAPI worker: {
        worker_info_dict['node_id']}: {worker_id}")


# 创建FastAPI实例
app = FastAPI(lifespan=lifespan)


@app.get("/", name="Frontend Pages")
async def read_index():
    index_path = Path("static/index.html")
    if not index_path.is_file():
        return PlainTextResponse(content=f"Backend server is running. Response from node {worker_info_dict['node_id']} worker {worker_info_dict['worker_id']}")
    return FileResponse(index_path)


@app.get("/test", name="Frontend Pages")
async def read_index():
    return PlainTextResponse('test_page')

# 导入路由
app.include_router(api_router)
app.include_router(wellknown_router)
app.include_router(nodeinfo_router)
app.include_router(setup_router)

# 静态文件服务
try:
    app.mount("/", StaticFiles(directory="static"), name="Frontend Pages")
except RuntimeError:
    pass

# 异常处理


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if (not isinstance(exc, (HTTPException, StarletteHTTPException))):
        raise exc
    handle_dict: dict[int, JSONResponse] = {
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
async def internal_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.error(f"An error occurred when access {
                     request.url}: ", exc_info=True)
        exception_id = await async_log_error_to_db(
            exc, worker_info_dict['node_id'], worker_info_dict['worker_id'])
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
    if request.url.path in ['/', '/setup/status', '/setup/init', '/docs', '/openapi.json']:
        return await call_next(request)
    else:
        if ready():
            return await call_next(request)
        else:
            return JSONResponse(
                content={
                    "status": "SERVER_ERROR",
                    "msg": "ServiceUnavailable",
                    "payload": {
                        "instruction": f'This endpoint is not available now. The Server is not ready. Please finish setuppp.',
                        'setup_url': f'{BACKEND_URL}'
                    }
                },
                status_code=503,
            )


@app.middleware("http")
async def add_worker_info(request: Request, call_next):
    logger.debug('Incoming request with header: ' + str({key: value for key, value in request.headers.items()}) + ' body: ' + str(await request.body()))
    response = await call_next(request)
    response.headers["X-Worker-ID"] = worker_info_dict['worker_id']
    response.headers["X-Node-ID"] = worker_info_dict['node_id']
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['*'])
