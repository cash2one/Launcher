@echo off

set venv=%userprofile%\Envs\launcher

%venv%\scripts\activate && celery flower --broker=redis://localhost:6379/0 --persistent=True --db=logs\flower.db

@echo on