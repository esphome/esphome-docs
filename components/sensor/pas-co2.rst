SCD4X CO₂, Temperature and Relative Humidity Sensor
===================================================

.. seo::
    :description: Instructions for setting up the Infinition XENSIV PAS CO2 sensor.
    :image: scd4x.jpg

The ``pas-co2`` sensor platform  allows you to use your Infinition XENSIV PAS CO2 sensor
(`datasheet <https://www.infineon.com/dgdl/Infineon-EVAL_PASCO2_SENSOR-DataSheet-v01_00-EN.pdf?fileId=5546d462758f5bd10175934ec4215c6a>`__) sensors with ESPHome.
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

.. figure:: images/scd4x.jpg
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pas-co2
        co2:
          name: "Workshop CO2"


Configuration variables:
------------------------

- **co2** (*Optional*): The information for the CO₂ sensor.

  - **name** (**Required**, string): The name for the CO₂eq sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **automatic_self_calibration** (*Optional*, boolean): Whether to enable
  automatic self calibration (ASC). Defaults to ``true``.

- **ambient_pressure_compensation** (*Optional*, int): Enable compensation
  of measured CO₂ values based on given ambient pressure in mBar.

- **altitude_compensation** (*Optional*, int): Enable compensating
  deviations due to current altitude (in metres). Notice: setting
  *altitude_compensation* is ignored if *ambient_pressure_compensation*
  is set.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``. The sensors internal measurement rate is aligned with ``update_interval`` 



See Also
--------

- :ref:`sensor-filters`
- :apiref:`pas-co2/pas-co2.h`
- :ghedit:`Edit`
