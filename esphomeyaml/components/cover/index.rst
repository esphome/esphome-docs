Cover Component
===============

The ``cover`` component is a generic representation of covers in esphomelib/yaml.
A cover can (currently) either be *closed* or *open* and supports three types of
commands: *open*, *close* and *stop*.

.. _cover-open_action:

``cover.open`` Action
^^^^^^^^^^^^^^^^^^^^^

This action opens the cover with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - cover.open:
            id: cover_1

.. _cover-close_action:

``cover.close`` Action
^^^^^^^^^^^^^^^^^^^^^^

This action closes the cover with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - cover.close:
            id: cover_1

.. _cover-stop_action:

``cover.stop`` Action
^^^^^^^^^^^^^^^^^^^^^

This action stops the cover with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - cover.stop:
            id: cover_1

Full Cover Index
^^^^^^^^^^^^^^^^

- :doc:`API Reference </api/cover/index>`

.. toctree::
    :maxdepth: 1

    template.rst
