DOCKER_USERNAME ?= jemfu
NAME ?= autoscaling
IMAGE_NAME ?= executor-autoscaling
VERSION_TAG ?= $(shell sed -n '/^__version__/p' ./__init__.py | cut -d \' -f2)
GIT_HASH ?= $(shell git log --format="%h" -n 1)

buildx:
	docker buildx build --platform linux/amd64,linux/arm64 --push -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION_TAG} -t ${DOCKER_USERNAME}/${IMAGE_NAME}:latest . -f Dockerfile