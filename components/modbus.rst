.. _modbus:

Modbus Component
================

.. seo::
    :description: Instructions for setting up Modbus in ESPHome.
    :keywords: Modbus

The Modbus protocol is used by many consumer and industrial devices for communication.
This component allows components in ESPHome to communicate to those devices.
Modbus requires a :ref:`UART Bus <uart>` to communicate.

.. code-block:: yaml

    # Example configuration entry
    uart:
      ...

    modbus:


Configuration variables:
------------------------

- **flow_control_pin** (*Optional*, :ref:`config-pin`): The pin used to switch flow control.
    This is useful for RS485 transeivers that do not have automatic flow control switching,
    like the common MAX485.

- **send_wait_time** (*Optional*, :ref:`time`): Time in milliseconds before a new modbus command is sent if an answer from a previous command is pending. Defaults to 250 ms.
    If multiple modbus devices are attached increasing this value can help avoiding to to overlapping reads.
    When 2 devices are sending a command at the same the the response read from uart can't be assigend to the proper design.
    This value defines the maximumm queuing time for a command before it is send anyways.


See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- :doc:`/components/number/modbus_controller`
- :doc:`/components/output/modbus_controller`
- :doc:`EPEVER MPPT Solar Charge Controller Tracer-AN Series</cookbook/tracer-an>`
- `Modbus RTU Protocol Description <https://www.modbustools.com/modbus.html>`__
- :ref:`uart`
- :apiref:`modbus/modbus.h`
- :ghedit:`Edit`
