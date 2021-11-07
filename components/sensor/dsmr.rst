DSMR Component
==============

.. seo::
    :description: Instructions for setting up DSMR Meter component in ESPHome.
    :image: dsmr.png

Component/Hub
*************

The DSMR component connects to Dutch Smart Meters which comply to DSMR (Dutch Smart Meter
Requirements), also known as ‘Slimme meter’ or ‘P1 port’.

This integration supports plain non encrypted telegrams and also encrypted as used in Luxembourg.
In case your equipment has encryption you must get a 32 character long encryption key from your energy company.

This component is passive, it does not transmit any data to your equipment, the equipment always transmits
data which this component decodes and updates the configured sensors at the pace the data is received.

- For official information about DSMR refer to: `DSMR Document <https://www.netbeheernederland.nl/dossiers/slimme-meter-15>`__
- For official information about the P1 port refer to: `P1 Companion Standard <https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf>`__

.. code-block:: yaml

    # Example configuration entry
    dsmr:
      decryption_key: !secret decryption_key

    sensor:
      - platform: dsmr
        energy_delivered_tariff1:
          name: Energy Consumed Tariff 1

    text_sensor:
      - platform: dsmr
        identification:
          name: "DSMR Identification"
        p1_version:
          name: "DSMR Version"


Configuration variables:

- **decryption_key** (*Optional*, string, :ref:`templatable <config-templatable>`, 32 characters, case insensitive): The key to decrypt the
  telegrams. Used in Lux only.
- **gas_mbus_id** (*Optional*, integer): The id of the gas meter. Defaults to ``1``.
- **crc_check** (*Optional*, boolean): Specifies if the CRC check must be done. This is required to be set to false for
  older DSMR versions as they do not provide a CRC. Defaults to ``true``.
- **max_telegram_length** (*Optional*, integer): The size of the buffer used for reading DSMR telegrams. Increase
  if you are reading from a smart meter that sends large telegrams. Defaults to ``1500``.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the UART hub.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID of the DSMR if you have multiple components.

Sensor
******

.. note:: Not all sensors are available on all devices.

Country specific sensors are listed last.

Configuration variables:

- **energy_delivered_tariff1** (*Optional*): Energy Consumed Tariff 1.

  - **name** (**Required**, string): The name for the energy_delivered_tariff1 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **energy_delivered_tariff2** (*Optional*): Energy Consumed Tariff 2.

  - **name** (**Required**, string): The name for the energy_delivered_tariff2 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **energy_returned_tariff1** (*Optional*): Energy Produced Tariff 1.

  - **name** (**Required**, string): The name for the energy_returned_tariff1 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **energy_returned_tariff2** (*Optional*): Energy Produced Tariff 2.

  - **name** (**Required**, string): The name for the energy_returned_tariff2 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_delivered** (*Optional*): Power Consumed.

  - **name** (**Required**, string): The name for the power_delivered sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_returned** (*Optional*): Power Produced.

  - **name** (**Required**, string): The name for the power_returned sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **electricity_failures** (*Optional*): Electricity Failures.

  - **name** (**Required**, string): The name for the electricity_failures sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **electricity_long_failures** (*Optional*): Long Electricity Failures.

  - **name** (**Required**, string): The name for the electricity_long_failures sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **voltage_l1** (*Optional*): Voltage Phase 1.

  - **name** (**Required**, string): The name for the voltage_l1 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **voltage_l2** (*Optional*): Voltage Phase 2.

  - **name** (**Required**, string): The name for the voltage_l2 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **voltage_l3** (*Optional*): Voltage Phase 3.

  - **name** (**Required**, string): The name for the voltage_l3 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **current_l1** (*Optional*): Current Phase 1.

  - **name** (**Required**, string): The name for the current_l1 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **current_l2** (*Optional*): Current Phase 2.

  - **name** (**Required**, string): The name for the current_l2 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **current_l3** (*Optional*): Current Phase 3.

  - **name** (**Required**, string): The name for the current_l3 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_delivered_l1** (*Optional*): Power Consumed Phase 1.

  - **name** (**Required**, string): The name for the power_delivered_l1 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_delivered_l2** (*Optional*): Power Consumed Phase 2.

  - **name** (**Required**, string): The name for the power_delivered_l2 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_delivered_l3** (*Optional*): Power Consumed Phase 3.

  - **name** (**Required**, string): The name for the power_delivered_l3 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_returned_l1** (*Optional*): Power Produced Phase 1.

  - **name** (**Required**, string): The name for the power_returned_l1 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_returned_l2** (*Optional*): Power Produced Phase 2.

  - **name** (**Required**, string): The name for the power_returned_l2 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power_returned_l3** (*Optional*): Power Produced Phase 3.

  - **name** (**Required**, string): The name for the power_returned_l3 sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **gas_delivered** (*Optional*): Gas Consumed.

  - **name** (**Required**, string): The name for the gas_delivered sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

