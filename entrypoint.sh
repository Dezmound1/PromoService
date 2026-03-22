#!/bin/bash

echo "applying migrations...⭐"
uv run ./promo_service/manage.py migrate
echo "✅--Done!--✅"

echo "seeding the database...⭐"
uv run ./promo_service/manage.py seed_db --clear
echo "✅--Done!--✅"

echo "🚀Starting the Django server...🚀"
uv run promo_service/manage.py runserver 0.0.0.0:8000