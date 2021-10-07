SGP40 Volatile Organic Compound Sensor
======================================

.. seo::
    :description: Instructions for setting up SGP40 Volatile Organic Compound sensor
    :image: sgp40.jpg

The ``sgp40`` sensor platform allows you to use your Sensirion SGP40 VOC sensor
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

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the CO₂eq sensor.
- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``
- **store_baseline** (*Optional*, boolean ): Stores and retrieves the baseline information for quicker startups. Defaults to ``true``
- **optimal_sampling** (*Optional*, boolean): This sensor need to be driven
  at a rate of 1Hz. If this option is ``true``, the sensor will be read out
  on device at the correct interval separately from the update_interval.
  This state will be reported to other components, or the front end at the
  update_interval, saving wifi power and network communication. If this
  parameter is ``false``, the sensor will be read at the update_interval.
  This will lead to incorrect values, but may be good enough for certain
  use cases. Defaults to ``true``.

- **compensation** (*Optional*): The block containing sensors used for compensation. If not set defaults will be used.

  - **temperature_source** (*Optional*, :ref:`config-id`): Give an external temperature sensor ID
    here. This can improve the sensor's internal calculations. Defaults to ``25``

  - **humidity_source** (*Optional*, :ref:`config-id`): Give an external humidity sensor ID
    here. This can improve the sensor's internal calculations. Defaults to ``50``

- All other options from :ref:`Sensor <config-sensor>`.

Example With Compensation
-------------------------
.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: sgp40
        name: "Workshop VOC"
        update_interval: 5s        
        compensation:
          humidity_source: dht1_hum
          temperature_source: dht1_temp 
          
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
