FROM postgres:18.6-trixie@sha256:ae6c78831cbc35fa3a4aaf4d763ddacf6183d6004774cc2dc28b3920410d1d1a

RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates; \
    test -s /etc/ssl/certs/ca-certificates.crt; \
    rm -rf /var/lib/apt/lists/*; \
    postgis_package_version='3.6.4+dfsg-2.pgdg13+1'; \
    pgvector_package_version='0.8.6-1.pgdg13+1'; \
    pgbackrest_package_version='2.59.1-1.pgdg13+1'; \
    printf '%s\n' \
      'deb [ signed-by=/usr/local/share/keyrings/postgres.gpg.asc ] https://apt-archive.postgresql.org/pub/repos/apt trixie-pgdg-archive main' \
      > /etc/apt/sources.list.d/pgdg.list; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      "postgresql-18-postgis-3=${postgis_package_version}" \
      "postgresql-18-pgvector=${pgvector_package_version}" \
      "pgbackrest=${pgbackrest_package_version}"; \
    test "$(dpkg-query -W -f='${Version}' postgresql-18-postgis-3)" = "${postgis_package_version}"; \
    test "$(dpkg-query -W -f='${Version}' postgresql-18-pgvector)" = "${pgvector_package_version}"; \
    test "$(dpkg-query -W -f='${Version}' pgbackrest)" = "${pgbackrest_package_version}"; \
    test "$(pgbackrest version)" = 'pgBackRest 2.59.1'; \
    test -f /usr/share/postgresql/18/extension/postgis.control; \
    test -f /usr/share/postgresql/18/extension/vector.control; \
    install -d -o root -g postgres -m 0750 /etc/pgbackrest; \
    install -d -o postgres -g postgres -m 0750 /var/lib/pgbackrest; \
    rm -rf /var/lib/apt/lists/*

COPY pgbackrest/pgbackrest.conf /etc/pgbackrest/pgbackrest.conf
RUN chown root:postgres /etc/pgbackrest/pgbackrest.conf \
    && chmod 0640 /etc/pgbackrest/pgbackrest.conf

COPY initdb/010-extensions.sql /docker-entrypoint-initdb.d/010-extensions.sql
