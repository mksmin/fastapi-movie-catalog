from pydantic import BaseModel


class MovieBase(BaseModel):
    id: int
    title: str
    description: str
    rating: float


class Movie(MovieBase):
    """
    Модель для представления фильма в API.
    """
