from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import IIIF2, OtherMetadataDict

## IIIF Image 2


@dataclass()
class IIIFImage2(IIIF2):
    pass


@dataclass()
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
            print("[WARNING] Image is missing 'context' field.")
        if id is None:
            print("[WARNING] Image is missing 'id' field.")
        if protocol is None:
            print("[WARNING] Image is missing 'protocol' field.")
        if width is None:
            print("[WARNING] Image is missing 'width' field.")
        if height is None:
            print("[WARNING] Image is missing 'height' field.")
        if profile is None:
            print("[WARNING] Image is missing 'profile' field.")

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
