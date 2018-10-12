SHT3X-D Temperature+Humidity Sensor
===================================

The ``sht3xd`` sensor platform Temperature+Humidity sensor allows you to use your Sensiron SHT31-D
(`datasheet <https://cdn-shop.adafruit.com/product-files/2857/Sensirion_Humidity_SHT3x_Datasheet_digital-767294.pdf>`__,
`Adafruit`_ ) sensors with
esphomelib. The :ref:`I²C Bus <i2c>` is
required to be set up in your configuration for this sensor to work.

.. _Adafruit: https://www.adafruit.com/product/2857

.. figure:: images/temperature-humidity.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: sht3xd
        temperature:
          name: "Living Room Temperature"
        humidity:
          name: "Living Room Humidity"
        address: 0x44
        update_interval: 15s

Configuration variables:
------------------------

- **temperature** (**Required**): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **humidity** (**Required**): The information for the humidity sensor.

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **address** (*Optional*, int): Manually specify the i^2c address of the sensor.
  Defaults to ``0x44``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``15s``. See :ref:`sensor-default_filter`.

See Also
--------

- :ref:`sensor-filters`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :doc:`API Reference </api/sensor/sht3xd>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/sht3xd.rst>`__

.. disqus::
