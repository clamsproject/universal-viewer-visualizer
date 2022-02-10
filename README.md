# Universal Viewer Web App for CLAMS/MMIF

This web app generates a IIIF manifest from an MMIF and displays the result using Universal Viewer.

## Supported annotation

1. Video Document Type
1. TimeFrame Annotation Types

## Installation via Docker 

Download or clone this repository and build a docker image using the `Dockerfile`.

```git clone https://github.com/clamsproject/universal-viewer-visualizer.git```

```cd universal-viewer-visualizer```

```docker image build . -t uv_consumer```

Once the image is ready, run it with container port 5000  exposed (`-p XXXX:5000`) and data repository is mounted inside `/app/static` directory of the container using  the command

```docker run --rm -p 5000:5000 -v /Users/shared/data/clams/:/app/static/data uv_consumer```

With the app running, visit [http://0.0.0.0:5000/upload](http://0.0.0.0:5000/upload) to upload an mmif file.

## Native Installation

### Requirements

1. Python 3.6 or later
1. git command line interface

### Instruction
First clone this repository and install python dependencies listed in `requirements.txt`.

```git clone https://github.com/clamsproject/universal-viewer-visualizer.git```

```cd universal-viewer-visualizer```

```pip install -r requirements.txt```

Copy, symlink, or mount your primary data source into `static` directory. The data folder should have a subfolder named `video`.

```ln -s /Users/shared/archive static/data```

Where the directory `/Users/shared/archive` contains the subdirectory `video`, containing the media files referenced by the mmif.

Set the `FLASK_APP` environment variable. 

```export FLASK_APP=app.py```

Run the flask app. By default the app will run on port 5000. To specify a different port using the command line option to the flask run command.

```flask run```

or to run on port 5001, for example:

```flask run -p 5001```

With the app running, visit [http://0.0.0.0:5000/upload](http://0.0.0.0:5000/upload) to upload an mmif file.

***Note***
The video location from the mmif is modified before being added to the iiif manifest. The modified filename consists of `data/video/{original_filename}`. This is to allow mmif's that result from local processing to be able to be used with this tool, assuming the data directory is linked as expected.


### Example MMIF
The following mmif can be used to test the tool.
```json
{"metadata": {"mmif": "http://mmif.clams.ai/0.4.0"}, "documents": [{"@type": "http://mmif.clams.ai/0.4.0/vocabulary/VideoDocument", "properties": {"mime": "video", "id": "d1", "location": "file:///data/clams/video/cpb-aacip-259-mp4vm595.h264.mp4"}}], "views": [{"id": "v_0", "metadata": {"timestamp": "2022-01-03T16:35:27.965525", "app": "http://mmif.clams.ai/apps/slatedetect/0.1", "contains": {"http://mmif.clams.ai/0.4.0/vocabulary/TimeFrame": {"timeUnit": "milliseconds", "document": "d1"}}, "parameters": {"timeUnit": "milliseconds", "sampleRatio": "10", "stopAt": "30", "stopAfterOne": "True", "minFrameCount": "10", "threshold": "0.5"}}, "annotations": [{"@type": "http://mmif.clams.ai/0.4.0/vocabulary/TimeFrame", "properties": {"start": 0, "end": 1034, "frameType": "slate", "id": "tf_1"}}]}]}
```

This file is in this repository as `example1.mmif`. For it to work you need access to `cpb-aacip-259-mp4vm595.h264.mp4`. There is also a file `example2.mmif` that adds some random timeframes, but it also assumes you have some video file available that is not in this repository.
