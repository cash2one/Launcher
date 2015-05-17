REM >> Windows batch file for running celery....change the virtual env directory....

@echo off

REM TODO: Prompt if using venv or not and then take input and execute...currently only assuemes venvwrapper...Do at home

set venv=%userprofile%\Envs\launcher

rem echo %venv%

%venv%\scripts\activate && celery worker -A Launcher.celery_obj -f logs\celery.worker.log --loglevel=INFO

@echo on
