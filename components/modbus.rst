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

See Also
--------

- :ref:`uart`
- :apiref:`modbus/modbus.h`
- :ghedit:`Edit`
