Dallas Temperature Sensor
=========================

.. seo::
    :description: Instructions for setting up Dallas temperature sensor hubs that can
      expose many temperature sensors on a single pin using the 1-Wire protocol.  Also
      supports the max31850 onewire thermocouple amplifier.
    :image: dallas.jpg
    :keywords: Dallas, ds18b20, onewire, max31850

.. _dallas-component:

Component/Hub
-------------

The ``dallas`` component allows you to use your
`DS18b20 <https://www.adafruit.com/product/374>`__
(`datasheet <https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf>`__)
and similar 1-Wire temperature sensors.

To use your :ref:`dallas sensor <dallas-sensor>`, first define a dallas “hub” with a pin and
id, which you will later use to create the sensors. The 1-Wire bus the
sensors are connected to should have an external pullup resistor of
about 4.7KΩ. For this, connect a resistor of *about* 4.7KΩ between ``3.3V``
and the data pin. Values ± 1KΩ will, in most cases, work fine as well,
if you don't have massively long wires.

.. code-block:: yaml

    # Example configuration entry
    dallas:
      - pin: 23

    # Individual sensors
    sensor:
      - platform: dallas
        address: 0x1c0000031edd2a28
        name: "Livingroom Temperature"

Configuration variables:
************************

- **pin** (**Required**, number): The pin the sensor bus is connected to. Please note that 1-wire 
  is a bi-directional bus so it requires both input and output from the pin.
- **update_interval** (*Optional*, :ref:`config-time`): The interval that the sensors should be checked.
  Defaults to 60 seconds.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _dallas-sensor:

Sensor
------

The ``dallas`` sensor allows you to use DS18B20 and similar sensors.
First, you need to define a :ref:`dallas sensor component <dallas-component>`.
The dallas sensor component (or "hub") is an internal model that defines which pins the DS18B20
sensors are connected to. This is because with these sensors you can actually connect multiple
sensors to a single pin (the onewire bus) and use them all at once.

To initialize a sensor, first supply either ``address`` **or** ``index`` to identify the sensor.

.. figure:: images/dallas-wired.jpg
    :align: center
    :width: 50.0%

    Wired Version of the DS18B20 1-Wire Temperature Sensor.

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

      # MAX31850 thermocouple
      - platform: dallas
        address: 0x082d4c0f49858c3b
        name: "Thermocouple Temperature"
        max31850: true

Configuration variables:
************************

- **address** (**Required**, int): The address of the sensor. Use either
  this option or index.
- **index** (**Required**, int): The index of the sensor starting with 0.
  So the first sensor will for example have index 0. :ref:`It’s recommended
  to use address instead <dallas-getting-ids>`.
- **resolution** (*Optional*, int): An optional resolution from 9 to
  12. Higher means more accurate. Defaults to the maximum for most Dallas temperature sensors: 12.
- **dallas_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`dallas hub <dallas-component>`.
  Use this if you have multiple dallas hubs.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **max31850** (*Optional*, boolean): Override the sensor type from the DS1825 to the MAX31850.
  Defaults to false.
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

<<<<<<< HEAD
Multiple dallas hubs
********************

Use this if you have multiple dallas hubs:

.. code-block:: yaml

    # Example configuration entry
    dallas:
      - pin: GPIO23
        id: hub_1
      - pin: GPIO24
        id: hub_2

    sensor:
      - platform: dallas
        dallas_id: hub_1
        # ...
      - platform: dallas
        dallas_id: hub_2
        # ...

=======
About the MAX31850
******************

The `MAX31850 <https://www.analog.com/media/en/technical-documentation/data-sheets/max31850-max31851.pdf>`
is a cold-junction compensated, onewire thermocouple-to-digital converter that performs
cold-junction compensation and digitizes the signal from a K-, J-, N-, T-, S-, R-, or
E-type thermocouple.  The reported onewire model ID of this chip overloads the value used
by the DS1825 chip, allowing the majority of the runtime firmware code to be reused.
The MAX31850 chip can also detect and report faults for the thermocouple junction,
including opens and shorts, that would typically indicate the juntion has failed
(such as it melted).  These faults show up to Home Assistant as an "unknown" sensor
value and are reported to the ESPHome log as ESP_LOGE errors. 
>>>>>>> dd5ed8cb (Added documentation for adding the MAX31850 to the Dallas)

See Also
--------

- :ref:`sensor-filters`
- :doc:`max6675`
- `Arduino DallasTemperature library <https://github.com/milesburton/Arduino-Temperature-Control-Library>`__
  by `Miles Burton <https://github.com/milesburton>`__
- :apiref:`dallas/dallas_component.h`
- :ghedit:`Edit`
