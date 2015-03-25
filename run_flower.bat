@echo off

venv\scripts\activate && celery flower --broker=redis://localhost:6379/0

@echo on