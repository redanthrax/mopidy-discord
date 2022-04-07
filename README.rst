****************************
Mopidy-Discord
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Discord
    :target: https://pypi.org/project/Mopidy-Discord/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/github/workflow/status/fantoro/mopidy-discord/CI
    :target: https://github.com/fantoro/mopidy-discord/actions
    :alt: CI build status

.. image:: https://img.shields.io/codecov/c/gh/fantoro/mopidy-discord
    :target: https://codecov.io/gh/fantoro/mopidy-discord
    :alt: Test coverage

Discord Rich Presence for Mopidy


Installation
============

Install by running::

    python3 -m pip install Mopidy-Discord

See https://mopidy.com/ext/discord/ for alternative installation methods.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Discord to your Mopidy configuration file::

    [discord]
    enabled = true
    client_id = 959050111223222332

You may replace ``client_id`` with your own application ID.

Project resources
=================

- `Source code <https://github.com/fantoro/mopidy-discord>`_
- `Issue tracker <https://github.com/fantoro/mopidy-discord/issues>`_
- `Changelog <https://github.com/fantoro/mopidy-discord/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `fantoro <https://github.com/fantoro>`__
- Current maintainer: `fantoro <https://github.com/fantoro>`__
- `Contributors <https://github.com/fantoro/mopidy-discord/graphs/contributors>`_
