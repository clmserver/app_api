from flask import Blueprint, request, jsonify

from libs.es import ESearch

serach_blue = Blueprint("search_blue", __name__)

@serach_blue.route('/api/search/', methods=("GET",))
def search_view():
    keyword = request.args.get('keyword',None)
    search = ESearch('mtindex')
    return jsonify(search.query(keyword))
