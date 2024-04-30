from fastapi.testclient import TestClient
from main import app  # 使用绝对导入来引用FastAPI实例

client = TestClient(app)


def test_read_index():
    response = client.get("/")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert response.headers['content-type'] == 'text/plain; charset=utf-8'
    else:
        assert response.json() == {"detail": "后台服务器运行正常，但前端页面未找到。"}
