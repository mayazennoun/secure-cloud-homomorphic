from flask import Flask, request, jsonify
from Pyfhel import Pyfhel, PyCtxt
import base64
import os

app = Flask(__name__)


HE = Pyfhel()
HE.contextGen(scheme='CKKS', n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60])

if not os.path.exists("public_key.pk"):
    raise FileNotFoundError(
        "Clé publique 'public_key.pk' introuvable. Lance client.py une première fois pour la générer."
    )
HE.load_public_key("public_key.pk")

def deserialize_ctxt(data_str):
    """Convertit une chaîne base64 en PyCtxt (avec instance HE)"""
    ctxt = PyCtxt(pyfhel=HE)  
    ctxt.from_bytes(base64.b64decode(data_str))
    return ctxt

def serialize_ctxt(ctxt):
    """Convertit un PyCtxt en chaîne base64 pour JSON"""
    return base64.b64encode(ctxt.to_bytes()).decode('utf-8')

@app.route('/compute', methods=['POST'])
def compute():
    try:
        data = request.json['encrypted_data']
        encrypted_list = [deserialize_ctxt(x) for x in data]

        
        sum_enc = encrypted_list[0]
        for enc in encrypted_list[1:]:
            sum_enc += enc
        mean_enc = sum_enc * (1 / len(encrypted_list))

        return jsonify({
            'sum': serialize_ctxt(sum_enc),
            'mean': serialize_ctxt(mean_enc)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
