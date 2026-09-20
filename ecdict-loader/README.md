# ECDICT Loader

`ecdict-loader` initializes the ECDICT dictionary used by Practice Service's
autocomplete endpoint.

## Responsibilities

- Wait for MySQL to become available.
- Create the `ecdict` table and add missing columns.
- Download ECDICT when the cache is empty.
- Import the CSV into MySQL with UTF-8 support.
- Skip the import when the table already contains data.
- Print a warning and exit cleanly when MySQL or the download source is
  unavailable.

The default download URL is:

```text
https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv
```

## Configuration

The loader reads these environment variables:

```text
MYSQL_HOST=mysql
MYSQL_DATABASE=speakscore
MYSQL_USER=speakscore
MYSQL_PASSWORD=...
ECDICT_URL=https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv
```

The CSV is stored as `/data/ecdict.csv`, which should be backed by the
`ecdict-cache` Docker volume so that later starts do not download it again.

## Restricted network environments

If the server cannot reach GitHub, download `ecdict.csv` on a machine with
working network access and copy it into the `ecdict-cache` volume. Restart the
loader afterward. The application can still start when the import is skipped,
but autocomplete will remain empty until the dictionary is imported.

When the loader is enabled as a Compose service, check the result with:

```bash
docker compose logs --tail=200 ecdict-loader
docker compose exec mysql \
  mysql -uspeakscore -p speakscore \
  -e "SELECT COUNT(*) AS total FROM ecdict;"
```

The loader is an initialization utility, not an online dictionary or a
context-aware language model. It supports prefix suggestions such as `wat`
→ `water`, but does not predict the next word in a sentence.
