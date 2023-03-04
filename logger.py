from flask import has_request_context, request   # Importation des modules Flask
import logging   # Importation du module logging pour configurer le logger
from pythonjsonlogger import jsonlogger   # Importation du module pour le formatter JSON
from datetime import datetime   # Importation du module pour récupérer la date et l'heure actuelles

jsonLogHandler = logging.StreamHandler()   # Création d'un StreamHandler pour la sortie de journalisation

# Définition de la classe MyJsonFormatter qui hérite de la classe JsonFormatter qui permet de formatter les logs en JSON
class MyJsonFormatter(jsonlogger.JsonFormatter):

    # Ajout des champs personnalisés au format JSON
    def add_fields(self, log_record, record, message_dict):
        super(MyJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # Récupération de la date et l'heure actuelles au format ISO 8601
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        # Vérification de l'existence d'un niveau de journalisation avant de l'ajouter au format JSON et le mettre en majuscule   
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        # Vérification de l'existence d'un contexte de requête avant d'ajouter les champs liés à la requête
        if has_request_context():
            log_record['url'] = request.url
            log_record['method'] = request.method
            log_record['ip'] = request.remote_addr
            log_record['user_agent'] = request.user_agent.string
            log_record['path'] = request.path


# Création d'un formatter MyJsonFormatter avec les champs personnalisés que l'on souhaite ajouter au format JSON et qui ont ete recupérés dans le contexte de la requête
formatter = MyJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s %(url)s %(method)s %(ip)s %(user_agent)s %(path)s')

# Configuration du handler de journalisation pour utiliser le formatter MyJsonFormatter
jsonLogHandler.setFormatter(formatter)
