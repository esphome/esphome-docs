SGP40 Volatile Organic Compound Sensor and SGP41 VOC and NOx Sensor
===================================================================

.. seo::
    :description: Instructions for setting up SGP40/SGP41 Volatile Organic Compound and NOx sensor
    :image: sgp40.jpg

The ``sgp4x`` sensor platform allows you to use your Sensirion SGP40 
(`SGP40 datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Sensirion_Gas_Sensors_SGP40_Datasheet.pdf>`__) or SGP41 
(`SGP41 datasheet <https://sensirion.com/media/documents/5FE8673C/61E96F50/Sensirion_Gas_Sensors_Datasheet_SGP41.pdf>`__) with ESPHome.
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
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
  - All other options from :ref:`Sensor <config-sensor>`.

- **nox** (*Optional*): NOx Index. Only available with SGP41. If a SGP40 sensor is detected this sensor will be ignored
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
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

- :doc:`sgp40`
- :ref:`sensor-filters`
- :doc:`dht`
- :doc:`dht12`
- :doc:`hdc1080`
- :doc:`htu21d`
- :doc:`sht3xd`
- :doc:`sht4x`
- :apiref:`sgp4x/sgp4x.h`
- :ghedit:`Edit`
