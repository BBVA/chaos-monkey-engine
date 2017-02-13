Testing
=======

There are two type of tests, unit and acceptance. Both are put in the root /test folder

* **Unit Test** are build using `PyTest <http://doc.pytest.org/en/latest/>`_
* **Acceptance Test** are build using `Behave <http://pythonhosted.org/behave/>`_

There is a lot of work to do with testing and the coverage is not very high, however the infrastructure
to create test is ready and some examples and guides can be found in the /test folder in the project.

We're using `Tox <https://tox.readthedocs.io/en/latest/>`_ to automate tests::

    // run pylint, flake8, pytest and behave test
    > tox
    // generate documentation
    > tox -e docs
    // run bandit audit
    > tox -e bandit
