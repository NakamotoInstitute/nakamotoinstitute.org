import os
from typing import Any, Dict, List, Optional, Tuple, Type

import yaml
from pydantic import BaseModel, ValidationError


def read_markdown_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def parse_front_matter(content: str) -> Tuple[Optional[Dict[Any, Any]], str]:
    split_content = content.split("---\n")
    if len(split_content) < 3:
        return None, content
    front_matter_str = split_content[1]
    remaining_content = "---\n".join(split_content[2:]).strip()
    return yaml.safe_load(front_matter_str), remaining_content


def validate_front_matter(
    front_matter: Dict[Any, Any], schema: Type[BaseModel]
) -> Optional[BaseModel]:
    try:
        return schema.parse_obj(front_matter)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None


def process_markdown_file(
    filepath: str, schema: Type[BaseModel]
) -> Tuple[Optional[Dict[Any, Any]], str]:
    content = read_markdown_file(filepath)
    raw_front_matter, remaining_content = parse_front_matter(content)

    if raw_front_matter:
        validated_front_matter = validate_front_matter(raw_front_matter, schema)
        if validated_front_matter:
            return validated_front_matter.dict(), remaining_content
        else:
            return None, remaining_content

    return None, content


def load_all_markdown_files(
    directory_path: str, schema: Type[BaseModel]
) -> List[Dict[str, Any]]:
    files_data: List[Dict[str, Any]] = []

    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".md"):
            filepath = os.path.join(directory_path, filename)
            front_matter_dict, remaining_content = process_markdown_file(
                filepath, schema
            )

            if front_matter_dict is not None:
                file_data = dict(
                    **front_matter_dict,
                    slug=filename.split(".")[0],
                    content=remaining_content,
                )
                files_data.append(file_data)

    return files_data


def extract_data_from_filename(filename):
    return filename.split(".")


def _setup_common_data(slug, lang, extension, directory_path, schema):
    filepath = os.path.join(directory_path, f"{slug}.{lang}.{extension}")
    content = read_markdown_file(filepath)
    raw_front_matter, remaining_content = parse_front_matter(content)

    if raw_front_matter is None:
        return None, None

    front_matter = validate_front_matter(raw_front_matter, schema)
    if front_matter is None:
        return None, None

    return front_matter.dict(), remaining_content
