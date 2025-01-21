from __future__ import annotations

from .iiif_dataclasses import MANIFEST2_CLASSES, MANIFEST3_CLASSES
from .iiif_dataclasses.image2 import Image2
from .iiif_dataclasses.image3 import Image3
from .utils import get_manifest, load_manifest


class UnknownClassError(ValueError):
    pass


def load_iiif_presentation(id: str, presentation_version: int | float | str):
    try:
        manifest = load_manifest(id)
    except FileNotFoundError:
        manifest = get_manifest(id)

    if presentation_version in [3, 3.0, "3", "3.0"]:
        manifest_class = MANIFEST3_CLASSES.get(manifest["type"], None)
    elif presentation_version in [2, 2.0, 2.1, "2", "2.0", "2.1"]:
        manifest_class = MANIFEST2_CLASSES.get(manifest["type"], None)
    else:
        raise ValueError(f"Presentation version {presentation_version} not supported.")

    if manifest_class is None:
        raise UnknownClassError(
            f"Class {manifest['type']} not found in IIIF Presentation {presentation_version}"
        )

    return manifest_class(**manifest)


def load_iiif_image(id: str, image_version: int | float | str):
    try:
        manifest = load_manifest(id)
    except FileNotFoundError:
        manifest = get_manifest(id)

    if image_version in [3, 3.0, "3", "3.0"]:
        return Image3(**manifest)
    elif image_version in [2, 2.0, 2.1, "2", "2.0", "2.1"]:
        return Image2(**manifest)
    else:
        raise ValueError(f"Presentation version {image_version} not supported.")
