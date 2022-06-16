from flask_restful import Resource

class Movies(Resource):

    def get(self):
        return {'data': "My important Data"}, 200  # return data with 200 OK


