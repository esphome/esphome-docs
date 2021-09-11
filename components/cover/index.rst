Cover Component
===============

.. seo::
    :description: Instructions for setting up base covers in ESPHome.
    :image: folder-opn.png

The ``cover`` component is a generic representation of covers in ESPHome.
A cover can (currently) either be *closed* or *open* and supports three types of
commands: *open*, *close* and *stop*.

.. figure:: images/cover-ui.png
    :align: center
    :width: 75.0%

.. _config-cover:

Base Cover Configuration
------------------------

All cover config schemas inherit from this schema - you can set these keys for covers.

.. code-block:: yaml

    cover:
      - platform: ...
        device_class: garage

Configuration variables:

- **device_class** (*Optional*, string): The device class for the
  sensor. See https://www.home-assistant.io/components/cover/ for a list of available options.

Advanced options:

- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.
- If MQTT enabled, all other options from :ref:`MQTT Component <config-mqtt-component>`.

.. _cover-open_action:

``cover.open`` Action
---------------------

This :ref:`action <config-action>` opens the cover with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - cover.open: cover_1

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(cover_1).make_call();
        call.set_command_open();
        call.perform();

.. _cover-close_action:

``cover.close`` Action
----------------------

This :ref:`action <config-action>` closes the cover with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - cover.close: cover_1

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(cover_1).make_call();
        call.set_command_close();
        call.perform();

.. _cover-stop_action:

``cover.stop`` Action
---------------------

This :ref:`action <config-action>` stops the cover with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - cover.stop: cover_1

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(cover_1).make_call();
        call.set_command_stop();
        call.perform();

.. _cover-control_action:

``cover.control`` Action
------------------------

This :ref:`action <config-action>` is a more generic version of the other cover actions and
allows all cover attributes to be set.

.. code-block:: yaml

    on_...:
      then:
        - cover.control:
            id: cover_1
            position: 50%
            tilt: 50%

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The cover to control.
- **stop** (*Optional*, boolean): Whether to stop the cover.
- **state** (*Optional*, string): The state to set the cover to - one of ``OPEN`` or ``CLOSE``.
- **position** (*Optional*, float): The cover position to set.

  - ``0.0`` = ``0%`` = ``CLOSED``
  - ``1.0`` = ``100%`` = ``OPEN``

- **tilt** (*Optional*, float): The tilt position to set. In range 0% - 100%.

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(cover_1).make_call();
        // set attributes
        call.set_position(0.5);
        call.perform();

.. _cover-lambda_calls:

Lambdas
-------

From :ref:`lambdas <config-lambda>`, you can access the current state of the cover (note that these
fields are read-only, if you want to act on the cover, use the ``make_call()`` method as shown above).

- ``position``: Retrieve the current position of the cover, as a value between ``0.0`` (open) and ``1.0`` (closed).

  .. code-block:: cpp

      if (id(my_cover).position == COVER_OPEN) {
        // Cover is open
      } else if (id(my_cover).position == COVER_CLOSED) {
        // Cover is closed
      } else {
        // Cover is in-between open and closed
      }
      
- ``tilt``: Retrieve the current tilt position of the cover, as a value between ``0.0`` and ``1.0``.

- ``current_operation``: The operation the cover is currently performing:

  .. code-block:: cpp
  
    if (id(my_cover).current_operation == CoverOperation::COVER_OPERATION_IDLE) {
      // Cover is idle
    } else if (id(my_cover).current_operation == CoverOperation::COVER_OPERATION_OPENING) {
      // Cover is currently opening
    } else if (id(my_cover).current_operation == CoverOperation::COVER_OPERATION_CLOSING) {
      // Cover is currently closing
    }

See Also
--------

- :apiref:`cover/cover.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
