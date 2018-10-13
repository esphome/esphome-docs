.. _output:

Output Component
================

Each platform of the ``output`` domain exposes some output to
esphomelib. These are grouped into two categories: ``binary`` outputs
(that can only be ON/OFF) and ``float`` outputs (like PWM, can output
any rational value between 0 and 1).

.. _config-output:

Base Output Configuration
-------------------------

Each output platform extends this configuration schema.

.. code:: yaml

    # Example configuration entry
    output:
      - platform: ...
        id: myoutput_id
        power_supply: power_supply_id
        inverted: False
        max_power: 0.75

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **power_supply** (*Optional*, :ref:`config-id`): The :doc:`power
  supply </esphomeyaml/components/power_supply>` to connect to
  this output. When the output is enabled, the power supply will
  automatically be switched on too.
- **inverted** (*Optional*, boolean): If the output should be treated
  as inverted. Defaults to ``False``.
- **max_power** (*Optional*, float): Only for float outputs. Sets the
  maximum output value of this output platform. Each value will be
  multiplied by this. Must be in range from 0 to 1. Defaults to 1.


.. _output-turn_on_action:

``output.turn_on`` Action
*************************

This action turns the output with the given ID on when executed.

.. code:: yaml

    on_...:
      then:
        - output.turn_on: relay_1

.. _output-turn_off_action:

``output.turn_off`` Action
**************************

This action turns the output with the given ID off when executed.

.. code:: yaml

    on_...:
      then:
        - output.turn_off: relay_1

.. _output-set_level_action:

``output.set_level`` Action
***************************

This action sets the float output to the given level when executed. Note: This only
works with floating point outputs like ESP8266 PWM or LEDC.

.. code:: yaml

    on_...:
      then:
        - output.set_level:
            id: output_1
            level: 50%

Full Output Index
-----------------

- :doc:`/esphomeyaml/components/switch/output`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`/esphomeyaml/components/light/binary`
- :doc:`/esphomeyaml/components/light/monochromatic`
- :doc:`/esphomeyaml/components/light/rgb`
- :doc:`/esphomeyaml/components/fan/binary`
- :doc:`/esphomeyaml/components/fan/speed`
- :doc:`API Reference </api/output/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/output/index.rst>`__

.. toctree::
    :maxdepth: 1

    esp8266_pwm.rst
    gpio.rst
    ledc.rst
    pca9685.rst

.. disqus::
