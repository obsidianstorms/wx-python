# Weather Runner


## Development Setup
### Intellij
1. Right click on the main repo folder (project root), Mark Directory as Sources Root.  **Might not be needed

1. File -> Project Structure -> Project SDK needs to be an installed python path and reference (eg: /usr/local/bin/python3)

## Pre-Build
As desired
* Edit Makefile container name `container`
* Edit docker-compose.yml `image` to match

## Build
`make build`
* Runs bootstrap.sh

## Run
`make run`
* Runs run.sh