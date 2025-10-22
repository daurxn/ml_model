from fastapi.testclient import TestClient

from app.main import app, model_service

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["model_accuracy"] >= 0.9


def test_predict_samples():
    # Known setosa-like sample
    r1 = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["class_label"] in {"setosa", "versicolor", "virginica"}

    # Another random sample from iris domain
    r2 = client.post("/predict", json={"features": [6.7, 3.1, 4.7, 1.5]})
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["class_label"] in {"setosa", "versicolor", "virginica"}
