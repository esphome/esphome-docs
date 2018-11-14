DHT12 Temperature+Humidity Sensor
=================================

.. seo::
    :description: Instructions for setting up DHT12 temperature and humidity sensors
    :image: dht12.jpg
    :keywords: dht12

The ``dht12`` Temperature+Humidity sensor allows you to use your DHT12
(`datasheet <http://www.robototehnika.ru/file/DHT12.pdf>`__,
`electrodragon`_) i2c-based sensor with esphomelib.

.. figure:: images/dht12-full.jpg
    :align: center
    :width: 50.0%

    DHT12 Temperature & Humidity Sensor.

.. _electrodragon: http://www.electrodragon.com/product/dht12/

.. figure:: images/temperature-humidity.png
    :align: center
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
------------------------

- **temperature** (**Required**): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **humidity** (**Required**): The information for the humidity sensor

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``15s``.
  See :ref:`sensor-default_filter`.

See Also
--------

- :ref:`sensor-filters`
- :doc:`dht`
- :doc:`hdc1080`
- :doc:`htu21d`
- :doc:`sht3xd`
- :doc:`API Reference </api/sensor/dht12>`
- `DHT12 Library <https://github.com/dplasa/dht>`__ by `Daniel Plasa <https://github.com/dplasa>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/dht12.rst>`__

.. disqus::
