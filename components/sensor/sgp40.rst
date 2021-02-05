SGP40 Volatile Organic Compound Sensor
==============================================

.. seo::
    :description: Instructions for setting up SGP40 Volatile Organic Compound sensor
    :image: sgp40.jpg

The ``sgp40`` sensor platform  allows you to use your Sensiron SGP40 VOC sensor
(`datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Sensirion_Gas_Sensors_SGP40_Datasheet.pdf>`__) with ESPHome.
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

.. figure:: images/sgp40.jpg
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: sgp40
        name: "Workshop VOC"
        update_interval: 5s
        store_baseline: "true"
        compensation:
          humidity_source: dht1_temp
          temperature_source: dht1_hum    


Configuration variables:
------------------------

- **name** (**Required**, string): The name for the CO₂eq sensor.
- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
- **store_baseline** (*Optional*, boolean ): Stores and retrieves the baseline infortmation for quicker startups

- **compensation** (*Optional*): The block containing sensors used for compensation.

  - **temperature_source** (*Optional*, :ref:`config-id`): Give an external temperature sensor ID
    here. This can improve the sensor's internal calculations.

  - **humidity_source** (*Optional*, :ref:`config-id`): Give an external humidity sensor ID
    here. This can improve the sensor's internal calculations.

- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :doc:`sht3xd`
- :apiref:`sgp40/sgp40.h`
- :ghedit:`Edit`
