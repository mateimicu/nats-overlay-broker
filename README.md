# KubeMQ overlay broker

Tools requires:

- `docker` CLI and Engine installed
- `make` to build the project and deploy the manifests

## Installation 

* Install docker and make sure it works `docker version` should return the version for both Client and Engine
* (optional) Run tests `make test`
* Create the Docker Image `make docker-package` (you can pass custom `IMG_NAME` and `IMG_TAG`)
* Push the docker image to a public registry `make docker-push` (you can pass custom `IMG_NAME` and `IMG_TAG`)
* Create the infrastructure `make create-infra`
* For testing purposes run the project `make run`

