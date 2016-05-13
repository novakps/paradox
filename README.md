# paradox
fake docking service.  Returns a 2D and 3D pair-of-docks.

How to run:

have rdkit installed. For OSX:

    brew update
    brew tap rdkit/rdkit
    brew install rdkit

checkout this repo and create a virtualenv

    virtualenv env

add the following to env/bin/activate to add rdkit to python path (these paths are not at all likely to be correct in your environment).

    # rdkit environment vars
    export RDBASE=/opt/boxen/homebrew/share/RDKit
    export PYTHONPATH=/opt/boxen/homebrew/lib/python2.7/site-packages:$PYTHONPATH

activate the virtualenv

    source env/bin/activate

install deps

    pip install -r requirements.txt

edit path to pymol in paradox.py, if necessary.

    pymol_path = '/Applications/MacPyMOL.app/Contents/MacOS/MacPyMOL'

start the server (pymol gui will start up too)

    python paradox.py

post something

    curl -X POST -d @caffeine.json http://localhost:5000/dock
