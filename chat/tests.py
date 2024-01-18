from django.test import TestCase

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"] # python3
    #return ["Hello World"] # python2uwsgi --http :8000 --wsgi-file test.py

