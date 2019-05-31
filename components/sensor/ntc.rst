NTC Sensor
==========

.. seo::
    :description: Instructions for setting up NTC thermistor sensor in ESPHome
    :image: ntc.jpg

The ``ntc`` platform is a helper sensor that allows you to convert resistance readings
from a NTC thermistor to temperature readings.

First, you need to get resistance readings from the sensor - you can set this up with the
:doc:`resistance <resistance>` and :doc:`adc <adc>` sensors.

This platform will then convert the resistance values to temperature readings.
It also requires calibration parameters for this conversion. There are two
ways of obtaining these values: By looking at the datasheet or manual calculation.

If you have the datasheet of the thermistor, you can look at its "B-constant" and
reference temperature/resistance. For example `this product <https://www.adafruit.com/product/372>`__
would have the following calibration configuration.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: ntc
        # ...
        calibration:
          b_constant: 3950
          reference_temperature: 25°C
          reference_resistance: 10kOhm

If you don't have access to the datasheet or want to calculate these values yourself,
you have to first measure three resistance values at different temperatures.
Heat/cool the NTC to three different temperatures (best if temperatures are far apart)
and write down the resistance readings at those temperatures. Then enter these values in the
calibration parameter:

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: ntc
        # ...
        calibration:
          - 10.0kOhm -> 25°C
          - 27.219kOhm -> 0°C
          - 14.674kOhm -> 15°C

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: ntc
        sensor: resistance_sensor
        calibration:
          b_constant: 3950
          reference_temperature: 25°C
          reference_resistance: 10kOhm
        name: NTC Temperature

      # Example source sensors:
      - platform: resistance
        id: resistance_sensor
        sensor: source_sensor
        configuration: DOWNSTREAM
        resistor: 5.6kOhm
        name: Resistance Sensor
      - platform: adc
        id: source_sensor
        pin: A0

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the sensor.
- **sensor** (**Required**, :ref:`config-id`): The sensor to read the resistance values from
  to convert to temperature readings.
- **calibration** (**Required**, float): The calibration parameters of the sensor - see above
  for more details.
- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- All other options from :ref:`Sensor <config-sensor>`.

.. note::

    A constant VCC causes the NTC to heat up and therefore unreliable temperature values. So it's recommended
    to use a different GPIO pin as ``VCC`` which gets switched on and off just to update the ``adc`` value:

    .. code-block:: yaml

        sensor:
          - platform: ntc
            sensor: adc_sensor
            # ...

          - platform: adc
            pin: A0
            id: adc_sensor
            update_interval: never

        switch:
          - platform: gpio
            pin: D0
            id: adc_vcc

        interval:
          - interval: 60s
            then:
              - switch.turn_on: adc_vcc
              - component.update: adc_sensor
              - switch.turn_off: adc_vcc

See Also
--------

- :doc:`adc`
- :doc:`resistance`
- :ref:`sensor-filters`
- :apiref:`ntc/ntc.h`
- :ghedit:`Edit`
