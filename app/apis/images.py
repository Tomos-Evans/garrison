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
            return 'https://media.licdn.com/dms/image/C4E03AQFqPA_LxawS7w/profile-displayphoto-shrink_800_800/0?e=1556755200&v=beta&t=mmZjGheYXuFeUK6bQ1cOSmTv46G5Bf46B8lHwPJrT1A', 200
