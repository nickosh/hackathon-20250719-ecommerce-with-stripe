ARG PLAYWRIGHT_CONTAINER_VERSION=next-jammy
FROM mcr.microsoft.com/playwright/python:${PLAYWRIGHT_CONTAINER_VERSION}

WORKDIR /tests

COPY pyproject.toml requirements.lock ./

RUN python -m pip install --upgrade pip --root-user-action=ignore && \
    python -m pip install uv --root-user-action=ignore && \
    python -m uv pip compile pyproject.toml -o requirements.txt && \
    python -m uv pip install --system -r requirements.txt && \
    playwright install

ENTRYPOINT ["pytest"]
