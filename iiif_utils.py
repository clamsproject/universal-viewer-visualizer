import json
import os
import tempfile
from typing import Dict

import mmif
from flask import url_for
from mmif import AnnotationTypes, DocumentTypes, Mmif
import datetime


def generate_iiif_manifest(in_mmif: mmif.Mmif):
    iiif_json = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "id": "http://0.0.0.0:5000/mmif_example_manifest.json",
        "type": "Manifest",
        "label": "NewsHour Sample",
        "description": f"generated at {datetime.datetime.now()}",
        "sequences": [
            {
                "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/sequence/1",
                "type": "Sequence",
                "canvases": [],
            }
        ],
        "structures": []
    }
    add_canvas_from_documents(in_mmif, iiif_json)
    add_structure_from_timeframe(in_mmif, iiif_json)
    return save_manifest(iiif_json)


def add_canvas_from_documents(in_mmif, iiif_json):
    video_documents = in_mmif.get_documents_by_type(DocumentTypes.VideoDocument)
    audio_documents = in_mmif.get_documents_by_type(DocumentTypes.AudioDocument)
    image_documents = in_mmif.get_documents_by_type(DocumentTypes.ImageDocument)
    all_documents = video_documents + audio_documents + image_documents
    document_canvas_dict = {}
    for _id, document in enumerate(all_documents, start=1):
        document_canvas_dict[document.id] = _id
        canvas = {
            "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/canvas/{_id}",
            "type": "Canvas",
            "label": "NewsHour",
            "height": 360,
            "width": 480,
            "duration": 660,
            "content": [
                {
                    "id": "...",
                    "type": "AnnotationPage",
                    "items": [
                        {
                            "id": "...",
                            "type": "Annotation",
                            "motivation": "painting",
                            "body": [
                                {
                                    "type": "Choice",
                                    "choiceHint": "user",
                                    "items": [
                                        {
                                            "id": build_document_url(document),
                                            "type": get_iiif_type(document),
                                            "label": "",
                                            "format": get_iiif_format(document)
                                        }
                                    ]
                                }
                            ],
                            "target": f"http://0.0.0.0:5000/mmif_example_manifest.json/canvas/{_id}"
                        }
                    ],
                }
            ],
        }
        # if not os.path.isfile(f"static{document.location_path()}"):
        #     shutil.copyfile(
        #         f"{document.location_path()}",
        #         f"static{os.path.basename(document.location_path())}"
        #     )
        iiif_json["sequences"][0]["canvases"].append(canvas)
        break # todo currently only supports single document, needs more work to align canvas values

def build_document_url(document):
    '''
    This trims off all of the path to the document except the filename then prepends data/video/. This is so
    mmif's from running locally can still be found if the viewe
    r is run in docker, assuming the volume mount or
    symlink is correctly set.
    '''
    location = document.location
    if location.startswith("file://"):
        location = document.location[7:]
    file_path = os.path.join("data", "video", os.path.basename(location))
    return url_for('static', filename=file_path)


def add_structure_from_timeframe(in_mmif: Mmif, iiif_json: Dict):
    # # get all views with timeframe annotations from mmif obj
    tf_views = in_mmif.get_views_contain(AnnotationTypes.TimeFrame)
    for range_id, view in enumerate(tf_views, start=1):
        view_range = tf_view_to_iiif_range(range_id, view)
        iiif_json["structures"].append(view_range)


def save_manifest(iiif_json: Dict) -> str:
    # generate a iiif manifest and save output file
    manifest = tempfile.NamedTemporaryFile('w', dir="static/", suffix='.json', delete=False)
    json.dump(iiif_json, manifest, indent=4)
    return manifest.name


def tf_view_to_iiif_range(range_id, view):
    view_range = {
        "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/range/{range_id}",
        "type": "Range",
        "label": f"View: {view.id}",
        "members": []
    }
    for annotation in view.annotations:
        if annotation.at_type == AnnotationTypes.TimeFrame:
            if 'timeUnit' in annotation.properties:
                annotation_unit = annotation.properties['timeUnit']
            elif 'timeUnit' in view.metadata.parameters:
                annotation_unit = view.metadata.parameters['timeUnit']
            else:
                raise Exception("Error finding timeframe unit.")
            frame_type = annotation.properties["frameType"]
            if annotation_unit == "frame":
                start_fn = int(annotation.properties["start"])
                end_fn = int(annotation.properties["end"])
                frame_rate = 29.97
                start_sec = int(start_fn // frame_rate)
                end_sec = int(end_fn // frame_rate)
            elif annotation_unit == "milliseconds":
                start_milli = int(annotation.properties["start"])
                end_milli = int(annotation.properties["end"])
                start_sec = int(start_milli // 1000)
                end_sec = int(end_milli // 1000)
            else:
                continue
            structure = {
                "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/range/{range_id}",
                "type": "Range",
                "label": f"{frame_type.capitalize()}",
                "members": [
                    {
                        "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/canvas/{1}#t={start_sec},{end_sec}",
                        # need to align id here to support more than one document
                        "type": "Canvas"
                    }
                ]
            }
            view_range["members"].append(structure)
    return view_range


def get_iiif_format(document):
    if document.is_type(DocumentTypes.VideoDocument):
        return 'video/mp4'
    elif document.is_type(DocumentTypes.ImageDocument):
        return "image/jpeg"
    else:
        raise ValueError("invalid document type for iiif canvas")


def get_iiif_type(document):
    if document.is_type(DocumentTypes.VideoDocument):
        return 'Video'
    elif document.is_type(DocumentTypes.ImageDocument):
        return 'Image'
    else:
        raise ValueError("invalid document type for iiif canvas")
