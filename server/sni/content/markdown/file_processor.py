from dataclasses import dataclass
from typing import Any, Type, TypeVar

from pydantic import BaseModel, ValidationError

from .renderer import MDRenderer

T = TypeVar("T", bound=BaseModel)


@dataclass
class ValidationResult:
    model: BaseModel | None
    data: dict[Any, Any] | None
    errors: list[str]
    is_valid: bool


def validate_single(data: dict[Any, Any] | None, schema: Type[T]) -> ValidationResult:
    if not data:
        return ValidationResult(None, None, ["No front matter provided"], False)

    try:
        model = schema.model_validate(data)
        return ValidationResult(model, model.model_dump(), [], True)
    except ValidationError as e:
        errors = []
        for error in e.errors():
            location = " -> ".join(str(loc) for loc in error["loc"])
            msg = f"{location}: {error['msg']}"
            errors.append(msg)
        return ValidationResult(None, None, errors, False)


def validate_front_matter(
    data: dict[Any, Any] | None, schemas: dict[str, Type[BaseModel]]
) -> dict[str, ValidationResult]:
    return {key: validate_single(data, schema) for key, schema in schemas.items()}


def process_file(
    filepath: str,
    schemas: dict[str, Type[BaseModel]],
) -> tuple[dict[str, ValidationResult], str, str]:
    raw_front_matter, processed_content, raw_content = MDRenderer.process_md(filepath)
    validation_results = validate_front_matter(raw_front_matter, schemas)

    failed_schemas = {
        key: results.errors
        for key, results in validation_results.items()
        if not results.is_valid
    }
    if failed_schemas:
        error_details = "\n".join(
            f"{schema}: {'; '.join(errors)}"
            for schema, errors in failed_schemas.items()
        )
        raise ValueError(
            f"File '{filepath}' failed schema validation:\n{error_details}"
        )

    return validation_results, processed_content, raw_content
