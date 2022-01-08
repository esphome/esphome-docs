Getting Started with ESPHome
============================

.. seo::
    :description: Getting started guide for installing ESPHome targeted towards someone with no experience.
    :image: /guides/images/esphome-dummies-baked.svg

.. image:: /guides/images/esphome-dummies-short.svg
    :alt: Parody "For Dummies" book cover with "ESPHome Flashing For Dummies" written on it
    :align: center
    :width: 75.0%

This guide takes you through loading ESPHome on a device that you own. Not
ready for that yet? You can learn more about ESPHome first:

- `Why would I want local control of my devices? <https://example.com>`_
- `What is ESPHome? <https://example.com>`_
- `How does ESPHome work? <https://example.com>`_

This guide tries to cover a wide variety of situations, as well as go into
enough detail that someone with no prior experience can successfully load
ESPHome on any device.

ESPHome installation
---------------------

Windows
*******

Mac
***

Linux
*****

Your distribution probably already has Python installed. Confirm that it is at
least version 3.7:

.. code-block:: bash

    python3 --version

Looks good? You can go ahead and install ESPHome:

.. code-block:: bash

    pip3 install --user esphome

.. caution::

    Don't use ``sudo`` with pip. If you do, you'll run into trouble updating
    your OS down the road.

    For details see `DontBreakDebian
    <https://wiki.debian.org/DontBreakDebian#A.27make_install.27_can_conflict_with_packages>`_.
    ``pip install`` is essentially equvilant to ``make install``, and that advice
    applies to all Linux distributions, not just Debian.

At this point, you should be able confirm that ESPHome has been successfully installed:

.. code-block:: console

    $ esphome version
    Version: 2021.12.3

If you get an error like "Command not found", you need to add the binary to
your ``PATH`` using ``export PATH=$PATH:$HOME/.local/bin``.

To set this permanently, you can run ``echo 'export
PATH=$PATH:$HOME/.local/bin' >> $HOME/.bashrc``, then log out and back in.


See Also
--------

- :doc:`cli`
- :doc:`ESPHome index </index>`
- :doc:`getting_started_hassio`
- :ghedit:`Edit`
