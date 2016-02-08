#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
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
    base_qry = """INSERT INTO Players (firstname, lastname, wins, losses, rank)
    VALUES ('{fname}', '{lname}', DEFAULT, DEFAULT, DEFAULT);"""
    full_name = name.split(" ")
    fname, lname = full_name if len(full_name) == 2 else [name, ""]
    qry = base_qry.format(fname=fname.replace("'", "''"), lname=lname.replace("'", "''"))
    with Cursor() as cursor:
        cursor.execute(qry)


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
        ret_val = sorted([(pid, " ".join([fn, ln]), w, w+l)
                          for pid, fn, ln, w, l in cursor.fetchall()], key=lambda x: x[2],
                         reverse=True)

    n = len(ret_val)
    i = 0
    while i < n:
        j = i
        while j < n-1 and ret_val[i][2] == ret_val[j][2]:
            j += 1
        sublist = ret_val[i:j]
        if len(sublist) > 1:
            sublist = sortByOWM(sublist)
            ret_val[i:j] = sublist
        i = j + 1

    return ret_val


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
    VALUES ('{w_id}', '{l_id}')""".format(w_id=winner, l_id=loser)

    winner_qry = """UPDATE Players
    SET wins = wins + 1
    WHERE id = {w_id}""".format(w_id=winner)

    loser_qry = """UPDATE Players
    SET losses = losses + 1
    WHERE id = {l_id}""".format(l_id=loser)

    with Cursor() as cursor:
        cursor.execute(match_qry)
        cursor.execute(winner_qry)
        cursor.execute(loser_qry)


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

    standings = [val for elem in playerStandings() for val in elem[:2]]
    pairings = zip(*[iter(standings)]*4)

    return pairings


def opponentMatchWins(p):
    '''Returns player p's oppenents match wins count'''

    match_qry = """SELECT winner, loser
    FROM Matches
    WHERE winner = {pid}
    OR
    loser = {pid}"""

    wins_qry = """SELECT wins FROM Players WHERE id = {pid}"""
    OWM = 0
    # conn = connect()
    # cur = conn.cursor()

    with Cursor() as cursor:
        # this returns something
        cursor.execute(match_qry.format(pid=p))
        p_opps = [opp for tpl in cursor.fetchall() for opp in tpl if opp != p]

        # sudden there are not tuples in the db??
        for opp in p_opps:
            qry = wins_qry.format(pid=opp)
            cursor.execute(qry)
            OWM += cursor.fetchone()[0]

    return OWM
