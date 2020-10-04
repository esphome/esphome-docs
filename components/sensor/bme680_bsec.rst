BME680 Temperature+Pressure+Humidity+Gas Sensor via BSEC
========================================================

.. seo::
    :description: Instructions for setting up BME680 temperature, humidity, pressure and gas sensors via BSEC.
    :image: bme680.jpg
    :keywords: BME680

The ``bme680_bsec`` sensor platform allows you to use your BME680
(`datasheet <https://cdn-shop.adafruit.com/product-files/3660/BME680.pdf>`__,
`Adafruit`_) temperature, pressure and humidity and gas sensors with ESPHome via the Bosch Sensortec Environmental Cluster (BSEC)
software library. The use of Bosch's proprietary algorithms provides additional Indoor Air Quality (IAQ), CO2 equivalent and Breath
Volatile Organic Compounds (VOC) equivalent measurements.

.. note::

    The Bosch BSEC library is only available for use after accepting its software license agreement. By enabling this component,
    you are explicitly agreeing to the terms of the `BSEC license agreement`_. You must not distribute any compiled firmware
    binaries that include this component.

The :ref:`I²C <i2c>` is required to be set up in your configuration for this sensor to work.

.. figure:: images/bme680-full.jpg
    :align: center
    :width: 50.0%

    BME680 Temperature, Pressure, Humidity & Gas Sensor.

.. _BSEC license agreement: https://ae-bst.resource.bosch.com/media/_tech/media/bsec/2017-07-17_ClickThrough_License_Terms_Environmentalib_SW_CLEAN.pdf

.. _Adafruit: https://www.adafruit.com/product/3660

.. code-block:: yaml

    # Example configuration entry
    bme680_bsec:
        address: 0x76
        temperature_offset: 0
        iaq_mode: static
        state_save_interval: 6h

    sensor:
      - platform: bme680_bsec
        temperature:
          name: "BME680 Temperature"
        pressure:
          name: "BME680 Pressure"
        humidity:
          name: "BME680 Humidity"
        gas_resistance:
          name: "BME680 Gas Resistance"
        iaq:
          name: "BME680 IAQ"
        co2_equivalent:
          name: "BME680 CO2 Equivalent"
        breath_voc_equivalent:
          name: "BME680 Breath VOC Equivalent"

    text_sensor:
      - platform: bme680_bsec
        iaq_accuracy:
          name: "BME680 IAQ Accuracy"

Configuration variables:
------------------------

The configuration is made up of three parts: The central hub, individual sensors, and accuracy text sensor.

Hub Configuration:

- **address** (*Optional*, int): Manually specify the I^2C address of
  the sensor. Defaults to ``0x76``. Another address can be ``0x77``.

- **temperature_offset** (*Optional*, float): Temperature offset if device is in enclosure and reads too high.
  Defaults to ``0``.

- **iaq_mode** (*Optional*, string): IAQ calculation mode. Default is ``static`` for mobile applications (e.g. fixed indoor devices).
  Can be ``mobile`` for mobile applications (e.g. carry-on devices).

- **state_save_interval** (*Optional*, :ref:`config-time`): The interval at which to save BSEC algorithm state to flash so that
  calibration does have to start from zero on device restart. Defaults to ``6h``.

Sensor Configuration:

- **temperature** (*Optional*): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **pressure** (*Optional*): The information for the pressure sensor.

  - **name** (**Required**, string): The name for the pressure sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **humidity** (*Optional*): The information for the humidity sensor.

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **gas_resistance** (*Optional*): The information for the gas sensor.

  - **name** (**Required**, string): The name for the gas resistance sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **iaq** (*Optional*): The information for the IAQ sensor.

  - **name** (**Required**, string): The name for the IAQ sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **co2_equivalent** (*Optional*): The information for the CO2 equivalent sensor.

  - **name** (**Required**, string): The name for the CO2 equivalent sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **breath_voc_equivalent** (*Optional*): The information for the Breath VOC equivalent humidity sensor.

  - **name** (**Required**, string): The name for the Breath VOC equivalent sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

Text Sensor Configuration:

- **iaq_accuracy** (*Optional*): The information for the IAQ accuracy sensor.

  - **name** (**Required**, string): The name for the IAQ accuracy sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`TextSensor <config-text_sensor>`.

.. figure:: images/bme680-bsec-ui.png
    :align: center
    :width: 80.0%

Multiple Sensors
----------------

It is possible to read from multiple sensors by configuring multiple instances of the platform hub as follows:

.. code-block:: yaml

    bme680_bsec:
      - id: bme680_one
        address: 0x76
      - id: bme680_two
        address: 0x77

    sensor:
      - platform: bme680_bsec
        bme680_bsec_id: bme680_one
        temperature:
          name: "BME680 One Temperature"
      - platform: bme680_bsec
        bme680_bsec_id: bme680_two
        temperature:
          name: "BME680 Two Temperature"

Indoor Air Quality (IAQ) Measurement
------------------------------------

Indoor Air Quality measurements are expressed in the IAQ index scale with 25IAQ corresponding to typical good air and 250IAQ
indicating typical polluted air after calibration.

.. _bsec-calibration:

IAQ Accuracy and Calibration
----------------------------

The BSEC algorithm automatically gathers data in order to calibrate the IAQ measurements. The IAQ Accuracy sensor will give one
of the following values:

- ``Stabilizing``: The devie has just started, and the sensor is stabilizing (this typically lasts 5 minutes)
- ``Uncertain``: The background history of BSEC is uncertain. This typically means the gas sensor data was too
  stable for BSEC to clearly define its reference.
- ``Calibrating``: BSEC found new calibration data and is currently calibrating.
- ``Calibrated``: BSEC calibrated successfully.

Once calibration is achieved, and every ``state_save_interval`` thereafter, the current algorithm state is saved to flash so that
the process does not have to start from zero on device restart.

See Also
--------

- :ref:`sensor-filters`
- :doc:`bme680`
- :apiref:`bme680_bsec/bme680_bsec.h`
- `BSEC Arduino Library <https://github.com/BoschSensortec/BSEC-Arduino-library>`__ by `Bosch Sensortec <https://www.bosch-sensortec.com/>`__
- `Bosch Sensortec Community <https://community.bosch-sensortec.com/t5/Bosch-Sensortec-Community/ct-p/bst_community>`__
- :ghedit:`Edit`
