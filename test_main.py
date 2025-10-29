import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_metrics_endpoint():
    # Make a request to the /metrics endpoint
    response = client.get("/metrics")

    # Assert that the response is successful
    assert response.status_code == 200

    # Assert that the response contains the expected keys
    data = response.json()
    assert "uptime_seconds" in data
    assert "request_count" in data
    assert "average_latency_ms" in data
    assert "status" in data

    # Assert that the status is "healthy"
    assert data["status"] == "healthy"

def test_request_count_increment():
    # Make a request to the root endpoint to increment the counter
    client.get("/")

    # Get the initial request count
    response1 = client.get("/metrics")
    initial_count = response1.json()["request_count"]

    # Make another request
    client.get("/")

    # Get the new request count
    response2 = client.get("/metrics")
    new_count = response2.json()["request_count"]

    # Assert that the request count has incremented by 2 (one for root, one for metrics)
    assert new_count == initial_count + 2

def test_metrics_data_types():
    # Make a request to the /metrics endpoint
    response = client.get("/metrics")

    # Assert that the response is successful
    assert response.status_code == 200

    # Assert that the data types are correct
    data = response.json()
    assert isinstance(data["uptime_seconds"], (int, float))
    assert isinstance(data["request_count"], int)
    assert isinstance(data["average_latency_ms"], (int, float))
    assert isinstance(data["status"], str)
