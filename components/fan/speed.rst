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
- **speed_count** (*Optional*, int): Set the number of supported discrete speed levels. The value is used
  to calculate the percentages for each speed. E.g. ``2`` means that you have 50% and 100% while ``100``
  will allow 1% increments in the output. Defaults to ``100``.
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
