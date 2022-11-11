Haier Climate
=============

.. seo::
    :description: Instructions for setting up a Haier climate devices.
    :image: air-conditioner.svg

The `haier` climate platform creates a Haier climate device.  
The component can be used as a replacement of a Haier proprietary WiFi modules such as KZW-W001 and KZW-W002.

.. code-block:: yaml

    logger:
        baud_rate: 0 #Disable UART logging for ESP8266

    uart:
        rx_pin: GPIO3
        tx_pin: GPIO1
        baud_rate: 9600

    climate:
        platform: haier
        name: Haier AC
        supported_swing_mode: vertical
        update_interval: 10s

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the climate device.
- **update_interval** (*Optional*, :ref:`config-time`): How often device will be polled for status. Defaults to `5s`.
- **supported_swing_modes** (*Optional*, string): Supported swing modes by AC. Possible values are: ``off``, ``vertical``, ``horizontal``, ``both``. Defaults to ``off``.
- All other options from :ref:`Climate <config-climate>`.

Hardware setup
--------------

Most units will have a dedicated USB-A port for Haier WiFi module.
The physical USB port is in fact UART and does not "speak" USB protocol.
It uses four USB pins as 5V, GND, RX, TX. 
You can use spare male USB cable to connect esphome device directly to the climate appliance.

Other units will not have USB ports, but will still probably have UART exposed somewhere on the main board. 

.. list-table:: Haier UART pinout
    :header-rows: 1

    * - Board
      - USB
      - Wire color
      - ESP8266
    * - 5V
      - VCC
      - red
      - 5V
    * - GND
      - GND
      - black
      - GND
    * - TX
      - DATA+
      - green
      - RX
    * - RX
      - DATA-
      - white
      - TX

.. figure:: images/usb_pinout.png
    :align: center
    :width: 70.0%

    USB Pinout

Acknowledgments:
----------------

This component is mainly based on the work done in `esphaier <https://github.com/MiguelAngelLV/esphaier>`__.

See Also
--------

- :doc:`/components/climate/index`
- :apiref:`haier/climate/haier.h`
- :ghedit:`Edit`
