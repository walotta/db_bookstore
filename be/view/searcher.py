from flask import Blueprint
from flask import request
from flask import jsonify
from typing import List, Any
from be.model import searcher

bp_searcher = Blueprint("search", __name__, url_prefix="/search")


@bp_searcher.route("/find_book_with_one_dict", methods=["POST"])
def find_book_with_one_dict():
    """
    This function can find books with one dict
    Input:
        dict_name:      str
        value:          str/int
        page_number:    int

    Return:
        {page_number, current_page}, List[store_id, book_title], return_code

    the dict can search by this function include:
        id: str
        title: str
        author: str
        publisher: str
        original_title: str
        translator: str
        pub_year: str
        pages: int
        price: int
        currency_unit: int
        binding: str
        isbn: str
        author_intro: str
        book_intro: str
    We can only search for the book whose property is fully match on these dicts.
    """
    dict_name: str = request.json.get("dict_name")
    value: List[Any] = request.json.get("value")
    # todo

    s = searcher.Searcher()

    code, book = s.find_book_with_one_dict(dict_name, value)
    return jsonify({"book": book}), code


@bp_searcher.route("/find_book_with_content", methods=["POST"])
def find_book_with_content():
    content_piece: str = request.json.get("content")

    s = searcher.Searcher()

    code, book = s.find_book_with_content(content_piece)
    return jsonify({"book": book}), code
