import socket
import time
from flask import request, _app_ctx_stack as stack
from statsd import StatsClient


def add_tags(metric, **tags):
    return ','.join([metric] + ['{}={}'.format(k, v) for k, v in tags.items()])


class FlaskStatsd(object):

    def __init__(self, app=None, host='localhost', port=8125, measurement=None):
        self.app = app
        self.hostname = socket.gethostname()
        self.statsd_host = host
        self.statsd_port = port
        self.measurement = measurement
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if not self.measurement:
            self.measurement = 'flask_statsd.{}'.format(self.app.name.strip('.'))
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        self.connection = self.connect()

    def connect(self):
        return StatsClient(host=self.statsd_host,
                           port=self.statsd_port,
                           maxudpsize=1024)

    def before_request(self):
        ctx = stack.top
        ctx._flask_statsd_request_begin_at = time.time()

    def after_request(self, resp):
        ctx = stack.top
        elapsed = (time.time() - ctx._flask_statsd_request_begin_at) * 1000

        status_code = resp.status_code
        endpoint = request.endpoint

        with self.connection.pipeline() as pipe:
            metric = add_tags(self.measurement, endpoint=endpoint, status_code=status_code, server=self.hostname)
            pipe.timing(metric, elapsed)

        return resp
