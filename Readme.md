To run project you need to have docker installed and opened.
After the installation you need to run the following commands at the root of the project in the terminal:
1. Build docker images 
docker-compose build
2. Run docker containers
docker-compose up
3. Get database backup from backup.sql
Mac:
docker-compose exec -T db psql -U postgres -d ai_use_cases -p 5433 < backup.sql
Windows:
type backup.sql | docker-compose exec -T db psql -U postgres -d ai_use_cases -p 5433 
4. Sync elasticsearch with initial data
docker-compose exec backend python3 sync_elasticsearch.py
