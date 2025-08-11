from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..load_iiif import load_iiif_presentation
from .base import IIIF3, OtherMetadataDict
from .dataclass_utils import GeoreferencingError, parse_item

## IIIF Presentation 3


@dataclass()
class IIIFPresentation3(IIIF3):
    @staticmethod
    def load(id: str) -> IIIFPresentation3:
        """
        Load a IIIF Presentation 3 object from a file or uri.

        Parameters
        ----------
        id : str
            The uri or filepath of the IIIF Presentation 3.

        Returns
        -------
        IIIFPresentation3
            The loaded IIIF Presentation 3 object.
        """
        return load_iiif_presentation(id, presentation_version=3)

    @staticmethod
    def from_file(path: str) -> IIIFPresentation3:
        """Load a IIIF Presentation 3 object from a file."""
        print(
            "[WARNING] `IIIFPresentation3.from_file` is deprecated. Use `IIIFPresentation3.load` instead."
        )
        return load_iiif_presentation(path, presentation_version=3)

    @staticmethod
    def from_url(uri: str) -> IIIFPresentation3:
        """Load a IIIF Presentation 3 object from a URL."""
        print(
            "[WARNING] `IIIFPresentation3.from_url` is deprecated. Use `IIIFPresentation3.load` instead."
        )
        return load_iiif_presentation(uri, presentation_version=3)

    @staticmethod
    def from_file_or_url(id: str) -> IIIFPresentation3:
        """Load a IIIF Presentation 3 object from a file or URL."""
        print(
            "[WARNING] `IIIFPresentation3.from_file_or_url` is deprecated. Use `IIIFPresentation3.load` instead."
        )
        return load_iiif_presentation(id, presentation_version=3)

    @staticmethod
    def parse_annotation(item: Any):
        try:
            return parse_item(item, GeoreferenceAnnotation3)
        except GeoreferencingError:
            return parse_item(item, Annotation3)

    @property
    def first_label(self):
        label = self.label

        if label is None:
            print("[WARNING] No label found in IIIF Presentation 3 object.")
            return None

        # label can be a string or list of strings
        if isinstance(label, str):
            return label
        elif isinstance(label, list):
            return label[0]


@dataclass()
class Annotation3(IIIFPresentation3):
    context: Any
    id: Any
    type: Any
    target: Any
    label: Any = None
    service: Any = None
    rendering: Any = None
    thumbnail: list[Any] = field(default_factory=list)
    motivation: Any = None
    body: Any = None
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        target: Any = None,
        label: Any = None,
        service: Any = None,
        rendering: Any = None,
        thumbnail: list[Any] = [],
        motivation: Any = None,
        body: Any = None,
        **kwargs,
    ):
        if context is None:
            print("[WARNING] Annotation is missing 'context' field.")
        if id is None:
            print("[WARNING] Annotation is missing 'id' field.")
        if type is None:
            print("[WARNING] Annotation is missing 'type' field.")
        if target is None:
            print("[WARNING] Annotation is missing 'target' field.")

        self.context = context
        self.id = id
        self.type = type
        self.target = target
        self.label = label
        self.service = service
        self.rendering = rendering
        self.thumbnail = thumbnail
        self.motivation = motivation
        self.body = body
        self.other_metadata = OtherMetadataDict(kwargs)

    def collect_annotations(self):
        return [self]

    def get_image_url(self):
        return self.target["source"]["id"]


@dataclass()
class GeoreferenceAnnotation3(Annotation3):
    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        target: Any = None,
        label: Any = None,
        service: Any = None,
        rendering: Any = None,
        thumbnail: list[Any] = [],
        motivation: Any = None,
        body: Any = None,
        **kwargs,
    ):
        if motivation != "georeferencing":
            raise GeoreferencingError("Motivation must be 'georeferencing'")

        super().__init__(
            context=context,
            id=id,
            type=type,
            target=target,
            label=label,
            service=service,
            rendering=rendering,
            thumbnail=thumbnail,
            motivation=motivation,
            body=body,
            **kwargs,
        )


