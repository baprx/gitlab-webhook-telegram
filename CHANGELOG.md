# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2023-05-29

### Bug Fixes

- Convert username to lowercase
- Add step to retrieve last tag

### Miscellaneous Tasks

- Update dependency pre-commit to v3.1.1
- Add ruff
- Add Docker build actions
- Rename step
- Update dependency pre-commit to v3.2.0
- Update dependency pre-commit to v3.2.1
- Update dependency python-telegram-bot to v20.2
- Update dependency black to v23.3.0
- Update dependency pre-commit to v3.2.2
- Update dependency pre-commit to v3.3.0
- Update dependency pre-commit to v3.3.1
- Update dependency python-telegram-bot to v20.3
- Update dependency pre-commit to v3.3.2
- Update dependency emoji to v2.4.0
- Bump pre-commits

## [1.1.1] - 2023-02-25

### Documentation

- Track issues in KNOWN_ISSUES.md

### Miscellaneous Tasks

- Restore project_token parameter
- Update CHANGELOG.md

## [1.1.0] - 2023-02-25

### Bug Fixes

- Issues when bootstrapping new gitlab webhook

### Documentation

- Update config example

### Features

- Convert scripts to async due to telegram v20 breaking changes

### Miscellaneous Tasks

- Add renovate.json
- Update dependency emoji to v2.1.0
- Update dependency python-telegram-bot to v13.14
- Bump hooks versions
- Bump python modules versions; Improve config example
- Add aiohttp
- Bump python image to 3.11
- Install setuptools before requirements
- Install gcc
- Allow specifying address to listen to
- Update dependency pre-commit to v2.21.0
- Make port and address optional by providing default value
- Add function return when missing
- Update dependency isort to v5.12.0
- Update dependency flake8 to v6
- Update dependency black to v22.12.0
- Update dependency pre-commit to v3
- Update dependency black to v23

### Other

- Bump to 1.1.0

## [1.0.9] - 2022-09-09

### Bug Fixes

- Use state field instead of merge_status to query status

### Refactor

- Add pre-commit hooks

## [1.0.8] - 2022-09-07

### Bug Fixes

- Fix socketserver port already in use error

### Miscellaneous Tasks

- Improve merge requests with the same features as job/pipelines

## [1.0.7] - 2022-09-06

### Miscellaneous Tasks

- Add .gitkeep to preserve directory structure
- Improve Docker COPY step with .dockerignore

## [1.0.6] - 2022-09-06

### Bug Fixes

- Include classes and configs directory to docker build

### Miscellaneous Tasks

- Mention original project

## [1.0.5] - 2022-09-06

### Refactor

- Improve code readability (split classes in separate files; Add def type hints ;tune formatter settings)

## [1.0.4] - 2022-09-05

### Bug Fixes

- Small fixed for pipeline handler

### Features

- Add inline keyboard updating job status and emoji.

### Miscellaneous Tasks

- Try not rebuilding if dependencies unchanged
- Edit message only if status changed
- Add logging if same request received without status change

## [1.0.3] - 2022-09-05

### Features

- Add inline keyboard updating job status and emoji. Avoids jobs spamming chat.
- Add URL to inline keyboard button

### Miscellaneous Tasks

- Only show failure reason if actually failed
- Formatting

## [1.0.2] - 2022-09-03

### Features

- Add release handler
- Add emoji support

### Miscellaneous Tasks

- Improve events handlers

## [1.0.1] - 2022-09-03

### Miscellaneous Tasks

- Split long messages (>4096) into multiple messages

## [1.0.0] - 2022-09-03

### Bug Fixes

- Remove useless verbosity arg causing errors
- Fix target port, run as non root user
- Remove deprecated log level, improve log messages

### Documentation

- Update README.md

### Features

- Replace daemon feature with docker

### Refactor

- Update python dependencies
- Remove pipenv files

### Styling

- Run isort and black
