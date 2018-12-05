Ultrasonic Distance Sensor
==========================

.. seo::
    :description: Instructions for setting up ultrasonic distance measurement sensors in esphomelib.
    :image: ultrasonic.jpg
    :keywords: ultrasonic, hc-sr04

The ultrasonic distance sensor allows you to use simple ultrasonic
sensors like the HC-SR04
(`datasheet <https://www.electroschematics.com/wp-content/uploads/2013/07/HC-SR04-datasheet-version-2.pdf>`__,
`sparkfun <https://www.sparkfun.com/products/13959>`__) with esphomelib
to measure distances. These sensors usually can’t measure anything more
than about two meters and may sometimes make some annoying clicking
sounds.

This sensor platform expects a sensor that can be sent a **trigger
pulse** on a specific pin and will send out a **echo pulse** once a
measurement has been taken. Because sometimes (for example if no object
is detected) the echo pulse is never returned, this sensor also has a
timeout option which specifies how long to wait for values. During this
timeout period the whole core will be blocked and therefore shouldn't be
set too high.

.. figure:: images/ultrasonic-full.jpg
    :align: center
    :width: 50.0%

    HC-SR04 Ultrasonic Distance Sensor.

.. figure:: images/ultrasonic-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: ultrasonic
        trigger_pin: D1
        echo_pin: D2
        name: "Ultrasonic Sensor"

Configuration variables:
------------------------

- **trigger_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The output pin to
  periodically send the trigger pulse to.
- **echo_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The input pin on which to
  wait for the echo.
- **name** (**Required**, string): The name of the sensor.
- **timeout_meter** (*Optional*, float): The number of meters for the
  timeout. Use either this or ``timeout_time``. Defaults to 2 meters.
- **timeout_time** (*Optional*, int): The number of microseconds for
  the timeout. Use either this or ``timeout_meter``. Defaults to
  11662µs.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``15s``. See :ref:`sensor-default_filter`.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

Ultrasonic Timeouts
-------------------

The ultrasonic sensor works by sending a small ultrasonic pulse out and then waiting until
the pulse arrives back. However, there are cases where no such signal arrives back. This is most commonly caused
by either having the sensor pointed at a soft surface that muffles the incoming signal. The other case where this
can happen is when the the object is too far away and the timeout set by the ``timeout_meter`` or ``timeout_time``
option kicks in.

To remove ``NAN`` values from the sensor stream, use the ``filter_nan`` :ref:`sensor filter <sensor-filters>`:

.. code-block:: yaml

    sensor:
      - platform: ultrasonic
        trigger_pin: D1
        echo_pin: D2
        name: "Ultrasonic Sensor"
        filters:
          -


See Also
--------

- :ref:`sensor-filters`
- :doc:`template`
- :doc:`API Reference </api/sensor/ultrasonic>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/ultrasonic.rst>`__

.. disqus::
