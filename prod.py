''' Gunicorn Configuration for Production '''
import multiprocessing

wsgi_app = "bd.wsgi:application"

bind = "localhost:8000"

keepalive = 1000

graceful_timeout = 1000

timeout = 180

capture_output = False

workers = multiprocessing.cpu_count() * 2 + 1

