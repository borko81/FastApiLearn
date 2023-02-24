from fastapi import HTTPException


def raise_not_found_exception():
    raise HTTPException(
        status_code=404,
        detail=f"That not found",
        headers={"X-Header-Error": f"Not found "},
    )
