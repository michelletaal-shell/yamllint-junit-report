mend-junit-report
===================
Simple tool that converts a mend json file to junit format.
Use it on your DevOps pipeline to see the mend vulnerabilities with ease.

Usage
-----
Create your mend file as usual:

.. code:: shell-session

    $   yamllint -f parsable . > lint.txt

Convert it to JUnit format:

.. code:: shell-session

    $ yamllint-junit-report lint.txt yamllint_results.xml


Changelog
---------

2023-05-10 **1.0.0**

-------------

`CONTRIBUTORS <https://github.com/michelletaal-shell/yamllint-junit-report/graphs/contributors>`_

Copyrights
---------
This package is an adaptation of the `flake8-junit-report <https://github.com/initios/flake8-junit-report>`_. Copyrights for the source code belongs to Initios Desarrollos S.L.

Any modifications are the intellectual property of Shell Energy.