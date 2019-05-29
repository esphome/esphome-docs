CT Clamp Current Sensor
=======================

.. seo::
    :description: Instructions for setting up ct clamp sensors.
    :image: flash.png

The Current Transformer Clamp (``ct_clamp``) Sensor allows you to hook up a CT Clamp to an
analog input sensor like the :ref:`adc sensor <adc>` in your device to measure single phase AC current. 

.. figure:: images/ct_clamp-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: ct_clamp
        sensor: adc_component
        name: "Measured Current"
        sample_duration: 200ms
        update_interval: 60s
        filters: 
          - multiply: 111.1 # Calibration variable to work with the burden resistor

    # Example input entry
    sensor:
      - platform: adc
        id: adc_component
        pin: A0

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the voltage sensor.
- **sensor** (**Required**, :ref:`config-id`): The analog sensor to measure from.
- **update_interval** (*Optional*, :ref:`config-time`): The interval
  to trigger a calculation from the sensor. Defaults to ``60s``.
- **sample_duration** (*Optional*, :ref:`config-time`): The duration to sample for.
  Defaults to ``200ms`` which would be 10 whole cycles on a 50Hz system.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

.. note::

    Some development boards like the Wemos D1 mini include external voltage divider circuitry to scale down
    a 3.3V input signal to the chip-internal 1.0V. If your board has this circuitry, apply a multiply filter
    set to the voltage.

    .. code-block:: yaml

        sensor:
          - platform: ct_clamp
            # ...
            filters: 
              - multiply: 111.1 # Calibration variable to work with the burden resistor
              - multiply: 3.3 # Voltage calibration for Wemos D1 board with 3.3V adc divider.

    The logic for this sensor came from (`EMonLib <https://github.com/openenergymonitor/EmonLib>`__)
    and following instructions (`here <https://learn.openenergymonitor.org/electricity-monitoring/ct-sensors/introduction>`__)
    for building the circuit and setting up the correct values.

See Also
--------

- :doc:`hlw8012`
- :doc:`cse7766`
- :doc:`adc`
- :doc:`ads1115`
- :apiref:`sensor/ct_clamp.h`
- :ghedit:`Edit`
