Ethernet Component
==================

.. seo::
    :description: Instructions for setting up the Ethernet configuration for your ESP32 node in ESPHome.
    :image: ethernet.svg
    :keywords: Ethernet, ESP32

This ESPHome component enables *wired* Ethernet connections for ESP32s.

Ethernet for ESP8266 is not supported.

This component and the Wi-Fi component may **not** be used simultaneously, even if both are physically available.

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

- **type** (**Required**, string): The type of LAN chipset/phy. Must be one of
  ``LAN8720``, ``TLK110`` or ``IP101`` (see datasheet for more details).
- **mdc_pin** (**Required**, :ref:`config-pin`): The MDC pin of the board.
  Usually this is ``GPIO23``.
- **mdio_pin** (**Required**, :ref:`config-pin`): The MDIO pin of the board.
  Usually this is ``GPIO18``.
- **clk_mode** (*Optional*, string): The clock mode of the data lines. See your board's
  datasheet for more details. Must be one of the following values:

  - ``GPIO0_IN`` (Default) - External clock
  - ``GPIO0_OUT`` - Internal clock
  - ``GPIO16_OUT`` - Internal clock
  - ``GPIO17_OUT`` - Internal clock

- **phy_addr** (*Optional*, int): The PHY addr type of the Ethernet controller. Defaults to 0.
- **power_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin controlling the
  power/reset status of the Ethernet controller. Leave unspecified for no power pin (default).
- **manual_ip** (*Optional*): Manually configure the static IP of the node.

  - **static_ip** (**Required**, IPv4 address): The static IP of your node.
  - **gateway** (**Required**, IPv4 address): The gateway of the local network.
  - **subnet** (**Required**, IPv4 address): The subnet of the local network.
  - **dns1** (*Optional*, IPv4 address): The main DNS server to use.
  - **dns2** (*Optional*, IPv4 address): The backup DNS server to use.

- **use_address** (*Optional*, string): Manually override what address to use to connect
  to the ESP. Defaults to auto-generated value. For example, if you have changed your
  static IP and want to flash OTA to the previously configured IP address.
- **domain** (*Optional*, string): Set the domain of the node hostname used for uploading.
  For example, if it's set to ``.local``, all uploads will be sent to ``<HOSTNAME>.local``.
  Defaults to ``.local``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.


.. note::

    If your Ethernet board is not designed with an ESP32 built in, it's common to attempt
    to use flying leads, dupont wires, etc. to connect the Ethernet controller to the ESP32.
    This approach is likely to fail, however, as the Ethernet interface uses a high frequency
    clock signal that will not travel reliably over these types of connections. For more
    information and wiring details refer to the link in the *See also* section.

Configuration for Olimex ESP32-POE
----------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO17_OUT
      phy_addr: 0
      power_pin: GPIO12

Configuration for Olimex ESP32-EVB
----------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO0_IN
      phy_addr: 0

Configuration for Olimex ESP32-GATEWAY
--------------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO17_OUT
      phy_addr: 0

Configuration for LILYGO TTGO T-Internet-POE ESP32-WROOM LAN8270A Chip
----------------------------------------------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO17_OUT
      phy_addr: 0

Configuration for Wireless Tag WT32-ETH01
-----------------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO0_IN
      phy_addr: 1
      power_pin: GPIO16

Configuration for OpenHacks LAN8720
-----------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      phy_addr: 1

.. note::

    This board has an issue that might cause the ESP32 to boot in program mode. When testing, make sure 
    you are monitoring the serial output and reboot the device several times to see if it boots into the 
    program properly.

Configuration for wESP32 board (up to rev 5)
--------------------------------------------

.. code-block:: yaml

    ethernet:
      type: LAN8720
      mdc_pin: GPIO16
      mdio_pin: GPIO17
      clk_mode: GPIO0_IN
      phy_addr: 0

.. note::

    Revision 5 and below of the wESP32 board use the LAN8720 Ethernet PHY.

Configuration for wESP32 board (rev 7 and upwards)
--------------------------------------------------

.. code-block:: yaml

    ethernet:
      type: RTL8201
      mdc_pin: GPIO16
      mdio_pin: GPIO17
      clk_mode: GPIO0_IN
      phy_addr: 0

.. note::

    Revision 7 and upwards of the wESP32 board use the RTL8201 Ethernet PHY.  Support for the RTL8201 is available from ESPHome version 2022.12 upwards.
    
Configuration for ESP32-Ethernet-Kit board
------------------------------------------

.. code-block:: yaml

    ethernet:
      type: IP101
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO0_IN
      phy_addr: 1
      power_pin: GPIO5
      

Configuration for M5Stack PoESP32 Unit
--------------------------------------

.. code-block:: yaml

    ethernet:
      type: IP101
      mdc_pin: GPIO23
      mdio_pin: GPIO18
      clk_mode: GPIO0_IN
      phy_addr: 1
      power_pin: GPIO5


See Also
--------

- :doc:`network`
- :apiref:`ethernet/ethernet_component.h`
- `ESP32 Ethernet PHY connection info <https://pcbartists.com/design/embedded/esp32-ethernet-phy-schematic-design/>`__
- :ghedit:`Edit`
