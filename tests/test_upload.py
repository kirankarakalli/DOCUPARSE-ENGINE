
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_file_success():
    fake_file_info = {
        "stored_filename": "test.txt",
        "size_in_bytes": 12,
        "file_path": "/tmp/test.txt",
    }

    fake_extraction = {
        "extracted_text": "Test document content",
        "structured_data": {"title": "Test"},
    }

    with (
        patch(
            "app.api.routes.document.save_file_to_disk",
            new_callable=AsyncMock,
            return_value=fake_file_info,
        ) as mock_save,
        patch(
            "app.api.routes.document.process_document",
            return_value=fake_extraction,
        ) as mock_process,
    ):
        response = client.post(
            "/api/uploadfile",
            files={
                "file": (
                    "test.txt",
                    b"Hello world!",
                    "text/plain",
                )
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["stored_filename"] == "test.txt"
    assert body["size_in_bytes"] == 12
    assert body["extracted_text"] == "Test document content"
    assert body["structured_data"] == {"title": "Test"}
    assert "upload_id" in body
    assert "status" in body

    mock_save.assert_called_once()
    mock_process.assert_called_once()
