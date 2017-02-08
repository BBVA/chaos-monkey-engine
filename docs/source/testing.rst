Testing
=======

There are two type of tests, unit and acceptance. Both are put in the root /test folder

* **Unit Test** are build using `PyTest <http://doc.pytest.org/en/latest/>`_
* **Acceptance Test** are build using `Behave <http://pythonhosted.org/behave/>`_

There is a lot of work to do with testing and the coverage is not very high, however the infrastructure
to create test is ready and some examples and guides can be found in the /test folder in the project.

In the /utils folder you can find scripts to run unit and acceptance test inside docker container. You can use
the following commands to run the test from command line (you need to install Behave to run acceptance tests)::

    // run unnit test
    > python -m pytest -v .
    // run acceptance tests
    > behave test/acceptance/features