@dataclass()
class AnnotationCollection3(IIIFPresentation3):
    context: Any
    id: Any
    type: Any
    label: Any = None
    rendering: Any = None
    partOf: Any = None
    next: Any = None
    first: Any = None
    last: Any = None
    service: Any = None
    total: Any = None
    thumbnail: list[Any] = field(default_factory=list)
    items: list[Annotation3] = field(default_factory=list)
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        label: Any = None,
        rendering: Any = None,
        partOf: Any = None,
        next: Any = None,
        first: Any = None,
        last: Any = None,
        service: Any = None,
        total: Any = None,
        thumbnail: list[Any] = [],
        items: list[Annotation3 | Any] = [],
        **kwargs,
    ):
        if context is None:
            print("[WARNING] AnnotationCollection is missing 'context' field.")
        if id is None:
            print("[WARNING] AnnotationCollection is missing 'id' field.")
        if type is None:
            print("[WARNING] AnnotationCollection is missing 'type' field.")

        self.context = context
        self.id = id
        self.type = type
        self.label = label
        self.rendering = rendering
        self.partOf = partOf
        self.next = next
        self.first = first
        self.last = last
        self.service = service
        self.total = total
        self.thumbnail = thumbnail
        self.items = [self.parse_annotation(item) for item in items]
        self.other_metadata = OtherMetadataDict(kwargs)

    def collect_annotations(self):
        return self.items


@dataclass()
class AnnotationPage3(IIIFPresentation3):
    context: Any
    id: Any
    type: Any
    items: list[Annotation3]
    label: Any = None
    rendering: Any = None
    service: Any = None
    thumbnail: list[Any] = field(default_factory=list)
    partOf: list[AnnotationCollection3] = field(default_factory=list)
    next: Any = None
    prev: Any = None
    first: Any = None
    last: Any = None
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        items: list[Annotation3 | Any] = [],
        label: Any = None,
        rendering: Any = None,
        service: Any = None,
        thumbnail: list[Any] = [],
        partOf: list[AnnotationCollection3 | Any] = [],
        next: Any = None,
        prev: Any = None,
        first: Any = None,
        last: Any = None,
        **kwargs,
    ):
        if context is None:
            print("[WARNING] AnnotationPage is missing 'context' field.")
        if id is None:
            print("[WARNING] AnnotationPage is missing 'id' field.")
        if type is None:
            print("[WARNING] AnnotationPage is missing 'type' field.")
        if items is None:
            print("[WARNING] AnnotationPage is missing 'items' field.")

        self.context = context
        self.id = id
        self.type = type
        self.items = [
            self.parse_annotation(item) for item in items
        ]  # list of annotations, see Annotation class
        self.label = label
        self.rendering = rendering
        self.service = service
        self.thumbnail = thumbnail
        self.partOf = [
            parse_item(part, AnnotationCollection3) for part in partOf
        ]  # list of annotation collections, see AnnotationCollection class
        self.next = next
        self.prev = prev
        self.first = first
        self.last = last
        self.other_metadata = OtherMetadataDict(kwargs)

    def collect_annotations(self):
        return self.items


