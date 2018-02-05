# Flask Empty API

Docker Powered Flask boilerplate for super fast prototyping.
Get you Flask Rest Token Authenticated Websocket-ready project
running with a single command.

## Getting Started

* Make sure docker, docker-compose and fabric are installed
* Clone the repo with any name you like
* Go to the project folder and run: `fab env:dev up` (project is now running)
* In another terminal, create the database with: `fab env:dev on:app run:"flask db upgrade"`

## Available Endpoints (out-of-the-box)

* /login
* /logout
* /  # index

## Useful

* `fab env:dev on:app run:"flask shell"`  # bring up flask shell
* `fab env:dev on:app run:"flask db migrate --rev-id 001 -m message"`  # create revision
* `fab env:dev attach:containerID`  # attach to tty; logs and pdb

## Deployment

* configure your swarm secrets
* tune flask configuration for security (SSL, MAILING, etc)
* make sure envfile variables are production ready
* open the champaign
