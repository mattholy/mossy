FROM node:20 as vue-builder
WORKDIR /app/frontend/mossy-zero
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ENV VITE_RUN_ENV=container
RUN npm run build


FROM python:3.12
WORKDIR /app
ARG RELEASE_TAG
ENV RELEASE_TAG=${RELEASE_TAG}
RUN pip install poetry
COPY backend/pyproject.toml backend/poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --only main
COPY --from=vue-builder /app/frontend/mossy-zero/dist /app/static
COPY backend /app

COPY backend/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
ENV RUNTIME="PRO"
CMD ["bash", "./entrypoint.sh"]
EXPOSE 8000