@dataclass()
class PlaceholderCanvas3(IIIFPresentation3):
    context: Any
    id: Any
    type: Any
    items: list[
        AnnotationPage3
    ]  # this is annotations with "painting" motivation (i.e. located on the canvas)
    label: Any = None
    height: Any = None
    width: Any = None
    duration: Any = None
    metadata: Any = None
    summary: Any = None
    requiredStatement: Any = None
    rendering: Any = None
    rights: Any = None
    navDate: Any = None
    navPlace: Any = None
    provider: Any = None
    seeAlso: Any = None
    service: Any = None
    thumbnail: list[Any] = field(default_factory=list)
    homepage: Any = None
    behavior: Any = None
    partOf: Any = None
    annotations: list[AnnotationPage3 | Any] = field(
        default_factory=list
    )  # this is more like metadata or supplementary info
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        items: list[AnnotationPage3 | Any] = [],
        label: Any = None,
        height: Any = None,
        width: Any = None,
        duration: Any = None,
        metadata: Any = None,
        summary: Any = None,
        requiredStatement: Any = None,
        rendering: Any = None,
        rights: Any = None,
        navDate: Any = None,
        navPlace: Any = None,
        provider: Any = None,
        seeAlso: Any = None,
        service: Any = None,
        thumbnail: list[Any] = [],
        homepage: Any = None,
        behavior: Any = None,
        partOf: Any = None,
        annotations: list[AnnotationPage3 | Any] = [],
        **kwargs,
    ):
        if context is None:
            print("[WARNING] PlaceholderCanvas is missing 'context' field.")
        if id is None:
            print("[WARNING] PlaceholderCanvas is missing 'id' field.")
        if type is None:
            print("[WARNING] PlaceholderCanvas is missing 'type' field.")
        if items is None:
            print("[WARNING] PlaceholderCanvas is missing 'items' field.")

        self.context = context
        self.id = id
        self.type = type
        self.items = [
            parse_item(item, AnnotationPage3) for item in items
        ]  # list of annotation pages, see AnnotationPage class
        self.label = label
        self.height = height
        self.width = width
        self.duration = duration
        self.metadata = metadata
        self.summary = summary
        self.requiredStatement = requiredStatement
        self.rendering = rendering
        self.rights = rights
        self.navDate = navDate
        self.navPlace = navPlace
        self.provider = provider
        self.seeAlso = seeAlso
        self.service = service
        self.thumbnail = thumbnail
        self.homepage = homepage
        self.behavior = behavior
        self.partOf = partOf
        self.annotations = [
            parse_item(annotation, AnnotationPage3, raise_error=False)
            for annotation in annotations
        ]  # more like supplementary info, don't use this one
        self.other_metadata = OtherMetadataDict(kwargs)

    def collect_annotations(self):
        annotations = []
        for item in self.items:
            annotations += item.collect_annotations()
        return annotations


@dataclass()
class AccompanyingCanvas3(PlaceholderCanvas3):
    pass


@dataclass()
class Canvas3(PlaceholderCanvas3):
    placeholderCanvas: PlaceholderCanvas3 = None
    accompanyingCanvas: AccompanyingCanvas3 = None

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        items: list[
            AnnotationPage3 | Any
        ] = [],  # this is annotations with "painting" motivation (i.e. located on the canvas)
        label: Any = None,
        height: Any = None,
        width: Any = None,
        duration: Any = None,
        metadata: Any = None,
        summary: Any = None,
        requiredStatement: Any = None,
        rendering: Any = None,
        rights: Any = None,
        navDate: Any = None,
        navPlace: Any = None,
        provider: Any = None,
        seeAlso: Any = None,
        service: Any = None,
        thumbnail: list[Any] = [],
        homepage: Any = None,
        behavior: Any = None,
        partOf: Any = None,
        annotations: list[
            AnnotationPage3 | Any
        ] = [],  # this is more like metadata or supplementary info
        placeholderCanvas: PlaceholderCanvas3 | Any = None,
        accompanyingCanvas: AccompanyingCanvas3 | Any = None,
        **kwargs,
    ):
        super().__init__(
            context=context,
            id=id,
            type=type,
            items=items,
            label=label,
            height=height,
            width=width,
            duration=duration,
            metadata=metadata,
            summary=summary,
            requiredStatement=requiredStatement,
            rendering=rendering,
            rights=rights,
            navDate=navDate,
            navPlace=navPlace,
            provider=provider,
            seeAlso=seeAlso,
            service=service,
            thumbnail=thumbnail,
            homepage=homepage,
            behavior=behavior,
            partOf=partOf,
            annotations=annotations,
            **kwargs,
        )
        self.placeholderCanvas = parse_item(placeholderCanvas, PlaceholderCanvas3)
        self.accompanyingCanvas = parse_item(accompanyingCanvas, AccompanyingCanvas3)


