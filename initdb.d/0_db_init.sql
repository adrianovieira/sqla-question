---- Create schema database
---- Create database table and its index

CREATE SCHEMA IF NOT EXISTS analysis;

CREATE TABLE IF NOT EXISTS analysis.surveys (
    id                   BIGINT PRIMARY KEY,
    origin               VARCHAR(15),
    response_status_id   INTEGER,
    created_at           TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX ON analysis.surveys (created_at, response_status_id, origin);

