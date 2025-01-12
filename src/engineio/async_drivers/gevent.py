from __future__ import absolute_import

import gevent
from gevent import queue
from gevent.event import Event
from gevent.threading import Thread
try:
    import geventwebsocket  # noqa
    _websocket_available = True
except ImportError:
    _websocket_available = False


class WebSocketWSGI(object):  # pragma: no cover
    """
    This wrapper class provides a gevent WebSocket interface that is
    compatible with eventlet's implementation.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'wsgi.websocket' not in environ:
            raise RuntimeError('You need to use the gevent-websocket server. '
                               'See the Deployment section of the '
                               'documentation for more information.')
        self._sock = environ['wsgi.websocket']
        self.environ = environ
        self.version = self._sock.version
        self.path = self._sock.path
        self.origin = self._sock.origin
        self.protocol = self._sock.protocol
        return self.app(self)

    def close(self):
        return self._sock.close()

    def send(self, message):
        return self._sock.send(message)

    def wait(self):
        return self._sock.receive()


_async = {
    'thread': Thread,
    'queue': queue.JoinableQueue,
    'queue_empty': queue.Empty,
    'event': Event,
    'websocket': WebSocketWSGI if _websocket_available else None,
    'sleep': gevent.sleep,
}
