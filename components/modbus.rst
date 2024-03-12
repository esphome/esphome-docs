.. _modbus:

Modbus Component
================

.. seo::
    :description: Instructions for setting up Modbus in ESPHome.
    :keywords: Modbus

The Modbus protocol is used by many consumer and industrial devices for communication.
This component allows components in ESPHome to communicate to those devices via RTU protocol. You can access the coils, inputs, holding, read registers from your devices as sensors, switches, selects, numbers or various other ESPHome components and present them to your favorite Home Automation system. You can even write them as binary or float ouptputs from ESPHome.

The various sub-components implement some of the Modbus functions below (depending on their required functionality):

+---------------+----------------------------+
| Function Code | Description                |
+===============+============================+
| 1             | Read Coil Status           |
+---------------+----------------------------+
| 2             | Read Discrete input Status |
+---------------+----------------------------+
| 3             | Read Holding Registers     |
+---------------+----------------------------+
| 4             | Read Input Registers       |
+---------------+----------------------------+
| 5             | Write Single Coil          |
+---------------+----------------------------+
| 6             | Write Single Register      |
+---------------+----------------------------+
| 15            | Write Multiple Coils       |
+---------------+----------------------------+
| 16            | Write Multiple Registers   |
+---------------+----------------------------+

Modbus RTU requires a :ref:`UART Bus <uart>` to communicate.

.. code-block:: yaml

    # Example configuration entry
    uart:
      ...

    modbus:


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

- **flow_control_pin** (*Optional*, :ref:`config-pin`): The pin used to switch flow control.
  This is useful for RS485 transceivers that do not have automatic flow control switching,
  like the common MAX485.

- **send_wait_time** (*Optional*, :ref:`config-time`): Time in milliseconds before the next ModBUS command is sent if an answer from a previous command is pending. Defaults to 250 ms.
  If multiple ModBUS devices are attached to the same bus increasing this value can help avoiding to to overlapping reads.
  When two devices are sending a command at the same time the response read from UART can't be assigned to the proper design.
  This value defines the maximum queuing time for a command before it is send anyways.
  
- **disable_crc** (*Optional*, boolean): Ignores a bad CRC if set to ``true``. Defaults to ``false``

Hardware TX buffer and flow control
-----------------------------------

On ESP32 it is possible to use hardware TX buffer to improve performance.
When enabled, use the hardware controlled ``flow_control_pin`` of the UART component instead of the software controlled version of the modbus component.

.. code-block:: yaml

    # Example configuration entry for ESP32 with flow control 
    uart:
        ...
        flow_control_pin: GPIO10
        tx_buffer_size: 128

    modbus:
        # Don't use `flow_control_pin` here

.. note::

    Without hardware TX buffer, the timer for ``send_wait_time`` starts after a request has been completely transmitted.
    With TX buffer enabled it starts at the beginning of the request.
    As a result, it may be necessary to adjust this setting, especially at low baud rates.


See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/output/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- :doc:`/components/number/modbus_controller`
- :doc:`/components/select/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- `Modbus RTU Protocol Description <https://www.modbustools.com/modbus.html>`__
- :ref:`uart`
- :apiref:`modbus/modbus.h`
- :ghedit:`Edit`
