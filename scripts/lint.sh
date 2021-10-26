#!/usr/bin/env bash

set -e
set -x

mypy edtvelizydiscord
flake8 edtvelizydiscord
black edtvelizydiscord --check
isort edtvelizydiscord --check-only
