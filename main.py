from WSGI.WSGIApplication import create_application_instance


if __name__ == '__main__':
    app = create_application_instance()
    app.run_application()
