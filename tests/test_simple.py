import pytest
from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)


class TestPingEndpoint:
    def test_ping_success(self):
        """Test successful ping response"""
        response = client.get("/ping")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "200 OK"}

    def test_ping_wrong_method(self):
        """Test ping endpoint with incorrect HTTP methods"""
        for method in ["post", "put", "delete", "patch"]:
            response = getattr(client, method)("/ping")
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestPredictEndpoint:
    @pytest.fixture
    def valid_text(self):
        return """This is a test text that needs to be summarized.
        It should be long enough to make sense for the summarization model.
        We're testing if our API endpoint works correctly with valid input."""

    def test_predict_success(self, valid_text):
        """Test successful prediction with valid input"""
        response = client.post("/predict", json={"text": valid_text})
        assert response.status_code == status.HTTP_200_OK
        assert "summary" in response.json()
        assert isinstance(response.json()["summary"], str)

    def test_predict_empty_request(self):
        """Test prediction with empty request body"""
        response = client.post("/predict", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_predict_missing_text(self):
        """Test prediction with missing text field"""
        response = client.post("/predict", json={"wrong_field": "some text"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_predict_empty_text(self):
        """Test prediction with empty text"""
        response = client.post("/predict", json={"text": ""})
        assert response.status_code == status.HTTP_200_OK

    def test_predict_invalid_text_type(self):
        """Test prediction with invalid text type"""
        response = client.post("/predict", json={"text": 123})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestErrorHandling:
    def test_not_found(self):
        """Test 404 response for non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_method_not_allowed(self):
        """Test method not allowed response"""
        response = client.post("/ping")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


if __name__ == "__main__":
    pytest.main(["-v", "--cov=main", "--cov-report=term-missing"])
