WiFi Component
==============

This core esphomelib component sets up WiFi connections to access points
for you. It needs to be in your configuration or otherwise esphomeyaml
will fail in the config validation stage.

It’s recommended to provide a static IP for your node, as it can
dramatically improve connection times.

.. code:: yaml

    # Example configuration entry
    wifi:
      ssid: MyHomeNetwork
      password: VerySafePassword

      # Optional manual IP
      manual_ip:
        static_ip: 10.0.0.42
        gateway: 10.0.0.1
        subnet: 255.255.255.0

Configuration variables:
------------------------

- **ssid** (*Optional*, string): The name (or `service set
  identifier <https://www.lifewire.com/definition-of-service-set-identifier-816547>`__)
  of the WiFi access point your device should connect to.
- **password** (*Optional*, string): The password (or PSK) for your
  WiFi network. Leave empty for no password.
- **manual_ip** (*Optional*): Manually configure the static IP of the node.

  - **static_ip** (*Required*, IPv4 address): The static IP of your node.
  - **gateway** (*Required*, IPv4 address): The gateway of the local network.
  - **subnet** (*Required*, IPv4 address): The subnet of the local network.
  - **dns1** (*Optional*, IPv4 address): The main DNS server to use.
  - **dns2** (*Optional*, IPv4 address): The backup DNS server to use.

- **hostname** (*Optional*, string): Manually set the hostname of the
  node. Can only be 63 long at max and must only contain alphanumeric
  characters plus dashes and underscores.
- **ap** (*Optional*): Enable an access point mode on the node.

  - **ssid** (*Required*, string): The name of the access point to create.
  - **password** (*Optional* string): The password for the access point. Leave empty for
    no password.
  - **channel** (*Optional*, int): The channel the AP should operate on from 1 to 14.
    Defaults to 1.
  - **manual_ip** (*Optional*): Manually set the IP options for the AP. Same options as
    manual_ip for station mode.

- **domain** (*Optional*, string): Set the domain of the node hostname used for uploading.
  For example, if it's set to ``.local``, all uploads will be sent to ``<HOSTNAME>.local``.
  Defaults to ``.local``.
- **reboot_timeout** (*Optional*, :ref:`time <config-time>`): The amount of time to wait before rebooting when no
  WiFi connection exists. Can be disabled by setting this to ``0s``, but note that the low level IP stack currently
  seems to have issues with WiFi where a full reboot is required to get the interface back working. Defaults to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

Access Point Mode
-----------------

Since version 1.3, esphomelib has an optional "Access Point Mode". If you include ``ap:``
in your wifi configuration, esphomelib will automatically set up an access point that you
can connect to. Additionally, you can specify both a "normal" station mode and AP mode at the
same time. This will cause esphomelib to only enable the access point when no connection
to the wifi router can be made.

See Also
--------

- :doc:`API Reference </api/core/wifi>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/wifi.rst>`__