@dataclass()
class Collection3(IIIFPresentation3):
    context: Any
    id: Any
    type: Any
    label: Any
    metadata: Any = None
    summary: Any = None
    requiredStatement: Any = None
    rendering: Any = None
    rights: Any = None
    navDate: Any = None
    navPlace: Any = None
    provider: Any = None
    seeAlso: Any = None
    services: Any = None
    service: Any = None
    placeholderCanvas: PlaceholderCanvas3 = None
    accompanyingCanvas: AccompanyingCanvas3 = None
    thumbnail: list[Any] = field(default_factory=list)
    homepage: Any = None
    behavior: Any = None
    partOf: Any = None
    items: list[Any] = field(default_factory=list)
    annotations: list[AnnotationPage3 | Any] = field(default_factory=list)
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        label: Any = None,
        metadata: Any = None,
        summary: Any = None,
        requiredStatement: Any = None,
        rendering: Any = None,
        rights: Any = None,
        navDate: Any = None,
        navPlace: Any = None,
        provider: Any = None,
        seeAlso: Any = None,
        services: Any = None,
        service: Any = None,
        placeholderCanvas: PlaceholderCanvas3 | Any = None,
        accompanyingCanvas: AccompanyingCanvas3 | Any = None,
        thumbnail: list[Any] = [],
        homepage: Any = None,
        behavior: Any = None,
        partOf: Any = None,
        items: list[Any] = [],
        annotations: list[AnnotationPage3 | Any] = [],
        **kwargs,
    ):
        if context is None:
            print("[WARNING] Collection is missing 'context' field.")
        if id is None:
            print("[WARNING] Collection is missing 'id' field.")
        if type is None:
            print("[WARNING] Collection is missing 'type' field.")
        if label is None:
            print("[WARNING] Collection is missing 'label' field.")

        self.context = context
        self.id = id
        self.type = type
        self.label = label
        self.metadata = metadata
        self.summary = summary
        self.requiredStatement = requiredStatement
        self.rendering = rendering
        self.rights = rights
        self.navDate = navDate
        self.navPlace = navPlace
        self.provider = provider
        self.seeAlso = seeAlso
        self.services = services
        self.service = service
        self.placeholderCanvas = parse_item(placeholderCanvas, PlaceholderCanvas3)
        self.accompanyingCanvas = parse_item(accompanyingCanvas, AccompanyingCanvas3)
        self.thumbnail = thumbnail
        self.homepage = homepage
        self.behavior = behavior
        self.partOf = partOf
        self.items = items
        self.annotations = [
            parse_item(annotation, AnnotationPage3, raise_error=False)
            for annotation in annotations
        ]
        self.other_metadata = OtherMetadataDict(kwargs)

    def collect_annotations(self):
        annotations = []
        for item in self.items:
            annotations += item.collect_annotations()
        return annotations


@dataclass()
class Range3(IIIFPresentation3):
    context: Any
    id: Any
    type: Any
    items: list[Any]
    label: Any = None
    rendering: Any = None
    supplementary: AnnotationCollection3 = None
    service: Any = None
    placeholderCanvas: PlaceholderCanvas3 = None
    accompanyingCanvas: AccompanyingCanvas3 = None
    annotations: list[AnnotationPage3 | Any] = field(default_factory=list)
    thumbnail: list[Any] = field(default_factory=list)
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        items: list[Any] = [],
        label: Any = None,
        rendering: Any = None,
        supplementary: AnnotationCollection3 | Any = None,
        service: Any = None,
        placeholderCanvas: PlaceholderCanvas3 | Any = None,
        accompanyingCanvas: AccompanyingCanvas3 | Any = None,
        annotations: list[AnnotationPage3 | Any] = [],
        thumbnail: list[Any] = [],
        **kwargs,
    ):
        if context is None:
            print("[WARNING] Range is missing 'context' field.")
        if id is None:
            print("[WARNING] Range is missing 'id' field.")
        if type is None:
            print("[WARNING] Range is missing 'type' field.")
        if items is None:
            print("[WARNING] Range is missing 'items' field.")

        self.context = context
        self.id = id
        self.type = type
        self.items = items
        self.label = label
        self.rendering = rendering
        self.supplementary = parse_item(supplementary, AnnotationCollection3)
        self.service = service
        self.placeholderCanvas = parse_item(placeholderCanvas, PlaceholderCanvas3)
        self.accompanyingCanvas = parse_item(accompanyingCanvas, AccompanyingCanvas3)
        self.annotations = [
            parse_item(annotation, AnnotationPage3, raise_error=False)
            for annotation in annotations
        ]
        self.thumbnail = thumbnail
        self.other_metadata = OtherMetadataDict(kwargs)


