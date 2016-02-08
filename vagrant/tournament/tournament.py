#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# import the custom Cursor class for usage in with statements:
from Cursor import Cursor


def deleteMatches():
    """Remove all the match records from the database."""

    qry_del = """TRUNCATE Matches RESTART IDENTITY CASCADE"""
    qry_players = """UPDATE Players
    SET wins = 0, losses = 0
    """
    with Cursor() as cursor:
        cursor.execute(qry_del)
        cursor.execute(qry_players)


def deletePlayers():
    """Remove all the player records from the database."""

    qry = """TRUNCATE Players RESTART IDENTITY CASCADE"""
    with Cursor() as cursor:
        cursor.execute(qry)


def countPlayers():
    """Returns the number of players currently registered."""

    qry = """SELECT COUNT(*) FROM Players"""
    with Cursor() as cursor:
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

    qry = """INSERT INTO Players (firstname, lastname, wins, losses, rank)
    VALUES ((%s), (%s), DEFAULT, DEFAULT, DEFAULT);"""
    full_name = name.split(" ")

    # Get the first and last name of the player. If name cannot be split
    # into 2, set the last name as the empty string
    fname, lname = full_name if len(full_name) == 2 else [name, ""]

    # Names may have a single-quote in them, escape it:
    with Cursor() as cursor:
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

    qry = """SELECT id, firstName, lastName, wins, losses FROM Players"""
    with Cursor() as cursor:
        cursor.execute(qry)
        standings = sorted([(pid, " ".join([fn, ln]), w, w+l)
                            for pid, fn, ln, w, l in cursor.fetchall()], key=lambda x: x[2],
                           reverse=True)

    n = len(standings)
    i = 0
    while i < n:
        # Search the standings for ties
        # Break any ties found by sending all tied players
        # in a list to be sorted by the OWM scores
        j = i
        while j < n-1 and standings[i][2] == standings[j][2]:
            j += 1
        tied_players = standings[i:j]

        if len(tied_players) > 1:
            # There are 2 or more tied players.
            # Sort the sublist containing them by their OWM scores
            OWM_sorted_players = sortByOWM(tied_players)
            standings[i:j] = OWM_sorted_players
        i = j + 1

    return standings


def sortByOWM(lst):
    """Returns lst sorted by the OWM value"""

    OWMS = [opponentMatchWins(p) for p, name, w, m in lst]
    return [p for (owm, p) in sorted(zip(OWMS, lst), reverse=True)]


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    match_qry = """INSERT INTO Matches (winner, loser)
    VALUES ((%s), (%s))"""

    winner_qry = """UPDATE Players
    SET wins = wins + 1
    WHERE id = (%s)"""

    loser_qry = """UPDATE Players
    SET losses = losses + 1
    WHERE id = (%s)"""

    with Cursor() as cursor:
        cursor.execute(match_qry, [winner, loser])
        cursor.execute(winner_qry, [winner])
        cursor.execute(loser_qry, [loser])


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

    wins_qry = """SELECT wins FROM Players WHERE id = (%s)"""
    OWM = 0

    with Cursor() as cursor:
        cursor.execute(match_qry, [p, p])
        p_opps = [opp for tpl in cursor.fetchall() for opp in tpl if opp != p]

        for opp in p_opps:
            qry = wins_qry
            cursor.execute(qry, [opp])
            OWM += cursor.fetchone()[0]

    return OWM
