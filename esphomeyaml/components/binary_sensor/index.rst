Binary Sensor Component
=======================

With esphomelib you can use different types of binary sensors. They will
automatically appear in the Home Assistant front-end and have several
configuration options.


.. _config-binary_sensor:

Base Binary Sensor Configuration
--------------------------------

All binary sensors have a platform and an optional device class. By
default, the binary will chose the appropriate device class itself, but
you can always override it.

.. code:: yaml

    binary_sensor:
      - platform: ...
        device_class: motion

Configuration variables:

- **device_class** (*Optional*, string): The device class for the
  sensor. See https://www.home-assistant.io/components/binary_sensor/
  for a list of available options.
- **filters** (*Optional*, list): A list of filters to apply on the binary sensor values such as
  inverting signals. See :ref:`binary_sensor-filters`.

Automations:

- **on_press** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the button is pressed. See :ref:`binary_sensor-on_press`.
- **on_release** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the button is released. See :ref:`binary_sensor-on_release`.
- **on_click** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the button is held down for a specified period of time.
  See :ref:`binary_sensor-on_click`.
- **on_double_click** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the button is pressed twice for specified periods of time.
  See :ref:`binary_sensor-on_double_click`.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

.. _binary_sensor-filters:

Binary Sensor Filters
---------------------

With binary sensor filters you can customize how esphomelib handles your binary sensor values even more.
They are similar to :ref:`Sensor Filters <sensor-filters>`.

.. code:: yaml

    binary_sensor:
      - platform: ...
        # ...
        filters:
          - invert:
          - delayed_on: 100ms
          - delayed_off: 100ms
          - lambda: >-
              if (id(other_binary_sensor).value) {
                return x;
              } else {
                return {};
              }
          - heartbeat: 5s

Supported filters:

- **invert**: Simple filter that just inverts every value from the binary sensor.
- **delayed_on**: When a signal ON is received, wait for the specified time period until publishing
  an ON state. If an OFF value is received while waiting, the ON action is discarded. Or in other words:
  Only send an ON value if the binary sensor has stayed ON for at least the specified time period.
  **Useful for debouncing push buttons**.
- **delayed_off**: When a signal OFF is received, wait for the specified time period until publishing
  an OFF state. If an ON value is received while waiting, the OFF action is discarded. Or in other words:
  Only send an OFF value if the binary sensor has stayed OFF for at least the specified time period.
  **Useful for debouncing push buttons**.
- **lambda**: Specify any :ref:`lambda <config-lambda>` for more complex filters. The input value from
  the binary sensor is ``x`` and you can return ``true`` for ON, ``false`` for OFF, and ``{}`` to stop
  the filter chain.
- **heartbeat**: Periodically send out the last received value from the binary sensor with the given
  interval. All state changes are still immediately published.

Binary Sensor Automation
------------------------

The triggers for binary sensors in esphomeyaml use the lingo from computer mouses. This naming might not
perfectly fit every use case, but at least makes the naming consistent. For example, a ``press`` is triggered
in the first moment when the button on your mouse is pushed down.

You can access the current state of the binary sensor in :ref:`lambdas <config-lambda>` using
``id(binary_sensor_id).value``.

.. _binary_sensor-on_press:

``on_press``
************

This automation will be triggered when the button is first pressed down, or in other words on the leading
edge of the signal.

.. code:: yaml

    binary_sensor:
      - platform: gpio
        # ...
        on_press:
          then:
            - switch.turn_on:
                id: relay_1

Configuration variables: See :ref:`Automation <automation>`.

.. _binary_sensor-on_release:

``on_release``
**************

This automation will be triggered when a button press ends, or in other words on the falling
edge of the signal.

.. code:: yaml

    binary_sensor:
      - platform: gpio
        # ...
        on_release:
          then:
            - switch.turn_off:
                id: relay_1

Configuration variables: See :ref:`Automation <automation>`.

.. _binary_sensor-on_click:

``on_click``
************

This automation will be triggered when a button is pressed down for a time period of length
``min_length`` to ``max_length``. Any click longer or shorter than this will not trigger the automation.
The automation is therefore also triggered on the falling edge of the signal.

.. code:: yaml

    binary_sensor:
      - platform: gpio
        # ...
        on_click:
          min_length: 50ms
          max_length: 350ms
          then:
            - switch.turn_off:
                id: relay_1

Configuration variables:

- **min_length** (*Optional*, :ref:`config-time`): The minimum duration the click should last. Defaults to ``50ms``.
- **max_length** (*Optional*, :ref:`config-time`): The maximum duration the click should last. Defaults to ``350ms``.
- See :ref:`Automation <automation>`.

.. _binary_sensor-on_double_click:

``on_double_click``
*******************

This automation will be triggered when a button is pressed down twice, with the first click lasting between
``min_length`` and ``max_length``. When a second leading edge then happens within ``min_length`` and
``max_length``, the automation is triggered.

.. code:: yaml

    binary_sensor:
      - platform: gpio
        # ...
        on_double_click:
          min_length: 50ms
          max_length: 350ms
          then:
            - switch.turn_off:
                id: relay_1

Configuration variables:

- **min_length** (*Optional*, :ref:`config-time`): The minimum duration the click should last. Defaults to ``50ms``.
- **max_length** (*Optional*, :ref:`config-time`): The maximum duration the click should last. Defaults to ``350ms``.
- See :ref:`Automation <automation>`.

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all binary sensors to do some
advanced stuff (see the full :doc:`API Reference </api/binary_sensor/index>` for more info).

- ``publish_state()``: Manually cause the binary sensor to publish and store a state from anywhere
  in the program.

  .. code:: yaml

      // Within lambda, publish an OFF state.
      id(my_binary_sensor).publish_state(false);

      // Within lambda, publish an ON state.
      id(my_binary_sensor).publish_state(true);

- ``value``: Retrieve the current value of the binary sensor.

  .. code:: yaml

      // Within lambda, get the binary sensor state and conditionally do something
      if (id(my_binary_sensor).value) {
        // Binary sensor is ON, do something here
      } else {
        // Binary sensor is OFF, do something else here
      }


See Also
--------

- :doc:`API Reference </api/binary_sensor/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/index.rst>`__

.. toctree::
    :maxdepth: 1

    gpio
    status
    esp32_ble_tracker
    esp32_touch
    template
    remote_receiver
    pn532
    rdm6300
    nextion

.. disqus::
