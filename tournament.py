#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    return DB, c


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE players, matches;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("SELECT count(*) as count from players;")
    result = c.fetchall()
    DB.commit()
    DB.close()
    return result[0][0]



def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    data = (name,)
    SQL = "INSERT INTO players (name) VALUES (%s);"
    c.execute(SQL, data)
    DB.commit()
    DB.close()


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
    DB, c = connect()
    # uses subqueries for matches won and matches played.
    c.execute("""
            SELECT players.id, players.name,
           (select count(*)
            from matches
            where matches.winner = players.id) as matches_won,
           (select count(*)
            from matches
            where players.id in (player1, player2)) as matches_played
            FROM players
            ORDER BY matches_won DESC
            """)
    result = c.fetchall()
    DB.commit()
    DB.close()
    return result



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    data = (winner, loser, winner, loser,)
    SQL = "INSERT INTO matches(player1, player2, winner, loser) values(%s, %s, %s, %s);"
    c.execute(SQL, data)
    DB.commit()
    DB.close()


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
    # call playerStandings
    standings = playerStandings()
    result = []
    # number of times to loop
    length = len(standings) / 2
    # pops the first and second elements of the list and puts them into array
    # creates new tuple with the elements
    # repeats loop
    for i in range(length):
        array = [standings.pop(0), standings.pop(0)]
        (p1_id, p1_name, p2_id, p2_name) = array[0][0], array[0][1], array[1][0], array[1][1]
        result.append((p1_id, p1_name, p2_id, p2_name))
    return result



