Ethernet Info Text Sensor
=========================

.. seo::
    :description: Instructions for setting up Ethernet info text sensors.
    :image: ethernet.svg

The ``ethernet_info`` text sensor platform exposes different Ethernet information
via text sensors.

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: ethernet_info
        ip_address:
          name: ESP IP Address
          address_0:
            name: ESP IP Address 0
          address_1:
            name: ESP IP Address 1
          address_2:
            name: ESP IP Address 2
          address_3:
            name: ESP IP Address 3
          address_4:
            name: ESP IP Address 4
        dns_address:
          name: ESP DNS Address
        mac_address:
          name: ESP MAC Address


Configuration variables:
------------------------

- **ip_address** (*Optional*): Expose the IP Address of the ESP as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **address_0-address_4** (*Optional*): With dual stack (IPv4 and IPv6) the device will have at least two IP addresses -- often more. To report all addresses the configuration may have up to five sub-sensors. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **dns_address** (*Optional*): Expose the DNS Address of the ESP as text sensor.
  :ref:`Text Sensor <config-text_sensor>`.
- **mac_address** (*Optional*): Expose the MAC Address of the ESP as text sensor.
  :ref:`Text Sensor <config-text_sensor>`.

See Also
--------

- :doc:`/components/ethernet`
- :apiref:`ethernet_info/ethernet_info_text_sensor.h`
- :ghedit:`Edit`
