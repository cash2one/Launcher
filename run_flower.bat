@echo off

set venv=%userprofile%\Envs\launcher

%venv%\scripts\activate && celery flower --broker=redis://localhost:6379/0

@echo on