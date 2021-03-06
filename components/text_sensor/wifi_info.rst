WiFi Info Text Sensor
=====================

.. seo::
    :description: Instructions for setting up WiFi info text sensors.
    :image: network-wifi.png

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
        networks:
          name: ESP Wifi Networks

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
- **networks** (*Optional*): Expose the list of WiFi networks found in the last WiFi scan. All options from
  :ref:`Text Sensor <config-text_sensor>`.
  A compact text format is used, and the string is limited to 255 chars, to conform to Home Assistant limits.
  Each network is listed as specified below, seperated by a "|": 
  
  * SSID
  * RSSI
  * BSSID in hexadecimal notation (without the ":" seperator)
  * Channel number  
  * State-Code bits in hexadecimal:
  
    * bit 0 - The network is password protected
    * bit 1 - The network is hidden
    * bit 2 - The network matches an entry in ESPHome's WiFi network list
    * bit 3 - The network BSSID matches the active network BSSID
  
  * Priority - The current priority used by ESPHome to select a network.

See Also
--------

- :apiref:`wifi_info/wifi_info_text_sensor.h`
- :ghedit:`Edit`
