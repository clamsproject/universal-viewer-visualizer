import mmif
from mmif import AnnotationTypes

def generate_iiif_manifest(mmif_str):
    # mmif_obj = mmif.Mmif(mmif_str)
    # # get all views with timeframe annotations from mmif obj
    # tf_views = mmif_obj.get_all_views_contain(AnnotationTypes.TimeFrame.value)
    # # for all timeframe annotations
    #
    # for view in tf_views:
    #     # get
    # # generate a iiif thing
    return '''{
    "id": "http://dlib.indiana.edu/iiif_av/lunchroom_manners",
    "type": "Manifest",
    "label": "Sample Newshour",
    "description": "A sample Newshour Video",
    "sequences": [
        {
            "id": "http://dlib.indiana.edu/iiif_av/lunchroom_manners/sequence/1",
            "type": "Sequence",
            "canvases": [
                {
                    "id": "http://dlib.indiana.edu/iiif_av/lunchroom_manners/canvas/1",
                    "type": "Canvas",
                    "label": "A sample Newshour Video",
                    "description": "a sample newshour video from the aapb",
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
                                                    "id": "/var/archive/video/cpb-aacip-507-0z70v8b343.mp4",
                                                    "type": "Video",
                                                    "label": "High",
                                                    "format": "video/mp4"
                                                }
                                            ]
                                        }
                                    ],
                                    "target": "http://dlib.indiana.edu/iiif_av/canvas/1"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "structures": [
        {
            "id": "http://dlib.indiana.edu/iiif_av/lunchroom_manners/range/3",
            "type": "Range",
            "label": "SMPTE Bars",
            "members": [
                {
                    "id": "http://dlib.indiana.edu/iiif_av/lunchroom_manners/canvas/1#t=0,59",
                    "type": "Canvas"
                }
            ]
        },
        {
            "id": "http://dlib.indiana.edu/iiif_av/lunchroom_manners/range/3",
            "type": "Range",
            "label": "Slate",
            "members": [
                {
                    "id": "http://dlib.indiana.edu/iiif_av/lunchroom_manners/canvas/1#t=60,112",
                    "type": "Canvas"
                }
            ]
        }
    ]
}'''

