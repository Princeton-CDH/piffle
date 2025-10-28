from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from piffle.iiif_dataclasses.base import IIIF2, OtherMetadataDict
from piffle.load_iiif import load_iiif_image

log = logging.getLogger(__name__)

## IIIF Image 2


@dataclass
class IIIFImage2(IIIF2):
    @staticmethod
    def load(id: str) -> Image2:
        """
        Load an IIIF Image 2 object from a file or uri.

        Parameters
        ----------
        id : str
            The uri or filepath of the IIIF Image 2.

        Returns
        -------
        Image2
            The loaded IIIF Image 2 object.
        """
        return load_iiif_image(id, image_version=2)

    @staticmethod
    def from_file(path: str) -> Image2:
        """Load an IIIF Image 2 object from a file."""
        log.warning(
            "`IIIFImage2.from_file` is deprecated. Use `IIIFImage2.load` instead."
        )
        return load_iiif_image(path, image_version=2)

    @staticmethod
    def from_url(uri: str) -> Image2:
        """Load an IIIF Image 2 object from a URL."""
        log.warning(
            "`IIIFImage2.from_url` is deprecated. Use `IIIFImage2.load` instead."
        )
        return load_iiif_image(uri, image_version=2)

    @staticmethod
    def from_file_or_url(id: str) -> Image2:
        """Load an IIIF Image 2 object from a file or URL."""
        log.warning(
            "`IIIFImage2.from_file_or_url` is deprecated. Use `IIIFImage2.load` instead."
        )
        return load_iiif_image(id, image_version=2)


@dataclass
class Image2(IIIFImage2):
    context: Any
    id: Any
    protocol: Any
    width: Any
    height: Any
    profile: Any
    type: Any = None
    sizes: Any = None
    tiles: Any = None
    attribution: Any = None
    license: Any = None
    logo: Any = None
    service: Any = None
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        protocol: Any = None,
        width: Any = None,
        height: Any = None,
        profile: Any = None,
        type: Any = None,
        sizes: Any = None,
        tiles: Any = None,
        attribution: Any = None,
        license: Any = None,
        logo: Any = None,
        service: Any = None,
        **kwargs,
    ):
        if context is None:
            log.warning("Image is missing 'context' field.")
        if id is None:
            log.warning("Image is missing 'id' field.")
        if protocol is None:
            log.warning("Image is missing 'protocol' field.")
        if width is None:
            log.warning("Image is missing 'width' field.")
        if height is None:
            log.warning("Image is missing 'height' field.")
        if profile is None:
            log.warning("Image is missing 'profile' field.")

        self.context = context
        self.id = id
        self.protocol = protocol
        self.width = width
        self.height = height
        self.profile = profile
        self.type = type
        self.sizes = sizes
        self.tiles = tiles
        self.attribution = attribution
        self.license = license
        self.logo = logo
        self.service = service
        self.other_metadata = OtherMetadataDict(kwargs)
