-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create tournament database
\c tournament

-- players: name, id, and current tournament
CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name TEXT
                      );

-- matches: stores the tournament, round, participants and outcome
CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      player1 INT REFERENCES players(id),
                      player2 INT REFERENCES players(id),
                      winner INT REFERENCES players(id),
                      loser INT REFERENCES players(id)
                      );



