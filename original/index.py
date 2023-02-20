from fastapi import FastAPI, Path, Query
from typing import Optional
from enum import Enum


BOOKS = {
    "book_1": {"title": "Title One", "author": "Author One"},
    "book_2": {"title": "Title Two", "author": "Author Two"},
    "book_5": {"title": "Title Five", "author": "Author Five"},
    "book_3": {"title": "Title Three", "author": "Author Three"},
    "book_4": {"title": "Title Four", "author": "Author Four"},
    "book_6": {"title": "Title Six", "author": "Author One"},
}


MIN_LENGTH = int(min(BOOKS).split("_")[-1])
MAX_LENGTH = int(max(BOOKS).split("_")[-1])


class BookOrder(str, Enum):
    ASC = "asc"
    DES = "des"


ordered_books = {
    "asc": sorted(BOOKS.items(), key=lambda x: int(x[0].split("_")[-1])),
    "des": sorted(BOOKS.items(), key=lambda x: -int(x[0].split("_")[-1])),
}


def unique_title_validator(title):
    UNICUQ_TITLE_VALIDATOR = [
        BOOKS[x] for x in BOOKS if title.lower() == BOOKS[x]["title"].lower()
    ]
    return UNICUQ_TITLE_VALIDATOR


app = FastAPI()


@app.get("/all_books")
async def get_all_books(
    order: Optional[BookOrder] = None, skipped: Optional[str] = None
) -> dict:
    """
    Get all books, parameter, validate order
    """
    if skipped and order:
        return {"message": "Not allowed two order in same time"}

    if skipped:
        NEW_BOOKS = BOOKS.copy()
        del NEW_BOOKS[skipped]
        return NEW_BOOKS

    if order:
        NEW_BOOKS = ordered_books[order]
        return NEW_BOOKS

    return BOOKS


@app.get("/old_current_book/{id_}")
async def get_current_book_number_old_style(id_: int):
    """
    Return books by store, validate from key value, old style
    """
    numbers_of_book = [int(b.split("_")[-1]) for b in BOOKS]
    if id_ not in numbers_of_book:
        return {"message": "Not Found book with that id"}
    return BOOKS[f"book_{id_}"]


@app.get("/current_book/{id_}")
async def get_current_book_number(
    id_: int = Path(title="Number of BOOKS length", ge=MIN_LENGTH, le=MAX_LENGTH)
):
    return BOOKS[f"book_{id_}"]


@app.get("/book_by_name/{name}")
async def return_book_by_key_name(name: str):
    """
    Return book from his key
    """
    if name.lower() not in BOOKS:
        return {"message": "That name was not in book store"}
    return BOOKS[name.lower()]


@app.get("/books_by_author_name/{name}")
async def get_book_by_author_name(name: str):
    """
    Return book by hist author name
    """
    result = [BOOKS[x] for x in BOOKS if name.lower() in BOOKS[x]["author"].lower()]
    if len(result):
        return {"result": result}
    return {"message": "That author not found in store"}


@app.get("/books_by_title/{title}")
async def return_book_by_title(name: str):
    """
    Return Book's by title
    """
    result = unique_title_validator(title)
    if len(result):
        return {"result": result}
    return {"message": "This title not found in store"}


# Post New book
@app.post("/new_book/{title}/{author}")
async def add_new_book(title: str, author: str):
    """
    Add new book, all is temporary, get last number and add second to increase that number
    """
    if len(BOOKS):
        validate_for_unique = unique_title_validator(title)
        if not len(validate_for_unique) > 0:
            current_length_of_books = MAX_LENGTH + 1
        else:
            return {"message": "That title already exists!"}
    else:
        current_length_of_books = 1

    new_name_of_book = f"book_{current_length_of_books}"
    BOOKS[new_name_of_book] = {"title": title, "author": author}
    return BOOKS


# Put with one path, and two query parameter's
@app.put("/current_book/{name}")
async def update_book(name: str, title: str, author: str):
    if name not in BOOKS:
        return {"message": "That name not in stock, change close"}

    validate_for_unique = unique_title_validator(title)

    if len(validate_for_unique):
        return {"message": "Taht tile is already in stock, change close"}

    BOOKS[name]["title"] = title
    BOOKS[name]["author"] = author

    return BOOKS


@app.patch("/current_book/{name}")
async def patch_book(
    name: str, title: Optional[str] = None, author: Optional[str] = None
):
    """
    Patch implementing
    """
    if name not in BOOKS:
        return {"message": "That name not in stock, change close"}

    if title:
        validate_for_unique = unique_title_validator(title)
        if len(validate_for_unique):
            return {"message": "That tile already exists in stock"}

    temporary_book = {"title": title, "author": author}

    temporary_book = {k: v for k, v in temporary_book.items() if v is not None}

    BOOKS[name].update(temporary_book)
    return BOOKS[name]


# Delete path
@app.delete("/delete/")
async def delete_book(name: str = Query(...)):
    """
    Delete with query paramether
    """
    if name in BOOKS:
        del BOOKS[name]
        return {"message": "Successfully delete that book", "status_code": 204}

    return {"message": "Error that name not found", "statuc_code": 404}
