WiFi Info Text Sensor
=====================

.. seo::
    :description: Instructions for setting up WiFi info text sensors.
    :image: network-wifi.svg

The ``wifi_info`` text sensor platform exposes different WiFi information
via text sensors.

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: wifi_info
        ip_address:
          name: ESP IP Address
          a0:
            name: ESP IP Address 0
          a1:
            name: ESP IP Address 1
          a2:
            name: ESP IP Address 2
          a3:
            name: ESP IP Address 3
          a4:
            name: ESP IP Address 4
        ssid:
          name: ESP Connected SSID
        bssid:
          name: ESP Connected BSSID
        mac_address:
          name: ESP Mac Wifi Address
        scan_results:
          name: ESP Latest Scan Results
        dns_address:
          name: ESP DNS Address

Configuration variables:
------------------------

- **ip_address** (*Optional*): Expose the IP Address of the ESP as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **a0-a4** (*Optional*): With IPv6 and dual stack the device get's at least two ip addresses, often more. To report all addresses the config could have up to 5 sub sensor to ip_address. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **ssid** (*Optional*): Expose the SSID of the currently connected WiFi network as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **bssid** (*Optional*): Expose the BSSID of the currently connected WiFi network as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **mac_address** (*Optional*): Expose the Mac Address of the WiFi card. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **scan_results** (*Optional*): Expose the latest networks found during the latest scan. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **dns_address** (*Optional*): Expose the DNS Address of the ESP as text sensor.
  :ref:`Text Sensor <config-text_sensor>`.


See Also
--------

- :doc:`/components/wifi`
- :doc:`/components/sensor/wifi_signal`
- :apiref:`wifi_info/wifi_info_text_sensor.h`
- :ghedit:`Edit`
