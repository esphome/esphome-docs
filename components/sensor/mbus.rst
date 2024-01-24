.. _mbus:

M-Bus Component
================

.. seo::
    :description: Instructions for setting up the M-Bus component.
    :image: mbus.png

The ``mbus`` component creates mbus connection to control a M-Bus slave device, letting your ESPHome node to act as a M-Bus master.
You can access registers from your slave M-Bus device as sensors and present them to your favorite Home Automation system.

.. figure:: /images/mbus.png
    :align: center
    :width: 25%

This is a partial porting of the `libmbus <https://github.com/rscada/libmbus/tree/master>`__ Library. 
More details about the M-Bus Protocol can be found here: `M-Bus specification <https://m-bus.com/documentation>`__


Hardware setup
--------------
M-Bus do not worke with TTL Level. 
You need an TTL to M-Bus Master module:

.. figure:: /images/mbus_master_module.jpg
    :align: center
    :width: 50%

The transceiver connects to the UART of the MCU. For ESP32, pin ``16`` to ``TXD`` and pin ``17`` to ``RXD`` are the default ones but any other pins can be used as well. You have to connect ``3.3V`` to ``TTLVCC`` at least ``5V`` to VIN and ``GND`` to ``GND``.
The M-Bus Clients are connected to ``M+``.

This module converts TTL Levels to Voltage and Current signals and provides the necessary power supply (+36V).


Configuration variables for M-Bus Component:
------------------------------------------------
- **mbus_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``mbus`` master.
- **secondary_address** (**Required**): The secondary address of the M-Bus slave.
- **interval** (*Optional*, :ref:`config-time`): Intervall of the command loop for reading the M-Bus Slaves (default=1min). 

Configuration variables for M-Bus Sensor:
------------------------------------------------
- **mbus_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``mbus`` master.
- **data_index** (**Required**): Index of the data in the M-Bus Client response. Index is 0 based.
- **factor** (*Optional*): Multiplier for scaling the reading (default=1.0). The value is devided by the factor to calculate the state for HA.

Operation Modes:
------------------------
If no ``secondary_address`` is set, the M-Bus Component starts to discover the connected Slaves in the M-Bus Network and prints the detected slave addresses to the log.

.. note::
   You have to set the ``logger level`` to at least ``DEBUG`` to see the detected slave addresses.

If the ``secondary_address`` is set, the M-Bus Components start the readout loop.

Example
------------------------
The following code creates a ``mbus`` master and a sensor defintion the read out the first data frame.

.. code-block:: yaml
    
    logger:
      tx_buffer_size: 1024
      level: DEBUG

    uart:
      id: m_bus
      baud_rate: 2400
      data_bits: 8
      parity: EVEN
      stop_bits: 1
      rx_pin: 16
      tx_pin: 17

    mbus:
      secondary_address: 0x0025426642042002
      interval: "5s"

    sensor:
    - platform: mbus_sensor
      data_index: 0
      factor: 10
      name: "Energy Consumption"
      accuracy_decimals: 1
      device_class: power
      icon: "mdi:flash"
      state_class: measurement
      unit_of_measurement: "Wh"

