from flask import has_request_context, request
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime

jsonLogHandler = logging.StreamHandler()

class MyJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):

        print("log_record: ", log_record)
        print("record: ", record)
        super(MyJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        # Add request context information
        if has_request_context():
            log_record['request_id'] = request.headers.get('X-Request-ID', None)
            log_record['request_path'] = request.path
            log_record['request_method'] = request.method
            log_record['request_remote_addr'] = request.remote_addr
            log_record['request_user_agent'] = request.user_agent.string
            log_record['request_content_type'] = request.content_type
            log_record['request_content_length'] = request.content_length


formatter = MyJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

jsonLogHandler.setFormatter(formatter)
