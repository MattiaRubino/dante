FROM postgres:18.4-trixie@sha256:a02db8cac496f15b094798a38254f14d6e00741f709360e5e00bb6668ea31636

RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates; \
    test -s /etc/ssl/certs/ca-certificates.crt; \
    rm -rf /var/lib/apt/lists/*; \
    postgis_package_version='3.6.4+dfsg-2.pgdg13+1'; \
    pgvector_package_version='0.8.6-1.pgdg13+1'; \
    printf '%s\n' \
      'deb [ signed-by=/usr/local/share/keyrings/postgres.gpg.asc ] https://apt-archive.postgresql.org/pub/repos/apt trixie-pgdg-archive main' \
      > /etc/apt/sources.list.d/pgdg.list; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      "postgresql-18-postgis-3=${postgis_package_version}" \
      "postgresql-18-pgvector=${pgvector_package_version}"; \
    test "$(dpkg-query -W -f='${Version}' postgresql-18-postgis-3)" = "${postgis_package_version}"; \
    test "$(dpkg-query -W -f='${Version}' postgresql-18-pgvector)" = "${pgvector_package_version}"; \
    test -f /usr/share/postgresql/18/extension/postgis.control; \
    test -f /usr/share/postgresql/18/extension/vector.control; \
    rm -rf /var/lib/apt/lists/*

COPY initdb/010-extensions.sql /docker-entrypoint-initdb.d/010-extensions.sql
