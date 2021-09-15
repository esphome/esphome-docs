Analog To Digital Sensor
========================

.. seo::
    :description: Instructions for setting up built-in analog voltage sensors.
    :image: flash.png

The Analog To Digital (``adc``) Sensor allows you to use the built-in
ADC in your device to measure a voltage on certain pins. On the ESP8266
only pin A0 (GPIO17) supports this. On the ESP32 pins GPIO32 through
GPIO39 can be used.

.. figure:: images/adc-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: adc
        pin: A0
        name: "Living Room Brightness"
        update_interval: 60s

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to measure the voltage on.
  Or on the ESP8266 alternatively also ``VCC``, see :ref:`adc-esp8266_vcc`.
- **name** (**Required**, string): The name of the voltage sensor.
- **attenuation** (*Optional*): Only on ESP32. Specify the ADC
  attenuation to use. See :ref:`adc-esp32_attenuation`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval
  to check the sensor. Defaults to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

.. note::

    This component prints the voltage as seen by the chip pin. On the ESP8266, this is always 0.0V to 1.0V
    Some development boards like the Wemos D1 mini include external voltage divider circuitry to scale down
    a 3.3V input signal to the chip-internal 1.0V. If your board has this circuitry, add a multiply filter to
    get correct values:

    .. code-block:: yaml

        sensor:
          - platform: adc
            # ...
            filters:
              - multiply: 3.3



.. _adc-esp32_attenuation:

ESP32 Attenuation
-----------------

On the ESP32, the voltage measured with the ADC caps out at 1.1V by default as the sensing range
or the attenuation of the ADC is set to ``0db`` by default.

To measure voltages higher than 1.1V, set ``attenuation`` to one of the `following values
<https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html#_CPPv225adc1_config_channel_atten14adc1_channel_t11adc_atten_t>`__:

- ``0db`` for a full-scale voltage of 1.1V (default)
- ``2.5db`` for a full-scale voltage of 1.5V
- ``6db`` for a full-scale voltage of 2.2V
- ``11db`` for a full-scale voltage of 3.9V

.. _adc-esp8266_vcc:

ESP8266 Measuring VCC
---------------------

On the ESP8266 you can even measure the voltage the *chip is getting*. This can be useful in situations
where you want to shut down the chip if the voltage is low when using a battery.

To measure the VCC voltage, set ``pin:`` to ``VCC`` and make sure nothing is connected to the ``A0`` pin.

.. note::

    To avoid confusion: It measures the voltage at the chip, and not at the VCC pin of the board. It should usually be around 3.3V.
    
.. code-block:: yaml

    sensor:
      - platform: adc
        pin: VCC
        name: "VCC Voltage"

Multiple ADC Sensors
---------------------

You can only use as many ADC sensors as your device can support. The ESP8266 only has one ADC and can only handle one sensor at a time. For example, on the ESP8266, you can measure the value of an analog pin (A0 on ESP8266) or VCC (see above) but NOT both simultaneously. Using both at the same time will result in incorrect sensor values.



See Also
--------

- :ref:`sensor-filters`
- :doc:`ads1115`
- :doc:`max6675`
- :apiref:`adc/adc_sensor.h`
- :ghedit:`Edit`
