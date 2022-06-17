from flask_restful import Resource
from flask import request

from routes.config import DB_name, eprint

import traceback
import sqlite3
import sys

class Movies(Resource):

    def post(self):

        try:
            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()
            print("Connection to the DB established")

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

            return {'Message': "Creation success", "MovieId": f"{movieId}"}, 201
        
        except PermissionError:
            eprint(f"Error -- You don't have the required permission to access this file")
            return {'Message': "Error -- You don't have the required permission to access this file"}, 401
        except Exception:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
            return {'Message': "An error occured"}, 500


    def put(self):
        try:
            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()
            print("Connection to the DB established")

            content_type = request.headers.get('Content-Type')
            if not (content_type == 'application/json'):
                {'Message': "Content-Type not supported!"}, 400
                return 'Content-Type not supported!'

            json = request.json

            if not json.get("MovieId"):
                return {'Message': "MovieId is required"}, 400

            cursor.execute("BEGIN TRANSACTION;")

            # INSERT UPDATE INFO REQUEST

            cursor.execute("COMMIT")
            conn.commit() # Need to commit to save the update in the DB
            conn.close()

            return {'Message': "Movie Updated"}, 201

        except PermissionError:
            eprint(f"Error -- You don't have the required permission to access this file")
            return {'Message': "Error -- You don't have the required permission to access this file"}, 401
        except Exception:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
            return {'Message': "An error occured"}, 500


    def delete(self):

        try:
            conn = sqlite3.connect(DB_name)
            cursor = conn.cursor()
            print("Connection to the DB established")

            content_type = request.headers.get('Content-Type')
            if not (content_type == 'application/json'):
                {'Message': "Content-Type not supported!"}, 400
                return 'Content-Type not supported!'

            json = request.json

            if not json.get("MovieId"):
                return {'Message': "MovieId is required"}, 400

            cursor.execute("BEGIN TRANSACTION;")

            # INSERT DELETE MOVIE REQUEST

            cursor.execute("COMMIT")
            conn.commit() # Need to commit to save the update in the DB
            conn.close()

            return {'Message': "Movie Deleted"}, 201

        except PermissionError:
            eprint(f"Error -- You don't have the required permission to access this file")
            return {'Message': "Error -- You don't have the required permission to access this file"}, 401
        except Exception:
            eprint(f"Error -- Exit the program...\n{traceback.print_exception(*sys.exc_info())}")
            return {'Message': "An error occured"}, 500


    def get(self):
        return {'Message': "Get movie not implemented"}, 200  # return data with 200 OK
