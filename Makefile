.PHONY: docker-down
docker-down:
	@docker-compose down

.PHONY: docker-start
docker-start:
	@docker-compose up -d

docker-exec: docker-start
	@docker-compose exec python3 bash

run: docker-start
	@docker-compose run python3 bash -c "cd /root/src/realestate && python main.py"
