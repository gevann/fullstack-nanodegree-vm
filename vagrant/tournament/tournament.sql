-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS Players CASCADE;
CREATE TABLE Players(
    id SERIAL PRIMARY KEY,
    firstName VARCHAR(15),
    lastName VARCHAR(50));

DROP TABLE IF EXISTS Matches CASCADE;
CREATE TABLE Matches(
    id SERIAL PRIMARY KEY,
    winner INT DEFAULT null REFERENCES Players(id) ON DELETE CASCADE,
    loser INT DEFAULT null REFERENCES Players(id) ON DELETE CASCADE);
