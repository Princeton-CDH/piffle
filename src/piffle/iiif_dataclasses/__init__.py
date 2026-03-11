from __future__ import annotations

from .presentation2 import (
    Annotation2,
    AnnotationList2,
    Canvas2,
    Collection2,
    Manifest2,
    Range2,
    Sequence2,
)
from .presentation3 import (
    AccompanyingCanvas3,
    Annotation3,
    AnnotationCollection3,
    AnnotationPage3,
    Canvas3,
    Collection3,
    GeoreferenceAnnotation3,
    Manifest3,
    PlaceholderCanvas3,
    Range3,
)

MANIFEST3_CLASSES = {
    "Collection": Collection3,
    "Manifest": Manifest3,
    "Canvas": Canvas3,
    "PlaceholderCanvas": PlaceholderCanvas3,
    "AccompanyingCanvas": AccompanyingCanvas3,
    "AnnotationCollection": AnnotationCollection3,
    "AnnotationPage": AnnotationPage3,
    "Annotation": Annotation3,
    "GeoreferenceAnnotation": GeoreferenceAnnotation3,
    "Range": Range3,
}

MANIFEST2_CLASSES = {
    "sc:Collection": Collection2,
    "sc:Manifest": Manifest2,
    "sc:Sequence": Sequence2,
    "sc:Range": Range2,
    "sc:Canvas": Canvas2,
    "sc:AnnotationList": AnnotationList2,
    "sc:Annotation": Annotation2,
}
