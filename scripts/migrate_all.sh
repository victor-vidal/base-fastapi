echo "MIGRATING ALL APPS..."

alembic -c ./app/analytics/alembic.ini upgrade head