BMP388 / BMP390 Temperature+Pressure Sensor
===========================================

.. seo::
    :description: Instructions for setting up BMP388 or BMP390 temperature and pressure sensors with ESPHome
    :image: bmp388.jpg
    :keywords: BMP388 BMP390

The ``bmp3xx`` sensor platform allows you to use your BMP388 or BMP390 
(`datasheet <https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp390-ds002.pdf>`__, `BMP390 product page <https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp390/>`__) temperature and pressure sensors with ESPHome. The :ref:`I²C <i2c>` bus is
required to be set up in your configuration for this sensor to work.

.. figure:: images/bmp388.jpg
    :align: center
    :width: 50.0%

    BMP388/BMP390 Temperature and Pressure Sensor.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: bmp3xx
        temperature:
          name: "Outside Temperature"
          oversampling: 16x
        pressure:
          name: "Outside Pressure"
        address: 0x77
        update_interval: 60s

Configuration variables:
------------------------

- **temperature** (*Optional*): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature
    sensor.
  - **oversampling** (*Optional*): The oversampling parameter for the temperature sensor.
    See :ref:`Oversampling Options <bmp3xx-oversampling>`.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **pressure** (*Optional*): The information for the pressure sensor.

  - **name** (**Required**, string): The name for the pressure sensor.
  - **oversampling** (*Optional*): The oversampling parameter for the temperature sensor.
    See :ref:`Oversampling Options <bmp3xx-oversampling>`.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **address** (*Optional*, int): Manually specify the I²C address of
  the sensor. Defaults to ``0x77``. Another address can be ``0x76``.
- **iir_filter** (*Optional*): Set up an Infinite Impulse Response filter to increase accuracy. One of
  ``OFF``, ``2x``, ``4x``, ``16x``, ``32``, ``64x``, ``128x``. Defaults to ``OFF``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.


.. _bmp3xx-oversampling:

Oversampling Options
--------------------

By default, the BMP3xx sensor measures pressure 16 times and temperature 2 times when requesting a new value. You can, however,
configure this amount. Possible oversampling values:

-  ``NONE`` (value is skipped)
-  ``2x``
-  ``4x``
-  ``8x``
-  ``16x`` (default)
-  ``32x``

See Also
--------

- :ref:`sensor-filters`
- :doc:`bme280`
- :doc:`bmp280`
- :doc:`bme680`
- :doc:`bmp085`
- :ghsources:`esphome/components/bmp3xx`
- `BMP3 sensor API <https://github.com/BoschSensortec/BMP3-Sensor-API>`__
- `BMP388/BMP390 Library <https://github.com/MartinL1/BMP388_DEV>`__ by  Martin Lindupp
- :ghedit:`Edit`
