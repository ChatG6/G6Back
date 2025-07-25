''' Gunicorn Configuration for development '''

wsgi_app = "bd.wsgi:application"

bind = "localhost:8000"

keepalive = 1000

graceful_timeout = 1000

timeout = 180

loglevel = "debug"

capture_output = True

daemon = False

workers = 5

reload = True
