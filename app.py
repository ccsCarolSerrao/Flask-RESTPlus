from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation') #,doc=False - Turn off - Don't show swagger documentation 

app.register_blueprint(blueprint)

app.config['SWAGGER_UI_JSONEDITOR'] = True

language_dto = api.model('Language', {'language': fields.String('The language.')})

language = []
python = {'language' : 'python', 'id': 1}
language.append(python)

@api.route('/language')
class Languafe(Resource):
    @api.marshal_with(language_dto, envelope='data')
    def get(self):
        return language

    @api.expect(language_dto)
    def post(self):
        new_language = api.payload
        new_language['id'] = len(language) + 1
        language.append(new_language)
        return {'result': 'Language added'}, 201

if __name__ == '__main__':
    app.run(debug=True)