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
    lastName VARCHAR(50),
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    rank INT DEFAULT null);

DROP TABLE IF EXISTS Matches CASCADE;
CREATE TABLE Matches(
    id SERIAL PRIMARY KEY,
    winner INT DEFAULT null,
    loser INT DEFAULT null,
    round INT,
    FOREIGN KEY(winner) REFERENCES Players(id),
    FOREIGN KEY(loser) REFERENCES Players(id));

DROP TABLE IF EXISTS PlaysIn CASCADE;
CREATE TABLE PlaysIn(
    player_1_id INT,
    player_2_id INT,
    match_id INT,
    FOREIGN KEY(player_1_id) REFERENCES Players(id),
    FOREIGN KEY(player_2_id) REFERENCES Players(id),
    FOREIGN KEY(match_id) REFERENCES Matches(id),
    PRIMARY KEY(match_id));
