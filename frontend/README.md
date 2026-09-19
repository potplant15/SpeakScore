# SpeakScore Frontend

Vue 3 + TypeScript + Vite frontend for the pronunciation practice flow.

## Run locally

```bash
npm install
npm run dev
```

The app talks only to Practice Service through `VITE_API_BASE_URL`.

## Requirements

- Node.js 20+
- npm 10+
- Practice Service running on port `8080`
- HTTPS or `localhost` for microphone recording

If npmjs.org is slow or unavailable, use the mirror:

```bash
npm config set registry https://registry.npmmirror.com
npm install --no-audit --no-fund --prefer-offline
```

For local development against a host-side Practice Service:

```bash
echo 'VITE_API_BASE_URL=http://127.0.0.1:8080/api/v1' > .env.local
```

Build the production bundle:

```bash
npm run build
npm run preview
```

## Docker

From the project root:

```bash
docker compose build frontend
docker compose up -d frontend
```

The production container serves the built files through Nginx on port 80. The root Compose file maps it to port 5173 for the host-side reverse proxy.
