import requests
from Pyfhel import Pyfhel, PyCtxt
import base64
import numpy as np
import os
import time


HE = Pyfhel()
HE.contextGen(scheme='CKKS', n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60])


keys_exist = os.path.exists("public_key.pk") and os.path.exists("secret_key.sk")
if not keys_exist:
    print("Clés introuvables, génération des clés...")
    HE.keyGen()
    HE.save_public_key("public_key.pk")
    HE.save_secret_key("secret_key.sk")
    print("Clés générées avec succès.")
else:
    HE.load_public_key("public_key.pk")
    HE.load_secret_key("secret_key.sk")

def serialize_ctxt(ctxt):
    return base64.b64encode(ctxt.to_bytes()).decode('utf-8')

def deserialize_ctxt(data_str):
    ctxt = PyCtxt(pyfhel=HE)
    ctxt.from_bytes(base64.b64decode(data_str))
    return ctxt


server_url = "http://127.0.0.1:5000/compute"
while True:
    try:
        
        requests.get("http://127.0.0.1:5000")
        break
    except requests.exceptions.ConnectionError:
        print("Serveur non disponible, attente de 2 secondes...")
        time.sleep(2)


data_input = input("Entrez vos nombres séparés par des espaces : ")
try:
    data = np.array([float(x) for x in data_input.strip().split()])
except ValueError:
    print("Erreur : veuillez entrer uniquement des nombres valides.")
    exit()


encrypted_data = [HE.encryptFrac(np.array([x])) for x in data]


payload = {"encrypted_data": [serialize_ctxt(x) for x in encrypted_data]}


try:
    response = requests.post(server_url, json=payload)
    result = response.json()

    if 'error' in result:
        print("Erreur serveur :", result['error'])
    else:
        
        sum_dec = HE.decryptFrac(deserialize_ctxt(result['sum']))[0]
        mean_dec = HE.decryptFrac(deserialize_ctxt(result['mean']))[0]

        print("Données originales :", data.tolist())
        print("Somme déchiffrée :", sum_dec)
        print("Moyenne déchiffrée :", mean_dec)
except requests.exceptions.ConnectionError:
    print("Erreur : impossible de se connecter au serveur. Assure-toi que cloud_server.py est lancé.")
except requests.exceptions.JSONDecodeError:
    print("Erreur : le serveur n'a pas renvoyé de JSON valide.")
