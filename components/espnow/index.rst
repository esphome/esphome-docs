espnow communication Component
==============================

.. seo::
    :description: Instructions for setting up the esphome component in ESPHome.
    :image: esp-now-logo.png

.. note::

    To enables the option to interact with other esp32 devices over the Espressif's ESP-NOW protocol, see
    :doc:`there documentation <https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/network/esp_now.html>`.

This commponent allows ESPHome to communicate with esp32 devices in a simple and unsustricted way. You can receive using an event handler and
and transmit data package via the `espnow.send` action, by broatcasting to every device or a specific device in your network.

.. note::

    Broadcast data package is not recommend, this will also reach not owned device from other that uses the esp-now protocol.
    The best solution is to minimalice the broadcasting as much as possible and use it only for identification purposes.


.. _config-espnow:

ESP-NOW Configuration
---------------------

.. code-block:: yaml

    # Example espnow configuration
    espnow:
      auto_add_peer: true
      channel: 1
      conformation_timeout: 5000
      auto_add_peer: true
      peers:
        - FF:FF:FF:FF:FF:FF
      on_receive:
        - logger.log:
            format: "Received: %s RSSI: %d"
            args: [ packet.payload_as_bytes(), packet.rssi]
      on_sent: 
        - logger.log:
            format: "Received: %s%s"
            args: [ packet.get_payload(), status?"":" [Failed]"]
      on_new_peer:
        - logger.log:
            format: "Peer %012llx is a new user. It will be added."
            args: [ packet.peer ]
        - espnow.add_peer: packet.peer



Configuration variables:

- **auto_add_peer** (*Optional*, boolean): This will allow the esp-now component to add a new incoming device to be added as peer.
- **channel** (*Optional*, int): The wifi channel that the esp-now communication will use to send/receive data package.
- **conformation_timeout** (*Optional*, int): Time between retries. 
- **auto_add_peer** (*Optional*, boolean): Enable adding new peers automatically.
- **peers** (*Optional*, list): A peer is the name for devices that uses esp-now. The list will have all MAC addresses from
  the devices where this device may communicate with.

Automations:
- **on_receive** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a data package is received. See :ref:`espnow-on_package_receiveds`.
- **on_new_peer** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a data package is received from an unknown peer. See :ref:`espnow-on_new_peer`.
- **on_sent** (*Optional*, :ref:`Automation <automation>`): An automation to perform to confirm that the dat package was send correctly or not. See :ref:`espnow-on_package_send`.

espnow Automation
-----------------

.. _espnow-on_receive:

``on_receive``
**************

This automation will be triggered when a data package is received. You can get the package data via the "it" variable. see :ref:`espnow-ESPNowPackage`.

.. code-block:: yaml

    espnow:
      on_receive:
        - logger.log:
            format: "Received: %s RSSI: %d"
            args: [ packet.payload_as_bytes(), packet.rssi]

Configuration variables: see :ref:`Automation <automation>`.


.. _espnow-on_sent:

``on_sent``
***********

This automation will be triggered when a data package is Sent. You can get the package data via the "packet" variable. see :ref:`espnow-ESPNowPackage`.
The status flag will tell of it was success. When the package was not sent properly it will try to send it at a later moment again. It will try this for 
5 times then none of the package will be send until it received a new data package from that device.

.. code-block:: yaml

    espnow:
      on_sent:
        - logger.log:
            format: "Packet sent: %s%s \n Send cound: %d   "
            args: [ packet.payload_as_bytes(), status?"":" [Failed]", packet->attempts]

Configuration variables: see :ref:`Automation <automation>`.

.. _espnow-on_new_peer:

``on_new_peer``
***************

This automation will be triggered when a data package is received from an unknown device. This trigger will only be fired when ``auto_add_peer`` is **false**.
To the sending peer addres can be found the package data via the "packet" variable. see :ref:`espnow-ESPNowPackage`.
To allow the the new device to be handled correctly you need to add it as a *new peer* with the ``espnow.add.peer`` action.

.. code-block:: yaml

    espnow:
      on_new_peer:
        - logger.log:
            format: "Received packet from new peer: 0x012llx "
            args: [ packet.peer ]
        - espnow.add.peer: packet.peer

Configuration variables: see :ref:`Automation <automation>`.


.. espnow-send_action:

``espnow.send`` Action
***********************

This is an :ref:`Action <config-action>` for sending a data package over the espnow protocol.

.. code-block:: yaml

    globals:
      - id: custom_peer
        type: uint64_t
        restore_value: yes
        initial_value: '66:55:44:33:22:11'
    
    binary_sensor:
      - platform: gpio
        pin: D2
        on_click:
         - espnow.send:
             peer: 11:22:33:44:55:66
             data: "The big angry wolf awakes"
         - espnow.send: 
             data: [0x00, 0x00, 0x34, 0x5d]
             peer: !lambda: "return id(custom_peer);"
         - espnow.send: 0x20DF10EF

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the espnow component to set.
- **data** (**Required**, multiple): The data that need to be send as broadcast or specific device.
- **peer** (*Optional*, Peer Address): The MAC address of the receiving device to connect to. When omitted it will broadcast the package to every device.

You can send data as string, as an array of bytes or as integer (Litle Ending). The maximal bytes that can be send is 240 bytes; 10 less then the offical protocol;
we will add an prefix and checksum code to the data.

.. espnow-add_peer:

``espnow.add.peer`` Action
**************************

This is an :ref:`Action <config-action>` to add a new peer to the internal allowed peers list.

.. code-block:: yaml

    espnow:
      on_new_peer:
        - logger.log:
            format: "Send data: %s \n New Peer: 0x%12h "
            args: [ packet.payload_as_bytes(), packet.peer]
        - espnow.add.peer: packet.peer


Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the espnow component to set.
- **peer** (**Required**, Peer Address): The Peer address that needs to be added to the list of allowed peers.


.. espnow-del_peer:

``espnow.del.peer`` Action
**************************

This is an :ref:`Action <config-action>` to remove a known peer from the internal allowed peers list.

.. code-block:: yaml

    espnow:
      on_new_peer:
        - espnow.add.peer: packet.peer
        - espnow.del.peer: packet.peer

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the espnow component to set.
- **peer** (**Required**, Peer Address): The Peer address that needs to be added to the list of allowed peers.


See Also
--------

- :apiref:`espnow/espnow.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:
