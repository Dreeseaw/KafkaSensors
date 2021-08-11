CREATE TABLE IF NOT EXISTS metrics (
  traveler_id varchar(250) NOT NULL,
  traveler_type varchar(250) NOT NULL,
  sensor_id integer NOT NULL,
  appears_at timestamp NOT NULL,
  max_speed double precision NOT NULL,
  min_speed double precision NOT NULL,
  avg_speed double precision NOT NULL,
  PRIMARY KEY (traveler_id)
);
