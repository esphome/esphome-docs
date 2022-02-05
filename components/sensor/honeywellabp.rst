Honeywell ABP Pressure Sensors
==============================

.. seo::
    :description: Instructions for setting up Honeywell ABP Pressure sensors
    :image: honeywellabp.jpg
    :keywords: Honeywell ABP

The ``honeywellabp`` sensor platform allows you to use your Honeywell ABP 
('website <https://sps.honeywell.com/us/en/products/sensing-and-iot/sensors/pressure-sensors/board-mount-pressure-sensors/basic-abp-series>'__,
`datasheet <https://prod-edam.honeywell.com/content/dam/honeywell-edam/sps/siot/en-us/products/sensors/pressure-sensors/board-mount-pressure-sensors/basic-abp-series/documents/sps-siot-basic-board-mount-pressure-abp-series-datasheet-32305128-ciid-155789.pdf?download=false>`__,
`Mouser <https://www.mouser.ca/new/honeywell/honeywell-abp-pressure-sensors/>'_) pressure and temperature sensors with ESPHome. The :ref:`SPI <spi>` is
required to be set up in your configuration for this sensor to work

.. figure:: images/honeywellabp.jpg
    :align: center
    :width: 50.0%

    Honeywell ABP Pressure and Temperature Sensor.

.. code-block:: yaml

    # Example configuration entry
    sensor:
    - platform: honeywellabp
        pressure:
            name: "Honeywell pressure"
            unit_of_measurement: "psi"
            min_pressure: 0
            max_pressure: 15
        temperature:
            name: "Honeywell temperature"
        cs_pin: GPIO5 #D5
        update_interval: 2s

Configuration variables:
------------------------

- **pressure** (*Optional*): The information for the pressure sensor.

  - **name** (**Required**, string): The name for the pressure sensor.
  - **min_pressure** (**Required**, int or float): Minumim pressure for the temperature sensor.
  - **max_pressure** (**Required**, int or float): Maximum pressure for the temperature sensor.

    From datasheet, used to calculate the pressure read by the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temperature** (*Optional*): The information for the temperature sensor.
    Some sensors do not have temperature sensing ability.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **cs_pin** (**Required**, :ref:`SPI <spi>`): Chip select pin.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.

See Also
--------

- :ref:`sensor-filters`
- :apiref:`honeywellabp/honeywellabp.h`
- :ghedit:`Edit`
