import re
import time
import socket
from flask import request
from flask import _app_ctx_stack as stack
from statsd import StatsClient


def _extract_request_path(url_rule):
    if not url_rule:
        return ''
    s = re.sub(r'/<.*>', '/', str(url_rule))
    s = re.sub(r'\.json$', '', s)
    return '.'.join(filter(None, s.split('/')))


def add_tags(path, **tags):
    if not tags:
        return path
    tag_str = ','.join([('%s=%s' % (k, v)) for k, v in tags.items()])
    return '%s,%s' % (path, tag_str)


class FlaskStatsd(object):

    def __init__(self, app=None, host='localhost', port=8125, prefix=''):
        self.app = app
        self.hostname = socket.gethostname()
        self.statsd_host = host
        self.statsd_port = port
        self.statsd_prefix = prefix
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        self.connection = self.connect()

    def connect(self):
        return StatsClient(host=self.statsd_host,
                           port=self.statsd_port,
                           prefix=self.app.name + self.statsd_prefix,
                           maxudpsize=1024)

    def before_request(self):
        ctx = stack.top
        ctx.request_begin_at = time.time()

    def after_request(self, resp):
        ctx = stack.top
        period = (time.time() - ctx.request_begin_at) * 1000
        status_code = resp.status_code
        path = _extract_request_path(request.url_rule or 'notfound')
        with self.connection.pipeline() as pipe:
            path = add_tags(path, server=self.hostname, status_code=status_code)
            pipe.incr(path)
            pipe.timing(path, period)
            overall_path = add_tags("request", server=self.hostname, status_code=status_code)
            pipe.incr(overall_path)
            pipe.timing(overall_path, period)

        return resp
