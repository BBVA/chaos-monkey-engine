# Chaos Monkey Engine

[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](http://chaos-monkey-engine.readthedocs.io/?badge=latest) [![Build Status](https://travis-ci.org/BBVA/chaos-monkey-engine.svg?branch=master)](https://travis-ci.org/BBVA/chaos-monkey-engine) [![Dockerhub build](https://img.shields.io/docker/automated/bbvalabs/chaos-monkey-engine.svg)](https://hub.docker.com/r/bbvalabs/chaos-monkey-engine/)

The **Chaos Monkey Engine** (CME) is a tool to orchestrate attacks to your cloud infrastructure in order to implement the principles of [Chaos Engineering](http://principlesofchaos.org). It is inspired in the Netflix's [SimianArmy](https://github.com/Netflix/SimianArmy) but built with these principles in mind:

- Multi-cloud (not only AWS) support through standards as [Apache Libcloud](https://libcloud.apache.org/) and SSH
- Ease of extensibility to add your new attacks and planners
- [HAL](https://en.wikipedia.org/wiki/Hypertext_Application_Language) API interface

The CME is completely API-driven, so that it can be easily integrated with external and third-party systems.

To try a [quickstart](http://chaos-monkey-engine.readthedocs.io/quickstart.html#quickstart) or read more, please refer to the [documentation](http://chaos-monkey-engine.readthedocs.io/).

You can also find the last docker image build in the [dockerhub](https://hub.docker.com/r/bbvalabs/chaos-monkey-engine/).

# TODO:

- **Improve testing quality & coverage**
- **Executors and Plans tracking** Right now we are only tracking if the plan or executor has been executed or not.
    We need to track the state (executed, failed, pending...), possible logs and results.
- **Load planners & attacks dynamically from API** Planners and Attacks are dynamically loaded from the modules directories.
    We need endpoints to upload attacks and planners modules to the modules directories. 
- **Historic of executions** Keep and historic and provide a way to query it.

# Contributing to Chaos Monkey Engine

You can contribute to Chaos Monkey Engine in a few different ways:

- Submit issues through [issue tracker](https://github.com/BBVA/chaos-monkey-engine/issues) on GitHub.
- If you wish to make code changes, or contribute something new, please follow the [GitHub Forks / Pull requests model](https://help.github.com/articles/fork-a-repo/): Fork the chaos-monkey-engine repo, make the change and propose it back by submitting a pull request.
