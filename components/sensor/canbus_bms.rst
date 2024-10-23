.. _canbus_bms:

CAN bus BMS interface
=====================

.. seo::
    :description: Instructions for capturing data from CAN bus connected BMSes
    :image: canbus-bms.svg
    :keywords: CAN BMS battery

CAN bus is a common communications channel for Battery Management Systems used to communicate with chargers,
inverters etc.. This component provides a means to capture data from a BMS being broadcast on the CAN bus and
import into ESPhome.

See :ref:`canbus` for more details on the CAN bus component, used by this component to interface to the bus.

Supported BMS Protocols
-----------------------

This component has been tested with BYD and Pylon compatible BMSes, and should also work with any BMS compatible with
SMA Sunny Island CAN protocol. CAN ids recognised are:

* 0x351 - charge/discharge limits
* 0x355 - charge and health status
* 0x356 - battery voltage, current and temperature
* 0x359 - alarm and warning flags (Pylon)
* 0x35A - alarm and warning flags (SMA)
* 0x35C - request charge/discharge flags
* 0x35E - battery name


Basic Configuration
-------------------

A physical CAN bus interface must be configured for each BMS using the :ref:`canbus` component, for example:

.. code-block:: yaml

    canbus:
      - id: can0
        platform: mcp2515
        cs_pin: GPIO4
        can_id: 0x35E
        bit_rate: 500kbps
        clock: 16MHZ

The SPI module may also have to be configured, depending on the CAN bus platform.

The basic BMS configuration is as follows:

.. code-block:: yaml

    canbus_bms:
      - id: bms0
        canbus_id: can0
        debug: true
        name: BMS Battery
        throttle: 10s
        timeout: 30s


Configuration variables:
************************

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation. Required when multiple BMSes are to be monitored.
- **canbus_id** (**Required**, int): The `id` of the canbus platform to be used for this entry.
- **debug** (*Optional*, boolean) default *false* enables additional logging
- **name** (*Optional*, string) A name for this entry
- **throttle** (*Optional*, :ref:`Time <config-time>`) Limit publishing of data for each sensor to this interval. Default is 15s.
- **timeout** (*Optional*, :ref:`Time <config-time>`) Mark a sensor as undefined if no data received within this interval. Default is 60s.


Sensors
-------

Sensors are configured as follows:

.. code-block:: yaml

    sensor:
      - platform: canbus_bms
        bms_id: bms0
        temperature:
          name: BMS Temperature
        voltage:
          name: BMS Voltage
        current:
          name: BMS Current
        charge:
          name: BMS Charge
        health:
          name: BMS Health
        max_charge_voltage:
          name: BMS Max Charge Voltage
        max_charge_current:
          name: BMS Max Charge Current
        max_discharge_current:
          name: BMS Max Discharge Current
        min_discharge_voltage:
          name: BMS Min Discharge Voltage

The meaning of each sensor should be obvious. Default units are V, A and °C. All other options from the :ref:`config-sensor` component are available. The `throttle` and `timeout` values in the `canbus_bms` configuration will
be applied to each sensor unless it already has its own :ref:`sensor-filters` block.

Binary Sensors
--------------

Binary sensors are configured as below:

.. code-block:: yaml

    binary_sensor:
      - platform: canbus_bms
        bms_id: bms0
        charge_enable:
          name: BMS Charge Enable
        discharge_enable:
          name: BMS Discharge Enable
        force_charge_1:
          name: BMS Force Charge 1
        force_charge_2:
          name: BMS Force Charge 2
        request_full_charge:
          name: BMS Request Full Charge
        warnings:
          name: BMS Warnings
        alarms:
          name: BMS Alarms


The `warnings` and `alarms` binary sensors are set whenever there is any warning or alarm respectively being
issued by the BMS. The nature of the warning or alarm is revealed by a corresponding text sensor.

The charge and discharge request flags are not supported by all BMSes so may not receive values.

Text Sensors
------------

.. code-block:: yaml

    text_sensor:
      - platform: canbus_bms
        bms_id: bms0
        bms_name:
          name: BMS Name
        warnings:
          name: BMS Warnings
        alarms:
          name: BMS Alarms


- **bms_name** is the name of the BMS as received on the CAN bus. Note that this may only be issued once every several minutes so may not immediately appear on connection.
- **warnings** will be a comma-separated list of current warnings. This will be empty if the binary sensor `warnings` is false.
- **alarms** is similar to `warnings` but for alarm states.

Multiple BMS
------------

Multiple instances of the BMS component may be configured. Each will require an `id`, and an associated CAN bus
component.

.. code-block:: yaml

    canbus_bms:
      - id: byd_bms
        canbus_id: can0
        debug: false
        name: BYD Battery
        throttle: 10s
        timeout: 30s
      - id: jakiper_bms
        canbus_id: can1
        name: Jakiper Battery
        debug: false
        throttle: 10s
        timeout: 30s

    sensor:
      - platform: canbus_bms
        bms_id: byd_bms
        temperature:
          name: BYD Temperature
        voltage:
          name: BYD Voltage

      - platform: canbus_bms
        bms_id: jakiper_bms
        temperature:
          name: Jakiper Temperature
        voltage:
          name: Jakiper Voltage
        current:
          name: Jakiper Current
        charge:
          name: Jakiper Charge
        health:
          name: Jakiper Health
