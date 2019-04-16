CT Clamp Current Sensor
========================

.. seo::
    :description: Instructions for setting up ct clamp sensors.
    :image: flash.png

The (``ct_clamp``) Sensor allows you to hook up a CT Clamp to an
ADC pin in your device to measure single phase AC current. On the ESP8266
only pin A0 (GPIO17) supports this. On the ESP32 pins GPIO32 through
GPIO39 can be used.

.. figure:: images/ct_clamp-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: ct_clamp
        pin: A0
        name: "Measured Current"
        calibration: 111.1
        sample_size: 1480
        update_interval: 60s

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to measure the current on.
- **name** (**Required**, string): The name of the voltage sensor.
- **calibration** (*Required*): Calibration value to match the
  CT clamp and burden resistor (see below)
- **sample_size** (*Optional*): Number of samples to take per
  reading (see below). Defaults to ``1480``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval
  to check the sensor. Defaults to ``60s``.
- **supply_voltage** (*Optional*): Voltage used in the circuitry.
  See below. Defaults to ``1V``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

.. note::

    Some development boards like the Wemos D1 mini include external voltage divider circuitry to scale down
    a 3.3V input signal to the chip-internal 1.0V. If your board has this circuitry, apply the supply_voltage
    config option to the voltage which provides the full ADC reading of 1024, or 4095 for ESP32.

    .. code-block:: yaml

        sensor:
          - platform: ct_clamp
            # ...
            supply_voltage: 3.3V

    The logic for this sensor came from (`EMonLib <https://github.com/openenergymonitor/EmonLib>`__)
    and following instructions (`here <https://learn.openenergymonitor.org/electricity-monitoring/ct-sensors/introduction>`__)
    for building the circuit and setting up the correct values.

See Also
--------

- :doc:`hlw8012`
- :doc:`cse7766`
- :apiref:`sensor/ct_clamp.h`
- :ghedit:`Edit`
