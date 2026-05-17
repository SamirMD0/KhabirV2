from __future__ import annotations


def test_cases_index_returns_json(client):
    response = client.get("/api/cases/")

    assert response.status_code == 200
    assert response.is_json

