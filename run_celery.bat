@echo off

venv\scripts\activate && celery worker -A Launcher.celery_obj -f celery.worker.log --loglevel=INFO

@echo on