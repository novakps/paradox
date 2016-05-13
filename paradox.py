'''
paradox
fake docking api using flask redkit and pymol xmlrpc


'''
from flask import Flask, jsonify, request
import base64
import os
from rdkit import Chem
from rdkit.Chem import AllChem
import subprocess
from tempfile import NamedTemporaryFile
import xmlrpclib

app = Flask(__name__)
pymol_path = '/Applications/MacPyMOL.app/Contents/MacOS/MacPyMOL'
proc = subprocess.Popen([pymol_path, '-R'])
pymol = xmlrpclib.Server('http://localhost:9123/RPC2')

@app.route('/dock', methods=['POST'])
def dock():
    ''' POST json containing a required 2D molfile string and an optional 3D molfile string.
     - Get back json containing fake-docked pse and 2D molfile aligned to original 2D that is derived from 3D--if present--or from orignal 2D. '''
    content = request.get_json(force=True)
    mol2d = content['2D']
    mol3d = content.get('3D')
    if mol2d:
        # always used as alignment template, also used as source if no 3D provided
        template = Chem.MolFromMolBlock(mol2d)
    if mol3d:
        # use 3D as source, if present
        source = Chem.MolFromMolBlock(mol3d)
    else:
        # otherwise use 2D as source
        source = template

    # convert to 3D and write to a temp file
    molecule = Chem.AddHs(source)
    AllChem.EmbedMolecule(molecule)
    AllChem.UFFOptimizeMolecule(molecule)
    f = NamedTemporaryFile(delete=False, suffix='.mol')
    writer = Chem.SDWriter(f)
    writer.write(molecule)
    writer.flush()
    f.close()

    # conversion to pse
    pymol.reinitialize()
    pymol.load(f.name)
    pymol.show('sticks')
    pse_name = f.name + '.pse'
    pymol.save(pse_name)
    with open(pse_name) as f_pse:
        encoded = base64.b64encode(f_pse.read())
    os.unlink(f.name)
    os.unlink(pse_name)

    # back to 2D and align with template
    AllChem.Compute2DCoords(molecule)
    AllChem.GenerateDepictionMatching2DStructure(molecule, template)
    result = {'2D': Chem.MolToMolBlock(molecule), 'base64pse': encoded }
    return jsonify(result);

if __name__ == '__main__':
    app.run(debug=True)
    proc.communicate()[0]
