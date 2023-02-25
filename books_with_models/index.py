from fastapi import FastAPI, HTTPException, Header

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from enum import Enum


from custom_exceptions.not_found_exception import raise_not_found_exception

app = FastAPI()


class BookReturn(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    price: float


class Book(BookReturn):
    id: UUID
    description: Optional[str] = Field(max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "id": "1367e493-5030-4a22-9f1d-c50638b4c04b",
                "name": "Borko",
                "description": "Book description",
                "price": 99.00,
            }
        }


class SortedBooks(str, Enum):
    Name = "name"
    Price = "price"


def custom_sorted(shelf):
    custom_sorted = {
        "name": shelf.sort(key=lambda x: x.name),
        "price": shelf.sort(key=lambda x: x.price),
    }
    return custom_sorted


BOOKS = []


def temporary_added_book_to_books():
    book_1 = Book(
        id="7367e493-5030-4a22-9f1d-c50638b4c04b",
        name="Book One",
        description="Description for first book",
        price=50.11,
    )

    book_2 = Book(
        id="70e70074-f0c0-4b54-8e45-f0774cc5115f",
        name="Book Two",
        description="Description for second book",
        price=20.11,
    )

    book_3 = Book(
        id="2c108374-79e4-41af-9f35-11b9f438bb80",
        name="Book Three",
        price=30.11,
    )

    book_4 = Book(
        id="54527d86-e956-4738-a1b5-e991c01e7c4a",
        name="Book Four",
        description="Description for fourth book",
        price=40.11,
    )

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


@app.get("/check_is_working", status_code=200)
async def check_is_work():
    return {"status": 200}


@app.get("/books", response_model=List[BookReturn])
async def return_all_books(
    l: Optional[int] = None,
    sorted: Optional[SortedBooks] = None,
    check_header: Optional[str] = Header(None),
) -> List[BookReturn]:
    if not check_header == "Borko":
        raise HTTPException(status_code=400)
    if len(BOOKS) == 0:
        temporary_added_book_to_books()

    TEMPORARY_BOOKS = BOOKS.copy()

    if sorted:
        print(sorted)
        custom_sorted(TEMPORARY_BOOKS)[sorted.value]

    if l and l < len(BOOKS):
        return TEMPORARY_BOOKS[:l]

    return TEMPORARY_BOOKS


@app.get("/book/{name}", status_code=200)
async def retrurn_book_by_id(name: str):
    book = [b for b in BOOKS if b.name.lower() == name.lower()]
    try:
        return book[0]
    except IndexError:
        raise_not_found_exception()


@app.post("/add_new_book", status_code=201)
async def add_new_book(book: Book):
    BOOKS.append(book)
    return {"message": "Write successfully"}


@app.put("/book/{id_}", status_code=201)
async def change_book(id_: UUID, book: Book) -> dict:
    for pos, line in enumerate(BOOKS):
        if line.id == id_:
            BOOKS[pos] = book
            return BOOKS[pos]
    raise_not_found_exception()


@app.delete("/book/{id_}", status_code=204)
async def remove_book(id_: UUID):
    for pos, line in enumerate(BOOKS):
        if line.id == id_:
            del BOOKS[pos]
            return 204
    raise_not_found_exception()
