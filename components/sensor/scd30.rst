SCD30 CO₂, Temperature and Relative Humidity Sensor
===================================================

.. seo::
    :description: Instructions for setting up SCD30 CO₂ Temperature and Relative Humidity Sensor
    :image: scd30.jpg

The ``scd30`` sensor platform  allows you to use your Sensiron SCD30 CO₂
(`datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9.5_CO2/Sensirion_CO2_Sensors_SCD30_Datasheet.pdf>`__) sensors with ESPHome.
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
        frc_baseline: 400
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

- **address** (*Optional*, int): Manually specify the I^2C address of the sensor.
  Defaults to ``0x61``.

- **altitude_compensation** (*Optional*, int): Set the altitude used for CO₂ measurement compensation,
  in meters above sea level. When absent, altitude compensation is disabled.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for actions.

.. _automatic_self_calibration:

- **automatic_self_calibration** (*Optional*, boolean): Enable the automatic self calibration
  process on the sensor. This allows the sensor automatically adjust its calibration when exposed
  to fresh air. Defaults to ``True``.

.. _frc_baseline:

- **frc_baseline** (*Optional*, int): Set the CO₂ level (in ppm) used when doing a forced
  recalibration. This is configurable between 400 - 2000 ppm, and is only used when the
  scd30.forced_recalibration_action_ is called.
  Defaults to ``400``.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.

.. _scd30.forced_recalibration_action:

``scd30.forced_recalibration`` Action
-------------------------------------

This :ref:`action <config-action>` executes forced recalibration (FRC) command on the sensor with the
given ID.

If you want to execute a forced recalibration, the SCD30 sensor must be in stable gas environment
(400-2000 ppm) for over 2 minutes and you execute this function. You can specifiy the CO₂ level that you
are calibrating with using frc_baseline_ configuration variable. See the sensor documentation for more
information on ASC and FRC operation.

Note: This action disables automatic sensor calibration until the next power cycle. Set
automatic_self_calibration_ to ``False`` if you want to want to only use FRC

.. code-block:: yaml

    on_...:
      then:
        - scd30.forced_recalibration: my_scd30_id

You can provide :ref:`service <api-services>` to call it from Home Assistant

.. code-block:: yaml

    api:
      services:
        - service: scd30_forced_recalibration
          then:
            - scd30.forced_recalibration: my_scd30_id

.. _scd30.asc_enable_action:

``scd30.asc_enable`` Action
---------------------------

This :ref:`action <config-action>` enables automatic sensor calibration on the sensor with the given ID.

.. code-block:: yaml

    on_...:
      then:
        - scd30.asc_enable: my_scd30_id

.. _scd30.asc_disable_action:

``scd30.asc_disable`` Action
----------------------------

This :ref:`action <config-action>` disables automatic sensor calibration on the sensor with the given ID.

.. code-block:: yaml

    on_...:
      then:
        - scd30.asc_disable: my_scd30_id

You can provide switch and control ASC from Home Assistant

.. code-block:: yaml

    switch:
      - platform: template
        name: "SCD30 ASC"
        optimistic: true
        on_turn_on:
          scd30.asc_enable: my_scd30_id
        on_turn_off:
          scd30.asc_disable: my_scd30_id

See Also
--------

- :ref:`sensor-filters`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :apiref:`scd30/scd30.h`
- :ghedit:`Edit`
