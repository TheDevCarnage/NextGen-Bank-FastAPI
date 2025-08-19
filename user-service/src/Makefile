build:
	docker compose -f docker-compose.yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.yml up -d

down-v:
	docker compose -f docker-compose.yml down -v

down:
	docker compose -f docker-compose.yml down

nextgen-config:
	docker compose -f docker-compose.yml config

makemigrations:
	docker compose -f docker-compose.yml exec -it api alembic revision --autogenerate -m "$(name)"

migrate:
	docker compose -f docker-compose.yml exec -it api alembic upgrade head

history:
	docker compose -f docker-compose.yml exec -it api alembic history

current-migration:
	docker compose -f docker-compose.yml exec -it api alembic current

downgrade:
	docker compose -f docker-compose.yml exec -it api alembic downgrade $(version)

inspect:
	docker network inspect nextgen_local_nw

psql:
	docker compose -f docker-compose.yml exec -it psql -U reesssaabh -d nextgen
