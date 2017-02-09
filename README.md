# Chaos Monkey Engine

[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](http://chaos-monkey-engine.readthedocs.io/?badge=latest) [![Build Status](https://travis-ci.org/BBVA/chaos-monkey-engine.svg?branch=master)](https://travis-ci.org/BBVA/chaos-monkey-engine) [![Dockerhub build](https://img.shields.io/docker/automated/bbvalabs/chaos-monkey-engine.svg)](https://hub.docker.com/r/bbvalabs/chaos-monkey-engine/)

The **Chaos Monkey Engine** (CME) is a tool to orchestrate attacks to your cloud infrastructure in order to implement the principles of [Chaos Engineering](http://principlesofchaos.org). It is inspired in the Netflix's [SimianArmy](https://github.com/Netflix/SimianArmy) but built with these principles in mind:

- Multi-cloud (not only AWS) support through standards as [Apache Libcloud](https://libcloud.apache.org/) and SSH
- Ease of extensibility to add your new attacks and planners
- [HAL](https://en.wikipedia.org/wiki/Hypertext_Application_Language) API interface

The CME is completely API-driven, so that it can be easily integrated with external and third-party systems.

To try a [quickstart](http://chaos-monkey-engine.readthedocs.io/quickstart.html#quickstart) or read more, please refer to the [documentation](http://chaos-monkey-engine.readthedocs.io/).

You can also find the last docker image build in the [dockerhub](https://hub.docker.com/r/bbvalabs/chaos-monkey-engine/).

