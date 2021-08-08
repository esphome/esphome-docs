DSMR Component
==============

.. seo::
    :description: Instructions for setting up DSMR Meter component in ESPHome.
    :image: dsmr.png

Component/Hub
*************

The DSMR component connects to Dutch Smart Meters which comply to DSMR (Dutch Smart Meter
Requirements), also known as ‘Slimme meter’ or ‘P1 poort’.

This integration supports plain non encrypted telegrams and also encrypted as used in Luxembourg.
In case your equipment has encryption you must get a 32 character long encryption key from your energy company.

This component is passive, it does not transmit any data to your equipment, the equipment always transmits
data which this component decodes and updates the configured sensors at the peace the data is received.

- For official information about DSMR refer to: `DSMR Document <https://www.netbeheernederland.nl/dossiers/slimme-meter-15>`__
- For official information about the P1 port refer to: `P1 Companion Standard <https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf>`__
- For unofficial hardware connection examples refer to: `Domoticx <http://domoticx.com/p1-poort-slimme-meter-hardware/>`__


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
  - All other options from :ref:`Text Sensor <config-text-sensor>`.


- **p1_version** (*Optional*): DSMR Version

  - **name** (**Required**, string): The name for the p1_version text sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Text Sensor <config-text-sensor>`.

Belgium

- **p1_version_be** (*Optional*): DSMR Version Beligum

  - **name** (**Required**, string): The name for the p1_version_be text sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Text Sensor <config-text-sensor>`.


See Also
--------

- :apiref:`dsmr/dsmr.h`
- :ghedit:`Edit`
