import cgi
import urllib


class Request(object):
    def __init__(self, environ):
        self.headers = self._parse_headers(environ)
        self.query = self._parse_query(environ)
        self.data = self._parse_data(environ)
        self.path = environ['PATH_INFO']

    @staticmethod
    def _parse_query(environ):
        query = urllib.parse.parse_qs(environ['QUERY_STRING'])
        return {k: v[0] for k, v in query.items()}

    @staticmethod
    def _parse_headers(environ):
        length = environ.get('CONTENT_LENGTH', 0)
        headers = {'CONTENT_LENGTH': 0 if not length else int(length)}
        wanted_headers = ['REQUEST_METHOD', 'PATH_INFO', 'REMOTE_ADDR',
                          'REMOTE_HOST', 'CONTENT_TYPE']
        for k, v in environ.items():
            if k in wanted_headers or k.startswith('HTTP'):
                headers[k] = v
        return headers

    def _parse_data(self, environ):
        content_type = environ['CONTENT_TYPE'].lower()
        if 'form' in content_type:
            data = {}
            env_data = cgi.FieldStorage(environ['wsgi.input'],
                                        environ=environ)
            for k in env_data.list:
                if isinstance(k, cgi.MiniFieldStorage):
                    if k.filename:
                        data[k.name] = k.file
                    else:
                        data[k.name] = k.value
            return data
        else:
            length = self.headers['CONTENT_LENGTH']
            return environ['wsgi.input'].read(length)