build:
	docker compose build

run:
	docker compose up --watch

start: build run

clear:
	docker compose down --remove-orphans

dummy-build:
	docker compose -f dummy-compose.yaml build

dummy-start:
	docker compose -f dummy-compose.yaml up -d
dummy-watch:
	docker compose -f dummy-compose.yaml up --build --watch 
dummy-clear:
	docker compose -f dummy-compose.yaml down --remove-orphans


# temporary
comfy-build:
	docker compose -f comfy-compose.yaml build

comfy-run:
	docker compose -f comfy-compose.yaml up -d 
	
comfy-start: comfy-build comfy-run