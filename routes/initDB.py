from algoliasearch.search_client import SearchClient
from flask_restful import Resource

import pandas as pd
import sqlite3
import sys
import traceback

import os.path

from routes.config import DB_name, eprint, algoliaId, algoliaToken


class InitDb(Resource):

    def post(self):

        try:
            # ###########
            # Read data #
            # ###########
            data_url = "https://gist.githubusercontent.com/praagyajoshi/3a1c652667920924e6e399bf039d339d/raw/299a8cdf068d31b34d474b2e69ed130937d98b81/movies.json"
            df = pd.read_json(data_url)


            # ################
            # Transform data #
            # ################
            # Remove the `actor_facets` column
            df = df.drop(['actor_facets'], axis = 1)

            # Reduce score to 2 decimal
            df['score'] = round(df.score, 2)


            # #########################################
            # Create index and sync data with Algolia #
            # #########################################
            # Connect and authenticate with your Algolia app
            client = SearchClient.create(algoliaId, algoliaToken)
            index = client.init_index("movies")
            # Clean the index in case it already exists
            index.delete().wait()

            # Convert df into dict and export it into algolia API to create the index "movies"
            df_export = df.to_dict(orient='records')
            index.save_objects(df_export)


            # #####################
            # Create the local DB #
            # #####################
            # Create a new table for actors, alternative_title and genre
            df_actors = df[["objectID","actors"]]
            df_actors = df_actors.explode('actors')
            df = df.drop(['actors'], axis = 1)

            df_titles = df[["objectID","alternative_titles"]]
            df_titles = df_titles.explode('alternative_titles')
            df = df.drop(['alternative_titles'], axis = 1)

            df_genres = df[["objectID","genre"]]
            df_genres = df_genres.explode('genre')
            df = df.drop(['genre'], axis = 1)

            # Init connection with the DB and create Tables if not exist yet
            if os.path.exists(DB_name):
                os.remove(DB_name)
            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()
            print("Connection to the DB established")

            # Create 4 Tables
            # Movies as the central table with unique entrie
            # Actors, Titles, Genre for the multiple entries column
            # objectID is the foreign key
            cursor.execute("CREATE TABLE IF NOT EXISTS Movies (title TEXT, year INTEGER, image TEXT, color TEXT, score REAL, rating INTEGER, objectID INTEGER PRIMARY KEY)")
            cursor.execute("CREATE TABLE IF NOT EXISTS Actors (objectID INTEGER, actors TEXT, \
                FOREIGN KEY (objectID) REFERENCES Movies (objectID))")
            cursor.execute("CREATE TABLE IF NOT EXISTS Titles (objectID INTEGER, alternative_titles TEXT, \
                FOREIGN KEY (objectID) REFERENCES Movies (objectID))")
            cursor.execute("CREATE TABLE IF NOT EXISTS Genre (objectID INTEGER, genre TEXT, \
                FOREIGN KEY (objectID) REFERENCES Movies (objectID))")

            # Insert data from df into tables
            df.to_sql('Movies', conn, if_exists='append', index=False)
            df_actors.to_sql('Actors', conn, if_exists='append', index=False)
            df_titles.to_sql('Titles', conn, if_exists='append', index=False)
            df_genres.to_sql('Genre', conn, if_exists='append', index=False)

            # committing our connection
            conn.commit()
            
            # close our connection
            conn.close()

            return {'Message': "DB ready"}, 200

        except PermissionError:
            eprint(f"Error -- You don't have the required permission to access this file")
            return {'Message': "Error -- You don't have the required permission to access this file"}, 401
        except Exception:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
            return {'Message': "An error occured"}, 500

