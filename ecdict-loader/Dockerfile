FROM alpine:3.20

RUN apk add --no-cache ca-certificates curl mariadb-client

WORKDIR /loader
COPY load-ecdict.sh .
COPY ecdict-schema.sql /schema/ecdict-schema.sql
RUN chmod +x load-ecdict.sh

ENTRYPOINT ["/loader/load-ecdict.sh"]
