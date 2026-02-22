build:
	docker compose build

run:
	docker compose up --watch

start: build run

clear:
	docker compose down --remove-orphans

milestone-build:
	docker compose -f docker-compose-milestone.yml build

milestone-start:
	docker compose -f docker-compose-milestone.yml up -d

milestone-clear:
	docker compose -f docker-compose.milestone.yml down --remove-orphans


# temporary
comfy-build:
	docker compose -f comfy-compose.yaml build

comfy-run:
	docker compose -f comfy-compose.yaml up -d 
	
comfy-start: comfy-build comfy-run