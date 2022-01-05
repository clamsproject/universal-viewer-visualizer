# Universal Viewer Web App for CLAMS/MMIF

This web app generates a IIIF manifest from an MMIF and displays the result using Universal Viewer.
## Supported annotation

1. Video Document Type
1. TimeFrame Annotation Types

## Installation 

## via Docker 

Running via [docker](https://www.docker.com/) is preferred way. Download or clone this repository and build a image using `Dockerfile`, by running the command 

```docker image build . -t uv_consumer```

Once the image is ready, run it with container port 5000 is exposed (`-p XXXX:5000`) and data repository is mounted inside `/app/static` directory of the container using  the command, ```docker run uv_consumer -it -p 5000:5000 -v /path/to/data/directory:/app/universal-viewer-consumer/static```
' See the last section for more details on data repository.

## Native installation

### Requirements

1. Python 3.6 or later
1. git command line interface

### Instruction
Simply clone this repository and install python dependencies listed in `requirements.txt`. Copy, symlink, or mount your primary data source into `static` directory. See next section for more details. 

And then copy (or symlink/mount) your primary data source into `static` directory. 

# Data source repository. 
Data source includes video, audio, and text (transcript) files that are subjects for the CLAMS analysis tools. To make this visualizer accessible to those files and able to display the contents on the web browser, source files needs to be located inside `static` directory. For example, if the path to a source file encoded in the MMIF is `/local/path/to/data/some-video-file.mp4`, the same file must exist as `static/local/path/to/data/some-video-file.mp4`. 
