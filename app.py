from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

language_dto = api.model('Language', {'language': fields.String('The language.')})

language = []
python = {'language' : 'python'}
language.append(python)

@api.route('/language')
class Languafe(Resource):
    def get(self):
        return language

    @api.expect(language_dto)
    def post(self):
        language.append(api.payload)
        return {'result': 'Language added'}, 201

if __name__ == '__main__':
    app.run(debug=True)