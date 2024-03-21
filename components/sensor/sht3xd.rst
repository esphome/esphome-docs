SHT3X-D Temperature+Humidity Sensor
===================================

.. seo::
    :description: Instructions for setting up SHT31-D/SHT3x and SHT85 temperature and humidity sensors
    :image: sht3xd.jpg

The ``sht3xd`` sensor platform Temperature+Humidity sensor allows you to use your Sensirion SHT31-D/SHT3x
(`datasheet <https://cdn-shop.adafruit.com/product-files/2857/Sensirion_Humidity_SHT3x_Datasheet_digital-767294.pdf>`__,
`Adafruit`_ ) and SHT85 (`datasheet <https://sensirion.com/media/documents/4B40CEF3/640B2346/Sensirion_Humidity_Sensors_SHT85_Datasheet.pdf>`__,
`Sensirion`_ ) sensors with Esphome.
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

.. _Adafruit: https://www.adafruit.com/product/2857
.. _Sensirion: https://sensirion.com/products/catalog/SHT85/

.. figure:: images/temperature-humidity.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: sht3xd
        temperature:
          name: "Living Room Temperature"
        humidity:
          name: "Living Room Humidity"
        address: 0x44
        update_interval: 60s

Configuration variables:
------------------------

- **temperature** (*Optional*): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **humidity** (*Optional*): The information for the humidity sensor.

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **address** (*Optional*, int): Manually specify the I²C address of the sensor.
  Defaults to ``0x44``. For SHT3x, an alternate address can be ``0x45`` while SHT85 supports only address ``0x44``
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **heater_enabled** (*Optional*, bool): Turn on/off heater at boot.
  This may help provide `more accurate readings in condensing conditions <https://forum.arduino.cc/t/atmospheric-sensors-in-condensing-conditions/412167>`_,
  but can also increase temperature readings and decrease humidity readings as a side effect.
  Defaults to ``false``.

See Also
--------

- :ref:`sensor-filters`
- :doc:`absolute_humidity`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :apiref:`sht3xd/sht3xd.h`
- :ghedit:`Edit`
