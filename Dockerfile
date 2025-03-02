FROM confluentinc/cp-server-connect-base:7.2.2

RUN confluent-hub install --no-prompt \
    debezium/debezium-connector-sqlserver:2.2.1
