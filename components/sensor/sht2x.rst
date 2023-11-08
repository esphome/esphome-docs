SHT2X Temperature+Humidity Sensor
===================================

.. seo::
    :description: Instructions for setting up SHT2x temperature and humidity sensors
    :image: sht2x.png

The ``sht2x`` sensor platform Temperature+Humidity sensor allows you to use your Sensirion SHT2x
(`datasheet <https://sensirion.com/media/documents/CCDE1377/635000A2/Sensirion_Datasheet_Humidity_Sensor_SHT20.pdf>`__,
`Sensirion`_ ) sensors with
ESPHome. The :ref:`I²C Bus <i2c>` is
required to be set up in your configuration for this sensor to work.

.. _Sensirion: https://sensirion.com/products/catalog/SHT20/

.. figure:: images/temperature-humidity.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: sht2x
        temperature:
          name: "Living Room Temperature"
        humidity:
          name: "Living Room Humidity"

Configuration variables:
------------------------

- **temperature** (**Required**): The information for the temperature sensor.

  - All other options from :ref:`Sensor <config-sensor>`.

- **humidity** (**Required**): The information for the humidity sensor.

  - All other options from :ref:`Sensor <config-sensor>`.

- **address** (*Optional*, int): Manually specify the I²C address of the sensor.
  Defaults to ``0x40``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``30s``.

See Also
--------

- :ref:`sensor-filters`
- :doc:`absolute_humidity`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :apiref:`sht2x/sht2x.h`
- :ghedit:`Edit`
