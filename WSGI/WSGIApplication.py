from functools import wraps
from wsgiref.simple_server import make_server
import re
from .Request import Request
from .Response import ErrorResponse
from .DBFileKeeper import DBFileKeeper
from .SQLiteWrapper import SQLiteWrapper
from Utils import read_file


class WSGIApplication(object):
    def __init__(self):
        self.url_patterns = {}
        self.db_object = self.get_or_create_db_object("create_db.sql")

    def route(self, url, methods=['GET']):
        def decorate(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            self.url_patterns[re.compile(url)] = \
                {'methods': methods, 'func': wrapper}
            return wrapper
        return decorate

    def get_view_func(self, path):
        for url_pattern, func in self.url_patterns.items():
            if url_pattern.match(path):
                return func
        return None

    def path_dispatch(self, request, response):
        method = request.headers['REQUEST_METHOD']
        view = self.get_view_func(request.path)
        if view is None:
            return ErrorResponse(response, 404)
        elif method not in view['methods']:
            return ErrorResponse(response, 405)
        else:
            return view['func'](request, response, self.db_object)

    def dispatch_request(self, environ, make_response):
        request = Request(environ)
        response = self.path_dispatch(request, make_response)
        return response

    def __call__(self, environ, make_response):
        response = self.dispatch_request(environ, make_response)
        return response.render()

    @staticmethod
    def get_or_create_db_object(init_script_path):
        db_file = DBFileKeeper("base.sqlite")
        full_db_file_path = db_file.get_path()
        if db_file.is_exist() is False:
            db_file.create_db_file()
            init_script_content = read_file(init_script_path)
            return SQLiteWrapper(full_db_file_path, init_script_content)
        return SQLiteWrapper(full_db_file_path)

    def run_server(self, host='', port=8080):
        httpd = make_server(host, port, self)
        httpd.serve_forever()

    def run_application(self):
        self.run_server()


def create_application_instance():
    from WSGI.Response import TemplateResponse, SuccessResponse, JSONResponse
    app = WSGIApplication()

    @app.route('/comment$')
    def comment(request, response, db_object):
        return TemplateResponse(response, 'templates/comment/comment.html')

    @app.route('/view$')
    def view(request, response, db_object):
        return TemplateResponse(response, 'templates/comment/view_all_comments.html')

    @app.route('/stat$')
    def stat(request, response, db_object):
        return TemplateResponse(response, 'templates/comment/stat.html')

    @app.route('/static/.*')
    def static(request, response, db_object):
        return TemplateResponse(response, 'templates/comment' + request.path)

    @app.route('/api/add_comment$', methods=['POST'])
    def add_comment(request, response, db_object):
        db_object.insert_comment(request.data)
        return SuccessResponse(response)

    @app.route('/api/remove_comment_by_id$', methods=['POST'])
    def remove_comment_by_id(request, response, db_object):
        db_object.remove_comment(int(request.data["commentID"]))
        return SuccessResponse(response)

    @app.route('/api/get_all_regions$', methods=['POST'])
    def get_all_regions(request, response, db_object):
        all_regions = db_object.get_all_regions()
        return JSONResponse(response, all_regions)

    @app.route('/api/get_all_cities_by_reg_id$', methods=['POST'])
    def get_all_cities_by_reg_id(request, response, db_object):
        all_cities = db_object.get_all_cities_by_reg_id(int(request.data["regionID"]))
        return JSONResponse(response, all_cities)

    @app.route('/api/get_all_comments$', methods=['POST'])
    def get_all_comments(request, response, db_object):
        all_comments = db_object.get_all_comments()
        return JSONResponse(response, all_comments)

    @app.route('/api/get_regions_stat$', methods=['POST'])
    def get_all_comments(request, response, db_object):
        region_stat = db_object.get_region_where_comments_more_than(5)
        return JSONResponse(response, region_stat)

    @app.route('/api/get_cities_stat$', methods=['POST'])
    def get_all_comments(request, response, db_object):
        cities_stat = db_object.get_cities_stat_by_region_id(int(request.data["regionID"]))
        return JSONResponse(response, cities_stat)
    return app
