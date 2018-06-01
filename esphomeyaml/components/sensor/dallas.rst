Dallas Temperature Sensor
=========================

The ``dallas`` sensor allows you to define sensors for you :doc:`dallas sensor hub </esphomeyaml/components/dallas>`.

To initialize a sensor, first supply either ``address`` **or** ``index`` to identify the sensor.

.. figure:: images/ds18b20-full.jpg
    :align: center
    :target: `Adafruit`_
    :width: 50.0%

    DS18b20 One-Wire Temperature Sensor. Image by `Adafruit`_.

.. _Adafruit: https://www.adafruit.com/product/374

.. figure:: images/temperature.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    dallas:
      - id: dallas_hub1
        pin: 23

    # Individual sensors
    sensor:
      - platform: dallas
        dallas_id: "dallas_hub1"
        address: 0x1C0000031EDD2A28
        index: 0
        name: "Living Room Temperature"

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **address** (**Required**, int): The address of the sensor. Use either
  this option or index.
- **index** (**Required**, int): The index of the sensor starting with 0.
  So the first sensor will for example have index 0. :ref:`It’s recommended
  to use address instead <dallas-getting-ids>`.
- **resolution** (*Optional*, int): An optional resolution from 8 to
  12. Higher means more accurate. Defaults to the maximum for most dallas temperature sensors: 12.
- **dallas_id** (*Optional*, :ref:`config-id`): The ID of the :doc:`dallas hub </esphomeyaml/components/dallas>`.
  Use this if you have multiple dallas hubs.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

.. _dallas-getting-ids:

Getting Sensor IDs
~~~~~~~~~~~~~~~~~~

It is highly recommended to use the ``address`` attribute for creating
dallas sensors, because if you have multiple sensors on a bus and the
automatic sensor discovery fails, all sensors indices will be shifted by
one. In order to get the address, simply start the firmware on your
device with a configured dallas hub and observe the log output (the :ref:`log
level <logger-log_levels>` must be set to at least
``debug``!). You will find something like this:

.. figure:: images/dallas-log.png

Next, individually warm up or cool down the sensors and observe the log
output to determine which address points to which sensor.

See Also
^^^^^^^^

- :ref:`sensor-filters`
- :doc:`/esphomeyaml/components/dallas`
- :doc:`max6675`
- :doc:`API Reference </api/sensor/dallas>`
