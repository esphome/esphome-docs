SCD30 CO₂, Temperature and Relative Humidity Sensor
===================================================

.. seo::
    :description: Instructions for setting up SCD30 CO₂ Temperature and Relative Humidity Sensor
    :image: scd30.jpg

The ``scd30`` sensor platform  allows you to use your Sensiron SCD30 CO₂  
(`datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/0_Datasheets/CO2/Sensirion_CO2_Sensors_SCD30_Datasheet.pdf>`__) sensors with ESPHome. 
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

.. figure:: images/scd30.jpg
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: scd30
        co2:
          name: "Workshop CO2"
          accuracy_decimals: 1
        temperature:
          name: "Workshop Temperature"
          accuracy_decimals: 2
        humidity:
          name: "Workshop Humidity"
          accuracy_decimals: 1
        address: 0x61
        altitude_compensation: 800m
        automatic_self_calibration: True
        update_interval: 5s
        

Configuration variables:
------------------------

- **co2** (**Required**): The information for the CO₂ sensor.

  - **name** (**Required**, string): The name for the CO₂ sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temperature** (**Required**): The information for the Temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.


- **humidity** (**Required**): The information for the Humidity sensor.

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **address** (*Optional*, int): Manually specify the i^2c address of the sensor.
  Defaults to ``0x61``.

- **altitude_compensation** (*Optional*, int): Set the altitude used for CO₂ measurement compensation,
  in meters above sea level. When absent, altitude compensation is disabled.

- **automatic_self_calibration** (*Optional*, boolean): Enable the automatic self calibration
  process on the sensor. This allows the sensor automatically adjust its calibration when exposed
  to fresh air. Defaults to ``True``.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.



See Also
--------

- :ref:`sensor-filters`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :apiref:`scd30/scd30.h`
- :ghedit:`Edit`
