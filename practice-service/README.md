# SpeakScore Practice Service

Practice Service is the Java business service. It creates practices, coordinates Reference Service and Evaluation Service, stores practice data and evaluation results in MySQL, and exposes the API used by the frontend.

## Requirements

- Java 21
- Maven 3.9+
- MySQL 8.0+
- Reference Service at `reference-service:8001`
- Evaluation Service at `evaluation-service:8002`

The default application port is `8080`.

## Configuration

Configure the MySQL connection and upstream service URLs in `src/main/resources/application.yml` or through environment variables. In Docker Compose, use service names instead of `localhost`:

```text
Reference Service:  http://reference-service:8001
Evaluation Service: http://evaluation-service:8002
```

ECDICT can be initialized with `src/main/resources/ecdict-schema.sql` and MySQL `LOAD DATA LOCAL INFILE`.

## Run locally

```bash
cd practice-service
mvn test
mvn spring-boot:run
```

Main endpoints:

```text
POST /api/v1/practices
GET  /api/v1/practices
GET  /api/v1/practices/{id}
GET  /api/v1/practices/{id}/audio
GET  /api/v1/practices/{id}/reference
POST /api/v1/practices/{id}/evaluate
```

Create a practice:

```bash
curl -X POST http://127.0.0.1:8080/api/v1/practices \
  -H 'Content-Type: application/json' \
  -d '{"text":"I would like some water.","accent":"en-US","gender":"female"}'
```

Submit audio:

```bash
curl -X POST http://127.0.0.1:8080/api/v1/practices/1/evaluate \
  -F 'audio=@recording.mp3'
```

Evaluation can take several minutes on a small CPU server. Keep frontend and reverse-proxy timeouts longer than model inference time.

## Docker

From the project root:

```bash
docker compose build practice-service
docker compose up -d practice-service
docker compose logs -f practice-service
```

Practice Service should normally remain private and be reached through the frontend reverse proxy or the internal Docker network.
