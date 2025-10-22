# ML API (FastAPI + Iris) — CI/CD через GitHub Actions

Простой пример Python‑проекта: FastAPI сервис с моделью классификации Iris (scikit‑learn). Настроен CI (pytest) и сборка Docker‑образа с публикацией в GHCR (GitHub Container Registry).

## Локальный запуск (Python)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте: http://127.0.0.1:8000/docs

## Локальный запуск (Docker)

```bash
docker build -t iris-api:local .
docker run --rm -p 8000:8000 iris-api:local
```

Или через docker-compose:

```bash
docker compose up --build
```

## Эндпоинты

- `GET /health` — статус сервиса, метрика точности модели
- `POST /predict` — предсказание класса

Пример запроса:

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

## Тесты

```bash
pytest -q
```

## CI/CD (GitHub Actions)

Workflow: `.github/workflows/ci.yml`
- На каждый push/PR: запускает тесты (pytest)
- На push в `main/master`: собирает Docker‑образ и публикует в GHCR

Публикация в GHCR использует `${{ secrets.GITHUB_TOKEN }}` (нужны права `packages: write`).
Теги образа:
- `ghcr.io/<owner>/<repo>:latest`
- `ghcr.io/<owner>/<repo>:sha-<commit>`

Если хотите публиковать в Docker Hub — замените шаг логина/теги и добавьте секреты `DOCKERHUB_USERNAME` и `DOCKERHUB_TOKEN`.

## Примечания

- Базовый образ: `python:3.11-slim`, добален пакет `libgomp1` для scikit-learn.
- Модель обучается на старте (данные Iris встроены в scikit-learn). Тренировка занимает <1 c.
