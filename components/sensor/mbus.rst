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

This module converts TTL Levels to Voltage and Current signals and provides the necessary power supply (36V).


Configuration variables for M-Bus Component:
------------------------------------------------
- **mbus_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``mbus`` master.
- **secondary_address** (**Required**): The secondary address of the M-Bus slave.
- **interval** (*Optional*, :ref:`config-time`): Intervall of the command loop for reading the M-Bus Slave (default=1min). 

Configuration variables for M-Bus Sensor:
------------------------------------------------
- **mbus_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``mbus`` master.
- **data_index** (**Required**): Index of the data in the M-Bus Client Response. Index is 0 base.
- **factor** (*Optional*): Multiplier for scaling the reading. 

Operation Modes:
------------------------
If no ``secondary_address`` is set, the M-Bus Component starts to discover the connected Slaves in the M-Bus Network and prints the detected slave addresses to the log.

.. note::
   You have to set the ``logger level`` to at least ``DEBUG`` to see the detected slave addresses.

If the ``secondary_address`` is set, the M-Bus Components start the readout mode.

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

Log Example
------------------------
.. code-block:: yaml


See Also
--------

- :ghedit:`Edit`
