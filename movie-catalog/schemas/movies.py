from typing import Annotated

from annotated_types import Ge, Le, Len, MaxLen
from pydantic import BaseModel

DESCRIPTION_MAX_LENGTH = 200
TITLE_MAX_LENGTH = 100

TitleString = Annotated[
    str,
    Len(min_length=1, max_length=TITLE_MAX_LENGTH),
]
DescriptionString = Annotated[
    str,
    MaxLen(DESCRIPTION_MAX_LENGTH),
]
RatingInteger = Annotated[
    int,
    Ge(1),
    Le(10),
]


class MovieBase(BaseModel):
    title: TitleString
    description: DescriptionString
    rating: RatingInteger


class MovieCreate(MovieBase):
    """
    Модель для создания фильма
    """

    title: TitleString
    description: DescriptionString = ""
    slug: Annotated[
        str,
        Len(min_length=3, max_length=50),
    ]
    rating: RatingInteger


class MovieUpdate(MovieBase):
    """
    Модель для обновления фильма
    """


class MovieUpdateForm(MovieBase):
    """
    Модель для обновления фильма в форме
    """

    description: DescriptionString = ""


class MovieUpdatePartial(BaseModel):
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
