# SpeakScore
SpeakScore is an English speaking practice tool that reads sentences aloud, recognizes users’ speech, and scores their pronunciation.

The service is currently available at [https://www.speakscore.icu/](https://www.speakscore.icu/).

## Project structure

```text
frontend/             Vue frontend
practice-service/     Spring Boot business service
reference-service/    Kokoro reference-audio and IPA service
evaluation-service/   Whisper and OpenPronounce evaluation service
compose.yml           Docker Compose deployment configuration
```

## Runtime requirements

### Local development

- Ubuntu 22.04 or 24.04, or WSL2 with Ubuntu
- Python 3.12
- Java 21
- Maven 3.9+
- Node.js 20+
- npm 10+
- MySQL 8.0+
- FFmpeg
- Git

Docker is optional for local development, but recommended for running the complete system consistently.

### Recommended server resources

The services can run on a small CPU server. At least 2 vCPU and 4 GB RAM is recommended for a smoother experience. Evaluation Service uses Whisper and OpenPronounce models, so the first evaluation may take longer on a 2 GB server.

## Dependencies

### Frontend

The frontend uses Vue 3, Vite, TypeScript and PrimeVue. Install dependencies from the `frontend` directory:

```bash
cd frontend
npm install --no-audit --no-fund --prefer-offline
```

If the npm registry is slow or unavailable, configure the mirror:

```bash
npm config set registry https://registry.npmmirror.com
npm install --no-audit --no-fund --prefer-offline
```

### Practice Service

Practice Service uses Java 21, Spring Boot 3.x, Maven and MySQL 8. Configure the database connection in the service configuration, then run:

```bash
cd practice-service
mvn test
mvn spring-boot:run
```

The default port is `8080`.

### Reference Service

Reference Service uses Python, FastAPI, Uvicorn, Kokoro and eSpeak NG. For local development:

```bash
cd reference-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

The default port is `8001`.

### Evaluation Service

Evaluation Service uses Python, FastAPI, Uvicorn, faster-whisper and OpenPronounce. For local development:

```bash
cd evaluation-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

The default port is `8002`.

## Starting the complete system with Docker Compose

From the project root:

```bash
docker compose build
docker compose up -d
```

Check service status:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs -f reference-service
docker compose logs -f evaluation-service
docker compose logs -f practice-service
```

Access the frontend at:

```text
http://localhost:5173
```

Service endpoints:

```text
Practice Service:   http://localhost:8080
Reference Service:  http://localhost:8001
Evaluation Service: http://localhost:8002
```

Stop services without deleting model or database volumes:

```bash
docker compose down
```

Avoid `docker compose down --volumes` unless it is intentional. That command deletes the MySQL, Kokoro and Hugging Face volumes.

## Basic health checks

```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
curl http://127.0.0.1:8080/api/v1/practices
```

Generate reference audio:

```bash
curl -X POST http://127.0.0.1:8001/api/v1/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"How are you today?","accent":"en-US","gender":"female"}' \
  --output test.mp3
```

## Model files and restricted networks

The services may need to download models from external websites during the first startup. The main model resources are:

- Kokoro: `kokoro-v1.0.onnx` and `voices-v1.0.bin`
- Whisper: the configured faster-whisper model
- OpenPronounce: `facebook/wav2vec2-lv-60-espeak-cv-ft`

If Hugging Face, GitHub or the Kokoro download site cannot be accessed from the server, do not repeatedly restart the containers. Download the required files on a machine with working network access, then upload them with `scp`.

### Whisper local mount

Place the Whisper model on the server, for example:

```text
/home/ubuntu/whisper-model/
```

The directory should contain files such as `config.json`, `model.bin`, `tokenizer.json` and `vocabulary.txt`. Mount it in `compose.yml`:

```yaml
volumes:
  - /home/ubuntu/whisper-model:/models/whisper:ro
environment:
  WHISPER_MODEL: /models/whisper
```

### Hugging Face cache for OpenPronounce

OpenPronounce uses the model `facebook/wav2vec2-lv-60-espeak-cv-ft`. Copy its complete Hugging Face cache into the named volume. The final path inside the container must be:

```text
/root/.cache/huggingface/hub/models--facebook--wav2vec2-lv-60-espeak-cv-ft
```

The cache must be under the `hub` directory. Placing `models--facebook--...` directly under `/root/.cache/huggingface` will not be detected.

After the cache is copied, add offline mode to the Evaluation Service:

```yaml
environment:
  HF_HOME: /root/.cache/huggingface
  HF_HUB_OFFLINE: "1"
  TRANSFORMERS_OFFLINE: "1"
```

Then recreate the service:

```bash
docker compose up -d --force-recreate evaluation-service
docker compose logs -f evaluation-service
```

### Kokoro model volume

Copy `kokoro-v1.0.onnx` and `voices-v1.0.bin` into the `speakscore_kokoro-models` volume. For example:

```bash
docker run --rm \
  -v speakscore_kokoro-models:/models \
  -v /home/ubuntu/kokoro-models:/source:ro \
  alpine sh -c 'cp -a /source/. /models/'
```

Then restart Reference Service:

```bash
docker compose up -d --force-recreate reference-service
```

### Verify model-related failures

Health checks only confirm that the web process is running. For model problems, inspect the service logs and make a real request:

```bash
docker compose logs --tail=200 evaluation-service
docker compose logs --tail=200 reference-service
```

Do not commit model files, access tokens, passwords or private server paths to Git. Store large models in Docker volumes or external storage.

## Production domain deployment

For production access, point the domain A record to the cloud server public IP. Only expose the web entry points publicly:

```text
TCP 80
TCP 443
```

Keep the application ports private. The recommended Docker Compose bindings are:

```yaml
ports:
  - "127.0.0.1:5173:80"
```

The `8001`, `8002`, `8080` and `3306` ports do not need to be exposed to the public network. Services communicate through the internal Docker network using service names such as `reference-service:8001` and `evaluation-service:8002`.

Install Nginx and Certbot on the server:

```bash
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx
```

Configure the domain's Nginx server block to proxy HTTPS traffic to the frontend:

```nginx
location / {
    proxy_pass http://127.0.0.1:5173;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    client_max_body_size 50m;
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
}
```

Request a certificate:

```bash
sudo certbot --nginx -d www.example.com
sudo nginx -t
sudo systemctl reload nginx
```

The application can then be accessed at `https://www.example.com`. HTTPS is required by browsers for microphone access.

Cloudflare Quick Tunnel is useful for temporary testing, but it is not required after the domain and HTTPS certificate are configured. Stop a temporary tunnel with:

```bash
docker rm -f speakscore-tunnel 2>/dev/null || true
```
