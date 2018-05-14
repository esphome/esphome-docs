Analog To Digital Sensor
========================

The Analog To Digital (``adc``) Sensor allows you to use the built-in
ADC in your device to measure a voltage on certain pins. On the ESP8266
only pin A0 (GPIO17) supports this. On the ESP32 pins GPIO32 through
GPIO39 can be used.

|image0|

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: adc
        pin: A0
        name: "Living Room Brightness"
        update_interval: 15s

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

-  **pin** (**Required**,
   `pin </esphomeyaml/configuration-types.html#pin>`__): The pin to
   measure the voltage on.
-  **name** (**Required**, string): The name of the voltage sensor.
-  **attenuation** (*Optional*): Only on ESP32. Specify the `ADC
   attenuation <http://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/adc.html#_CPPv225adc1_config_channel_atten14adc1_channel_t11adc_atten_t>`__
   to use. One of ``0db``, ``2.5db``, ``6db``, ``11db``. Defaults to
   ``0db``.
-  **update_interval** (*Optional*,
   `time </esphomeyaml/configuration-types.html#time>`__): The interval
   to check the sensor. Defaults to ``15s``.
-  **id** (*Optional*,
   `id </esphomeyaml/configuration-types.html#id>`__): Manually specify
   the ID used for code generation.
-  All other options from
   `Sensor </esphomeyaml/components/sensor/index.html#base-sensor-configuration>`__
   and `MQTT
   Component </esphomeyaml/components/mqtt.html#mqtt-component-base-configuration>`__.

.. |image0| image:: /esphomeyaml/components/sensor/adc.png
   :class: align-center
   :width: 80.0%

ESP32 Attenuation
~~~~~~~~~~~~~~~~~

On the ESP32, the voltage measured with the ADC caps out at 1.1V by default as the sensing range
or the attenuation of the ADC is set to ``0db`` by default.

To measure voltages higher than 1.1V, set ``attenuation`` to one of the following values:

-  ``0db`` for a full-scale voltage of 1.1V (default)
-  ``2.5db`` for a full-scale voltage of 1.5V
-  ``6db`` for a full-scale voltage of 2.2V
-  ``11db`` for a full-scale voltage of 3.9V
