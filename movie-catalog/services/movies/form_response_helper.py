from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse

from templating import templates


class FormResponseHelper:
    def __init__(
        self,
        model: type[BaseModel],
        template_name: str,
    ) -> None:
        self.model = model
        self.template_name = template_name

    @classmethod
    def format_pydantic_error(
        cls,
        error: ValidationError,
    ) -> dict[str, str]:
        return {str(err["loc"][0]): err["msg"] for err in error.errors()}

    def render(
        self,
        request: Request,
        *,
        form_data: BaseModel | Mapping[str, Any] | None = None,
        errors: dict[str, str] | None = None,
        pydantic_error: ValidationError | None = None,
        form_validated: bool = False,
    ) -> HTMLResponse:
        context: dict[str, Any] = {}
        model_schema = self.model.model_json_schema()

        if pydantic_error:
            errors = self.format_pydantic_error(pydantic_error)

        context.update(
            model_schema=model_schema,
            errors=errors,
            form_validated=form_validated,
            form_data=form_data,
        )
        return templates.TemplateResponse(
            request=request,
            name=self.template_name,
            context=context,
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
                if form_validated and errors
                else status.HTTP_200_OK
            ),
        )
