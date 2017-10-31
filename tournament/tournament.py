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
    db = connect()
    cursor = db.cursor()
    cursor.execute("update players set numWins = 0, numMatches = 0;")
    cursor.execute("delete from matches;")
    db.commit()
    db.close()

def deletePlayers():
    db = connect()
    cursor = db.cursor()    
    cursor.execute("delete from players;")
    db.commit()
    db.close()
    """Remove all the player records from the database."""

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("select count(*) from players;")
    result = cursor.fetchall()
    return result[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cmd = "insert into players(name,numMatches,numWins) values (%s, %s, %s);"
    cursor.execute(cmd, (name, 0, 0))
    db.commit()
    db.close()

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
    db = connect()
    cursor = db.cursor()
    cursor.execute("select id, name, numWins, numMatches from players order by numWins desc;")
    return cursor.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cmd = "insert into matches (winner, loser) values (%s, %s);"
    cursor.execute(cmd, (winner, loser))
    cmd = "update players set numMatches = numMatches + 1 where id = %s or id = %s;"
    cursor.execute(cmd, (winner,loser)) 
    cmd = "update players set numWins = numWins+1 where id = %s;"
    cursor.execute(cmd, (winner,))
    db.commit()
    db.close()
 
 
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
    
    # db = connect()
    # cursor = db.cursor()
    # cursor.execute("""select distinct temp.id1 , temp.n1, temp.id2, temp.n2 from 
    #     (select a.id as id1, a.name as n1, b.id as id2, b.name as n2
    #         from players as a, 
    #         players as b
    #         where a.numWins = b.numWins and
    #               a.numMatches = b.numMatches and
    #               a.id < b.id) as temp;""")
    # return cursor.fetchall()

    rankings = playerStandings()
    pairings = []
    for i in range(0, len(rankings), 2):
        (id1, name1, wins1, matches1) = rankings[i]
        (id2, name2, wins2, matches2) = rankings[i+1]
        if wins1 == wins2 and matches1 == matches2:
            pairings.append((id1, name1, id2, name2))
        else:
            return []
    return pairings

