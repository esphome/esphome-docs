Ethernet Component
==================

.. seo::
    :description: Instructions for setting up the Ethernet configuration for your ESP32 node in esphomelib.
    :image: ethernet.png
    :keywords: Ethernet, ESP32

.. warning::

    This integration is experimental as I don't have the hardware to test it (yet).
    If you can verify it works (or if it doesn't), notify me on `discord <https://discord.gg/KhAMKrd>`__.

This core esphomelib component sets up ethernet connections for ESP32s.
Ethernet for ESP8266 is not supported.

.. code-block:: yaml

    # Example configuration entry
    ethernet:
      type: LAN8720
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO0_IN
      phy_addr: 0

      # Optional manual IP
      manual_ip:
        static_ip: 10.0.0.42
        gateway: 10.0.0.1
        subnet: 255.255.255.0

Configuration variables:
------------------------

- **type** (**Required**, string): The type of LAN chipset. Must be one of
  ``LAN8720`` or ``TLK110`` (see datasheet for more details).
- **mdc_pin** (**Required**, :ref:`config-pin`): The MDC pin of the board.
  Usually this is ``GPIO23``.
- **mdio_pin** (**Required**, :ref:`config-pin`): The MDIO pin of the board.
  Usually this is ``GPIO18``.
- **clk_mode** (*Optional*, string): The clock mode of the data lines, this must be one
  of these values: (see datasheet of your board for more details)

  - ``GPIO0_IN`` (Default) - External clock
  - ``GPIO0_OUT`` - Internal clock
  - ``GPIO16_OUT`` - Internal clock
  - ``GPIO17_OUT`` - Internal clock

- **phy_addr** (*Optional*, int): The PHY addr type of the ethernet controller. Defaults to 0.
- **power_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin with which
  to control the power of the board. Leave unspecified for no power pin (default)

- **manual_ip** (*Optional*): Manually configure the static IP of the node.

  - **static_ip** (*Required*, IPv4 address): The static IP of your node.
  - **gateway** (*Required*, IPv4 address): The gateway of the local network.
  - **subnet** (*Required*, IPv4 address): The subnet of the local network.
  - **dns1** (*Optional*, IPv4 address): The main DNS server to use.
  - **dns2** (*Optional*, IPv4 address): The backup DNS server to use.

- **hostname** (*Optional*, string): Manually set the hostname of the
  node. Can only be 63 long at max and must only contain alphanumeric
  characters plus dashes and underscores.
- **domain** (*Optional*, string): Set the domain of the node hostname used for uploading.
  For example, if it's set to ``.local``, all uploads will be sent to ``<HOSTNAME>.local``.
  Defaults to ``.local``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

Configuration for wESP32 board
------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO16
      mdio_pin: GPIO17
      clk_mode: GPIO0_IN
      phy_addr: 0


See Also
--------

- :doc:`API Reference </api/core/wifi>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/ethernet.rst>`__

.. disqus::
