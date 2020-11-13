import json
import os
import tempfile

import mmif
from mmif import AnnotationTypes, DocumentTypes
import shutil


def generate_iiif_manifest(mmif_str):
    mmif_obj = mmif.Mmif(mmif_str)
    ## get all videos todo make this work for audio too
    video_paths = [
        doc.properties["location"]
        for doc in mmif_obj.get_documents_by_type(DocumentTypes.VideoDocument)
    ]
    audio_paths = [
        doc.properties["location"]
        for doc in mmif_obj.get_documents_by_type(DocumentTypes.AudioDocument)
    ]
    document_paths = video_paths + audio_paths
    iiif_json = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "id": "http://0.0.0.0:5000/mmif_example_manifest.json",
        "type": "Manifest",
        "label": "NewsHour Sample",
        "description": "A sample AAPB video",
        "sequences":[
            {
                "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/sequence/1",
                "type": "Sequence",
                "canvases": [],
            }
        ],
        "structures":[]
    }
    for id, document_path in enumerate(document_paths, start=1):
        canvas = {
            "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/canvas/{id}",
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
                                    "type":"Choice",
                                    "choiceHint":"user",
                                    "items": [
                                        {
                                            "id": f"static{document_path}",
                                            "type": "Video",
                                            "label": "",
                                            "format": "video/mp4",
                                        }
                                    ]
                                }
                            ],
                            "target":f"http://0.0.0.0:5000/mmif_example_manifest.json/canvas/{id}"
                        }
                    ],
                }
            ],
        }
        if not os.path.isfile(f"static{document_path}"):
            shutil.copyfile(
                f"{document_path}",
                # f"/Users/kelleylynch/data/clams/video/{os.path.basename(document_path)}",
                f"static{document_path}"
            )
        iiif_json["sequences"][0]["canvases"].append(canvas)
        break # todo currently only supports single document, needs more work to align canvas values

    # # get all views with timeframe annotations from mmif obj
    tf_views = mmif_obj.get_all_views_contain(AnnotationTypes.TimeFrame.value)

    for _id, view in enumerate(tf_views, start=1):
        for annotation in view.annotations:
            if annotation.at_type == AnnotationTypes.TimeFrame.value:
                if 'unit' in view.metadata.contains[AnnotationTypes.TimeFrame.value]:
                    annotation_unit = view.metadata.contains[AnnotationTypes.TimeFrame.value]['unit']
                else:
                    annotation_unit = annotation.properties['unit']
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
                    start_sec = int(start_milli//1000)
                    end_sec = int(end_milli//1000)
                else:
                    continue
                structure = {
                    "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/range/{_id}",
                    "type": "Range",
                    "label": f"{frame_type}",
                    "members": [
                        {
                            "id": f"http://0.0.0.0:5000/mmif_example_manifest.json/canvas/{1}#t={start_sec},{end_sec}",
                        # need to align id here to support more than one document
                            "type": "Canvas"
                        }
                    ]
                }
                iiif_json["structures"].append(structure)
    # # generate a iiif manifest and save output file
    manifest = tempfile.NamedTemporaryFile('w', dir="static/", suffix='.json', delete=False)
    json.dump(iiif_json, manifest, indent=4)
    return manifest.name
