/* udpd.sqlite */
CREATE TABLE IF NOT EXISTS "dgram" (
  id varchar(64) PRIMARY KEY NOT NULL,
  rid integer,
  json varchar(128),
  received timestamp DEFAULT((DATETIME('now', 'localtime'))),
  chk integer DEFAULT(0)
);

CREATE INDEX IF NOT EXISTS index_received ON dgram (received DESC);

