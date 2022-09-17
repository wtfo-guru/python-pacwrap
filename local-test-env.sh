#!/bin/bash

IMAGE=${1:-ghcr.io/qs5779/python-multi:edge}

docker pull "$IMAGE"

docker run \
  --rm \
  --tty \
  --interactive \
  --volume "$(git rev-parse --show-toplevel)":/var/code/ \
  "$IMAGE"  /bin/bash
