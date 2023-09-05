include ./.env

build:
	docker build -t property_crawlers --no-cache .

run:
	docker run --env-file .env --name property_crawlers -d --network=propertycrawler_crawler_network property_crawlers
