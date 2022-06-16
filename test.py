#!/usr/bin/env python3


import sys
import pandas as pd

import sqlite3
import sys
import traceback


debug = True

def main():

    # data_url = "https://gist.githubusercontent.com/praagyajoshi/3a1c652667920924e6e399bf039d339d/raw/299a8cdf068d31b34d474b2e69ed130937d98b81/movies.json"

    df = pd.read_json("./movies.json") # DEBUG
    # df = pd.read_json(data_url)

    # Remove the `actor_facets` column
    df = df.drop(['actor_facets'], axis = 1)
    # df = df.drop(['alternative_titles'], axis = 1)

    # Reduce score to 2 decimal
    df['score'] = round(df.score, 2)

    print(df.info())

    #  Create a new df for actors
    df_actors = df[["objectID","actors"]]
    df_actors = df_actors.explode('actors')
    print(df_actors.info())
    print(df_actors)
    # Drop actors from movie list
    df = df.drop(['actors'], axis = 1)

    df_titles = df[["objectID","alternative_titles"]]
    df_titles = df_titles.explode('alternative_titles')
    print(df_titles.info())
    print(df_titles)
    # Drop alternative_titles from movie list
    df = df.drop(['alternative_titles'], axis = 1)

    df_genres = df[["objectID","genre"]]
    df_genres = df_genres.explode('genre')
    print(df_genres.info())
    print(df_genres)
    # Drop genre from movie list
    df = df.drop(['genre'], axis = 1)

    print(df.info())
    print(df)

    try:
        # Init connection with the DB and create Tables if not exist yet
        conn = sqlite3.connect("movies_algolia.db")
        cursor = conn.cursor()
        print("Connection to the DB established")

        # Create 4 Tables
        # Movies as the central table with unique entrie
        # Actors, Titles, Genre for the multiple entries column
        # objectID is the foreign key
        cursor.execute("CREATE TABLE IF NOT EXISTS Movies (title TEXT, year INT, image TEXT, color TEXT, score REAL, rating INT, objectID INT UNIQUE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Actors (objectID INT, actors TEXT, \
            FOREIGN KEY (objectID) REFERENCES Movies (objectID))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Titles (objectID INT, alternative_titles TEXT, \
            FOREIGN KEY (objectID) REFERENCES Movies (objectID))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Genre (objectID INT, genre TEXT, \
            FOREIGN KEY (objectID) REFERENCES Movies (objectID))")

        # Insert data from df into tables
        df.to_sql('Movies', conn, if_exists='append', index=False)
        df_actors.to_sql('Actors', conn, if_exists='append', index=False)
        df_titles.to_sql('Titles', conn, if_exists='append', index=False)
        df_genres.to_sql('Genre', conn, if_exists='append', index=False)



    except PermissionError:
        eprint(f"Error -- You don't have the required permission to access this file")
    except Exception:
        if debug:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
        else:
            eprint("Error -- Exit the program.")



def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



if __name__ == "__main__":
    main()
