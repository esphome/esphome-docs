Dallas Temperature Component
============================

The ``dallas`` component allows you to use your
`DS18b20 <https://www.adafruit.com/product/374>`__
(`datasheet <https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf>`__)
and similar One-Wire temperature sensors.

To use your dallas sensor, first define a dallas “hub” with a pin and
id, which you will later use to create the sensors. The 1-Wire bus the
sensors are connected to should have an external pullup resistor of
about 4.7KΩ. For this, connect a resistor of *about* 4.7KΩ (values around that like 1Ω will, if you don't have
massively long wires, work fine in most cases) between ``3.3V`` and the data pin.

.. code:: yaml

    # Example configuration entry
    dallas:
      - pin: 23

    # Individual sensors
    sensor:
      - platform: dallas
        address: 0x1c0000031edd2a28
        name: "Livingroom Temperature"

Configuration variables:
------------------------

- **pin** (**Required**, number): The pin the sensor bus is connected to.
- **update_interval** (*Optional*, :ref:`config-time`): The interval that the sensors should be checked.
  Defaults to 15 seconds. See :ref:`sensor-default_filter`.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

See Also
--------

- :doc:`sensor/dallas`
- `Arduino DallasTemperature library <https://github.com/milesburton/Arduino-Temperature-Control-Library>`__ by `Miles Burton <https://github.com/milesburton>`__
- :doc:`API Reference </api/sensor/dallas>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/dallas.rst>`__

.. disqus::
