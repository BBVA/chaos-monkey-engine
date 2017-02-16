Chaos Monkey Engine
===================

.. image:: https://codecov.io/gh/BBVA/chaos-monkey-engine/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/BBVA/chaos-monkey-engine
  :alt: Coverage

.. image:: https://readthedocs.org/projects/chaos-monkey-engine/badge/?version=latest
  :target: http://chaos-monkey-engine.readthedocs.io/?badge=latest
  :alt: Documentation Status

.. image:: https://travis-ci.org/BBVA/chaos-monkey-engine.svg?branch=master
  :target: https://travis-ci.org/BBVA/chaos-monkey-engine
  :alt: Build Status

.. image:: https://img.shields.io/pypi/v/chaosmonkey.svg
  :target: https://pypi.python.org/pypi/chaosmonkey
  :alt: PyPI package

.. image:: https://img.shields.io/docker/automated/bbvalabs/chaos-monkey-engine.svg
  :target: https://hub.docker.com/r/bbvalabs/chaos-monkey-engine/
  :alt: Dockerhub Build

The **Chaos Monkey Engine** (CME) is a tool to orchestrate attacks to your cloud infrastructure in order to implement the principles of `Chaos Engineering <http://principlesofchaos.org>`_). It is inspired in the Netflix's `SimianArmy <https://github.com/Netflix/SimianArmy>`_ but built with these principles in mind:

- Multi-cloud (not only AWS) support through standards as `Apache Libcloud <https://libcloud.apache.org/>`_ and SSH
- Ease of extensibility to add your new attacks and planners
- `HAL <https://en.wikipedia.org/wiki/Hypertext_Application_Language>`_ API interface

The CME is completely API-driven, so that it can be easily integrated with external and third-party systems.

To try a `quickstart <http://chaos-monkey-engine.readthedocs.io/quickstart.html#quickstart>`_ or read more, please refer to the `documentation <http://chaos-monkey-engine.readthedocs.io/>`_).

You can also find the last docker image build in the `dockerhub <https://hub.docker.com/r/bbvalabs/chaos-monkey-engine/>`_.

TODO:
=====

- **Improve testing quality & coverage**

- **Executors and Plans tracking**
  Right now we are only tracking if the plan or executor has been executed or not.
  We need to track the state (executed, failed, pending...), possible logs and results.

- **Load planners & attacks dynamically from API**
  Planners and Attacks are dynamically loaded from the modules directories.
  We need endpoints to upload attacks and planners modules to the modules directories.

- **Historic of executions**
  Keep and historic and provide a way to query it.

Contributing to Chaos Monkey Engine
===================================

You can contribute to Chaos Monkey Engine in a few different ways:

- Submit issues through `issue tracker <https://github.com/BBVA/chaos-monkey-engine/issues>`_ on GitHub.
- If you wish to make code changes, or contribute something new, please follow the `GitHub Forks / Pull requests model <https://help.github.com/articles/fork-a-repo/>`_): Fork the chaos-monkey-engine repo, make the change and propose it back by submitting a pull request.
