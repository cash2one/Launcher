@echo off

set venv=%userprofile%\Envs\launcher

rem echo %venv%

%venv%\scripts\activate && celery worker -A Launcher.celery_obj -f logs\celery.worker.log --loglevel=INFO

@echo on
