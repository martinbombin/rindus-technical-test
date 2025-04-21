# Build & Push Docker Image
build:
	docker build -t martinbombin/rindus-technical-test:0.1.0 . -f Dockerfile

push:
	docker push martinbombin/rindus-technical-test:0.1.0

# Docker Compose
up:
	env -i docker-compose --env-file .env -f docker-compose.yml up --build

mysql:
	env -i docker-compose --env-file .env -f docker-compose.yml up --build mysql

down:
	docker-compose down --volumes --remove-orphans

prune:
	docker system prune -f

# Tests
test:
	env -i docker-compose --env-file .env.test -f docker-compose.test.yml up --build

test-mysql:
	env -i docker-compose --env-file .env.test -f docker-compose.test.yml up --build mysql_integration_tests

pytest:
	export $(grep -v '^#' .env.test | xargs) && pytest

# Kubernetes
kube-apply:
	kubectl apply -f kubernetes/

kube-forward:
	kubectl port-forward service/app 8000:80