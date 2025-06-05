import os
from collections import defaultdict
from pathlib import Path

from sqlalchemy import select

from sni.utils.files import split_filename


def load_basic_fs_state(directory):
    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                files[filepath] = {"filepath": filepath}
    return files


def load_translated_fs_state(directory):
    slug_map = defaultdict(dict)
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".md"):
                slug, locale, *_ = split_filename(filename)
                filepath = os.path.join(root, filename)
                slug_map[slug][locale] = filepath
    return slug_map


def load_manifest_based_fs_state(directory):
    slug_map = {}
    for entry in os.scandir(directory):
        if entry.is_dir():
            slug = entry.name
            manifest_file = os.path.join(entry.path, "manifest.md")
            content_dir = os.path.join(entry.path, "content")
            if os.path.isfile(manifest_file) and os.path.isdir(content_dir):
                slug_map[slug] = {
                    "manifest": manifest_file,
                    "content_dir": content_dir,
                    "directory": entry.path,
                }
    return slug_map


def load_basic_db_state(session, model):
    items = session.scalars(select(model)).all()
    return {item.content.file_metadata.filename: item for item in items}


def load_translated_db_state(session, translation_model, content_key):
    slug_map = {}
    translations = session.scalars(select(translation_model)).all()
    for t in translations:
        filename = t.content.file_metadata.filename
        if Path(filename).suffix:  # has extension → file
            canonical = getattr(t, content_key, None)
            slug = canonical.slug
            slug_map.setdefault(slug, {"canonical": canonical, "translations": {}})
            slug_map[slug]["translations"][t.locale] = t
    return slug_map


def load_manifest_based_db_state(session, translation_model, content_key):
    slug_map = {}
    translations = session.scalars(select(translation_model)).all()
    for t in translations:
        filename = t.content.file_metadata.filename
        if not Path(filename).suffix:  # no extension → directory
            canonical = getattr(t, content_key, None)
            if canonical:
                slug_map.setdefault(
                    t.slug, {"canonical": canonical, "translations": {}}
                )
                slug_map[t.slug]["translations"][t.locale] = t
    return slug_map
