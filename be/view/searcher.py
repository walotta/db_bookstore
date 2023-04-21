from flask import Blueprint
from flask import request
from flask import jsonify
from typing import List, Any
from be.model import searcher

bp_searcher = Blueprint("search", __name__, url_prefix="/search")


@bp_searcher.route("/find_book", methods=["POST"])
def find_book():
    """
    This function can find books with one dict
    Input:
        kind:           str
        store_id:       str
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
    The kind should be "one_dict","tags","content"
    The store_id could be None
    """
    kind: str = request.json.get("kind")
    store_id: str = request.json.get("store_id")
    dict_name: str = request.json.get("dict_name")
    value: List[str] = request.json.get("value")
    page_number: int = request.json.get("page_number")

    s = searcher.Searcher()

    if kind == "one_dict":
        total_page, books = s.find_book_with_one_dict(
            dict_name, value[0], page_number, store_id
        )
    elif kind == "tags":
        total_page, books = s.find_book_with_tag(value, page_number, store_id)
    elif kind == "content":
        total_page, books = s.find_book_with_content(value[0], page_number, store_id)
    else:
        pass

    code = 200
    return (
        jsonify(
            {
                "current_page": page_number,
                "total_page": total_page,
                "book_information": books,
            }
        ),
        code,
    )
