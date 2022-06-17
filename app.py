from flask import Flask
from flask_restful import Api

from routes.initDB import InitDb
from routes.movies import Movies


app = Flask(__name__)
api = Api(app)


api.add_resource(Movies, '/api/v1/movies')
api.add_resource(InitDb, '/api/v1/initdb')


@app.route('/')
def Hello_algolia():
    return '<h1>Hello in my Algolia Test</h1>'


if __name__ == "__main__":
    app.run(debug=True)