from annotated_types import Le, Ge, Len
from typing import Annotated

from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: str
    rating: float


class MovieCreateSchema(MovieBase):
    """
    Модель для создания фильма
    """

    title: Annotated[
        str,
        Len(min_length=5, max_length=100),
    ]
    description: Annotated[
        str,
        Len(min_length=10, max_length=250),
    ]
    rating: Annotated[
        int,
        Ge(1),
        Le(10),
    ]


class Movie(MovieBase):
    """
    Модель для представления фильма в API.
    """

    id: int
