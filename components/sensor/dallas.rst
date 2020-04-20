Dallas Temperature Sensor
=========================

.. seo::
    :description: Instructions for setting up dallas temperature sensor hubs that can
      expose many temperature sensors on a single pin using the one wire protocol.
    :image: dallas.jpg
    :keywords: Dallas, ds18b20, onewire

.. _dallas-component:

Component/Hub
-------------

The ``dallas`` component allows you to use your
`DS18b20 <https://www.adafruit.com/product/374>`__
(`datasheet <https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf>`__)
and similar One-Wire temperature sensors.

To use your :ref:`dallas sensor <dallas-sensor>`, first define a dallas “hub” with a pin and
id, which you will later use to create the sensors. The 1-Wire bus the
sensors are connected to should have an external pullup resistor of
about 4.7KΩ. For this, connect a resistor of *about* 4.7KΩ (values around that like 1Ω will, if you don't have
massively long wires, work fine in most cases) between ``3.3V`` and the data pin.

.. code-block:: yaml

    # Example configuration entry
    dallas:
      - pin: 23

Configuration variables:
************************

- **pin** (**Required**, number): The pin the sensor bus is connected to.
- **update_interval** (*Optional*, :ref:`config-time`): The interval that the sensors should be checked.
  Defaults to 60 seconds.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **auto_setup_sensors** (*Optional*, boolean): Instruct the hub component to automatically setup and 
  configure discovered Dallas sensors. See :ref:`dallas-auto_setup_sensors`.
  Defaults to ``False``
- **sensor_name_template** (*Optional*, string): Automatically generated sensors will dynamically receive 
  a ``name`` formatted through this format string ( See c std library ``printf`` for syntax).
  The internal hub code provides 2 arguments to the printf expression: the node name and the sensor hex address.
  Deafults to '%s.%s'
- **resolution** (*Optional*, int): An optional resolution for automatically generated sensors. 
  Defaults to the maximum for most Dallas temperature sensors: 12.
- **unit_of_measurement** (*Optional*, string): Manually set the unit
  of measurement the automatically generated sensor should advertise its values with. This does
  not actually do any maths (conversion between units).
  Defaults to '°C'
- **icon** (*Optional*, icon): Manually set the icon to use for the sensor in the frontend.
  Defaults to 'mdi:thermometer'
- **accuracy_decimals** (*Optional*, int): Manually set the accuracy of decimals to use when reporting values.
  Defaults to 1

.. _dallas-sensor:

Sensors
-------

The ``dallas`` sensor allows you to use ds18b20 and similar sensors.
First, you need to define a :ref:`dallas sensor component <dallas-component>`.
The dallas sensor component (or "hub") is an internal model that defines which pins the ds18b20
sensors are connected to. This is because with these sensors you can actually connect multiple
sensors to a single pin and use them all at once.

To initialize a sensor, first supply either ``address`` **or** ``index`` to identify the sensor.

.. figure:: images/dallas-wired.jpg
    :align: center
    :width: 50.0%

    Wired Version of the DS18b20 One-Wire Temperature Sensor.

.. _Adafruit: https://www.adafruit.com/product/374

.. figure:: images/temperature.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    dallas:
      - pin: GPIO23

    # Individual sensors
    sensor:
      - platform: dallas
        address: 0x1C0000031EDD2A28
        name: "Living Room Temperature"

Configuration variables:
************************

- **address** (**Required**, int): The address of the sensor. Use either
  this option or index.
- **index** (**Required**, int): The index of the sensor starting with 0.
  So the first sensor will for example have index 0. :ref:`It’s recommended
  to use address instead <dallas-getting-ids>`.
- **resolution** (*Optional*, int): An optional resolution from 8 to
  12. Higher means more accurate. Defaults to the maximum for most dallas temperature sensors: 12.
- **dallas_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`dallas hub <dallas-component>`.
  Use this if you have multiple dallas hubs.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

.. _dallas-getting-ids:

Getting Sensor IDs
******************

It is highly recommended to use the ``address`` attribute for creating
dallas sensors, because if you have multiple sensors on a bus and the
automatic sensor discovery fails, all sensors indices will be shifted by
one. In order to get the address, simply start the firmware on your
device with a configured dallas hub and observe the log output (the :ref:`log
level <logger-log_levels>` must be set to at least
``debug``!). Note that you don't need to define the individual sensors just yet, as
the scanning will happen even with no sensors connected. For example with this configuration:

.. code-block:: yaml

    # Example configuration entry
    dallas:
      - pin: GPIO23

    # Note you don't have to add any sensors at this point

You will find something like this:

.. figure:: images/dallas-log.png

Now we can add the individual sensors to our configuration:

.. code-block:: yaml

    # Example configuration entry
    dallas:
      - pin: GPIO23

    sensor:
      - platform: dallas
        address: 0xA40000031F055028
        name: "Temperature #1"
      - platform: dallas
        address: 0xDD0000031EFB0428
        name: "Temperature #2"
      - platform: dallas
        # ...

Next, individually warm up or cool down the sensors and observe the log again.
You will see the outputted sensor values changing when they're being warmed.
When you're finished mapping each address to a name, just change the ``Temperature #1``
to your assigned names and you should be ready.

.. _dallas-auto_setup_sensors:

Automatic Sensors Setup
***********************

You would normally setup your sensors by explicitly declaring them with their `address`
according to the :ref:`dallas-sensor` section. This way you have to know the
specific sensor address to configure beforehand (or by using the debug log exposed by the 
`dallas` hub - See :ref:`dallas-getting-ids`). The option to use the sensor `index` too 
is not reliable as stated in the section.
With automatic sensor setup instead you will not need any address information beforehand since
the dallas hub component will automatically instantiate every sensor attached to the bus during 
the initial discovery process. This way you can attach any sensor to the bus and see it inside 
the fontend as soon as the node initializes itself (during boot then - no hot-plug here!).
The sensors generated through this model will receive a default setup as configured 
in :ref:`dallas-component`. The relevant option here is `sensor_name_template` which allows for a
dynamically generated sensor name according to the format string provided. The formatting function
receives two string arguments (c code here): the `device_name` of the EspHome node and 
the hex `address` of the discovered sensor

.. code-block:: yaml

    # Example configuration entry
    dallas:
      - pin: GPIO1
        auto_setup_sensors: true
        sensor_name_template: '%s.Temperature %s'
        resolution: 9

This code block example shows how to provide a basic configuration. Every sensor here will
be set to a 9 bit resolution and the name following the example would be something like
'my_awesome_node.Temperature BE0316838979FF28'.
Automatically detected sensors will not conflict with static ones configured in 
:ref:`Sensor <dallas-sensor>`. If during initialization any sensor address matches a 
configured one through :ref:`Sensor <dallas-sensor>` the latter configuration will prevail. This way
you can still provide custom settings (i.e. filters or so) for very specific sensors.

See Also
--------

- :ref:`sensor-filters`
- :doc:`max6675`
- `Arduino DallasTemperature library <https://github.com/milesburton/Arduino-Temperature-Control-Library>`__
  by `Miles Burton <https://github.com/milesburton>`__
- :apiref:`dallas/dallas_component.h`
- :ghedit:`Edit`
