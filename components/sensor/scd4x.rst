SCD4X CO₂, Temperature and Relative Humidity Sensor
===================================================

.. seo::
    :description: Instructions for setting up SCD4X CO₂ Temperature and Relative Humidity Sensor
    :image: scd4x.jpg

The ``scd4x`` sensor platform  allows you to use your Sensirion SCD4X CO₂
(`datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9.5_CO2/Sensirion_CO2_Sensors_SCD4x_Datasheet.pdf>`__) sensors with ESPHome.
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

.. figure:: images/scd4x.jpg
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: scd4x
        co2:
          name: "Workshop CO2"
        temperature:
          name: "Workshop Temperature"
        humidity:
          name: "Workshop Humidity"


Configuration variables:
------------------------

- **co2** (*Optional*): The information for the CO₂ sensor.

  - **name** (**Required**, string): The name for the CO₂eq sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temperature** (*Optional*): The information for the Temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.


- **humidity** (*Optional*): The information for the Humidity sensor.

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temperature_offset** (*Optional*, float):  The temperature offset can depend
  on various factors such as the SCD4x measurement mode, self-heating of close
  components, the ambient temperature and air flow. This variable allows the
  compensation of those effects by setting a temperature offset. Defaults to
  ``4°C``.

- **automatic_self_calibration** (*Optional*, bool): Whether to enable
  automatic self calibration (ASC). Defaults to ``true``.

- **ambient_pressure_compensation** (*Optional*, int): Enable compensation
  of measured CO₂ values based on given ambient pressure in mBar.

- **altitude_compensation** (*Optional*, int): Enable compensating
  deviations due to current altitude (in metres). Notice: setting
  *altitude_compensation* is ignored if *ambient_pressure_compensation*
  is set.

- **compensation** (*Optional*): External sensors used for compensation.

  - **pressure_source** (*Optional*, :ref:`config-id`): Set an external pressure sensor ID used for ambient pressure compensation.
    The pressure sensor must report pressure in hPa.

  - **altitude_source** (*Optional*, :ref:`config-id`): Set an external altitude sensor ID for altitude compensation
    The altitude sensor must report altitude in metres.  Notice: setting
    *altitude_source* is ignored if *pressure_source*  is set.

- **address** (*Optional*, int): Manually specify the I²C address of the sensor.
  Defaults to ``0x62``.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.

Automation
-----------------

Ambient pressure compensation and altitude compensation can be changed from :ref:`lambdas <config-lambda>`


``set_ambient_pressure_compensation(  <pressure in bar)"``

and


``>set_altitude_compensation(  altitude in m)"``

Example
*******

Note: that the pressure from bme280 is in hPa and must be converted to bar.

.. code-block:: yaml

  sensor:
    - platform: scd4x
      id: scd41
      i2c_id: bus_a
      co2:
        name: co2
        id: co2

    - platform: bme280
      pressure:
        name: "BME280-Pressure"
        id: bme280_pressure
        oversampling: 1x
        on_value:
          then:
            - lambda: "id(scd41)->set_ambient_pressure_compensation(x / 1000.0);"


See Also
--------

- :ref:`sensor-filters`
- :doc:`scd30`
- :apiref:`scd4x/scd4x.h`
- :ghedit:`Edit`
