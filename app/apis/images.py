from flask_restplus import Resource, Namespace
from flask import jsonify
import requests

ns = Namespace('images', description='Images')

@ns.route('/<term>')
class Images(Resource):
    @staticmethod
    def get(term):
        try:
            url = f'https://pixabay.com/api/?key=11771710-8053c75c0a60a509145c0a14a&q={term}&image_type=photo&per_page=3'
            r = requests.get(url)
            return jsonify(r.json())
        except Exception:
            return '', 200
