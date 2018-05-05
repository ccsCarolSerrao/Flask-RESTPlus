from flask import Flask, Blueprint, request
from flask_restplus import Api, Resource, fields
from functools import wraps

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
            blueprint, 
            authorizations=authorizations,
            doc='/documentation'
        ) #,doc=False - Turn off - Don't show swagger documentation 

app.register_blueprint(blueprint)

def token_required(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        
        if not token:
            return {'message': 'Token is missing.'}, 401

        if token != 'mytoken':
            return {'message': 'Token is wrong.'}, 401
        
        return f(*args, **kwargs)
    
    return decorate

        

app.config['SWAGGER_UI_JSONEDITOR'] = True

language_dto = api.model('Language', {'language': fields.String('The language.')})

language = []
python = {'language' : 'python', 'id': 1}
language.append(python)

@api.route('/language')
class Languafe(Resource):
    @api.doc(security='apikey')
    @token_required
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