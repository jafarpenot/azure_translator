import os
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

from languages import CONTENT_TYPES, GLOSSARY_CONTENT_TYPES

load_dotenv()

API_VERSION = "2024-05-01"


class TranslationError(Exception):
    pass


def _content_type_for(filename: str, mapping: dict) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in mapping:
        raise TranslationError(f"Unsupported file extension: {ext}")
    return mapping[ext]


def translate_document(
    file_bytes: bytes,
    filename: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    glossary_bytes: Optional[bytes] = None,
    glossary_filename: Optional[str] = None,
) -> bytes:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
    if not endpoint or not api_key:
        raise TranslationError(
            "Missing AZURE_TRANSLATOR_ENDPOINT or AZURE_TRANSLATOR_KEY (check your .env)"
        )

    url = f"{endpoint}/translator/document:translate"
    params = {
        "targetLanguage": target_lang,
        "api-version": API_VERSION,
    }
    if source_lang:
        params["sourceLanguage"] = source_lang

    headers = {"Ocp-Apim-Subscription-Key": api_key}

    doc_ct = _content_type_for(filename, CONTENT_TYPES)
    files = {"document": (filename, file_bytes, doc_ct)}

    if glossary_bytes and glossary_filename:
        gloss_ct = _content_type_for(glossary_filename, GLOSSARY_CONTENT_TYPES)
        files["glossary"] = (glossary_filename, glossary_bytes, gloss_ct)

    response = requests.post(
        url, params=params, headers=headers, files=files, timeout=(30, 300)
    )

    if response.status_code != 200:
        try:
            payload = response.json()
            msg = payload.get("error", {}).get("message", response.text)
        except Exception:
            msg = response.text
        raise TranslationError(f"Azure returned {response.status_code}: {msg}")

    return response.content
