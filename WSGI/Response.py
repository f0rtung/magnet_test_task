import http.client as httplib
import os
from Utils import read_file
from abc import ABCMeta, abstractmethod
import json


class BaseResponse(metaclass=ABCMeta):
    def __init__(self, make_response, content_type, code):
        self.code = code
        self.content_type = content_type
        self.response_formatted_code = self.format_response_code()
        make_response(self.response_formatted_code,
                      self.content_type)

    def format_response_code(self):
        return '{} {}'.format(self.code,
                              httplib.responses[self.code])

    @abstractmethod
    def render(self):
        pass


class EmptyResponse(BaseResponse):
    def __init__(self, make_response, code):
        super().__init__(make_response,
                         [("content-type", "text/html")],
                         code)

    def render(self):
        yield self.response_formatted_code.encode('utf-8')


class ErrorResponse(EmptyResponse):
    def __init__(self, make_response, error_code):
        super().__init__(make_response, error_code)


class SuccessResponse(EmptyResponse):
    def __init__(self, make_response):
        super().__init__(make_response, 200)


class TemplateResponse(BaseResponse):
    def __init__(self, make_response, template_path):
        super().__init__(make_response,
                         self.get_file_content_type(template_path),
                         200)
        self.template_path = template_path

    @staticmethod
    def get_file_content_type(template_path):
        default_content_type = "text/html"
        content_type = {
            ".css": "text/css",
            ".js": "text/javascript",
            ".html": default_content_type
        }
        file_extension = os.path.splitext(template_path)[1]
        return [
            (
                "content-type",
                content_type.get(file_extension, default_content_type)
            )
        ]

    def load_template_content(self):
        template_content = read_file(self.template_path)
        return str(template_content).encode('utf-8')

    def render(self):
        template_content = self.load_template_content()
        yield template_content


class JSONResponse(BaseResponse):
    def __init__(self, make_response, data):
        super().__init__(make_response,
                         [("content-type", "application/json")],
                         200)
        self.data = data

    def render(self):
        data_as_json = json.dumps(self.data)
        yield str(data_as_json).encode('utf-8')

