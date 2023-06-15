#!/bin/sh

if [ $1 = "app" ]; then
    echo "start app"
    /usr/local/bin/python -m gunicorn apidemo.wsgi_docker -b 0.0.0.0 -w4 -k gevent
fi


if [ $1 = "local_app" ]; then
    echo "start app"
    python -m gunicorn apidemo.wsgi -b 0.0.0.0 -w4 -k gevent
fi