#!/bin/bash
python manage.py migrate rooms zero
python manage.py migrate rooms 
python manage.py create_superuser