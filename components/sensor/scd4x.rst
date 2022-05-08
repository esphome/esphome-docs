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

- **automatic_self_calibration** (*Optional*, boolean): Whether to enable
  automatic self calibration (ASC). Defaults to ``true``.

- **ambient_pressure_compensation** (*Optional*, int): Enable compensation
  of measured CO₂ values based on given ambient pressure in mBar.

- **altitude_compensation** (*Optional*, int): Enable compensating
  deviations due to current altitude (in metres). Notice: setting
  *altitude_compensation* is ignored if *ambient_pressure_compensation*
  is set.

- **address** (*Optional*, int): Manually specify the I²C address of the sensor.
  Defaults to ``0x62``.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.


``scd4x.perform_forced_calibration`` Action
-------------------------------------------

Performs a forced calibration, making the currently measured CO₂ value match the provided target value.

.. code-block:: yaml

    on_...:
      then:
        - scd4x.perform_forced_calibration: 450

Configuration options:

- **co2** (*Optional*, int, :ref:`templatable <config-templatable>`): The target CO₂ value in parts per million.
  Defaults to ``410`` which is the approximate atmospheric co2 level as of 2018 (`source <https://en.wikipedia.org/wiki/Carbon_dioxide_in_Earth%27s_atmosphere#Current_concentration>`__).

Requires the sensor to be fully initialized and running, fails otherwise.
If successful, difference in current calibration will be written to the log.

Use this if ``automatic_self_calibration`` is not applicable and was therefore turned off.
This is useful if it can't be guaranteed that the sensor is exposed to outside air at least once every 7 days.
For details, check the `sensor's datasheet <https://sensirion.com/media/documents/C4B87CE6/61652F80/Sensirion_CO2_Sensors_SCD4x_Datasheet.pdf>`__ under `3.7 Field Calibration`.

Note that using this action alone does **not** turn off automatic self calibration.
I.e. if ``automatic_self_calibration`` was not set to ``false``, self calibration will overwrite the calibration eventually.


See Also
--------

- :ref:`sensor-filters`
- :doc:`scd30`
- :apiref:`scd4x/scd4x.h`
- :ghedit:`Edit`
