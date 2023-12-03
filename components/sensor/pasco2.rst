PASCO2 CO₂, Temperature and Relative Humidity Sensor
===================================================

.. seo::
    :description: Instructions for setting up PASCO2 CO₂ Temperature and Relative Humidity Sensor
    :image: pasco2.jpg

The ``pasco2`` sensor platform  allows you to use your Infineon PASCO2 CO₂
(`datasheet <https://www.infineon.com/dgdl/Infineon-PASCO2V01-DataSheet-v01_03-DataSheet-v01_03-EN.pdf?fileId=8ac78c8c80027ecd01809278f1af1ba2>`__) sensors with ESPHome.
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

   figure:: images/pasco2.jpg
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pasco2
        co2:
          name: "Workshop CO2"


Configuration variables:
------------------------

- **co2** (*Required*): The information for the CO₂ sensor.

  - **name** (**Required**, string): The name for the CO₂eq sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.


- **automatic_self_calibration** (*Optional*, boolean): Whether to enable
  automatic self calibration (ASC). Defaults to ``true``.

- **ambient_pressure_compensation** (*Optional*, int): Enable compensation
  of measured CO₂ values based on given ambient pressure in mBar.


- **measurement_mode** (*Optional*): Set measurement mode for pasco2.

  - ``periodic``: The sensor takes a new measurement every 5 seconds. This is the default mode.
  - ``single_shot``: A measurement is started in every update interval.


- **ambient_pressure_compensation_source** (*Optional*, :ref:`config-id`): Set an external pressure sensor ID used for ambient pressure compensation.
  The pressure sensor must report pressure in hPa. the correction is applied before updating the state of the co2 sensor.

- **address** (*Optional*, int): Manually specify the I²C address of the sensor.
  Defaults to ``0x28``.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.

Actions:
--------

.. _perform_forced_calibration_action:

``perform_forced_calibration`` Action
---------------------------------------------

This :ref:`action <config-action>` manually calibrates the sensor to the provided value in ppm.
Operate the PASCO2 in the operation mode later used in normal sensor operation (periodic measurement or single shot) for > 3 minutes in an environment with homogenous and constant CO2 concentration before performing a forced recalibration.
As of Dec 2023 the average fresh air Co² concentration is 400 ppm.

.. code-block:: yaml

    on_...:
      then:
        - pasco2.perform_forced_calibration:
            value: 400   # outside average Dec 2023
            id: my_pasco2

value can also be a template, for example to define a Home Assistant calibration service:

.. code-block:: yaml

    api:
      services:
        - service: calibrate_co2_value
          variables:
            co2_ppm: int
          then:
          - pasco2.perform_forced_calibration:
              value: !lambda 'return co2_ppm;'
              id: my_pasco2


.. _factory_reset_action:


Pressure compensation
---------------------

A static ambient pressure value can be set with `ambient_pressure_compensation`. It can also be changed dynamically with :ref:`lambdas <config-lambda>` using `set_ambient_pressure_compensation(<mBar>)`, or by pointing `ambient_pressure_compensation_source` to a local pressure sensor.

Example with a local sensor
***************************

Note: remember your pressure sensor needs to output in mBar

.. code-block:: yaml

    sensor:
      - platform: bme280
        pressure:
          name: "Ambient Pressure"
          id: bme_pressure

      - platform: pasco2
        measurement_mode: periodic
        enable_pin: GPIO47
        ambient_pressure_compensation_source: bme_pressure
        temperature_offset: 0
        co2:
          name: "CO2 level"

Example with a remote sensor
****************************

This example creates a service `set_ambient_pressure` that can be called from Home Assistant:

.. code-block:: yaml

    api:
      services:
        - service: set_ambient_pressure
          variables:
            pressure_mbar: int
          then:
            - lambda: "id(my_pasco2)->set_ambient_pressure_compensation(pressure_mbar);"

    sensor:
      - platform: pasco2
        id: my_pasco2
        measurement_mode: periodic
        temperature_offset: 0
        co2:
          name: "CO2 level"


See Also
--------

- :ref:`sensor-filters`
- :apiref:`pasco2/pasco2.h`
- :ghedit:`Edit`
