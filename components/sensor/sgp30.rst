SGP30 CO₂ and Volatile Organic Compound Sensor
==============================================

.. seo::
    :description: Instructions for setting up SGP30 CO₂eq and Volatile Organic Compound sensor
    :image: sgp30.jpg

The ``sgp30`` sensor platform allows you to use your Sensirion SGP30 multi-pixel gas
(`datasheet <https://sensirion.com/media/documents/984E0DD5/61644B8B/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf>`__) sensors or the SVM30 breakout-boards  (`product page <https://sensirion.com/products/catalog/SVM30/>`__) with ESPHome.
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

.. figure:: images/eco2-tvoc.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: sgp30
        eco2:
          name: "Workshop eCO2"
          accuracy_decimals: 1
        tvoc:
          name: "Workshop TVOC"
          accuracy_decimals: 1
        store_baseline: yes
        address: 0x58
        update_interval: 1s

Configuration variables:
------------------------

- **eco2** (**Required**): The information for the CO₂eq. sensor.

  - **name** (**Required**, string): The name for the CO₂eq sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **tvoc** (**Required**): The information for the total Volatile Organic Compounds sensor.

  - **name** (**Required**, string): The name for the TVOC sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **store_baseline** (*Optional*, boolean): Store the sensor baselines persistently when calculated or updated.
  Defaults to yes.

- **address** (*Optional*, int): Manually specify the I²C address of the sensor.
  Defaults to ``0x58``.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``1s``.

Advanced:

- **baseline** (*Optional*): The block containing baselines for calibration purposes. See :ref:`sgp30-calibrating` for more info.

  - **eco2_baseline** (**Required**, int): The eCO2 baseline for calibration purposes. After OTA, this value is used to calibrate the sensor.

  - **tvoc_baseline** (**Required**, int): The TVOC baseline for calibration purposes. After OTA, this value is used to calibrate the sensor.

- **eco2_baseline** (*Optional*): The information for the CO₂eq. baseline value sensor. Baseline value is published in decimals.

  - **name** (**Required**, string): The name for the CO₂eq baseline value sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **tvoc_baseline** (*Optional*): The information for the TVOC baseline value sensor. Baseline value is published in decimals.

  - **name** (**Required**, string): The name for the TVOC baseline value sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **compensation** (*Optional*): The block containing sensors used for compensation. Both values must be supplied in order to be able to generate the absolute humidity to be reported to the sensor.

  - **temperature_source** (*Optional*, :ref:`config-id`): Give an external temperature sensor ID
    here. The data must be in Celsius. This can improve the sensor's internal calculations.

  - **humidity_source** (*Optional*, :ref:`config-id`): Give an external relative humidity sensor ID
    here. This can improve the sensor's internal calculations.

.. _sgp30-calibrating:

Calibrating Baseline
--------------------

The SGP30 sensor will re-calibrate its baseline each time it is powered on. During the first power-up this will take up to 12 hours.
Exposing to outside air for at least 10 minutes cumulative time is advised during the calibration period.

For best performance and faster startup times, the current **baseline** needs to be persistently stored on the device before shutting it down and set again accordingly after boot up.
It implies that if the sensor reboots at a time when the air is less clean than normal, the values will have a constant offset and cannot be compared to the values before the last boot.

Using the **store_baseline** option will automatically store the baseline values after calibration or when it is updated during operation. When booting up, the stored values will then be
(re)applied in the sensor. Stored baselines are cleared after OTA.

Another method is to manually specify the baseline values in the configuration file. To do this, let the sensor boot up with no baseline set and let the sensor calibrate itself.
After around 12 hours you can then view the remote logs on the ESP. The nexttime the sensor is read out, you will see a log message with something like
``Current eCO2 baseline: 0x86C5, TVOC baseline: 0x8B38``.

Another way to obtain the baseline values is to configure the eco2 and TVOC baseline value sensors. Values will be published to your Home Automation system.
Convert the decimal value to hex value before use (e.g. 37577 --> 0x92C9)

Now set the baseline property in your configuration file like so with the value you got
via the logs:

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: sgp30
        # ...
        baseline:
          eco2_baseline: 0x86C5
          tvoc_baseline: 0x8B38

The next time you upload the code, the SGP30 will be continue its operation with this baseline and you will get consistent values.

Please note while the sensor is off, baseline values are valid for a maximum of seven days.

See Also
--------

- :ref:`sensor-filters`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :doc:`sht3xd`
- :apiref:`sgp30/sgp30.h`
- :ghedit:`Edit`
