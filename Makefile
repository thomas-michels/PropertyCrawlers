include ./.env

build:
	docker build -t property_crawlers --no-cache .

run:
	docker run --env-file .env --name property_crawlers -d --network=${NETWORK} property_crawlers
