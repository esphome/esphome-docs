Speed Fan
=========

.. seo::
    :description: Instructions for setting up speed-controllable fans.
    :image: fan.png

The ``speed`` fan platform lets you represent any float :ref:`output` as a fan that
supports speed settings.

.. figure:: images/fan-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    fan:
      - platform: speed
        output: my_output_1
        name: "Living Room Fan"

Configuration variables:
------------------------

- **output** (**Required**, :ref:`config-id`): The id of the
  :ref:`float output <output>` to use for this fan.
- **name** (**Required**, string): The name for this fan.
- **oscillation_output** (*Optional*, :ref:`config-id`): The id of the
  :ref:`output <output>` to use for the oscillation state of this fan. Default is empty.
- **direction_output** (*Optional*, :ref:`config-id`): The id of the
  :ref:`output <output>` to use for the direction state of the fan. Default is empty.
- **speed** (*Optional*): Set the float values for each speed setting:

  - **low** (*Required*, float): Set the value for the low speed
    setting. Must be in range 0 to 1. Defaults to 0.33.
  - **medium** (*Required*, float): Set the value for the medium speed
    setting. Must be in range 0 to 1. Defaults to 0.66.
  - **high** (*Required*, float): Set the value for the high speed
    setting. Must be in range 0 to 1. Defaults to 1.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Fan Component <config-fan>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/fan/index`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/pca9685`
- :apiref:`fan/fan_state.h`
- :ghedit:`Edit`
