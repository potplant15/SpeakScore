#!/bin/sh
set -u

MYSQL_HOST="${MYSQL_HOST:-mysql}"
MYSQL_DATABASE="${MYSQL_DATABASE:-speakscore}"
MYSQL_USER="${MYSQL_USER:-speakscore}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-}"
ECDICT_URL="${ECDICT_URL:-https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv}"
CSV_PATH="/data/ecdict.csv"

mysql_cmd() {
  mysql --protocol=tcp -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" "$@"
}

echo "[ecdict-loader] Waiting for MySQL..."
i=0
while ! mysqladmin --protocol=tcp -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" ping --silent >/dev/null 2>&1; do
  i=$((i + 1))
  if [ "$i" -ge 30 ]; then
    echo "[ecdict-loader] WARNING: MySQL is unavailable; skipping ECDICT initialization."
    exit 0
  fi
  sleep 2
done

echo "[ecdict-loader] Ensuring ECDICT table exists..."
if ! mysql_cmd < /schema/ecdict-schema.sql; then
  echo "[ecdict-loader] WARNING: Could not create or inspect the ECDICT table; skipping import."
  exit 0
fi

for definition in \
  "definition TEXT" \
  "collins TINYINT" \
  "oxford TINYINT" \
  "tag VARCHAR(128)" \
  "exchange VARCHAR(255)" \
  "detail TEXT" \
  "audio VARCHAR(255)"; do
  column=${definition%% *}
  exists=$(mysql_cmd -N -B -e "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='${MYSQL_DATABASE}' AND table_name='ecdict' AND column_name='${column}';" 2>/dev/null || echo 0)
  if [ "$exists" = "0" ]; then
    echo "[ecdict-loader] Adding missing column: $column"
    mysql_cmd -e "ALTER TABLE ecdict ADD COLUMN $column ${definition#* };" || {
      echo "[ecdict-loader] WARNING: Could not add column $column; skipping import."
      exit 0
    }
  fi
done

count=$(mysql_cmd -N -B -e "SELECT COUNT(*) FROM ecdict;" 2>/dev/null || echo 0)
if [ "$count" -gt 0 ] 2>/dev/null; then
  echo "[ecdict-loader] ECDICT already contains $count rows; skipping import."
  exit 0
fi

if [ ! -s "$CSV_PATH" ]; then
  echo "[ecdict-loader] Downloading ECDICT from $ECDICT_URL"
  if ! curl --fail --location --retry 3 --retry-delay 3 --connect-timeout 15 \
    --output "${CSV_PATH}.download" "$ECDICT_URL"; then
    rm -f "${CSV_PATH}.download"
    echo "[ecdict-loader] WARNING: ECDICT download failed; skipping import."
    echo "[ecdict-loader] Place ecdict.csv in the ecdict-cache volume and restart this service."
    exit 0
  fi
  mv "${CSV_PATH}.download" "$CSV_PATH"
fi

echo "[ecdict-loader] Importing ECDICT. This may take several minutes..."
if ! mysql_cmd --local-infile=1 <<SQL
LOAD DATA LOCAL INFILE '${CSV_PATH}'
INTO TABLE ecdict
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 LINES
(word, @phonetic, @definition, @translation, @pos, @collins, @oxford, @tag,
 @bnc, @frq, @exchange, @detail, @audio)
SET phonetic = NULLIF(@phonetic, ''),
    definition = NULLIF(@definition, ''),
    translation = NULLIF(@translation, ''),
    pos = NULLIF(@pos, ''),
    collins = NULLIF(@collins, ''),
    oxford = NULLIF(@oxford, ''),
    tag = NULLIF(@tag, ''),
    bnc = NULLIF(@bnc, ''),
    frq = NULLIF(@frq, ''),
    exchange = NULLIF(@exchange, ''),
    detail = NULLIF(@detail, ''),
    audio = NULLIF(@audio, '');
SQL
then
  echo "[ecdict-loader] WARNING: ECDICT import failed; application continues without suggestions."
  exit 0
fi

count=$(mysql_cmd -N -B -e "SELECT COUNT(*) FROM ecdict;" 2>/dev/null || echo 0)
echo "[ecdict-loader] ECDICT initialization finished with $count rows."
exit 0

