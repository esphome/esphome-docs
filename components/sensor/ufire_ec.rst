uFire EC sensor
===================

.. seo::
    :description: Instructions for setting up uFire EC sensor in esphome
    :image: ufire_ec.png
    :keywords: ufire ec sensor temperature esphome

The ``ufire_ec`` sensor platform allows you to use your uFire EC sensor with
ESPHome. The :ref:`I²C Bus <i2c>` is
required to be set up in your configuration for this sensor to work.
It required also to have an temperature sensor in the liquit tank; this can
be on the same board or external sensor linked to the uFire EC configuration.

.. figure:: images/ufire_ec.png
    :align: center
    :width: 100.0%

.. code-block:: yaml

    # Example configuration entry
    api:
      services:
        - service: ec_calibrate_probe
          variables:
          solution: float
          then:
            - ufire_ec.calibrate_probe:
              id: ufire_ec_board
              solution: !lambda "return solution;"
              temperature: !lambda "return id(temperature_sensor).state;"
        - service: ec_reset
          then:
            - ufire_ec.reset:
              id: ufire_ec_board

    i2c:

    sensor:
      - platform: ufire_ec  
        id: ufire_ec_board
        temperature:
          id: temperature
          name: Temperature
        ec:
          name: EC


Configuration variables:
------------------------

- **address** (**Optional**, int): Specify the I²C address of the sensor. Defaults to ``0x3C``,
  this address work with the Isolated EC boards for Mod-EC use ``0x0a``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- **temperature_sensor** (*Optional*, :ref:`config-id`): Set the ID of the temperature
  sensor. Only needed if the onboard temperature sensor is not used.
- **ec** (*Optional*, :ref:`<config-sensor>`): Set the EC sensor configuration.
- **temperature** (*Optional*, :ref:`<config-sensor>`): Set the onboard temperature sensor configuration.
  Can't be used together with ``temperature_sensor``.
- **temperature_compensation** (*Optional*, float): Set the temperature compensation for the EC
  sensor. Defaults to ``25.0``.
- **temperature_coefficient** (*Optional*, float): Set the temperature coefficient for the EC
  sensor. Defaults to ``0.019``.
- All other options from :ref:`Sensor <config-sensor>`.

lambda calls
------------

From :ref:`lambdas <config-lambda>`, you can calibrate the EC sensor.

- ``calibrate_probe(solution float, temperature float)``: Calibrate the EC sensor.
- ``reset()``: Reset the calibrate the EC sensor.


See Also
--------

- :ref:`sensor-filters`
- :apiref:`ufire_ec/ufire_ec.h`
- :ghedit:`Edit`
