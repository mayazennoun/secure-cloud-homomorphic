# Secure Cloud Homomorphic

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)  

Prototype de calculs sécurisés sur des données chiffrées dans le cloud utilisant le chiffrement homomorphe CKKS.

---

## Fonctionnalités


- 🔑 Génération automatique de clés publiques et privées
- 🔒 Chiffrement des données côté client
- 🖥️ Calculs homomorphes côté serveur (somme, moyenne)
- 📤 Transmission sécurisée des données
- 📥 Déchiffrement des résultats côté client
- 🖊️ Entrée dynamique des données via le terminal

---

## Technologies

- **Python 3.13**  
- **Pyfhel (CKKS)**  
- **Flask**  
- **Requests**  
- **NumPy**

---

## Flux Client-Serveur

```text
Client -> Chiffrement des données -> Serveur
Serveur -> Calcul homomorphe -> Résultat chiffré -> Client
Client -> Déchiffrement -> Affichage des résultats
