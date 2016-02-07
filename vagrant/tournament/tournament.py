#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    qry = """TRUNCATE Matches CASCADE"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(qry)
    cursor.close()
    conn.commit()
    conn.close()
    return (cursor.close and conn.closed)


def deletePlayers():
    """Remove all the player records from the database."""
    qry = """TRUNCATE Players CASCADE"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(qry)
    cursor.close()
    conn.commit()
    conn.close()
    return (cursor.close and conn.closed)


def countPlayers():
    """Returns the number of players currently registered."""
    qry = """SELECT COUNT(*) FROM Players"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(qry)
    results = cursor.fetchone()
    cursor.close()
    conn.close()
    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    base_qry = """INSERT INTO Players (firstname, lastname, wins, losses, rank)
    VALUES ('{fname}', '{lname}', DEFAULT, DEFAULT, DEFAULT);"""
    # p_id = 1 + countPlayers()
    full_name = name.split(" ")
    fname, lname = full_name
    qry = base_qry.format(fname=fname, lname=lname)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(qry)
    cursor.close()
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    cursor = conn.cursor()
    qry = """SELECT id, firstName, lastName, wins, losses FROM Players"""

    cursor.execute(qry)
    return sorted([(pid, " ".join([fn, ln]), w, l) for pid, fn, ln, w, l in cursor.fetchall()],
                  key=lambda x: x[2])


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pass


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pass
