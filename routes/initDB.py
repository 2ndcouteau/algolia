from flask_restful import Resource, Api, reqparse

import sys
import pandas as pd

import sqlite3
import sys


class InitDb(Resource):

    def post(self):


        # data_url = "https://gist.githubusercontent.com/praagyajoshi/3a1c652667920924e6e399bf039d339d/raw/299a8cdf068d31b34d474b2e69ed130937d98b81/movies.json"

        df = pd.read_json("./movies.json") # DEBUG
        # df = pd.read_json(data_url)

        print(df.info())

        return {'Message': "DB ready"}, 200


