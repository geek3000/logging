## Objectif
Le but de ce TP est de mettre en place un système de journalisation pour une application Flask. Nous utiliserons Docker pour lancer l'application et observer les logs.


## Étapes

### Étape 1 : Création du projet Flask
Tout d'abord, nous allons créer un projet Flask simple pour l'utiliser dans ce TP. Voici les étapes à suivre pour créer un projet Flask :

1. Créer un nouveau répertoire pour le projet :

```bash
mkdir flask-logging
cd flask-logging
```

2. Créer un environnement virtuel pour le projet :

```bash
python -m venv .venv
```

3. Activer l'environnement virtuel :

```bash
source .venv/bin/activate
```

4. Installer Flask :

```bash
pip install Flask
```

5. Créer un fichier app.py avec le contenu suivant :

```python
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
    return "Hello, World!"   # Renvoie une chaîne de caractères "Hello, World!"

if __name__ == '__main__':
  app.run(debug=True)   # Lancement de l'application Flask en mode debug

```

Ce code définit une application Flask simple qui renvoie une chaîne de caractères "Hello, World!" lorsqu'elle est accédée à la racine de l'application.


### Étape 2 : Ajout du système de journalisation
Maintenant que nous avons créé une application Flask, nous allons ajouter un système de journalisation pour enregistrer les événements dans les logs. Pour cela, nous allons utiliser le code que nous avons commenté plus tôt :

```python
from flask import has_request_context, request
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime

jsonLogHandler = logging.StreamHandler()

class MyJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):

        super(MyJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


        if has_request_context():
            log_record['url'] = request.url
            log_record['method'] = request.method
            log_record['ip'] = request.remote_addr
            log_record['user_agent'] = request.user_agent.string
            log_record['path'] = request.path


formatter = MyJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s %(url)s %(method)s %(ip)s %(user_agent)s %(path)s')

jsonLogHandler.setFormatter(formatter)

```

Ce code définit une classe MyJsonFormatter qui hérite de JsonFormatter pour ajouter des champs personnalisés au format JSON. Le code crée ensuite un StreamHandler pour la sortie de journalisation et configure ce handler pour utiliser MyJsonFormatter. Le résultat est un handler de journalisation capable de formater les messages en JSON avec des champs supplémentaires liés à la requête, tels que l'URL, la méthode HTTP, l'adresse IP, le user agent et le chemin de la requête.

### Etape 3 : Utilisation de Docker

1. Notre fabuleux Dockerfile

Nous allons maintenant créer un fichier Dockerfile qui nous permettra de construire une image Docker pour notre application Flask. Le fichier Dockerfile est un fichier de configuration qui contient les instructions pour construire une image Docker.

Créez un fichier Dockerfile à la racine de votre projet avec le contenu suivant :

```Dockerfile
# Utilisez une image Python 3.9
FROM python:3.9

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers de l'application dans le conteneur
COPY requirements.txt .
COPY app.py .
COPY logger.py .

# Installez les dépendances de l'application
RUN pip install -r requirements.txt

# Exposez le port 5000
EXPOSE 5000

# Démarrez l'application Flask
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

```

2. Construction d'image docker de notre application

Nous allons maintenant construire l'image Docker pour notre application Flask en exécutant la commande suivante dans le terminal :

```bash
docker build -t flask-logging .
```

Cette commande construit l'image Docker en utilisant le fichier Dockerfile et lui donne le nom flask-logging.

3. Exécution du conteneur Docker

Nous allons maintenant exécuter le conteneur Docker en utilisant la commande suivante :

```bash
docker run -p 5000:5000 --name myapp flask-logging
```

Cette commande:

- Exécute le conteneur Docker en utilisant l'image flask-logging
- Relie le port 5000 du conteneur au port 5000 de votre machine locale
- Nomme notre container **myapp**

4. Test de notre application

Ouvrez votre navigateur web et accédez à l'URL http://localhost:5000/. Vous devriez voir le message "ok" s'afficher dans votre navigateur.

5. Consultons nos logs

Vous pouvez vérifier les logs de l'application en utilisant la commande suivante dans un nouveau terminal :

```bash
docker logs -f myapp
```

Cette commande affiche les logs de l'application en temps réel. Vous devriez voir les logs en format JSON s'afficher dans le terminal.

# Bravo

Vous avez reussi a integrer un systeme de journalisation dans une application web Flask