SGP40 Volatile Organic Compound Sensor and SGP41 VOC and NOx Sensor
===================================================================

.. seo::
    :description: Instructions for setting up SGP40/SGP41 Volatile Organic Compound and NOx sensor
    :image: sgp40.jpg

The ``sgp4x`` sensor platform allows you to use your Sensirion SGP40
(`datasheet <https://sensirion.com/media/documents/296373BB/6203C5DF/Sensirion_Gas_Sensors_Datasheet_SGP40.pdf>`__) or SGP41
(`datasheet <https://sensirion.com/media/documents/5FE8673C/61E96F50/Sensirion_Gas_Sensors_Datasheet_SGP41.pdf>`__) with ESPHome.
The type of sensor used is automatically detected.
The :ref:`I²C Bus <i2c>` is required to be set up in your configuration for this sensor to work.

.. note::

    This sensor need to be driven at a rate of 1Hz. Because of this, the
    sensor will be read out on device once a second separately from the
    update_interval.  The state will be reported to other components, or
    the front end at the update_interval, saving wifi power and network
    communication.

.. figure:: images/sgp40.jpg
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: sgp4x
        voc:
          name: "VOC Index"
        nox:
          name: "NOx Index"


Configuration variables:
------------------------

- **voc** (*Optional*): VOC Index

  - **algorithm_tuning** (*Optional*): The VOC algorithm can be customized by tuning 6 different parameters. For more details see `Engineering Guidelines for SEN5x <https://sensirion.com/media/documents/25AB572C/62B463AA/Sensirion_Engineering_Guidelines_SEN5x.pdf>`__

    - **index_offset** (*Optional*): VOC index representing typical (average) conditions. Allowed values are in range 1..250. The default value is 100.
    - **learning_time_offset_hours** (*Optional*): Time constant to estimate the VOC algorithm offset from the history in hours. Past events will be forgotten after about twice the  learning time. Allowed values are in range 1..1000. The default value is 12 hour
    - **learning_time_gain_hours** (*Optional*): Time constant to estimate the VOC algorithm gain from the history in hours. Past events will be forgotten after about twice the learning time. Allowed values are in range 1..1000. The default value is 12 hours.
    - **gating_max_duration_minutes** (*Optional*): Maximum duration of gating in minutes (freeze of estimator during high VOC index signal). Zero disables the gating. Allowed values are in range 0..3000. The default value is 180 minutes
    - **std_initial** (*Optional*): Initial estimate for standard deviation. Lower value boosts events during initial learning period, but may result in larger device-todevice variations. Allowed values are in range 10..5000. The default value is 50.
    - **gain_factor** (*Optional*): Gain factor to amplify or to attenuate the VOC index output. Allowed values are in range 1..1000. The default value is 230.


  - All other options from :ref:`Sensor <config-sensor>`.

- **nox** (*Optional*): NOx Index. Only available with SGP41. If a SGP40 sensor is detected this sensor will be ignored

  - **algorithm_tuning** (*Optional*): The NOx algorithm can be customized by tuning 5 different parameters.For more details see `Engineering Guidelines for SEN5x <https://sensirion.com/media/documents/25AB572C/62B463AA/Sensirion_Engineering_Guidelines_SEN5x.pdf>`__

    - **index_offset** (*Optional*): NOx index representing typical (average) conditions. Allowed values are in range 1..250. The default value is 100.
    - **learning_time_offset_hours** (*Optional*): Time constant to estimate the NOx algorithm offset from the history in hours. Past events will be forgotten after about twice the  learning time. Allowed values are in range 1..1000. The default value is 12 hour
    - **learning_time_gain_hours** (*Optional*): Time constant to estimate the NOx algorithm gain from the history in hours. Past events will be forgotten after about twice the learning time. Allowed values are in range 1..1000. The default value is 12 hours.
    - **gating_max_duration_minutes** (*Optional*): Maximum duration of gating in minutes (freeze of estimator during high NOx index signal). Zero disables the gating. Allowed values are in range 0..3000. The default value is 180 minutes
    - **std_initial** (*Optional*): The initial estimate for standard deviation parameter has no impact for NOx. This parameter is still in place for consistency reasons with the VOC tuning parameters command. This parameter must always be set to 50.
    - **gain_factor** (*Optional*): Gain factor to amplify or to attenuate the VOC index output. Allowed values are in range 1..1000. The default value is 230.

  - All other options from :ref:`Sensor <config-sensor>`.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``
- **store_baseline** (*Optional*, boolean): Stores and retrieves the baseline information for quicker startups. Defaults to ``true``

- **compensation** (*Optional*): The block containing sensors used for compensation. If not set defaults will be used.

  - **temperature_source** (*Optional*, :ref:`config-id`): Give an external temperature sensor ID
    here. This can improve the sensor's internal calculations. Defaults to ``25``

  - **humidity_source** (*Optional*, :ref:`config-id`): Give an external humidity sensor ID
    here. This can improve the sensor's internal calculations. Defaults to ``50``


Example With Compensation
-------------------------
.. code-block:: yaml

    # Example configuration entry
    sensor:
    - platform: sgp4x
      voc:
        name: "VOC Index"
      nox:
        name: "NOx Index"
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
- :doc:`sht4x`
- :apiref:`sgp4x/sgp4x.h`
- :ghedit:`Edit`
