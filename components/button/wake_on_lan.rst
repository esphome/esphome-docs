Wake-on-LAN Button
====================

.. seo::
    :description: Instructions for setting up buttons that can send wakeup packets to computers on the network.
    :image: radio-tower.svg

The ``wake_on_lan`` button platform allows you to send a Wake-on-LAN magic packet to a computer on the network
by specifying its MAC address.

.. code-block:: yaml

    # Example configuration entry
    button:
      - platform: wake_on_lan
        name: "Start the Server"
        target_mac_address: E9:48:B8:CA:58:A1

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the button.
- **target_mac_address** (**Required**, MAC Address): The MAC Address of the target computer.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Button <config-button>`.

See Also
--------

- :doc:`template`
- :apiref:`wake_on_lan/wake_on_lan.h`
- :ghedit:`Edit`
