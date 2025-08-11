import json
import os
from unittest.mock import patch

import pytest
import requests

from piffle.iiif_dataclasses.presentation2 import IIIFPresentation2, Manifest2
from piffle.iiif_dataclasses.presentation3 import (
    Annotation3,
    AnnotationPage3,
    GeoreferenceAnnotation3,
    IIIFPresentation3,
)
from piffle.utils import IIIFException, format_manifest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


class TestIIIFPresentation:
    test_manifest = os.path.join(FIXTURE_DIR, "chto-manifest.json")

    def test_from_file(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert isinstance(pres, IIIFPresentation2)
        assert pres.type == "sc:Manifest"

    def test_from_url(self):
        manifest_url = "http://ma.ni/fe.st"
        with open(self.test_manifest) as manifest:
            data = json.load(manifest, object_hook=format_manifest)
        with patch("piffle.utils.requests.get") as mock_get:
            mockresponse = mock_get.return_value
            mockresponse.status_code = requests.codes.ok
            mockresponse.json.return_value = data
            pres = IIIFPresentation2.load(manifest_url)
            assert pres.type == "sc:Manifest"
            mock_get.assert_called_with(manifest_url)

            # error handling
            # bad status code response on the url
            with pytest.raises(IIIFException) as excinfo:
                mockresponse.status_code = requests.codes.forbidden
                mockresponse.reason = "Forbidden"
                IIIFPresentation2.load(manifest_url)
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
                IIIFPresentation2.load(manifest_url)
            assert "No JSON found" in str(excinfo.value)

            # json parsing error
            with pytest.raises(IIIFException) as excinfo:
                # content type header indicates json, but parsing failed
                mockresponse.headers = {"content-type": "application/json"}
                mockresponse.json.side_effect = json.decoder.JSONDecodeError(
                    "err", "doc", 1
                )
                IIIFPresentation2.load(manifest_url)
            assert "Error parsing JSON" in str(excinfo.value)

    def test_short_id(self):
        manifest_uri = self.test_manifest
        assert IIIFPresentation2.load(manifest_uri).short_id == "ph415q7581"

        # TODO: replace this with a canvas json file saved to fixtures
        # canvas_uri = "https://ii.if/resources/p0c484h74c/manifest/canvas/ps7527b878"
        # assert IIIFPresentation2.load(canvas_uri).short_id == "ps7527b878"

    def test_toplevel_attrs(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert pres.context == "http://iiif.io/api/presentation/2/context.json"
        assert (
            pres.id
            == "https://plum.princeton.edu/concern/scanned_resources/ph415q7581/manifest"
        )
        assert pres.type == "sc:Manifest"
        assert pres.label[0] == "Chto my stroim : Tetrad\u02b9 s kartinkami"
        assert pres.viewingHint == "paged"
        assert pres.viewingDirection == "left-to-right"

    def test_nested_attrs(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert isinstance(pres.sequences, list)
        assert (
            pres.sequences[0].id
            == "https://plum.princeton.edu/concern/scanned_resources/ph415q7581/manifest/sequence/normal"
        )
        assert pres.sequences[0].type == "sc:Sequence"
        assert isinstance(pres.sequences[0].canvases, list)
        assert (
            pres.sequences[0].canvases[0].id
            == "https://plum.princeton.edu/concern/scanned_resources/ph415q7581/manifest/canvas/p02871v98d"
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

        # accessing missing keys as item vs accessing as attribute
        # currently results in different errors
        # (accurate, but potentially confusing?)

        # -- Can no longer access using item syntax
        # with pytest.raises(KeyError):
        #     assert not pres["label"]
        # with pytest.raises(KeyError):
        #     assert not pres["type"]

        with pytest.raises(AttributeError):
            pres.label
        with pytest.raises(AttributeError):
            pres.type

    def test_first_label(self):
        pres = IIIFPresentation2.load(self.test_manifest)
        assert pres.first_label == pres.label[0]
        pres.label = "unlisted single title"
        assert pres.first_label == pres.label


class TestIIIFPresentation2:
    test_manifest = os.path.join(FIXTURE_DIR, "manifest2.json")

    def test_from_file(self):
        pres = IIIFPresentation2.load(self.test_manifest)
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
            pres = IIIFPresentation2.load(manifest_url)
            assert pres.type == "sc:Manifest"
            mock_get.assert_called_with(manifest_url)

            # error handling
            # bad status code response on the url
            with pytest.raises(IIIFException) as excinfo:
                mockresponse.status_code = requests.codes.forbidden
                mockresponse.reason = "Forbidden"
                IIIFPresentation2.load(manifest_url)
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
                IIIFPresentation2.load(manifest_url)
            assert "No JSON found" in str(excinfo.value)

            # json parsing error
            with pytest.raises(IIIFException) as excinfo:
                # content type header indicates json, but parsing failed
                mockresponse.headers = {"content-type": "application/json"}
                mockresponse.json.side_effect = json.decoder.JSONDecodeError(
                    "err", "doc", 1
                )
                IIIFPresentation2.load(manifest_url)
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


class TestIIIFPresentation3:
    test_annotation = os.path.join(FIXTURE_DIR, "annotation3.json")
    test_georeference_annotation = os.path.join(
        FIXTURE_DIR, "georeference_annotation3.json"
    )
    test_annotation_page = os.path.join(FIXTURE_DIR, "annotationpage3.json")

    def test_annotation_from_file(self):
        pres = IIIFPresentation3.load(self.test_annotation)
        assert isinstance(pres, IIIFPresentation3)
        assert isinstance(pres, Annotation3)
        assert pres.type == "Annotation"

    def test_georeference_annotation_from_file(self):
        pres = IIIFPresentation3.load(self.test_georeference_annotation)
        assert isinstance(pres, IIIFPresentation3)
        assert isinstance(pres, Annotation3)
        assert isinstance(pres, GeoreferenceAnnotation3)
        assert pres.type == "GeoreferenceAnnotation"

    def test_annotation_page_from_file(self):
        pres = IIIFPresentation3.load(self.test_annotation_page)
        assert isinstance(pres, IIIFPresentation3)
        assert isinstance(pres, AnnotationPage3)
        assert pres.type == "AnnotationPage"

    def test_from_url(self):
        manifest_url = "http://ma.ni/fe.st"
        with open(self.test_annotation) as manifest:
            data = json.load(manifest, object_hook=format_manifest)
        with patch("piffle.utils.requests.get") as mock_get:
            mockresponse = mock_get.return_value
            mockresponse.status_code = requests.codes.ok
            mockresponse.json.return_value = data
            pres = IIIFPresentation3.load(manifest_url)
            assert pres.type == "Annotation"
            mock_get.assert_called_with(manifest_url)

            # error handling
            # bad status code response on the url
            with pytest.raises(IIIFException) as excinfo:
                mockresponse.status_code = requests.codes.forbidden
                mockresponse.reason = "Forbidden"
                IIIFPresentation3.load(manifest_url)
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
                IIIFPresentation3.load(manifest_url)
            assert "No JSON found" in str(excinfo.value)

            # json parsing error
            with pytest.raises(IIIFException) as excinfo:
                # content type header indicates json, but parsing failed
                mockresponse.headers = {"content-type": "application/json"}
                mockresponse.json.side_effect = json.decoder.JSONDecodeError(
                    "err", "doc", 1
                )
                IIIFPresentation3.load(manifest_url)
            assert "Error parsing JSON" in str(excinfo.value)

    def test_annotation_short_id(self):
        assert (
            IIIFPresentation3.load(self.test_annotation).short_id == "5cf13f6681d355e3"
        )

    def test_annotation_page_short_id(self):
        with pytest.raises(AttributeError):
            IIIFPresentation3.load(self.test_annotation_page).short_id

    def test_annotation_toplevel_attrs(self):
        pres = IIIFPresentation3.load(self.test_annotation)
        assert pres.context == [
            "http://iiif.io/api/extension/georef/1/context.json",
            "http://iiif.io/api/presentation/3/context.json",
        ]
        assert pres.id == "https://annotations.allmaps.org/maps/5cf13f6681d355e3"
        assert pres.type == "Annotation"
        assert pres.motivation == "georeferencing"

        assert pres.label is None

    def test_annotation_page_toplevel_attrs(self):
        pres = IIIFPresentation3.load(self.test_annotation_page)
        assert pres.context == "http://www.w3.org/ns/anno.jsonld"
        assert pres.type == "AnnotationPage"
        assert pres.id is None
        assert pres.label is None

    def test_annotation_nested_attrs(self):
        pres = IIIFPresentation3.load(self.test_annotation)
        assert isinstance(pres.body, dict)
        assert pres.body["type"] == "FeatureCollection"
        assert pres.body["transformation"] == {
            "type": "polynomial",
            "options": {"order": 1},
        }
        assert isinstance(pres.body["features"], list)
        assert pres.body["features"][0]["type"] == "Feature"
        assert pres.body["features"][0] == {
            "type": "Feature",
            "properties": {"resourceCoords": [1801, 2421]},
            "geometry": {"type": "Point", "coordinates": [4.9282778, 52.3552603]},
        }

    def test_annotation_page_nested_attrs(self):
        pres = IIIFPresentation3.load(self.test_annotation_page)
        assert isinstance(pres.items, list)
        assert isinstance(pres.items[0], GeoreferenceAnnotation3)
        assert (
            pres.items[0].id == "https://annotations.allmaps.org/maps/5cf13f6681d355e3"
        )
        assert pres.items[0].context == [
            "http://iiif.io/api/extension/georef/1/context.json",
            "http://iiif.io/api/presentation/3/context.json",
        ]
        assert pres.items[0].motivation == "georeferencing"
        assert pres.items[0].body["type"] == "FeatureCollection"
        assert pres.items[0].body["transformation"] == {
            "type": "polynomial",
            "options": {"order": 1},
        }
        assert isinstance(pres.items[0].body["features"], list)
        assert pres.items[0].body["features"][0]["type"] == "Feature"
        assert pres.items[0].body["features"][0] == {
            "type": "Feature",
            "properties": {"resourceCoords": [1801, 2421]},
            "geometry": {"type": "Point", "coordinates": [4.9282778, 52.3552603]},
        }

    def test_set(self):
        pres = IIIFPresentation3.load(self.test_annotation)
        pres.label = "New title"
        pres.type = "sc:Collection"
        assert pres.label == "New title"
        assert pres.type == "sc:Collection"

    def test_del(self):
        pres = IIIFPresentation3.load(self.test_annotation)

        # label value is None but is still in the dict
        assert hasattr(pres, "label")
        assert "label" in pres.__dict__.keys()

        del pres.label
        assert "label" not in pres.__dict__.keys()
        # TODO: The below still returns true - I think since base class as the label field always
        # assert not hasattr(pres, "label")

        assert hasattr(pres, "type")
        del pres.type
        assert not hasattr(pres, "type")

        with pytest.raises(AttributeError):
            pres.type

    def test_first_label(self):
        pres = IIIFPresentation3.load(self.test_annotation)
        pres.first_label is None
        pres.label = ["first title", "second title"]
        assert pres.first_label == pres.label[0]
        pres.label = "unlisted single title"
        assert pres.first_label == pres.label