Belgium

- **gas_delivered_be** (*Optional*): Gas Consumed Belgium.

  - **name** (**Required**, string): The name for the gas_delivered_be sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

Luxembourg

- **energy_delivered_lux** (*Optional*): Energy Consumed Luxembourg

  - **name** (**Required**, string): The name for the energy_delivered_lux sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **energy_returned_lux** (*Optional*): Energy Produced Luxembourg

  - **name** (**Required**, string): The name for the energy_returned_lux sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.


Text Sensor
***********

Configuration variables:

- **identification** (*Optional*): DSMR Identification

  - **name** (**Required**, string): The name for the identification text sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Text Sensor <config-text_sensor>`.

- **p1_version** (*Optional*): DSMR Version

  - **name** (**Required**, string): The name for the p1_version text sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Text Sensor <config-text_sensor>`.

- **gas_delivered_text** (*Optional*): A text sensor which unformatted gas data. You need to
  apply a custom parsing of this value depending on your meter format.

  - **name** (**Required**, string): The name for the p1_version text sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Text Sensor <config-text_sensor>`.

Belgium

- **p1_version_be** (*Optional*): DSMR Version Belgium

  - **name** (**Required**, string): The name for the p1_version_be text sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Text Sensor <config-text_sensor>`.

Older DSMR meters support
*************************

Version 2.2 is supported with the following configuration:

.. code-block:: yaml

    # Custom uart settings for DSMR v2.2
    uart:
      baud_rate: 9600
      data_bits: 7
      parity: NONE
      stop_bits: 1

    dsmr:
      crc_check: false

    sensor:
      - platform: dsmr
        energy_delivered_tariff1:
          name: dsmr_energy_delivered_tariff1
        energy_delivered_lux:
          name: dsmr_energy_delivered_tarifflux

    text_sensor:
      - platform: dsmr
        identification:
          name: "dsmr_identification"
        p1_version:
          name: "dsmr_p1_version"
        gas_delivered_text:
          name: "gas delivered raw"

Tips for improving reader results
*********************************

When telegrams are sometimes missed, or when you get a lot of CRC errors, then you might have to do some
changes to get better reader results.

It is recommended to set the ``rx_buffer_size`` option of the UART bus to at least the maximum telegram size,
which defaults to 1500 bytes. The default UART read buffer is quite small an can easily overflow, causing
bytes of data getting lost.

.. code-block:: yaml

    # Example configuration
    uart:
      pin: D7
      baud_rate: 115200
      rx_buffer_size: 1700

    dsmr:
      max_telegram_length: 1700

It's best when a hardware UART is used for reading the P1 data. Whether or not hardware UART is used can
be checked in the config dump that you get when connecting to the API logger. Example logging output:

.. code-block:: text

    [02:38:37][C][uart.arduino_esp8266:095]: UART Bus:
    [02:38:37][C][uart.arduino_esp8266:097]:   RX Pin: GPIO13
    [02:38:37][C][uart.arduino_esp8266:099]:   RX Buffer Size: 1500
    [02:38:37][C][uart.arduino_esp8266:101]:   Baud Rate: 115200 baud
    [02:38:37][C][uart.arduino_esp8266:102]:   Data Bits: 8
    [02:38:37][C][uart.arduino_esp8266:103]:   Parity: NONE
    [02:38:37][C][uart.arduino_esp8266:104]:   Stop bits: 1
    [02:38:37][C][uart.arduino_esp8266:106]:   Using hardware serial interface.
                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using an ESP8266, then GPIO13 (e.g. pin D7 on a D1 Mini) can be used for hardware RX. However, to
actually make it work, serial logging must be disabled to keep the hardware UART available for D7.

.. code-block:: yaml

    # Example configuration for ESP8266
    logger:
      baud_rate: 0
      level: DEBUG

    uart:
      pin: GPIO13
      baud_rate: 115200


See Also
--------

- :apiref:`dsmr/dsmr.h`
- :ghedit:`Edit`
