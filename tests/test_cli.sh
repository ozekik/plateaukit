#!/usr/bin/env bash

set -ev

cd "$(dirname "$0")"

plateaukit () {
    python ../plateaukit "$@"
}

# TODO: Test remote install

# Spec v2
plateaukit install plateau-30422-taiji-cho-2021.v2 --force --local ./fixtures/30422_taiji-cho_2021_citygml_2_op.zip
plateaukit prebuild plateau-30422-taiji-cho-2021.v2 -t bldg

plateaukit export-geojson --dataset plateau-30422-taiji-cho-2021.v2 /tmp/output.geo.json
plateaukit export-cityjson --dataset plateau-30422-taiji-cho-2021.v2 /tmp/output.city.json

plateaukit export-geojson --dataset plateau-30422-taiji-cho-2021.v2 /tmp/output.geo.jsonl --seq
plateaukit export-cityjson --dataset plateau-30422-taiji-cho-2021.v2 /tmp/output.city.jsonl --seq

plateaukit info plateau-30422-taiji-cho-2021.v2
plateaukit info plateau-28225-asago-shi-2022.v2

# Spec v3
plateaukit install plateau-30422-taiji-cho-2021 --force --local ./fixtures/30422_taiji-cho_city_2021_citygml_4_op.zip
plateaukit prebuild plateau-30422-taiji-cho-2021 -t bldg

plateaukit export-geojson --dataset plateau-30422-taiji-cho-2021 /tmp/output.geo.json
plateaukit export-cityjson --dataset plateau-30422-taiji-cho-2021 /tmp/output.city.json

plateaukit export-geojson --dataset plateau-30422-taiji-cho-2021 /tmp/output.geo.jsonl --seq
plateaukit export-cityjson --dataset plateau-30422-taiji-cho-2021 /tmp/output.city.jsonl --seq

plateaukit info plateau-30422-taiji-cho-2021
plateaukit info plateau-28225-asago-shi-2022

plateaukit config
