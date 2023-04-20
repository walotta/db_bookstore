from flask import Blueprint
from flask import request
from flask import jsonify
from typing import List, Any
from be.model import searcher

bp_searcher = Blueprint("auth", __name__, url_prefix="/auth")


@bp_searcher.route("/find_book", methods=["POST"])
def find_book():
    # user_id: str = request.json.get("user_id")
    # store_id: str = request.json.get("store_id")
    # books: List[Any] = request.json.get("books")
    # id_and_count = []
    # for book in books:
    #     book_id = book.get("id")
    #     count = book.get("count")
    #     id_and_count.append((book_id, count))

    # b = Buyer()
    # code, message, order_id = b.new_order(user_id, store_id, id_and_count)
    # return jsonify({"message": message, "order_id": order_id}), code
    pass
