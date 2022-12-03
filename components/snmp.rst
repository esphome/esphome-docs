SNMP Component
==================

.. seo::
    :description: Instructions for setting up SNMP component in ESPhome.
    :image: snmp.svg
    :keywords: SNMP

This ESPHome component enables support for SNMP protocol. The protocol is widely 
used in network management for network monitoring.

This component requires Wi-Fi enabled. It supports version **2c** of the protocol. All items are read only.

.. code-block:: yaml

    # Example configuration entry
    snmp:
      contact: Joe
      location: Basement

Configuration variables:
------------------------

- **contact** (*Optional*, string): Value for `sysContact` (`1.3.6.1.2.1.1.4`) OID
- **location** (*Optional*, string): Value for `sysLocation` (`1.3.6.1.2.1.1.6`) OID

.. note::

    SNMT is not supported for Ethernet.

OID
---

System
~~~~~~

- `1.3.6.1.2.1.1.1` (sysDescr): System description including firmware version and board type
- `1.3.6.1.2.1.1.2` (sysObjectId): Object id, different for ESP32 and ESP8266
- `1.3.6.1.2.1.1.3` (sysUptime): The time (in hundredths of a second) since Wi-Fi established connection
- `1.3.6.1.2.1.1.4` (sysContact): Identification of the contact person. Set by `contact` configuration entry
- `1.3.6.1.2.1.1.5` (sysName): Name of the node
- `1.3.6.1.2.1.1.6` (sysLocation): Physical location of the node. Set by `location` configuration entry
- `1.3.6.1.2.1.1.7` (sysServices): Set of services. Always `64`
- `1.3.6.1.2.1.25.1.1` (hrSystemUptime): The amount of time since the bootup

Storage
~~~~~~~

Information about FLASH and RAM.

- `1.3.6.1.2.1.25.2.2` (hrMemorySize): The amount of standard RAM memory in kb

FLASH

- `1.3.6.1.2.1.25.2.3.1.1.1`: (hrStorageIndex): Always `1`
- `1.3.6.1.2.1.25.2.3.1.3.1`: (hrStorageDesc): Description of the storage: `FLASH`
- `1.3.6.1.2.1.25.2.3.1.4.1`: (hrAllocationUnit): Always `1`
- `1.3.6.1.2.1.25.2.3.1.5.1`: (hrStorageSize): FLASH memory size
- `1.3.6.1.2.1.25.2.3.1.6.1`: (hrStorageUsed): FLASH memory usage

SPI RAM

For ESP8266 it show `0` as size and usage.

- `1.3.6.1.2.1.25.2.3.1.1.2`: (hrStorageIndex): Always `2`
- `1.3.6.1.2.1.25.2.3.1.3.2`: (hrStorageDesc): Description of the storage: `PSI RAM`
- `1.3.6.1.2.1.25.2.3.1.4.2`: (hrAllocationUnit): Always `1`
- `1.3.6.1.2.1.25.2.3.1.5.2`: (hrStorageSize): SPI RAM memory size
- `1.3.6.1.2.1.25.2.3.1.6.2`: (hrStorageUsed): SPI RAM memory usage

Wi-Fi
~~~~~

Wi-Fi signal details.

- `1.3.9999.4.1.0`: RSSI
- `1.3.9999.4.2.0`: BSSI
- `1.3.9999.4.3.0`: SSID
- `1.3.9999.4.4.0`: IP address


ESP32 heap
~~~~~~~~~~

Available only on ESP32 based chips.

- `1.3.9999.32.1.0`: Heap size
- `1.3.9999.32.2.0`: Free heap
- `1.3.9999.32.2.0`: Minimum free heap
- `1.3.9999.32.2.0`: Maximum allocated heap


ESP8266 heap
~~~~~~~~~~~~

Available only for ESP8266 chips.

- `1.3.9999.8266.1.0`: Free heap
- `1.3.9999.8266.2.0`: Heap fragmentation in percents
- `1.3.9999.8266.2.0`: Maximum size of free heap block


Chip
~~~~

- `1.3.9999.2.1.0`: chip type, `32` for EPS32, `8266` for ESP8266
- `1.3.9999.2.2.0`: CPU Clock
- `1.3.9999.2.3.0`: Chip model fo ESP32 or core version for ESP8266
- `1.3.9999.2.4.0`: Number of CPU cores
- `1.3.9999.2.5.0`: ESP32 chip revision or `0` for ESP8266


See Also
--------

- :doc:`network`
- :apiref:`snmp/snmp_component.h`
- :ghedit:`Edit`
