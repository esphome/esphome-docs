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


Configuration variables:
------------------------

- **ip_address** (*Optional*): Expose the IP Address of the ESP as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.

See Also
--------

- :apiref:`ethernet_info/ethernet_info_text_sensor.h`
- :ghedit:`Edit`
