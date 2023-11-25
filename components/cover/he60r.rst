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

A sample configuration entry is here (this corresponds to the sample circuit below.) Pin numbers should be specified
to match your hardware configuration. The TX pin is inverted in this configuration since the sample circuit
uses an inverting transistor driver to send data.

.. code-block:: yaml

    # Example configuration entry

    uart:
      - id: door_uart
        baud_rate: 1200
        parity: even
        stop_bits: 1
        tx_pin:
          number: 23
          inverted: true
        rx_pin: 22

    cover:
      platform: he60r
      id: garage_door
      name: Garage Door
      open_duration: 14s
      close_duration: 14s

    binary_sensor:
      - platform: gpio
        pin:
          number: 14
          mode:
            input: true
            pullup: true
        name: "Garage Door Button"
        filters:
          - delayed_on: 50ms
          - delayed_off: 50ms
        on_press:
          then:
            - cover.toggle: garage_door


Hardware Connection
-------------------

This component makes use of the HE60R keypad communication interface. This is a single-wire half duplex serial
connection. A sample circuit is shown below which also draws power from the HE60R - note that the 3.3V regulator must
be a switching type, a linear regulator will draw too much current and run hot. You can of course simply power
the ESP32 via USB from 5V.


.. figure:: images/he60r-sch.jpg


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the cover.
- **open_duration** (*Optional*, :ref:`config-time`): The time required for the door to fully open from the closed position.
- **close_duration** (*Optional*, :ref:`config-time`): The time required for the door to fully close from the open position.
- All other options from :ref:`Cover <config-cover>`.


See Also
--------

- :doc:`index`
- :ref:`automation`
- :ghedit:`Edit`
