#!make
# include .env
# export $(shell sed 's/=.*//' .env)

.PHONY:run
run:
	@env/bin/python3 main.py

.PHONY:requirements
requirements:
	@env/bin/pip3 freeze > requirements.txt
