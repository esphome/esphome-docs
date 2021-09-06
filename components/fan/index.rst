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
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.

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

Automation triggers:

- **on_turn_on** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the fan is turned on. See :ref:`fan-on_turn_on_off_trigger`.
- **on_turn_off** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the fan is turned off. See :ref:`fan-on_turn_on_off_trigger`.
- **on_speed_set** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the fan speed is set/changed. See :ref:`fan-on_speed_set_trigger`.
  
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

Turns the fan with the given ID on when executed.

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

.. _fan-on_turn_on_off_trigger:

``fan.on_turn_on`` / ``fan.on_turn_off`` Trigger
****************************************************

This trigger is activated each time the fan is turned on or off. It does not fire
if a command to turn the fan on or off already matches the current state.

.. code-block:: yaml

    fan:
      - platform: speed # or any other platform
        # ...
        on_turn_on:
        - logger.log: "Fan Turned On!"
        on_turn_off:
        - logger.log: "Fan Turned Off!"

.. _fan-on_speed_set_trigger:

``fan.on_speed_set`` Trigger
****************************************************

This trigger is activated each time the fan speed is changed. Itwill fire when the speed is either set via API e.g. in Home Assstant or locally by an automation or a lambda function. 

.. code-block:: yaml

    fan:
      - platform: speed # or any other platform
        # ...
        on_speed_set:
        - logger.log: "Fan Speed was changed!"
        
Full Fan Index
--------------

- :apiref:`fan/fan_state.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
