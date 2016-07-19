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

    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM scores;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(id) FROM players;")
    rows = c.fetchall()
    conn.close()
    return int(rows[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    conn.commit()
    c = conn.cursor()
    c.execute("""
              INSERT INTO scores (player, wins, losses)
              VALUES ((SELECT id FROM players WHERE name = %s),0,0);
              """, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("""
              SELECT s.player, p.name, s.wins, s.wins + s.losses
              FROM scores AS s
              INNER JOIN players AS p ON p.id = s.player
              ORDER BY wins DESC;
              """)
    rows = c.fetchall()
    conn.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE scores SET wins = wins + 1 WHERE player = %s;",
              (winner,))
    c.execute("UPDATE scores SET losses = losses + 1 WHERE player = %s",
              (loser,))
    conn.commit()
    conn.close()


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
        name2: the second player's name2
    """
    conn = connect()
    c = conn.cursor()

    # create pairings by:
    # 1. get ids, players, scores ordered by wins descending
    # 2. pair adjacent rows by joining even rows and odd rows from 1.
    # NOTE: referenced this stackoverflow post about
    # joining tables by row number: http://bit.ly/1Nz0N0q
    c.execute("""
              SELECT even.player, even.name, odd.player, odd.name
              FROM (
                SELECT even.player, even.name, ROW_NUMBER()
                        OVER (ORDER BY wins DESC) AS row
                    FROM (
                        SELECT s.player, p.name, s.wins, ROW_NUMBER()
                            OVER (ORDER BY wins DESC) AS row
                        FROM scores AS s
                        INNER JOIN players AS p ON p.id = s.player
                    ) AS even
                WHERE even.row % 2 = 1
              ) even
              JOIN (
                SELECT odd.player, odd.name, ROW_NUMBER()
                        OVER (ORDER BY wins DESC) AS row
                    FROM (
                        SELECT s.player, p.name, s.wins, ROW_NUMBER()
                            OVER (ORDER BY wins DESC) AS row
                        FROM scores AS s
                        INNER JOIN players AS p ON p.id = s.player
                    ) AS odd
                WHERE odd.row % 2 = 0
              ) odd
              ON even.row = odd.row;
              """)

    rows = c.fetchall()
    conn.close()
    return rows
