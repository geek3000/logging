from flask import has_request_context, request
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime

jsonLogHandler = logging.StreamHandler()

class MyJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):

        super(MyJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
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
