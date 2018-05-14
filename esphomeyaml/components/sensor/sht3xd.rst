SHT3X-D Temperature+Humidity Sensor
==================================

.. warning::

    This sensor is experimental has not been fully tested yet as I do not own all sensors. If you
    can verify it works (or if it doesn't), please notify me on discord.

The ``sht3xd`` sensor platform Temperature+Humidity sensor allows you to use your Sensiron SHT31-D
(`datasheet <https://cdn-shop.adafruit.com/product-files/2857/Sensirion_Humidity_SHT3x_Datasheet_digital-767294.pdf>`__,
`Adafruit`_ ) sensors with
esphomelib. The `I²C bus </esphomeyaml/components/i2c.html>`__ is
required to be set up in your configuration for this sensor to work.

.. figure:: /esphomeyaml/components/sensor/sht3xd-full.jpg
   :align: center
   :target: `Adafruit`_
   :width: 50.0%

   SHT3X-D Temperature & Humidity Sensor. Image by `Adafruit`_.

.. _Adafruit: https://www.adafruit.com/product/2857

|image0|

.. |image0| image:: /esphomeyaml/components/sensor/temperature-humidity.png
   :class: align-center
   :width: 80.0%

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: sht3xd
        temperature:
          name: "Living Room Temperature"
        humidity:
          name: "Living Room Humidity"
        accuracy: high
        address: 0x44
        update_interval: 15s

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

-  **temperature** (**Required**): The information for the temperature
   sensor

   -  **name** (**Required**, string): The name for the temperature
      sensor.
   -  All other options from
      `Sensor </esphomeyaml/components/sensor/index.html#base-sensor-configuration>`__
      and `MQTT
      Component </esphomeyaml/components/mqtt.html#mqtt-component-base-configuration>`__.

-  **humidity** (**Required**): The information for the humidity sensor

   -  **name** (**Required**, string): The name for the humidity sensor.
   -  All other options from
      `Sensor </esphomeyaml/components/sensor/index.html#base-sensor-configuration>`__
      and `MQTT
      Component </esphomeyaml/components/mqtt.html#mqtt-component-base-configuration>`__.

-  **address** (*Optional*, int): Manually specify the i^2c address of the sensor.
   Defaults to ``0xff``.
-  **accuracy** (*Optional*, string): The accuracy of the sensor. One of ``low``, ``medium`` and ``high``.
   Defaults to ``high``.
-  **update_interval** (*Optional*, `time </esphomeyaml/configuration-types.html#time>`__): The interval to check the
   sensor. Defaults to ``15s``.
-  **id** (*Optional*, `id </esphomeyaml/configuration-types.html#id>`__): Manually specify the ID used for code
   generation.
