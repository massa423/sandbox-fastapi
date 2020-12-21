from fastapi.testclient import TestClient
from intro import app

client = TestClient(app)


def test_read_hello():
    """
    test_read_hello
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"text": "hello world"}


def test_read_declare_request_body():
    """
    test_read_declare_request_body
    """
    response = client.post(
        "/post",
        json={
            "string": "foo",
            "lists": [1, 2],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "text": "hello, foo, None, [1, 2]",
    }
