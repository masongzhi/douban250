TAG = $(shell date +%Y%m%d%H%M%S)
BETA_TAG=beta
LATEST_TAG=latest
REGISTRY=masongzhi
NAME=douban250
BRANCH_NAME=$(shell git rev-parse --abbrev-ref HEAD)

scrapy:
	echo building scrapy:latest
	cp ./docker/scrapy_Dockerfile ./Dockerfile && \
	docker build -t ${REGISTRY}/scrapy:${LATEST_TAG} .
	docker push ${REGISTRY}/scrapy:${LATEST_TAG}
prod:
	echo building ${NAME}:prod
	cp ./docker/douban250_Dockerfile ./Dockerfile && \
					docker build -t ${REGISTRY}/${NAME}:prod .
	docker push ${REGISTRY}/${NAME}:prod
run:
	pipenv run scrapy crawl douban250 -o result.json
