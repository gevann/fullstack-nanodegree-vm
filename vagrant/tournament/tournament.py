#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# import the custom Cursor class for usage in with statements:
from Database import Database
from Database import Cursor


def deleteMatches():
    """Remove all the match records from the database."""

    qry_del = """TRUNCATE Matches RESTART IDENTITY CASCADE"""
    with Cursor(tournament_database) as cursor:
        cursor.execute(qry_del)


def deletePlayers():
    """Remove all the player records from the database."""

    qry = """TRUNCATE Players RESTART IDENTITY CASCADE"""
    with Cursor(tournament_database) as cursor:
        cursor.execute(qry)


def countPlayers():
    """Returns the number of players currently registered."""

    qry = """SELECT COUNT(*) FROM Players"""
    with Cursor(tournament_database) as cursor:
        cursor.execute(qry)
        results = cursor.fetchone()
    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    qry = """INSERT INTO Players (firstname, lastname)
    VALUES ((%s), (%s));"""
    full_name = name.split(" ")

    # Get the first and last name of the player. If name cannot be split
    # into 2, set the last name as the empty string
    fname, lname = full_name if len(full_name) == 2 else [name, ""]

    # Names may have a single-quote in them, escape it:
    with Cursor(tournament_database) as cursor:
        cursor.execute(qry, [fname, lname])


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

    qry = """WITH w AS (
    SELECT winner AS id, COUNT(winner) AS wins FROM matches GROUP BY winner),
    l AS (
    SELECT loser AS id, COUNT(loser) AS losses FROM matches GROUP BY loser)
    SELECT p.id, p.firstname, p.lastname, wins, losses FROM w FULL OUTER JOIN l ON (w.id = l.id)
    RIGHT OUTER JOIN Players p ON (w.id = p.id OR l.id = p.id);"""

    with Cursor(tournament_database) as cursor:
        cursor.execute(qry)
        standings = sorted([(pid, " ".join([fn, ln]), (w or 0), (w or 0) + (l or 0))
                            for pid, fn, ln, w, l in cursor.fetchall()], key=lambda x: x[2],
                           reverse=True)

    n = len(standings)
    i = 0
    while i < n-1:
        # Search the standings for ties
        # Break any ties found by sending all tied players
        # in a list to be sorted by the OWM scores
        # i the is index of the first player with score = x, and
        # j is the index of the first player (sequencially from i) with score != x.
        # This leaves us a slice of players [i:j], where each player as the same score.
        j = i
        while j < n-1 and standings[i][2] == standings[j][2]:
            j += 1
        tied_players = standings[i:j]

        if len(tied_players) > 1:
            # There are 2 or more tied players.
            # Sort the sublist containing them by their OWM scores
            OWM_sorted_players = sortByOWM(tied_players)
            standings[i:j] = OWM_sorted_players
        i = j

    return standings


def sortByOWM(lst):
    """Returns lst sorted by the OWM value"""

    OWMS = [opponentMatchWins(p) for p, name, w, m in lst]
    return [p for (owm, p) in sorted(zip(OWMS, lst), reverse=True, key=lambda x: x[0])]


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # qry = """INSERT INTO Matches (id, winner, loser)
    # VALUES (DEFAULT, (%s), (%s))"""
    qry = "INSERT INTO MATCHES VALUES (DEFAULT, %s, %s)"

    with Cursor(tournament_database) as cursor:
        cursor.execute(qry, [winner, loser])


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

    # create a flat list of all players sorted by their standing
    standings = [val for elem in playerStandings() for val in elem[:2]]

    # zip the flat list standings into a list of 4-tuples)
    pairings = zip(*[iter(standings)]*4)

    return pairings


def opponentMatchWins(p):
    '''Returns player p's oppenents match wins count'''

    match_qry = """SELECT winner, loser
    FROM Matches
    WHERE winner = (%s)
    OR
    loser = (%s)"""

    # wins_qry = """SELECT wins FROM Players WHERE id = (%s)"""
    wins_qry = """SELECT COUNT(*) FROM Matches WHERE winner = (%s)"""
    OWM = 0

    with Cursor(tournament_database) as cursor:
        cursor.execute(match_qry, [p, p])
        p_opps = [opp for tpl in cursor.fetchall() for opp in tpl if opp != p]

        for opp in p_opps:
            qry = wins_qry
            cursor.execute(qry, [opp])
            OWM += cursor.fetchone()[0]

    return OWM


tournament_database = Database('tournament', 'tournament.sql')
