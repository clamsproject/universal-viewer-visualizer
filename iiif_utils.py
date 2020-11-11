import json
import os
import mmif
from mmif import AnnotationTypes, DocumentTypes
import shutil


def generate_iiif_manifest(mmif_str):
    mmif_obj = mmif.Mmif(mmif_str)
    ## get all videos todo make this work for audio too
    document_paths = [
        doc.properties["location"]
        for doc in mmif_obj.get_documents_by_type(DocumentTypes.VideoDocument)
    ]
    iiif_json = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "id": "mmif_example_manifest.json",
        "type": "Manifest",
        "label": {"en": ["NewsHour Sample"]},
        "sequences":[
            {
                "id": f"mmif_example_manifest.json/sequence/1",
                "type": "Sequence",
                "canvases": [],
                "structures":[]
            }
        ]
    }
    for id, document_path in enumerate(document_paths, start=1):
        canvas = {
            "id": f"mmif_example_manifest.json/canvas/{id}",
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
                            "target":f"mmif_example_manifest.json/canvas/{id}"
                        }
                    ],
                }
            ],
        }
        shutil.copyfile(
            f"{document_path}",
            f"static{document_path}",
        )
        iiif_json["sequences"][0]["canvases"].append(canvas)
        break # todo currently only supports single document, needs more work to align canvas values

    # # get all views with timeframe annotations from mmif obj
    tf_views = mmif_obj.get_all_views_contain(AnnotationTypes.TimeFrame.value)

    for id, view in enumerate(tf_views):
        if view.properties["unit"] != "frame":
            continue
        start_fn = view.properties["start"]
        end_fn = view.properties["end"]
        frame_rate = 29.97
        frame_type = view.properties.get("frameType")

        start_sec = start_fn/frame_rate
        end_sec = end_fn/frame_rate

        structure = {
            "id":f"mmif_example_manifest.json/range/{id}",
            "type":"Range",
            "label":f"{frame_type}",
            "members":[
                {
                    "id":f"mmif_example_manifest.json/canvas/{1}/t={start_sec},{end_sec}", # need to align id here to support more than one document
                    "type":"Canvas"
                }
            ]
        }
        iiif_json["structures"].append(structure)

    # # generate a iiif manifest and save output file
    with open(os.path.join("temp", "manifests", "manifest.json"), "w") as out:
        json.dump(iiif_json, out)
    return
