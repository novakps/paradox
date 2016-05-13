# paradox
fake docking service.  Returns a 2D and 3D pair-of-docks.

How to run:

have rdkit installed. For OSX:

    brew update
    brew tap rdkit/rdkit
    brew install rdkit

checkout this repo and create a virtualenv

    virtualenv env

add the following two line to env/bin/activate to add rdkit to python path

    # rdkit environment vars
    export RDBASE=/opt/boxen/homebrew/share/RDKit
    export PYTHONPATH=/opt/boxen/homebrew/lib/python2.7/site-packages:$PYTHONPATH

activate the virtualenv

    source env/bin/activate

install deps

    pip install -r requirements.txt

start the server

    python paradox.py
