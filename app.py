from flask import Flask
from flask_restful import Api

from routes.initDB import InitDb
from routes.movies import Movies


app = Flask(__name__)
api = Api(app)


api.add_resource(Movies, '/api/v1/movies')
api.add_resource(InitDb, '/api/v1/initdb')


# @app.route('/api/v1/movies') # POST
# @app.route('/api/v1/movies') # PUT
# @app.route('/api/v1/movies') # DELETE
# @app.route('/api/v1/initdb') # POST


@app.route('/')
def Hello_algolia():
    return '<h1>Hello Algolia Test</h1>'



if __name__ == "__main__":
    app.run(debug=True)