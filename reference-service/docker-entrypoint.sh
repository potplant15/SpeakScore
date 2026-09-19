#!/bin/sh
set -eu

model_dir=$(dirname "$KOKORO_MODEL_PATH")
mkdir -p "$model_dir"

download_if_missing() {
  target="$1"
  url="$2"

  if [ -s "$target" ]; then
    echo "Using cached model file: $target"
    return
  fi

  echo "Downloading Kokoro model file: $target"
  temporary="${target}.download"
  rm -f "$temporary"
  curl --fail --location --retry 3 --retry-delay 2 --output "$temporary" "$url"
  test -s "$temporary"
  mv "$temporary" "$target"
}

download_if_missing "$KOKORO_MODEL_PATH" "$KOKORO_MODEL_URL"
download_if_missing "$KOKORO_VOICES_PATH" "$KOKORO_VOICES_URL"

exec uvicorn app.main:app --host 0.0.0.0 --port 8001
