from annotated_types import Le, Ge, Len, MaxLen
from typing import Annotated

from pydantic import BaseModel

TitleString = Annotated[
    str,
    Len(min_length=1, max_length=100),
]
DescriptionString = Annotated[
    str,
    MaxLen(200),
]
RatingInteger = Annotated[
    int,
    Ge(1),
    Le(10),
]


class MovieBase(BaseModel):
    title: str
    description: str
    rating: float


class MovieCreateSchema(MovieBase):
    """
    Модель для создания фильма
    """

    title: TitleString
    description: DescriptionString
    slug: Annotated[
        str,
        Len(min_length=3, max_length=50),
    ]
    rating: RatingInteger


class MovieUpdateSchema(MovieBase):
    """
    Модель для обновления фильма
    """

    title: TitleString
    description: DescriptionString
    rating: RatingInteger


class MovieUpdatePartialSchema(MovieBase):
    """
    Модель для частичного обновления фильма
    """

    title: TitleString | None = None
    description: DescriptionString | None = None
    rating: RatingInteger | None = None


class MovieRead(MovieBase):
    """
    Модель для чтения фильма
    """

    slug: str


class Movie(MovieBase):
    """
    Модель для представления фильма в API.
    """

    slug: str
    notes: (
        Annotated[
            str,
            MaxLen(300),
        ]
        | None
    ) = None
