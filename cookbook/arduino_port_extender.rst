Arduino Port Extender
=====================

.. seo::
    :description: Instructions on using an Arduino board, like the Pro Mini for extending ports of a ESPHome node
    :image: arduino_pro_mini.jpg
    :keywords: Arduino port extender ESPHome

The Arduino is a widely used microcontroller, easy to use and accesible.
With this sketch you can use any compatible Arduino board with ESPHome and read and write pins.


.. figure:: images/arduino_pro_mini.jpg
    :align: center
    :width: 75.0%


The Arduino is connected to the ESP via I²C. Most Arduinos use the ``A4`` and ``A5`` pins for the I²C bus
so those pins are not available to read from ESPHome.
It is recommended to use a 3.3V I/O level Arduino, however using 5V Arduinos seems to work too. In the latter
case you should power your 5V Arduino with 3.3V otherwise you will need a level converter for the
I²C bus.

Currently it is supported:

    - reading digital inputs
    - reading analog inputs
    - writing digital outputs

The Arduino sketch can be retrieved from `Here <https://github.com/glmnet/esphome_devices/tree/master/ArduinoPortExtender/src>`__

You need to download `ape.h <https://github.com/glmnet/esphome_devices/blob/master/ape.h>`__ and include the ape.h in the ESPHome configuration.

.. code-block:: yaml

    esphome:
      ...
      includes:
          - ape.h

Setup your :ref:`I²C Bus <i2c>` and assign it an ``id``:

.. code-block:: yaml

 i2c:
   id: i2c_component

By default ESP8266 uses ``SDA`` pin ``GPIO4`` which you need to connect to Arduino's ``A4`` and the ``SCL``
is ``GPIO5`` which goes to Arduino's ``A5``.

Then create a ``custom_component``, this will be the main component we will be referencing later when creating
individual IOs.

.. code-block:: yaml

  custom_component:
    - id: ape
      lambda: |-
        auto ape_component = new ArduinoPortExtender(i2c_component, 0x08);
        return {ape_component};

By default the I²C address is ``0x08`` but you can change it on the arduino sketch so you can have more slaves
on the same bus.

Now it is time to add the ports

Binary_Sensor
-------------

When adding binary sensors the pins are configured as INPUT_PULLUP, you can use any PIN from 0 to 13 or
``A0`` to ``A3`` (``A4`` and ``A5`` are used for I²C and ``A6`` and ``A7`` do not support internal pull up)

.. note::

    Arduino PIN 13 usually has a LED conected to it and using it as digital input with the built in internal
    pull up might be problematic, using it as an output is preferred.

To setup binary sensors, create a custom platform as below, list in braces all the sensors you want,
in the example below two binary sensors are declared on pin 9 and A0 (number 14)

Then declare the ESPHome reference of the binary sensor in the same order as declared in the lambda:

.. code-block:: yaml

  binary_sensor:
    - platform: custom
      lambda: |-
        return {ape_binary_sensor(ape, 9),
                ape_binary_sensor(ape, 14) // 14 = A0
                };

      binary_sensors:
        - id: binary_sensor_pin2
          name: Binary sensor pin 2
        - id: binary_sensor_pin3
          name: Binary sensor pin 3
          on_press:
            ...

The listed `binary_sensors` supports all options from :ref:`Binary Sensor <config-binary_sensor>` like
automations and filters.

Sensor
------

Sensors allows for reading the analog value of an analog pin, those are from ``A0`` to ``A7`` except for
``A4`` and ``A5``. The value returned goes from 0 to 1023 (the value returned by the arduino ``analogRead``
function).

Arduino analog inputs measures voltage. By default the sketch is configured to use the Arduino internal VREF
comparer setup to 1 volt, so voltages bigger are read as 1023. You can configure Arduino to compare the
voltage to VIN voltage, this voltage might be 5 volts or 3.3 volts, depending on how you are powering it. To
do so, pass an additional true value to the hub constructor:

``auto ape_component = new ArduinoPortExtender(i2c_component, 0x08, true);``

To setup sensors, create a custom platform as below, list in braces all the sensors you want,
in the example below two sensors are declared on pin ``A1`` and ``A2``

Then declare the ESPHome reference of the sensor in the same order as declared in the lambda:

.. code-block:: yaml

  sensor:
    - platform: custom
      lambda: |-
        return {ape_analog_input(ape, 1),  // 1 = A1
                ape_analog_input(ape, 2)};
      sensors:
        - name: Analog A1
          id: analog_a1
          filters:
            - throttle: 1s
        - name: Analog A2
          id: analog_a2
          filters:
            - throttle: 2s

The listed ``sensors`` supports all options from :ref:`Sensor <config-sensor>` like
automations and filters.

.. note::

  Sensors are polled by default every loop cycle so it is recommended to use the ``throttle`` filter
  to not flood the network.

Output
------

Arduinos binary outputs are supported in pins from 0 to 13.

To setup outputs, create a custom platform as below, list in braces all the outputs you want,
in the example below two outputs are declared on pin ``3`` and ``4``

.. code-block:: yaml

  output:
  - platform: custom
    type: binary
    lambda: |-
      return {ape_binary_output(ape, 3),
              ape_binary_output(ape, 4)};
    outputs:
      - id: output_pin_3
        inverted: true
      - id: output_pin_4
        inverted: true

  switch:
    - platform: output
      name: Switch pin 3
      output: output_pin_3

  light:
    - platform: binary
      name: Switch pin 4
      output: output_pin_4

See Also
--------

- :doc:`/devices/nodemcu_esp8266`
- :ghedit:`Edit`
