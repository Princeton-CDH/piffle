from __future__ import annotations

from dataclasses import dataclass


class OtherMetadataDict(dict):
    """Base attrdict class for all other metadata dictionaries."""

    pass


@dataclass()
class IIIFBase:
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            other_metadata = super().__getattribute__("other_metadata")
            if name in other_metadata:
                return self.other_metadata[name]
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def __delattr__(self, name):
        try:
            super().__delattr__(name)
            return
        except AttributeError:
            if name in self.other_metadata:
                del self.other_metadata[name]
                return
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    @property
    def short_id(self):
        """Generate a short id from full manifest/canvas uri identifiers
        for use in local urls.  Logic is based on the recommended
        url pattern from the IIIF Presentation 2.0 specification."""

        # shortening should work reliably for uris that follow
        # recommended url patterns from the spec
        # http://iiif.io/api/presentation/2.0/#a-summary-of-recommended-uri-patterns
        #   manifest:  {scheme}://{host}/{prefix}/{identifier}/manifest
        #   canvas: {scheme}://{host}/{prefix}/{identifier}/canvas/{name}
        id = self.id
        # remove trailing /manifest or /manifest.json at the end of the url, if present
        if id.endswith("/manifest"):
            id = id[: -len("/manifest")]
        elif id.endswith("/manifest.json"):
            id = id[: -len("/manifest.json")]
        # split on slashes and return the last portion
        return id.split("/")[-1]


@dataclass()
class IIIF3(IIIFBase):
    """Base class for IIIF 3.0 objects."""

    pass


@dataclass()
class IIIF2(IIIFBase):
    """Base class for IIIF 2.0 objects."""

    pass
