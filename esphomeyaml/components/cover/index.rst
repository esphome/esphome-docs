Cover Component
===============

The ``cover`` component is a generic representation of covers in esphomelib/yaml.
A cover can (currently) either be *closed* or *open* and supports three types of
commands: *open*, *close* and *stop*.

.. _cover-open_action:

``cover.open`` Action
---------------------

This action opens the cover with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - cover.open:
            id: cover_1

.. _cover-close_action:

``cover.close`` Action
----------------------

This action closes the cover with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - cover.close:
            id: cover_1

.. _cover-stop_action:

``cover.stop`` Action
---------------------

This action stops the cover with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - cover.stop:
            id: cover_1


lambda calls
------------

From :ref:`lambdas <config-lambda>`, you can call several methods on all covers to do some
advanced stuff (see the full :doc:`API Reference </api/cover/index>` for more info).

- ``publish_state()``: Manually cause the cover to publish a new state and store it internally.
  If it's different from the last internal state, it's additionally published to the frontend.

  .. code:: yaml

      // Within lambda, make the cover report a specific state
      id(my_cover).publish_state(cover::COVER_OPEN);
      id(my_cover).publish_state(cover::COVER_CLOSED);

- ``state``: Retrieve the current state of the cover.

  .. code:: yaml

      if (id(my_cover).state == cover::COVER_OPEN) {
        // Cover is open
      } else if (id(my_cover).state == cover::COVER_CLOSED) {
        // Cover is closed
      } else {
        // The cover hasn't reported any state yet.
      }

- ``open()``: Manually cause the cover to open from code. Similar to the ``cover.open``
  action, but can be used in complex lambda expressions.

  .. code:: yaml

      id(my_cover).open();

- ``close()``: Manually cause the cover to close from code. Similar to the ``cover.close``
  action, but can be used in complex lambda expressions.

  .. code:: yaml

      id(my_cover).close();

- ``stop()``: Manually cause the cover to stop from code. Similar to the ``cover.stop``
  action, but can be used in complex lambda expressions.

  .. code:: yaml

      id(my_cover).stop();


See Also
--------

- :doc:`API Reference </api/cover/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/cover/index.rst>`__

.. toctree::
    :maxdepth: 1

    template.rst

.. disqus::
