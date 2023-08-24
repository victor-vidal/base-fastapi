echo "MIGRATING ALL APPS..."

alembic -c ./app/fraud/alembic.ini upgrade head