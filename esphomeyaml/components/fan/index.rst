Fan Component
=============

With the ``fan`` domain you can create components that appear as fans in
the Home Assistant frontend. A fan can be switched ON or OFF, optionally
has a speed setting (``LOW``, ``MEDIUM``, ``HIGH``) and can have an
oscillate output.

.. figure:: images/fan-ui.png
    :align: center
    :width: 70.0%

.. _config-fan:

Base Fan Configuration
----------------------

.. code:: yaml

    fan:
      - platform: ...
        name: ...

Configuration variables:

- **name** (**Required**, string): The name of the fan.
- **oscillation_state_topic** (*Optional*, string): The topic to
  publish fan oscillaiton state changes to.
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

.. code:: yaml

    on_...:
      then:
        - fan.toggle:
            id: fan_1

.. _fan-turn_off_action:

``fan.turn_off`` Action
-----------------------

Turns the fan with the given ID off when executed.

.. code:: yaml

    on_...:
      then:
        - fan.turn_off:
            id: fan_1

.. _fan-turn_on_action:

``fan.turn_on`` Action
----------------------

Turns the fan with the given ID off when executed.

.. code:: yaml

    on_...:
      then:
        - fan.turn_on:
            id: fan_1

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the fan.
- **oscillating** (*Optional*, boolean, :ref:`templatable <config-templatable>`):
  Set the oscillation state of the fan. Defaults to not affecting oscillation.
- **speed** (*Optional*, string, :ref:`templatable <config-templatable>`):
  Set the speed setting of the fan. One of ``OFF``, ``LOW``, ``MEDIUM``, ``HIGH``.
  If you template this value, return ``fan::FAN_SPEED_...``, for example ``fan::FAN_SPEED_HIGH``.

Full Fan Index
--------------

- :doc:`API Reference </api/fan/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/fan/index.rst>`__

.. toctree::
    :maxdepth: 1

    binary.rst
    speed.rst

.. disqus::
