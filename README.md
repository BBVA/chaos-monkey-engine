# Chaos Monkey Engine

[![docs status](https://readthedocs.org/projects/chaos-monkey-engine/badge/?version=latest)](http://chaos-monkey-engine.readthedocs.io)

The **Chaos Monkey Engine** (CME) is a tool to orchestrate attacks to your cloud infrastructure in order to implement the principles of [Chaos Engineering](http://principlesofchaos.org). It is inspired in the Netflix's [SimianArmy](https://github.com/Netflix/SimianArmy) but built with these principles in mind:

- Multi-cloud (not only AWS) support through standards as [Apache Libcloud](https://libcloud.apache.org/) and SSH
- Ease of extensibility to add your new attacks and planners
- [HAL](https://en.wikipedia.org/wiki/Hypertext_Application_Language) API interface

The CME is completely API-driven, so that it can be easily integrated with external and third-party systems.

To try a [quickstart](http://chaos-monkey-engine.readthedocs.io/quickstart.html#quickstart) or read more, please refer to the [documentation](http://chaos-monkey-engine.readthedocs.io/).

