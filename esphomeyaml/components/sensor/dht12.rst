DHT12 Temperature+Humidity Sensor
=================================

.. warning::

    This sensor is experimental has not been fully tested yet as I do not own all sensors. If you
    can verify it works (or if it doesn't), please notify me on `discord <https://discord.gg/KhAMKrd>`__.

The DHT12 Temperature+Humidity sensor allows you to use your DHT12
(`datasheet <http://www.robototehnika.ru/file/DHT12.pdf>`__,
`electrodragon`_) i2c-based sensor with esphomelib.

.. figure:: /esphomeyaml/components/sensor/dht12-full.jpg
    :align: center
    :target: `electrodragon`_
    :width: 50.0%

    DHT12 Temperature & Humidity Sensor. Image by `electrodragon`_.

.. _electrodragon: http://www.electrodragon.com/product/dht12/

|image0|

.. |image0| image:: /esphomeyaml/components/sensor/temperature-humidity.png
    :class: align-center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: dht12
        temperature:
          name: "Living Room Temperature"
        humidity:
          name: "Living Room Humidity"
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

-  **update_interval** (*Optional*, `time </esphomeyaml/configuration-types.html#time>`__): The interval to check the
   sensor. Defaults to ``15s``.
-  **id** (*Optional*, `id </esphomeyaml/configuration-types.html#id>`__): Manually specify the ID used for code
   generation.
