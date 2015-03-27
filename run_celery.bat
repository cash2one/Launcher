@echo off

venv\scripts\activate && celery worker -A Launcher.celery_obj --loglevel=INFO

@echo on