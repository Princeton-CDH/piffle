import json
import os
from unittest.mock import patch

import pytest
import requests

from piffle.iiif_dataclasses.presentation2 import IIIFPresentation2, Manifest2
from piffle.utils import IIIFException, format_manifest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


class TestIIIFPresentation2:
    test_manifest = os.path.join(FIXTURE_DIR, "manifest2.json")

    def test_load(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert isinstance(pres, IIIFPresentation2)
        assert isinstance(pres, Manifest2)
        assert pres.type == "sc:Manifest"

    def test_from_file(self):
        pres = IIIFPresentation2.from_file(self.test_manifest)
        assert isinstance(pres, IIIFPresentation2)
        assert isinstance(pres, Manifest2)
        assert pres.type == "sc:Manifest"

    def test_from_url(self):
        manifest_url = "http://ma.ni/fe.st"
        with open(self.test_manifest) as manifest:
            data = json.load(manifest, object_hook=format_manifest)
        with patch("piffle.utils.requests.get") as mock_get:
            mockresponse = mock_get.return_value
            mockresponse.status_code = requests.codes.ok
            mockresponse.json.return_value = data
            pres = IIIFPresentation2.from_url(manifest_url)
            assert pres.type == "sc:Manifest"
            mock_get.assert_called_with(manifest_url)

            # error handling
            # bad status code response on the url
            with pytest.raises(IIIFException) as excinfo:
                mockresponse.status_code = requests.codes.forbidden
                mockresponse.reason = "Forbidden"
                IIIFPresentation2.from_url(manifest_url)
            assert "Error retrieving manifest" in str(excinfo.value)
            assert "403 Forbidden" in str(excinfo.value)

            # valid http response but not a json response
            with pytest.raises(IIIFException) as excinfo:
                mockresponse.status_code = requests.codes.ok
                # content type header does not indicate json
                mockresponse.headers = {"content-type": "text/html"}
                mockresponse.json.side_effect = json.decoder.JSONDecodeError(
                    "err", "doc", 1
                )
                IIIFPresentation2.from_url(manifest_url)
            assert "No JSON found" in str(excinfo.value)

            # json parsing error
            with pytest.raises(IIIFException) as excinfo:
                # content type header indicates json, but parsing failed
                mockresponse.headers = {"content-type": "application/json"}
                mockresponse.json.side_effect = json.decoder.JSONDecodeError(
                    "err", "doc", 1
                )
                IIIFPresentation2.from_url(manifest_url)
            assert "Error parsing JSON" in str(excinfo.value)

    def test_short_id(self):
        assert IIIFPresentation2.load(self.test_manifest).short_id == "sanborn00003_001"

        # TODO: replace this with a canvas json file saved to fixtures
        # canvas_uri = "https://ii.if/resources/p0c484h74c/manifest/canvas/ps7527b878"
        # assert IIIFPresentation2.load(canvas_uri).short_id == "ps7527b878"

    def test_toplevel_attrs(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert pres.context == "http://iiif.io/api/presentation/2/context.json"
        assert pres.id == "https://www.loc.gov/item/sanborn00003_001/manifest.json"
        assert pres.type == "sc:Manifest"
        assert (
            pres.label
            == "Sanborn Fire Insurance Map from Albertville, Marshall County, Alabama."
        )
        assert pres.viewingHint == "paged"
        assert pres.viewingDirection == "left-to-right"

    def test_nested_attrs(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert isinstance(pres.sequences, list)
        assert pres.sequences[0].id is None
        assert pres.sequences[0].type == "sc:Sequence"
        assert isinstance(pres.sequences[0].canvases, list)
        assert (
            pres.sequences[0].canvases[0].id
            == "https://tile.loc.gov/image-services/iiif/service:gmd:gmd397m:g3974m:g3974am:g3974am_g000031927:00003_1927-0001"
        )

    def test_set(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        pres.test_attribute = "test value"
        pres.label = "New title"
        pres.type = "sc:Collection"
        assert pres.test_attribute == "test value"
        assert pres.label == "New title"
        assert pres.type == "sc:Collection"

    def test_del(self):
        pres = IIIFPresentation2.load(self.test_manifest)

        assert hasattr(pres, "label")  # this one has a label
        del pres.label
        assert not hasattr(pres, "label")

        assert hasattr(pres, "type")
        del pres.type
        assert not hasattr(pres, "type")

        # deleted attributes shouldn't exist
        with pytest.raises(AttributeError):
            pres.label
        with pytest.raises(AttributeError):
            pres.type

    def test_first_label(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert (
            pres.first_label
            == "Sanborn Fire Insurance Map from Albertville, Marshall County, Alabama."
        )
        pres.label = "unlisted single title"
        assert pres.first_label == pres.label
