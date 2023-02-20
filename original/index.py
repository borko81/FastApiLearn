from fastapi import FastAPI


BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
    'book_6': {'title': 'Title Six', 'author': 'Author One'},
}


app = FastAPI()


@app.get('/all_books')
async def get_all_books() -> dict:
    return BOOKS


@app.get('/current_book/{id_}')
async def get_current_book_number(id_: int):
    """
        Return all books from store
    """
    numbers_of_book = [int(b.split('_')[-1]) for b in BOOKS]
    print(numbers_of_book)
    if id_ not in numbers_of_book:
        return {"message": "Not Found book with that id"}
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
    result = [BOOKS[x]
              for x in BOOKS if name.lower() in BOOKS[x]['author'].lower()]
    if len(result):
        return {"result": result}
    return {"message": "That author not found in store"}


@app.get("/books_by_title/{name}")
async def return_book_by_title(name: str):
    """
        Return Book's by title
    """
    result = [BOOKS[x]
              for x in BOOKS if name.lower() in BOOKS[x]['title'].lower()]
    if len(result):
        return {"result": result}
    return {"message": "This title not found in store"}