Log Example for slave discover
------------------------------
.. code-block:: text

     1 [D][mbus:115]: Found a device on secondary address 0x0025426642042002.
     2 [D][mbus_frame:259]:  Variable Data:
     3 [D][mbus_frame:260]:   Header:
     4 [D][mbus_frame:264]:    id = 66.42.25.00 (0x00254266)
     5 [D][mbus_frame:267]:    manufacturer = ABB
     6 [D][mbus_frame:268]:    version = 0x20
     7 [D][mbus_frame:270]:    medium = Electricity
     8 [D][mbus_frame:271]:    access no = 0x9B
     9 [D][mbus_frame:272]:    status = 0x20
    10 [D][mbus_frame:273]:    signature = 00.00
    11 [D][mbus_frame:274]:   Records:
    12 [D][mbus_frame:286]:    DIF: 0x0E DIFE:  VIF: 0x84 VIFE: 00 Data: 37.38.00.00.00.00 (6). (ID: 0, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 255, Type: BCD_48, 3837.000000)
    13 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 10 VIF: 0x84 VIFE: 00 Data: 37.38.00.00.00.00 (6). (ID: 1, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 1, Type: BCD_48, 3837.000000)
    14 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 20 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 2, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 2, Type: BCD_48, 0.000000)
    15 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 30 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 3, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 3, Type: BCD_48, 0.000000)
    16 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 80.10 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 4, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 4, Type: BCD_48, 0.000000)
    17 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 40 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 5, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 0, Type: BCD_48, 0.000000)
    18 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 50 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 6, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 1, Type: BCD_48, 0.000000)
    19 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 60 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 7, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 2, Type: BCD_48, 0.000000)
    20 [D][mbus_frame:286]:    DIF: 0x8E DIFE: 70 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 8, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 3, Type: BCD_48, 0.000000)
    21 [D][mbus_frame:286]:    DIF: 0x8E DIFE: C0.10 VIF: 0x84 VIFE: 00 Data: 00.00.00.00.00.00 (6). (ID: 9, Function: Instantaneous value, Unit: Energy (10^1 Wh), Tariff: 4, Type: BCD_48, 0.000000)
    22 [D][mbus_frame:286]:    DIF: 0x01 DIFE:  VIF: 0xFF VIFE: 93.00 Data: 01. (ID: 10, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: INT8, 0.000000)
    23 [D][mbus_frame:286]:    DIF: 0x04 DIFE:  VIF: 0xFF VIFE: A0.15 Data: 00.00.00.00. (ID: 11, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: DATE_TIME_32, 0.000000)
    24 [D][mbus_frame:286]:    DIF: 0x04 DIFE:  VIF: 0xFF VIFE: A1.15 Data: 00.00.00.00. (ID: 12, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: DATE_TIME_32, 0.000000)
    25 [D][mbus_frame:286]:    DIF: 0x04 DIFE:  VIF: 0xFF VIFE: A2.15 Data: 00.00.00.00. (ID: 13, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: DATE_TIME_32, 0.000000)
    26 [D][mbus_frame:286]:    DIF: 0x04 DIFE:  VIF: 0xFF VIFE: A3.15 Data: 00.00.00.00. (ID: 14, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: DATE_TIME_32, 0.000000)
    27 [D][mbus_frame:286]:    DIF: 0x07 DIFE:  VIF: 0xFF VIFE: A6.00 Data: 00.00.00.00.00.00.00.00 (8). (ID: 15, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: INT64, 0.000000)
    28 [D][mbus_frame:286]:    DIF: 0x07 DIFE:  VIF: 0xFF VIFE: A7.00 Data: 06.00.00.00.00.00.00.00 (8). (ID: 16, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: INT64, 0.000000)
    29 [D][mbus_frame:286]:    DIF: 0x07 DIFE:  VIF: 0xFF VIFE: A8.00 Data: 00.00.00.00.00.00.00.00 (8). (ID: 17, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: INT64, 0.000000)
    30 [D][mbus_frame:286]:    DIF: 0x07 DIFE:  VIF: 0xFF VIFE: A9.00 Data: 00.00.00.00.00.00.00.00 (8). (ID: 18, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: INT64, 0.000000)
    31 [D][mbus_frame:286]:    DIF: 0x0D DIFE:  VIF: 0xFD VIFE: 8E.00 Data: 30.2E.31.32.2E.31.42 (7). (ID: 19, Function: Instantaneous value, Unit: , Tariff: 255, Type: NO_DATA, 0.000000)
    32 [D][mbus_frame:286]:    DIF: 0x0D DIFE:  VIF: 0xFF VIFE: AA.00 Data: 30.30.31.2D.33.31.33.20.33.32.42 (11). (ID: 20, Function: Instantaneous value, Unit: Manufacturer specific, Tariff: 255, Type: NO_DATA, 0.000000)

* Line 1: Discovered scondary address. Past this value to the ``secondary_address`` variable.
* Line 12 - 32: Detected M-Bus records.
   * ID: The ``data_index`` of the M-Bus Signal to read this record.
   * Unit: Unit + Factor of the value. Factor 10^1: ``factor`` must be set to 10 to read Wh. Without setting the ``factor`` the value ist Wh * 10. To read kWh set the Factor to 10000.
   * Type: Data type of the value.

Known Limitations
-----------------
* Slave discovery may not work if the secondary address starts with a value not equal to 0 due to the fixed discovery mask. 
* All code is tested with a M-Bus Network with one slave and may not work if multiple slaves connected.
* Only BCD, Integer and Float values are supported.
* Custom Data is not supported.

See Also
--------

- :ghedit:`Edit`
