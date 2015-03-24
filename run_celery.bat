@echo off

venv\scripts\activate && celery worker -A Launcher.celery --loglevel=INFO

@echo on