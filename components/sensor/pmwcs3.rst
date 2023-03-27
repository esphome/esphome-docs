PMWCS3 Capacitive Soil Moisture and Temperature Sensor
======================================================

.. seo::
    :description: Instructions for setting up PMWCS3 capacitive soil moisture sensor in ESPHome.
    :image: pmwcs3.jpg
    :keywords: PMWCS3

The ``pmwcs3`` sensor platform allows you to use your PMWCS3
(`informations <https://tinovi.com/wp-content/uploads/2020/01/PM-WCS-3-I2C.pdf>`__)
capacitive soil moisture and temperature sensor with ESPHome. The :ref:`I²C bus <i2c>` is required to be set up in
your configuration for this sensor to work.

.. figure:: images/pmwcs3.jpg
    :align: center
    :width: 80.0%

    PMWCS3 Capacitive Soil Moisture and Temperature Sensor.


.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pmwcs3
        e25:
          name: "pmwcs3 e25"    
        ec:
          name: "pmwcs3 ec"
        temperature:
          name: "pmwcs3 temperature" 
        vwc:
          name: "pmwcs3 vwc"
        address: 0x63
        update_interval: 60s
 
Configuration variables:
------------------------

- **e25** (*Optional*): Electrical Conductivity, reference at 25°C in dS/m. All options from
  :ref:`Sensor <config-sensor>`.
- **ec** (*Optional*): Electrical Conductivity in mS/m. All options from
  :ref:`Sensor <config-sensor>`.
- **temperature** (*Optional*): Soil temperature in °C.
  All options from :ref:`Sensor <config-sensor>`.
- **vwc** (*Optional*): Volumetric water content in cm3cm−3.
  All options from :ref:`Sensor <config-sensor>`.
- **address** (*Optional*, int): Manually specify the I²C address of the sensor.
  Defaults to ``0x63``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
  
See Also
--------

- :ref:`sensor-filters`
- :apiref:`pmwcs3/pmwcs3.h`
- `Temperature Compensation for Conductivity <https://www.aqion.de/site/112>` by `Aqion`__
- `PMWCS3 Library <https://github.com/tinovi/i2cArduino>`__ by `@tinovi <https://github.com/tinovi>`__
- :ghedit:`Edit`
