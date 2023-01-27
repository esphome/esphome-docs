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
        ssid:
          name: ESP Connected SSID
        bssid:
          name: ESP Connected BSSID
        mac_address:
          name: ESP Mac Wifi Address
        scan_results:
          name: ESP Latest Scan Results

Configuration variables:
------------------------

- **ip_address** (*Optional*): Expose the IP Address of the ESP as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **ssid** (*Optional*): Expose the SSID of the currently connected WiFi network as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **bssid** (*Optional*): Expose the BSSID of the currently connected WiFi network as a text sensor. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **mac_address** (*Optional*): Expose the Mac Address of the WiFi card. All options from
  :ref:`Text Sensor <config-text_sensor>`.
- **scan_results** (*Optional*): Expose the latest networks found during the latest scan. All options from
  :ref:`Text Sensor <config-text_sensor>`.

See Also
--------

- :doc:`/components/wifi`
- :doc:`/components/sensor/wifi_signal`
- :apiref:`wifi_info/wifi_info_text_sensor.h`
- :ghedit:`Edit`