@dataclass()
class Manifest3(IIIFPresentation3):
    context: Any
    id: Any
    type: Any
    label: Any
    metadata: Any = None
    summary: Any = None
    requiredStatement: Any = None
    rendering: Any = None
    service: Any = None
    services: Any = None
    viewingDirection: Any = None
    placeholderCanvas: PlaceholderCanvas3 = None
    accompanyingCanvas: AccompanyingCanvas3 = None
    rights: Any = None
    start: Any = None
    navDate: Any = None
    navPlace: Any = None
    provider: Any = None
    seeAlso: Any = None
    thumbnail: list[Any] = field(default_factory=list)
    homepage: Any = None
    behavior: Any = None
    partOf: Any = None
    items: list[Canvas3] = field(default_factory=list)
    structures: list[Range3] = field(default_factory=list)
    annotations: list[AnnotationPage3 | Any] = field(default_factory=list)
    other_metadata: OtherMetadataDict = field(default_factory=OtherMetadataDict)

    def __init__(
        self,
        context: Any = None,
        id: Any = None,
        type: Any = None,
        label: Any = None,
        metadata: Any = None,
        summary: Any = None,
        requiredStatement: Any = None,
        rendering: Any = None,
        service: Any = None,
        services: Any = None,
        viewingDirection: Any = None,
        placeholderCanvas: PlaceholderCanvas3 | Any = None,
        accompanyingCanvas: AccompanyingCanvas3 | Any = None,
        rights: Any = None,
        start: Any = None,
        navDate: Any = None,
        navPlace: Any = None,
        provider: Any = None,
        seeAlso: Any = None,
        thumbnail: list[Any] = [],
        homepage: Any = None,
        behavior: Any = None,
        partOf: Any = None,
        items: list[Canvas3 | Any] = [],
        structures: list[Range3 | Any] = [],
        annotations: list[AnnotationPage3 | Any] = [],
        **kwargs,
    ):
        if context is None:
            print("[WARNING] Manifest is missing 'context' field.")
        if id is None:
            print("[WARNING] Manifest is missing 'id' field.")
        if type is None:
            print("[WARNING] Manifest is missing 'type' field.")
        if label is None:
            print("[WARNING] Manifest is missing 'label' field.")

        self.context = context
        self.id = id
        self.type = type
        self.label = label
        self.metadata = metadata
        self.summary = summary
        self.requiredStatement = requiredStatement
        self.rendering = rendering
        self.service = service
        self.services = services
        self.viewingDirection = viewingDirection
        self.placeholderCanvas = parse_item(placeholderCanvas, PlaceholderCanvas3)
        self.accompanyingCanvas = parse_item(accompanyingCanvas, AccompanyingCanvas3)
        self.rights = rights
        self.start = start
        self.navDate = navDate
        self.navPlace = navPlace
        self.provider = provider
        self.seeAlso = seeAlso
        self.thumbnail = thumbnail
        self.homepage = homepage
        self.behavior = behavior
        self.partOf = partOf
        self.items = [
            parse_item(item, Canvas3) for item in items
        ]  # list of canvases, see Canvas class
        self.structures = [parse_item(structure, Range3) for structure in structures]
        self.annotations = [
            parse_item(annotation, AnnotationPage3, raise_error=False)
            for annotation in annotations
        ]
        self.other_metadata = OtherMetadataDict(kwargs)

    def collect_annotations(self):
        annotations = []
        for item in self.items:
            annotations += item.collect_annotations()
        return annotations
