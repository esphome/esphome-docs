Non-Invasive Power Meter
========================

.. seo::
    :description: Instructions for hacking your power meter at home to measure your power usage.
    :image: power_meter.jpg

So an essential part of making your home smart is knowing how much power it uses over
the day. Tracking this can be difficult, often you need to install a completely new
power meter which can often cost a bunch of money. However, quite a few power meters
have a red LED on the front that blinks every time that one Wh has been used.

The simple idea therefore is: Why don't we just abuse that functionality to make the power-meter
IoT enabled? We just have to hook up a simple photoresistor in front of that aforementioned
LED and track the amount of pulses we receive. Then using esphomelib we can instantly have
the power meter show up in Home Assistant 🎉

Hooking it all up is quite easy: Just buy a suitable photoresistor (make sure the wave length
approximately matches the one from your power meter). Then connect it using a simple variable
resistor divider (see `this article <https://blog.udemy.com/arduino-ldr/>`__ for inspiration).
And... that should already be it :)

.. figure:: images/power_meter-header.jpg
    :align: center
    :width: 80.0%

For esphomelib, you can then use the
:doc:`pulse counter sensor </esphomeyaml/components/sensor/pulse_counter>` using below configuration:

.. code-block:: yaml

    sensor:
      - platform: pulse_counter
        pin: GPIO12
        unit_of_measurement: 'kW'
        name: 'Power Meter'
        filters:
          - multiply: 0.06

Adjust ``GPIO12`` to match your set up of course. The output from the pulse counter sensor is in
``pulses/min`` and we also know that 1000 pulses from the LED should equal 1kWh of power usage.
Thus, rearranging the expression yields a proportional factor of ``0.06`` from ``pulses/min`` to
``kW``.

And if a technician shows up and he looks confused about what the heck you have done to your
power meter, tell them about esphomelib 😉

.. note::

    Photoresistors often have a bit of noise during their switching phases. So in certain situations,
    a single power meter tick can result in many pulses being counted. This effect is especially big on
    ESP8266s. If you're experiencing this, try enabling the ``internal_filter:`` filter option:

    .. code-block:: yaml

        sensor:
          - platform: pulse_counter
            # ...
            internal_filter: 10us

See Also
--------

- :doc:`/esphomeyaml/components/sensor/pulse_counter`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/cookbook/power_meter.rst>`__

.. disqus::
