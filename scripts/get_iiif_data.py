#!/usr/bin/env python

import argparse
import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from piffle.presentation import IIIFException, IIIFPresentation

csv_fields = [
    "manifest_url",
    "manifest_order",
    "id",
    "label",
    "image_iiif_id",
    "width",
    "height",
    "download_path",
]


def download_iiif_content(iiif_url: str, output_dir: Path):
    try:
        iiif_pres = IIIFPresentation.from_file_or_url(iiif_url)
    except IIIFException as err:
        print(err)
        return

    # assumed by default to be collection or multi-volume work
    info = ""
    num_manifests = 0
    num_canvases = 0
    if hasattr(iiif_pres, "manifests"):
        num_manifests = len(iiif_pres.manifests)
        info = f"({num_manifests:,} manifests)"
        print(f"{iiif_pres.label} {info}")
    elif hasattr(iiif_pres, "sequences"):
        num_canvases = len(iiif_pres.sequences[0].canvases)
        info = f"({num_canvases:,} canvases)"
    # tqdm.write(f"{iiif_pres.label} {info}")

    if num_manifests:
        for manifest in tqdm(iiif_pres.manifests[:35], desc="Manifests", position=1):
            download_iiif_content(manifest.id, output_dir)

    elif num_canvases:
        identifier = None
        for mdata in iiif_pres.metadata:
            if mdata["label"].lower() == "identifier":
                identifier = mdata["value"][0]
                break
        if identifier and identifier.startswith("<a href"):
            id_tag = BeautifulSoup(identifier, "html.parser")
            identifier = next(iter(id_tag.strings))  # full ark url
            identifier = identifier[
                identifier.find("ark:/") :
            ]  # get substring starting with ark:/
        if identifier is None:
            print(f"Could not find identifier for {iiif_url}")
            return

        # convert ark identifier to make a filename-safe id
        file_id = identifier.replace("/", "-").replace(":", "-")
        image_dir = output_dir / file_id
        image_dir.mkdir(exist_ok=True, parents=True)

        csv_file = output_dir / "image_metadata.csv"
        init_csv = not csv_file.exists()
        # open the csv file for appending; write the header on first creation
        with csv_file.open("a") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=csv_fields)
            if init_csv:
                csvwriter.writeheader()
            # use truncated work label for canvas progress bar
            work_label = iiif_pres.label
            if len(work_label) > 20:
                work_label = f"{work_label[:20]}..."
            for i, canvas in tqdm(
                enumerate(iiif_pres.sequences[0].canvases),
                desc=f"Images|{work_label}",
                total=num_canvases,
                position=0,  # display above manifest progress bar (?)
            ):
                canvas_id = canvas.short_id(canvas.id)
                image_filename = image_dir / f"{canvas_id}.jpg"
                # only download and record in metadata if we don't already have this file
                if not image_filename.is_file():
                    image_url = canvas["images"][0]["resource"]["@id"]
                    image = requests.get(image_url)
                    with image_filename.open("wb") as imgoutput:
                        imgoutput.write(image.content)

                    # figgy manifests include width & height on the canvas
                    # object and also in the image resource; use if easily accessible
                    width = canvas.width
                    height = canvas.height

                    csvwriter.writerow(
                        {
                            "manifest_url": iiif_pres.id,
                            "manifest_order": i,
                            "id": canvas_id,
                            "label": canvas.label,
                            "image_iiif_id": canvas.images[0].resource.id,
                            "width": width,
                            "height": height,
                            "download_path": image_filename,
                        }
                    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("iiif_url")
    parser.add_argument("image_dir", type=Path)
    args = parser.parse_args()
    download_iiif_content(args.iiif_url, args.image_dir)
    # TODO: work-level metadata file?
    # summarize work done: # volumes, # images, how many previously downloaded, how many inaccessible
    # NOTE: some manuscripts use structure + range to provide alpha labels for pages


if __name__ == "__main__":
    main()
