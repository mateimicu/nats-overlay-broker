IMG_NAME ?= matei10/nats-overlay-brokers
IMG_TAG ?= latest
MODE ?= "broker"
STACK_NAME ?= "ebs-cluster"

NEXT_TAG := $(shell . .venv/bin/activate && ./get_next_tag.py matei10/nats-overlay-brokers)

all: test docker-package deploy

# Run tests
bare-test: lint 
	. .venv/bin/activate && pytest --cov=nats_overlay_broker nats_overlay_broker

test: virtualenv bare-test

# run an agent
bare-run:
	. .venv/bin/activate && nats_overlay_broker ${MODE}

run: virtualenv bare-run

# Profile an agent
bare-profile-run: 
	rm -r output.profile || true
	. .venv/bin/activate && python -m cProfile -o output.profile ./nats_overlay_broker/cli.py ${MODE}
	snakeviz output.profile

profile-run: virtualenv bare-proile-run

# Run pylint against code
lint:
	. .venv/bin/activate && pylint --rcfile=.pylintrc nats_overlay_broker/

virtualenv:
	pip3 install --user virtualenv
	virtualenv .venv -p python3.7
	. .venv/bin/activate && pip3 install -r requirements.txt
	. .venv/bin/activate && pip3 install -r test-requirements.txt
	. .venv/bin/activate && pip3 install -e .

# Build the docker image
docker-package:
	docker build . -t ${IMG_NAME}:${IMG_TAG} -t ${IMG_NAME}:${NEXT_TAG}

# Push the docker image
#
docker-push: docker-push-img-tag docker-push-next-tag

docker-push-img-tag:
	docker push ${IMG_NAME}:${IMG_TAG} 

docker-push-next-tag:
	docker push ${IMG_NAME}:${NEXT_TAG}

docker-publish: docker-package docker-push

docker-run: docker-package
	docker run -ti -e MODE="${MODE}" ${IMG_NAME}:${IMG_TAG}

infra-update: docker-publish
	export IMG_NEW_TAG="${NEXT_TAG}" && docker stack deploy --compose-file infra.yaml ${STACK_NAME}


infra-offline: 
	export IMG_NEW_TAG="${IMG_TAG}" && docker stack deploy --compose-file infra.yaml ${STACK_NAME}
deploy: destory-stack infra-update

destory-stack:
	docker stack rm ${STACK_NAME}

destroy-containers:
	docker ps -qa  | xargs docker rm -f {}

destroy-images:
	docker image prune -f -a 

destroy:  destory-stack destroy-containers destroy-images

logs:
	./logs.sh ${CONTAINER}
