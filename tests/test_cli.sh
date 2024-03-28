#!/usr/bin/env bash

set -ev

cd "$(dirname "$0")"

plateaukit () {
    python ../plateaukit "$@"
}

# TODO: Test remote install
plateaukit install plateau-30422-taiji-cho-2021 --force --local ./fixtures/30422_taiji-cho_2021_citygml_2_op.zip
plateaukit generate-cityjson --dataset plateau-30422-taiji-cho-2021 /tmp/output.city.json
plateaukit info plateau-30422-taiji-cho-2021
plateaukit info plateau-28225-asago-shi-2022
