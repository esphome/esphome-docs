HE60R Garage Door Opener
========================

.. seo::
    :description: Setting up a Chamberlain HomEntry HE60R and similar garage door openers
    :image: he60r.jpg

.. figure:: images/he60r.jpg
    :align: right

The ``he60r`` cover platform allows you to control a HomEntry HE60R
garage door opener. These units were made by Chamberlain and sold through Bunnings. It is *likely* that this
component will also work with other older Chamberlain garage door openers. It is not currently compatible with
newer Chamberlain units that use the Security+ 2.0 protocol.

This component makes use of the HE60R keypad communication interface. This is a single-wire half duplex serial
connection and requires a :ref:`uart` component to be configured. The uart **must** be set to 1200 baud, EVEN parity. See
below for a sample hardware interface.

.. code-block:: yaml

    # Example configuration entry

    uart:
      - id: door_uart
        baud_rate: 1200
        parity: even
        stop_bits: 1
        tx_pin: GPIOXX
        rx_pin: GPIOXX

    cover:
      platform: he60r
      id: garage_door
      name: Garage Door


Configuration variables:
------------------------

- **open_duration** (*Optional*, :ref:`config-time`): The time required for the door to fully open from the closed position. Default 15s.
- **close_duration** (*Optional*, :ref:`config-time`): The time required for the door to fully close from the open position. Default 15s.
- All other options from :ref:`Cover <config-cover>`.

The open and close duration serve to estimate the position to provide feedback during travel and for partial open/close
requests. These can be adjusted according to your door's actual operation. Enabling DEBUG logging will report the
actual open and close times which will help to refine these timings.

Hardware Connection
-------------------

A sample circuit is shown below which also draws power from the HE60R - note that the 3.3V regulator must
be a switching type, a linear regulator would draw too much current and run hot. You can of course simply power
the ESP32 via USB from 5V. This circuit also includes a manual control button connected to a GPIO.

Any microcontroller board supported by ESPHome should be suitable for this application.


.. figure:: images/he60r-sch.jpg
    :target: /_images/he60r-sch.jpg


Note that this circuit inverts the TX line. A configuration for this would look something like:

.. code-block:: yaml

    # Example configuration entry

    uart:
      - id: door_uart
        baud_rate: 1200
        parity: even
        stop_bits: 1
        tx_pin:
          number: GPIOXX
          inverted: true
        rx_pin: GPIOXX

    cover:
      platform: he60r
      id: garage_door
      name: Garage Door

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIOXX
          inverted: true
          mode:
            input: true
            pullup: true
        name: "Garage Door Manual Button"
        # debounce the switch
        filters:
          - delayed_on: 50ms
          - delayed_off: 50ms
        on_press:
          then:
            - cover.toggle: garage_door



See Also
--------

- :doc:`index`
- :ref:`automation`
- :ref:`gpio-binary-sensor`
- :ghedit:`Edit`
