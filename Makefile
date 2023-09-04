include ./.env

build:
	docker build -t property_worker --no-cache .

run:
	docker run --env-file .env.container --name property_worker -d --network=propertycrawler_crawler_network property_worker
