up:
	@echo "Starting backend in cli mode..."
	docker-compose -f docker/docker-compose.yml up --build
	@echo "Backend started in cli mode"

upd:
	@echo "Starting backend in daemon mode..."
	docker-compose -f docker/docker-compose.yml up --build -d
	@echo "Backend started in daemon mode"

down:
	@echo "Stopping backend..."
	docker-compose -f docker/docker-compose.yml down
	@echo "Backend stopped"

migrate:
	@echo "Migrating database..."
	docker-compose -f docker/docker-compose.yml run --rm django python manage.py migrate
	@echo "Database migrated successfully"

docker_django_shell:
	docker -f docker/docker-compose.yml exec -it django bash

docker_postgres_shell:
	docker -f docker/docker-compose.yml exec -it db bash

start_backend: down upd migrate
	@echo "Backend started"

start: start_backend

create_super_user:
	@echo "Creating super user..."
	docker-compose -f docker/docker-compose.yml run --rm django python manage.py createsuperuser --noinput

dupd: down upd
	@echo "Backend restarted"

load_fixtures:
	@echo "Loading fixtures..."
	docker-compose -f docker/docker-compose.yml run --rm django python manage.py loaddata apps/hotels/fixtures/amenities.json
	docker-compose -f docker/docker-compose.yml run --rm django python manage.py loaddata apps/hotels/fixtures/hotel_types.json
	docker-compose -f docker/docker-compose.yml run --rm django python manage.py loaddata apps/hotels/fixtures/room_types.json
	@echo "Fixtures loaded successfully"
