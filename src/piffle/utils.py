from __future__ import annotations

import json

import requests


class IIIFException(Exception):
    """Custom exception for IIIF errors"""


def format_manifest(d: dict):
    formatted = {}
    for k, v in d.items():
        if k.startswith("@"):
            k = k.replace("@", "")  # for now, just remove the @
            formatted.setdefault("_at_fields", []).append(k)
        if k.startswith("_"):
            k = k.replace("_", "")  # for now, just remove the _
            formatted.setdefault("_underscore_fields", []).append(k)
        formatted[k] = v
    return formatted


def get_manifest(url: str):
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        try:
            return response.json(object_hook=format_manifest)
        except json.decoder.JSONDecodeError as err:
            # if json fails, two possibilities:
            # - we didn't actually get json (e.g. redirect for auth)
            if "application/json" not in response.headers["content-type"]:
                raise IIIFException(f"No JSON found at {url}")
            # - there is something wrong with the json
            raise IIIFException(f"Error parsing JSON for {url}: {err}")

    raise IIIFException(
        f"Error retrieving manifest at {url}: {response.status_code} {response.reason}"
    )


def load_manifest(path: str):
    with open(path) as manifest:
        return json.load(manifest, object_hook=format_manifest)
