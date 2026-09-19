# ECDICT setup

The suggestion endpoint reads the official ECDICT data from MySQL. The large
dictionary file is intentionally kept outside the repository.

## Download

```bash
mkdir -p ~/speakscore-data
curl -L https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv \
  -o ~/speakscore-data/ecdict.csv
```

## Create the table

```bash
mysql -u speakscore -p speakscore \
  < src/main/resources/ecdict-schema.sql
```

## Import the CSV

MySQL must allow local file loading for this command:

```bash
mysql --local-infile=1 -u speakscore -p speakscore
```

Then run:

```sql
LOAD DATA LOCAL INFILE '/home/fanwenhao/speakscore-data/ecdict.csv'
INTO TABLE ecdict
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(word, phonetic, definition, translation, pos, collins, oxford, tag,
 bnc, frq, exchange, detail, audio);
```

After importing, test:

```bash
curl 'http://localhost:8080/api/v1/suggestions?prefix=wat'
```
