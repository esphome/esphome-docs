DSMR Component
==============

.. seo::
    :description: Instructions for setting up DSMR Slimme Meter component in ESPHome.
    :image: pcf8574.jpg

Component/Hub
*************

The DSMR component connects to Dutch Smart Meters which comply to DSMR (Dutch Smart Meter
Requirements), also known as ‘Slimme meter’ or ‘P1 poort’.

- For official information about DSMR refer to: `DSMR Document <https://www.netbeheernederland.nl/dossiers/slimme-meter-15>`__
- For official information about the P1 port refer to: `P1 Companion Standard <https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf>`__
- For unofficial hardware connection examples refer to: `Domoticx <http://domoticx.com/p1-poort-slimme-meter-hardware/>`__


.. figure:: images/pcf8574-full.jpg
    :align: center
    :width: 80.0%

    PCF8574 I/O Expander.

.. _SparkFun: https://www.sparkfun.com/products/retired/8130

.. code-block:: yaml

    # Example configuration entry
    dsmr:
      decryption_key: !secret decryption_key

    sensor:
      - platform: dsmr
        energy_delivered_tariff1:
          name: dsmr_energy_delivered_tariff1

    text_sensor:
      - platform: dsmr
        identification:
          name: "dsmr_identification"
        p1_version:
          name: "dsmr_p1_version"


Configuration variables:

- **decryption_key** (*Optional*, string, 32 characters, case insensitive): The key to decrypt the
  telegrams. Used in Lux only.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the UART hub.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID of the DSMR if you have multiple components.

Sensor
******

The following sensors are supported

Configuration variables:



See Also
--------

- :apiref:`dsmr/dsmr.h`
- :ghedit:`Edit`
