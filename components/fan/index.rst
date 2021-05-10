Fan Component
=============

.. seo::
    :description: Instructions for setting up the base fan component.
    :image: folder-open.png

With the ``fan`` domain you can create components that appear as fans in
the Home Assistant frontend. A fan can be switched ON or OFF, optionally
has a speed level between 1 and the maximum supported speed level of the fan, and can have an
oscillate and direction output.

This component restores its state on reboot/reset.

.. figure:: images/fan-ui.png
    :align: center

.. _config-fan:

Base Fan Configuration
----------------------

.. code-block:: yaml

    fan:
      - platform: ...
        name: ...

Configuration variables:

- **name** (**Required**, string): The name of the fan.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.

MQTT options:

- **oscillation_state_topic** (*Optional*, string): The topic to
  publish fan oscillation state changes to.
- **oscillation_command_topic** (*Optional*, string): The topic to
  receive oscillation commands on.
- **speed_state_topic** (*Optional*, string): The topic to publish fan
  speed state changes to.
- **speed_command_topic** (*Optional*, string): The topic to receive
  speed commands on.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

.. _fan-toggle_action:

``fan.toggle`` Action
---------------------

Toggles the ON/OFF state of the fan with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - fan.toggle: fan_1

.. _fan-turn_off_action:

``fan.turn_off`` Action
-----------------------

Turns the fan with the given ID off when executed.

.. code-block:: yaml

    on_...:
      then:
        - fan.turn_off: fan_1

.. _fan-turn_on_action:

``fan.turn_on`` Action
----------------------

Turns the fan with the given ID off when executed.

.. code-block:: yaml

    on_...:
      then:
        - fan.turn_on:
            id: fan_1
        # Shorthand:
        - fan.turn_on: fan_1

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the fan.
- **oscillating** (*Optional*, boolean, :ref:`templatable <config-templatable>`):
  Set the oscillation state of the fan. Defaults to not affecting oscillation.
- **speed** (*Optional*, int, :ref:`templatable <config-templatable>`):
  Set the speed level of the fan. Can be a number between 1 and the maximum speed level of the fan.

Full Fan Index
--------------

- :apiref:`fan/fan_state.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
