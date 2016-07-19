-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS players;

-- table to hold basic player information (name)
CREATE TABLE players(
		id serial NOT NULL,
		name varchar(30) NOT NULL,
		PRIMARY KEY (id)
		);

-- table to keep track of each player's wins and losses
CREATE TABLE scores(
		player int REFERENCES players(id) ON DELETE CASCADE,
		wins int NOT NULL,
		losses int NOT NULL
		);
