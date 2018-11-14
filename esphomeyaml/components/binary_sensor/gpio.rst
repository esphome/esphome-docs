GPIO Binary Sensor
==================

.. seo::
    :description: Instructions for setting up GPIO binary sensors with esphomelib.
    :image: pin.svg

The GPIO Binary Sensor platform allows you to use any input pin on your
device as a binary sensor.

.. figure:: images/gpio-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: gpio
        pin: D2
        name: "Living Room Window"
        device_class: window

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to periodically check.
- **name** (**Required**, string): The name of the binary sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`
  and :ref:`MQTT Component <config-mqtt-component>`.

.. note::

    For some applications such as reed switches you need to set the pin mode to ``INPUT_PULLUP``
    like this:

    .. code:: yaml

        binary_sensor:
          - platform: gpio
            pin:
              number: D2
              mode: INPUT_PULLUP
            name: ...

Inverting Values
----------------

Use the ``inverted`` property of the :ref:`Pin Schema <config-pin_schema>` to invert the binary
sensor:

.. code:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: gpio
        pin:
          number: D2
          inverted: True
        name: ...

Debouncing Values
-----------------

Some binary sensors are a bit unstable and quickly transition between the ON and OFF state while
they're pressed. To fix this and debounce the signal, use the :ref:`binary sensor filters <binary_sensor-filters>`:

.. code:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: gpio
        pin: D2
        name: ...
        filters:
          - delayed_on: 10ms

Above example will only make the signal go high if the button has stayed high for more than 10ms.
Alternatively, below configuration will make the binary sensor publish an ON value immediately, but
will wait 10ms before publishing an OFF value:

.. code:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: gpio
        pin: D2
        name: ...
        filters:
          - delayed_off: 10ms

See Also
--------

- :doc:`/esphomeyaml/components/binary_sensor/index`
- :ref:`config-pin_schema`
- :doc:`API Reference </api/binary_sensor/gpio>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/gpio.rst>`__

.. disqus::
