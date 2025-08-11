from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..load_iiif import load_iiif_image
from .base import IIIF3, OtherMetadataDict

## IIIF Image 3


@dataclass()
class IIIFImage3(IIIF3):
    @staticmethod
    def load(id: str) -> Image3:
        """
        Load a IIIF Image 3 object from a file or uri.

        Parameters
        ----------
        id : str
            The uri or filepath of the IIIF Image 3.

        Returns
        -------
        Image3
            The loaded IIIF Image 3 object.
        """
        return load_iiif_image(id, image_version=3)

    @staticmethod
    def from_file(path: str) -> Image3:
        """Load an IIIF Image 3 object from a file."""
        print(
            "[WARNING] `IIIFImage3.from_file` is deprecated. Use `IIIFImage3.load` instead."
        )
        return load_iiif_image(path, image_version=3)

    @staticmethod
    def from_url(uri: str) -> Image3:
        """Load an IIIF Image 3 object from a URL."""
        print(
            "[WARNING] `IIIFImage3.from_url` is deprecated. Use `IIIFImage3.load` instead."
        )
        return load_iiif_image(uri, image_version=3)

    @staticmethod
    def from_file_or_url(id: str) -> Image3:
        """Load an IIIF Image 3 object from a file or URL."""
        print(
            "[WARNING] `IIIFImage3.from_file_or_url` is deprecated. Use `IIIFImage3.load` instead."
        )
        return load_iiif_image(id, image_version=3)


@dataclass()
class Image3(IIIFImage3):
    context: Any
    id: Any
    type: Any
    protocol: Any
    profile: Any
    width: Any
    height: Any
    maxWidth: Any = None
    maxHeight: Any = None
    maxArea: Any = None
    sizes: Any = None
    tiles: Any = None
    preferredFormats: Any = None
    extraQualities: Any = None
    extraFormats: Any = None
    extraFeatures: Any = None
    rights: Any = None
    label: Any = None
    format: Any = None
    seeAlso: Any = None
    partOf: Any = None
    service: Any = None
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        protocol: Any = None,
        profile: Any = None,
        width: Any = None,
        height: Any = None,
        maxWidth: Any = None,
        maxHeight: Any = None,
        maxArea: Any = None,
        sizes: Any = None,
        tiles: Any = None,
        preferredFormats: Any = None,
        extraQualities: Any = None,
        extraFormats: Any = None,
        extraFeatures: Any = None,
        rights: Any = None,
        label: Any = None,
        format: Any = None,
        seeAlso: Any = None,
        partOf: Any = None,
        service: Any = None,
        **kwargs,
    ):
        if context is None:
            print("[WARNING] Image is missing 'context' field.")
        if id is None:
            print("[WARNING] Image is missing 'id' field.")
        if type is None:
            print("[WARNING] Image is missing 'type' field.")
        if protocol is None:
            print("[WARNING] Image is missing 'protocol' field.")
        if profile is None:
            print("[WARNING] Image is missing 'profile' field.")
        if width is None:
            print("[WARNING] Image is missing 'width' field.")
        if height is None:
            print("[WARNING] Image is missing 'height' field.")

        self.context = context
        self.id = id
        self.type = type
        self.protocol = protocol
        self.profile = profile
        self.width = width
        self.height = height
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.maxArea = maxArea
        self.sizes = sizes
        self.tiles = tiles
        self.preferredFormats = preferredFormats
        self.extraQualities = extraQualities
        self.extraFormats = extraFormats
        self.extraFeatures = extraFeatures
        self.rights = rights
        self.label = label
        self.format = format
        self.seeAlso = seeAlso
        self.partOf = partOf
        self.service = service
        self.other_metadata = OtherMetadataDict(kwargs)
