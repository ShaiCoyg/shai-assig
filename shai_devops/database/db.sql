use db;

CREATE TABLE access_log(
  date_time DATETIME,
  client_ip VARCHAR(255),
  server_ip VARCHAR(255)
);

CREATE TABLE counter(
  value int
);