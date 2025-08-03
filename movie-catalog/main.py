import uvicorn
from fastapi import (
    FastAPI,
    Request,
)

app = FastAPI(title="Movie Catalog")


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
