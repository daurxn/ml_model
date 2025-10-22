# Отчёт: CI/CD для Python‑проекта (FastAPI + Iris) на GitHub Actions

## Шаги

1. Создан минимальный проект:
   - `app/main.py` — FastAPI API: `/health`, `/predict`
   - `app/model.py` — обучение RandomForest на Iris при старте
   - `tests/test_app.py` — pytest: здоровье и базовые предсказания, проверка точности ≥ 0.9
   - Зависимости: `requirements.txt`
2. Контейнеризация:
   - `Dockerfile` (python:3.11-slim, `libgomp1` для scikit‑learn, `uvicorn` как CMD)
   - `.dockerignore`
   - `docker-compose.yml` для локального запуска
3. CI/CD (GitHub Actions):
   - `.github/workflows/ci.yml` — job `test` (pytest) и job `docker` (build+push в GHCR)
   - Публикация использует `${{ secrets.GITHUB_TOKEN }}` с правами `packages: write`
4. Документация:
   - `README.md` — локальный запуск, Docker, CI/CD

## Особенности и сложности

- Склейка ML + slim-образ: scikit‑learn требует OpenMP runtime → добавлен `libgomp1` через apt.
- Публикация в GHCR:
  - Требуются `permissions: packages: write` в workflow
  - Теги выстраиваются по `github.repository_owner` и `github.event.repository.name`
- Детерминизм качества модели: фиксирован `random_state`; увеличено число деревьев до 200 → точность стабильно ≥ 0.9.

## Результаты

- На каждый коммит: прогоняются тесты.
- На push в `main/master`: собирается и публикуется образ в GHCR с тегами `latest` и `sha-<commit>`.
- Сервис поднимается локально через Python, Docker или `docker compose`.

## Возможные улучшения

- Добавить линтинг/форматирование (ruff/black), type‑check (mypy).
- Кэширование модели или отделение тренировки от запуска.
- CD: авторазвёртывание на тестовый сервер или Kubernetes (Minikube), health‑checks.
- SAST/Dependency Review, SBOM и provenance (attestations) в цепочке сборки.
