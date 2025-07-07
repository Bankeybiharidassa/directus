#!/bin/bash
# Basic installer for Nucleus CRM demo environment
set -e

python3 -m venv venv
source venv/bin/activate
pip install -r CRM/requirements.txt
npm install --prefix CRM/node_backend

echo "Backend and auth services can be started with ./test_install.sh"
