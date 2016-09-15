import logging
import logging.handlers

import socket
import traceback
import requests

class HTTPSHandler(logging.Handler):
    TIMEOUT = 0.2
    def __init__(self, url, fqdn=False, localname=None, facility=None):
        logging.Handler.__init__(self)
        self.url = url
        self.fqdn = fqdn
        self.localname = localname
        self.facility = facility

    def get_full_message(self, record):
        if record.exc_info:
            return '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            return record.getMessage()

    def emit(self, record):
        try:
            payload = self.format(record)
            requests.post(self.url, data=payload, timeout=self.TIMEOUT)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
