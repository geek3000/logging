from flask import Flask, request   # Importation de Flask et request
from logger import jsonLogHandler  # Importation du module pour le handler de logging JSON
from flask.logging import default_handler  # Importation du handler de logging par défaut de Flask
import logging   # Importation du module logging pour configurer le logger

app = Flask(__name__)   # Création de l'application Flask

# Vérification que l'application n'est pas en mode debug
if app.debug != True:

  # Configuration du logger pour utiliser le handler de logging JSON
  logging.getLogger().addHandler(jsonLogHandler)

  # Désactivation de la journalisation par défaut de Flask
  log = logging.getLogger('werkzeug')
  log.disabled = True

  # Configuration du logger de l'application pour utiliser le handler de logging JSON
  app.logger.setLevel(logging.INFO)
  app.logger.removeHandler(default_handler)
  app.logger.addHandler(jsonLogHandler)

# Fonction appelée avant chaque requête reçue par l'application
@app.before_request
def before():
    app.logger.info("request")   # Ajout d'une ligne de journalisation pour chaque requête

# Route principale de l'application
@app.route('/')
def main():
    return "ok"   # Renvoie une chaîne de caractères "ok"

if __name__ == '__main__':
  app.run(debug=True)   # Lancement de l'application Flask en mode debug
