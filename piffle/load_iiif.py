from __future__ import annotations

from .utils import get_manifest, load_manifest


class UnknownClassError(ValueError):
    pass


def load_iiif_presentation(id: str, presentation_version: int | float | str = "infer"):
    """Load a IIIF presentation manifest.

    Parameters
    ----------
    id : str
        The uri or filepath of the IIIF presentation.
    presentation_version : int | float | str
        The version of the IIIF presentation (2 or 3). Default is "infer" so will automatically try to detect the version.

    Returns
    -------
    IIIFBase
        The loaded IIIF presentation object.

    Raises
    ------
    ValueError
        If the presentation version is not supported.
    UnknownClassError
        If the manifest type is not found in the IIIF presentation classes.
    """
    try:
        manifest = load_manifest(id)
    except FileNotFoundError:
        manifest = get_manifest(id)

    if presentation_version in [3, 3.0, "3", "3.0"]:
        from .iiif_dataclasses import MANIFEST3_CLASSES

        manifest_class = MANIFEST3_CLASSES.get(manifest["type"], None)
    elif presentation_version in [2, 2.0, 2.1, "2", "2.0", "2.1"]:
        from .iiif_dataclasses import MANIFEST2_CLASSES

        manifest_class = MANIFEST2_CLASSES.get(manifest["type"], None)
    elif presentation_version == "infer":
        from .iiif_dataclasses import MANIFEST2_CLASSES, MANIFEST3_CLASSES

        all_classes = MANIFEST2_CLASSES | MANIFEST3_CLASSES
        manifest_class = all_classes.get(manifest["type"], None)
    else:
        raise ValueError(f"Presentation version {presentation_version} not supported.")

    if manifest_class is None:
        raise UnknownClassError(
            f"Class {manifest['type']} not found in IIIF Presentation {presentation_version}"
        )

    return manifest_class(**manifest)


def load_iiif_image(id: str, image_version: int | float | str):
    """Load a IIIF image.

    Parameters
    ----------
    id : str
        The uri or filepath of the IIIF image.
    image_version : int | float | str
        The version of the IIIF image (2 or 3).

    Returns
    -------
    IIIFBase
        The loaded IIIF image object.

    Raises
    ------
    ValueError
        If the image version is not supported.
    """
    try:
        manifest = load_manifest(id)
    except FileNotFoundError:
        manifest = get_manifest(id)

    if image_version in [3, 3.0, "3", "3.0"]:
        from .iiif_dataclasses.image3 import Image3

        return Image3(**manifest)
    elif image_version in [2, 2.0, 2.1, "2", "2.0", "2.1"]:
        from .iiif_dataclasses.image2 import Image2

        return Image2(**manifest)
    else:
        raise ValueError(f"Image version {image_version} not supported.")
