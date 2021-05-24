Teleinformation from Linky electrical counter.
==============================================

.. seo::
    :description: Instructions for setting up French Teleinformation
    :image: teleinfo.jpg
    :keywords: teleinfo

The ``teleinfo`` component allows you to retrieve data from a 
French electrical counter using Teleinformation (`datasheet <https://www.enedis.fr/sites/default/files/Enedis-NOI-CPT_54E.pdf>`__). It works with Linky electrical
counter but also legacy EDF electrical counter.

.. figure:: images/teleinfo-full.jpg
    :align: center
    :width: 50.0%

    Linky electrical counter

..

A simple electronic assembly with an optocoupler a MOSFET and some resistors lets you retrieve detailed power consumption or power production information.
The following diagram shows an example of a tested circuit that works for both historical and standard mode:

.. figure:: images/teleinfo-circuit.png
    :align: center
    :width: 70.0%

    Circuit example to connect Linky to ESP MCU.

..

As the communication with the Teleinformation is done using UART, you need to
have an :ref:`UART bus <uart>` in your configuration with the ``rx_pin``
connected to the output of the optocoupler component. Additionally, you need to
set the baud rate to 9600bps if counter is configured to work in standard
mode or 1200bps in historical mode.  To find out which mode you are using,
simply press -/+ buttons on the counter and look for `Standard mode` or
`Historical mode` as below.

.. figure:: images/teleinfo-standard.jpg
    :align: center
    :width: 50.0%

    Linky electrical counter configured in standard mode.

..

.. figure:: images/teleinfo-historical.jpg
    :align: center
    :width: 50.0%

    Linky electrical counter configured in historical mode.

..

.. code-block:: yaml

    # Example configuration for historical mode
    uart:
      id: uart_bus
      rx_pin: GPIO3
      baud_rate: 1200
      parity: EVEN
      data_bits: 7

    logger:
      baud_rate: 0 #disable logging over uart

    sensor:
      - platform: teleinfo
        update_interval: 60s
        historical_mode: true
        tags:
         - tag_name: "HCHC"
           sensor:
            name: "hchc"
            unit_of_measurement: "Wh"
            icon: mdi:flash
         - tag_name: "HCHP"
           sensor:
            name: "hchp"
            unit_of_measurement: "Wh"
            icon: mdi:flash
         - tag_name: "PAPP"
           sensor:
            name: "papp"
            unit_of_measurement: "VA"
            icon: mdi:flash


In historical mode Linky provides a set of tags that each contain a corresponding value field (see datasheet link above).

In standard mode Linky also provides several tags that contain not only a value field but an additional timestamp field (again see datasheet for details).
To read out this timestamp instead of the value field of a given tag, simply set the data_class of the corresponding sensor to `timestamp`.

To read both the timestamp *and* the value, create the same `tag_name` twice with different data_classes, as shown in the example below.

*Important:* To interpret Linky timestamps correctly, ESPHome must know the timezone of your system. To provide that you must include the Time component into your node configuration and configure it with the correct `timezone` property (see example).


.. code-block:: yaml

    # Example configuration for standard mode
    uart:
      id: uart_bus
      rx_pin: GPIO3
      baud_rate: 9600
      parity: EVEN
      data_bits: 7

    logger:
      baud_rate: 0 #disable logging over uart

    # read time and timezone Home Assistant
    time:
      - platform: homeassistant
        timezone: "Europe/Paris"
        id: ha_time

    # create two sensors that read value and timestamp from the same tag in standard mode
    sensor:
      - platform: teleinfo
        update_interval: 60s
        historical_mode: false
        tags:
          - tag_name: "SMAXSN"
            sensor:
              # read value of tag
              name: "Linky: Max. power today"
              device_class: "power"
              unit_of_measurement: "VA"
          - tag_name: "SMAXSN"
            sensor:
              # read Linky timestamp of same tag as above
              name: "Linky: Time of max. power today"
              device_class: "timestamp"
              unit_of_measurement: ""


Configuration variables:
------------------------

- **tags** (**Required**): Specify the tag you want to retrieve from the Teleinformation and select with what name to transmit it.

  - **tag_name** (**Required**, string): The name of the tag corresponding to what the electrical counter send.
  - **sensor** (**Required**, :ref:`Sensor <config-sensor>`): Associate a sensor with the tag. See options from :ref:`Sensor <config-sensor>`. When in standard mode you may create a sensor with `device_class: timestamp` to read the timestamp field of a Linky tag instead of its value field.

- **historical_mode** (*Optional*): Wether to use historical mode or standard mode.
  With historical mode, baudrate of 1200 must be used whereas 9600 must be used in
  standard mode. Defaults to ``False``.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

See Also
--------

- :apiref:`teleinfo/teleinfo.h`
- :ghedit:`Edit`
