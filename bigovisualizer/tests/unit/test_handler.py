import math
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from hello_world.app import app

client = TestClient(app)
TYPES = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(2^n)"]


def fetch(complexity, n):
    return client.get(f"/bigO/{quote(complexity, safe='')}", params={"n": n})


@pytest.mark.parametrize("complexity", TYPES)
@pytest.mark.parametrize("n", [1, 10, 19, 20, 21, 999, 1000, 1001, 50000, 100000])
def test_response_contract(complexity, n):
    response = fetch(complexity, n)
    assert response.status_code == 200
    data = response.json()
    x, y = data["n"], data["y"]
    assert len(x) == len(y) <= 1000
    assert x[0] == 1 and x[-1] == n
    assert x == sorted(set(x))
    if complexity != "O(2^n)":
        assert len(x) == min(n, 1000)
        if n <= 1000:
            assert x == list(range(1, n + 1))
        else:
            gaps = [b - a for a, b in zip(x, x[1:])]
            assert max(gaps) - min(gaps) <= 1
    for point, value in zip(x, y):
        if complexity == "O(2^n)" and point >= 20:
            assert value is None
        else:
            expected = {
                "O(1)": lambda: 1,
                "O(log n)": lambda: math.log2(point),
                "O(n)": lambda: point,
                "O(n log n)": lambda: point * math.log2(point),
                "O(n^2)": lambda: point ** 2,
                "O(2^n)": lambda: 2 ** point,
            }[complexity]()
            assert value == pytest.approx(expected)
    if complexity == "O(2^n)":
        assert x[:min(n, 20)] == list(range(1, min(n, 20) + 1))


@pytest.mark.parametrize("n", [0, -1, 100001, "not-a-number", "1.5"])
def test_invalid_input(n):
    assert fetch("O(n)", n).status_code == 422


def test_missing_input():
    assert client.get("/bigO/O(n)").status_code == 422


def test_unknown_complexity():
    assert fetch("unknown", 100).status_code == 400


@pytest.mark.parametrize("complexity", TYPES)
def test_maximum_payload_is_bounded(complexity):
    assert len(fetch(complexity, 100000).content) < 50000


def test_root():
    assert client.get("/").json() == {"message": "Big-O Visualizer API is running!"}


def test_lambda_adapter():
    import json
    from pathlib import Path
    from hello_world.app import handler

    event = json.loads((Path(__file__).parents[2] / "events/event.json").read_text())
    event.update(path="/bigO/O(n)", body=None, queryStringParameters={"n": "100000"})
    event["requestContext"]["httpMethod"] = "GET"
    response = handler(event, None)
    assert response["statusCode"] == 200
    data = json.loads(response["body"])
    assert len(data["n"]) == len(data["y"]) == 1000
    assert data["n"][0] == 1 and data["n"][-1] == 100000
