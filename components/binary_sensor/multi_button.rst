GPIO Multi Button
==================

.. seo::
    :description: Instructions for setting up a button connected to a GPIO with support for multiple presses and press&hold (or a combination).
    :image: pin.png

The MultiButton component monitors a push-button connected to a GPIO and reports on simple button press(es) / sequences with simple codes.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: multi_button
        name: "Living room media button"
        pin:
          number: 25
          inverted: True
          mode: INPUT_PULLUP
        
For this configuration, the push-button has to be connected to the GPIO 25 on one end and to GND on the other hand. The GPIO's state is normally
high (because of the pull-up) and becomes low if the button is pressed, hence the inversion of the pin's logical level.

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to periodically check.
- **name** (**Required**, string): The name of the binary sensor.
- **debounce** (*Optional*, integer): The time in [ms] a button state needs to be stable to be recognized and not ignored as bouncing
- **timeout** (*Optional*, integer): The timeout in [ms] before an event is recognized and published. A double press must have a smaller pause than this between two presses
- **threshold** (*Optional*, integer): The threshold in [ms] where a normal press becomes a press&hold
- **frequency** (*Optional*, float): The rate in [Hz] (times per second) at which updates are being published during a press&hold
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` (not actually useful).


How it works
---------------------------

The component will register as a normal Sensor in Home Assistant (even though it is more like a binary sensor hardware wise..).

- If the button is pressed shortly once, the sensor state becomes 1 and then 0 again.
- If the button is pressed shortly twice, the sensor state becomes 2 and then 0 again.
- If the button is pressed shortly x times, the sensor state becomes x and then 0 again.
- If the button is pressed and held, the sensor state becomes 101, 102, 103 and so on until the button is released, which resets it to 0 again.
- If the button is pressed shortly once and then immediately pressed and held, the sensor state becomes 201, 202, 203 and so on until the button is released, which resets it to 0 again.
- If the button is pressed shortly x times and then immediately pressed and held, the sensor state becomes 100x+1, 100x+2, 100x+3 and so on until the button is released, which resets it to 0 again.

As an example you could add an automation in Home Assistant to trigger play/pause if the sensor's state changes to 1.
Or increase the playback volume every time the sensor has a value between 101 and 199,
and decrease the playback volume every time the sensor has a value between 201 and 299.

Timing configuration
---------------------------

As described above you can optionally change timings to your likings

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: multi_button
        name: "Living room media button"
        debounce: 30
        timeout: 300
        threshold: 500
        frequency: 2
        pin: 25

Pin configuration
---------------------------

Please refer to :ref:`config-pin_schema` for details on how to configure the pin entry to your needs.
The :doc:`/components/binary_sensor/gpio` has good explanations on this topic.

See Also
--------

- :doc:`/components/binary_sensor/gpio`
- :ref:`config-pin_schema`
- :apiref:`gpio/multi_button/multi_button.h`
- :ghedit:`Edit`
