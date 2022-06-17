from algoliasearch.search_client import SearchClient

from flask_restful import Resource
from flask import Flask, request

from routes.config import DB_name, eprint, algoliaId, algoliaToken, index_name

import traceback
import sqlite3
import sys

app = Flask(__name__)

class Movies(Resource):

    def post(self, movieId=None):

        try:
            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()
            # print("Connection to the DB established")

            content_type = request.headers.get('Content-Type')
            if not (content_type == 'application/json'):
                {'Message': "Content-Type not supported!"}, 400
                return 'Content-Type not supported!'

            #  Get Params from json form
            json = request.json

            if not json.get("title") or not json.get("year"):
                return {'Message': "Title and Year are required"}, 400

            # Check if the movie already exist in DB
            notNewMovie = cursor.execute("SELECT title FROM Movies WHERE title=? AND year=?", (json.get("title"), json.get("year"),)).fetchone()
            if notNewMovie:
                return {'Message': f'The movie \'{json.get("title")} - {json.get("year")}\' has already been inserted in the DB'}, 400

            cursor.execute("BEGIN TRANSACTION;")

            ret = cursor.execute("INSERT INTO Movies('title','year','image','color','score','rating') VALUES (?, ?, ?, ?, ?, ?)",
            (json.get("title"),
            json.get("year"),
            json.get("image", None),
            json.get("color", None),
            json.get("score", None),
            json.get("rating", None),))

            #  Save the MovieId/objectID to return it in the response
            movieId = ret.lastrowid

            # For each params, check if exist and insert it in its normalized table
            if json.get("actors", None):
                actors_insert = [(elem ,movieId) for elem in json.get("actors")] if isinstance(json.get("actors"), list) else [(json.get("actors"), movieId)]
                cursor.executemany("INSERT INTO Actors ('actors','objectID') VALUES (?, ?)", actors_insert)

            if json.get("alternative_titles", None):
                titles_insert = [(elem ,movieId) for elem in json.get("alternative_titles")] if isinstance(json.get("alternative_titles"), list) else [(json.get("alternative_titles"), movieId)]
                cursor.executemany("INSERT INTO Title ('alternative_titles','objectID') VALUES (?, ?)", titles_insert)

            if json.get("genre", None):
                genre_insert = [(elem ,movieId) for elem in json.get("genre")] if isinstance(json.get("genre"), list) else [(json.get("genre"), movieId)]
                cursor.executemany("INSERT INTO Genre ('genre','objectID') VALUES (?, ?)", genre_insert)

            cursor.execute("COMMIT")
            conn.commit() # Need to commit to save the insert in the DB
            conn.close()

            # SYNC with Algolia-API
            # Connect and authenticate with your Algolia app
            client = SearchClient.create(algoliaId, algoliaToken)
            index = client.init_index(index_name)
            index.save_object({
                'title': json.get("title"),
                'year': json.get("year"),
                'image': json.get("image", None),
                'color': json.get("color", None),
                'score': json.get("score", None),
                'rating': json.get("rating", None),
                'actors': json.get("actors", None),
                'alternative_titles': json.get("alternative_titles", None),
                'genre': json.get("genre", None),
                'objectID': movieId
            })

            return {'Message': "Creation success", "MovieId": f"{movieId}"}, 201
        
        except PermissionError:
            eprint(f"Error -- You don't have the required permission to access this file")
            return {'Message': "Error -- You don't have the required permission to access this file"}, 401
        except Exception:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
            return {'Message': "An error occured"}, 500

    def put(self, movieId=None):
        try:
            if not movieId:
                return {'Message': "movieId is required in the path url"}, 400

            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()
            # print("Connection to the DB established")

            content_type = request.headers.get('Content-Type')
            if not (content_type == 'application/json'):
                {'Message': "Content-Type not supported!"}, 400
                return 'Content-Type not supported!'

            json = request.json

            # Check if the movie exist in DB
            notNewMovie = cursor.execute("SELECT objectID FROM Movies WHERE objectID=?", (movieId,)).fetchone()
            if not notNewMovie:
                return {'Message': f'The movie \'{movieId}\' does not exist in DB'}, 400

            cursor.execute("BEGIN TRANSACTION;")

            # Update Movies table only if necessary
            if any([key in json for key in ["title", "year", "image", "color", "score", "rating"]]):
                req = "UPDATE Movies SET "
                params = []
                if json.get("title", None):
                    req += "title = ?,"
                    params.append(json.get("title"))
                if json.get("year", None):
                    req += "year = ?,"
                    params.append(json.get("year"))
                if json.get("image", None):
                    req += "image = ?,"
                    params.append(json.get("image"))
                if json.get("color", None):
                    req += "color = ?,"
                    params.append(json.get("color"))
                if json.get("score", None):
                    req += "score = ?,"
                    params.append(json.get("score"))
                if json.get("rating", None):
                    req += "rating = ?,"
                    params.append(json.get("rating"))

                #  Remove the last comma
                req = req[:-1]

                req += " WHERE objectID = ?"
                params.append(movieId)

                cursor.execute(req, params)


            # For each params, check if exist and update/replace it in its normalized table
            if json.get("actors", None):
                cursor.execute("DELETE FROM Actors WHERE objectID = ? ", (movieId,))
                actors_insert = [(elem ,movieId) for elem in json.get("actors")] if isinstance(json.get("actors"), list) else [(json.get("actors"), movieId)]
                cursor.executemany("INSERT INTO Actors ('actors','objectID') VALUES (?, ?)", actors_insert)

            if json.get("alternative_titles", None):
                cursor.execute("DELETE FROM Titles WHERE objectID = ? ", (movieId,))
                titles_insert = [(elem ,movieId) for elem in json.get("alternative_titles")] if isinstance(json.get("alternative_titles"), list) else [(json.get("alternative_titles"), movieId)]
                cursor.executemany("INSERT INTO Titles ('alternative_titles','objectID') VALUES (?, ?)", titles_insert)

            if json.get("genre", None):
                cursor.execute("DELETE FROM Genre WHERE objectID = ? ", (movieId,))
                genre_insert = [(elem ,movieId) for elem in json.get("genre")] if isinstance(json.get("genre"), list) else [(json.get("genre"), movieId)]
                cursor.executemany("INSERT INTO Genre ('genre','objectID') VALUES (?, ?)", genre_insert)


            cursor.execute("COMMIT")
            conn.commit() # Need to commit to save the update in the DB
            conn.close()

            # SYNC with Algolia-API
            # Connect and authenticate with your Algolia app
            client = SearchClient.create(algoliaId, algoliaToken)
            index = client.init_index(index_name)
            index.partial_update_object({
                'title': json.get("title"),
                'year': json.get("year"),
                'image': json.get("image", None),
                'color': json.get("color", None),
                'score': json.get("score", None),
                'rating': json.get("rating", None),
                'actors': json.get("actors", None),
                'alternative_titles': json.get("alternative_titles", None),
                'genre': json.get("genre", None),
                'objectID': movieId
            })

            return {'Message': f"Movie {movieId} Updated"}, 201

        except PermissionError:
            eprint(f"Error -- You don't have the required permission to access this file")
            return {'Message': "Error -- You don't have the required permission to access this file"}, 401
        except Exception:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
            return {'Message': "An error occured"}, 500


    def delete(self, movieId=None):

        try:
            if not movieId:
                return {'Message': "movieId is required in the path url"}, 400

            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()
            # print("Connection to the DB established")

            # Check if the movie exist in DB
            notNewMovie = cursor.execute("SELECT objectID FROM Movies WHERE objectID=?", (movieId,)).fetchone()
            if not notNewMovie:
                return {'Message': f'The movie \'{movieId}\' does not exist in DB'}, 400

            cursor.execute("BEGIN TRANSACTION;")

            # Delete all the entries with the target movieId
            cursor.execute("DELETE FROM Movies WHERE objectID = ? ", (movieId,))
            cursor.execute("DELETE FROM Actors WHERE objectID = ? ", (movieId,))
            cursor.execute("DELETE FROM Titles WHERE objectID = ? ", (movieId,))
            cursor.execute("DELETE FROM Genre WHERE objectID = ? ", (movieId,))

            cursor.execute("COMMIT")
            conn.commit() # Need to commit to save the update in the DB
            conn.close()

            # SYNC with Algolia-API
            # Connect and authenticate with your Algolia app
            client = SearchClient.create(algoliaId, algoliaToken)
            index = client.init_index(index_name)
            index.delete_object(movieId)

            return {'Message': f"Movie {movieId} deleted"}, 201

        except PermissionError:
            eprint(f"Error -- You don't have the required permission to access this file")
            return {'Message': "Error -- You don't have the required permission to access this file"}, 401
        except Exception:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
            return {'Message': "An error occured"}, 500


    def get(self):
        return {'Message': "Get movie not implemented"}, 200
