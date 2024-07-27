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


.. _config-button:

ESP-NOW Configuration
---------------------

.. code-block:: yaml

    # Example espnow configuration
    espnow:
      auto_add_peer: true
      # encrypt_key: xyz  // not supported yet.
      channel: 1
      peers:
        - FF:FF:FF:FF:FF:FF
      on_package_received:
        - logger.log:
            format: "Received: %s RSSI: %d"
            args: [ it->data().data(),  it->rssi()]


Configuration variables:

- **encrypt_key** (*Optional*, string): A key that can be set to encrypt the content.
- **auto_add_peer** (*Optional*, boolean): This will allow the esp-now component to add a new incoming device to be added as peer.
- **channel** (*Optional*, int): The wifi channel that the esp-now communication will use to send/receive data package.
- **peers** (*Optional*, list): A peer is the name for devices that uses esp-now. The list will have all MAC addresses from
  the devices where this device may communicate with.

Automations:
- **on_package_received** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  data package is received. See :ref:`espnow-on_package_receiveds`.
- **on_new_peer** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  data package is received from an unknown peer. See :ref:`espnow-on_new_peer`.
- **on_package_send** (*Optional*, :ref:`Automation <automation>`): An automation to perform to
  confirm that the dat package was send correctly or not. See :ref:`espnow-on_package_send`.

espnow Automation
-----------------

.. _espnow-on_package_receiveds:

``on_package_receiveds``
***********************

This automation will be triggered when a data package is received. You can get the package data via the "it" variable. see :ref:`espnow-ESPNowPackage`.

.. code-block:: yaml

    espnow:
      on_package_received:
        - logger.log:
            format: "Received: %s RSSI: %d"
            args: [ it->data().data(),  it->rssi()]

Configuration variables: see :ref:`Automation <automation>`.


.. _espnow-on_package_send:

``on_package_receiveds``
************************

This automation will be triggered when a data package is Send. You can get the package data via the "it" variable. see :ref:`espnow-ESPNowPackage`.
The status flag will tell of it was success. When the package was not sent properly it will try at a later moment again. It will try this for 5 times then
none of the package will be send until it received a new data package from that device.

.. code-block:: yaml

    espnow:
      on_package_send:
        - logger.log:
            format: "Send data: %s \n Send cound: %d "
            args: [ it->data().data(), it->get_counter()]

Configuration variables: see :ref:`Automation <automation>`.

.. _espnow-on_package_send:

``on_package_send``
******************

This automation will be triggered when a data package is Send. You can get the package data via the "it" variable. see :ref:`espnow-ESPNowPackage`.
The status flag will tell of it was success. When the package was not sent properly it will try at a later moment again. It will try this for 5 times then
none of the package will be send until it received a new data package from that device.

.. code-block:: yaml

    espnow:
      on_package_send:
        - logger.log:
            format: "Send data: %s \n Send cound: %d "
            args: [ it->data().data(), it->get_counter()]

Configuration variables: see :ref:`Automation <automation>`.

.. _espnow-on_new_peer:

``on_new_peer``
***************

This automation will be triggered when a data package is received from an unknown device. This trigger will only be fired when ``auto_add_peer`` is **false**.
To the sending MAC addres can be found the package data via the "it" variable. see :ref:`espnow-ESPNowPackage`.
To allow the the new device to be handled correctly you need to add it as a *new peer* with the ``espnow.add.peer`` action.

.. code-block:: yaml

    espnow:
      on_new_peer:
        - logger.log:
            format: "Send data: %s \n New Peer: 0x%12h "
            args: [ it->data().data(), it->mac_address() ()]

Configuration variables: see :ref:`Automation <automation>`.


.. espnow-send_action:

``espnow.send`` Action
***********************

This is an :ref:`Action <config-action>` for sending a data package over the espnow protocol.

.. code-block:: yaml

    - espnow.send: "The big angry wolf awakes"
    - espnow.send: [0x00, 0x00, 0x34, 0x5d]
    - espnow.send: 0x20DF10EF

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the espnow component to set.
- **data** (**Required**, multiple): The data that need to be send as broadcast or specific device.
- **mac_address** (*Optional*, MAC Address): The MAC address of the receiving device to connect to. When omitted it will broadcast the package to every device.

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
            args: [ it->data().data(), it->mac_address()]
        - espnow.add.peer: it->mac_address()
Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the espnow component to set.
- **mac_address (**Required**, MAC Address): The MAC address that needs to be added to the list of allowed peers.


.. espnow-del_peer:

``espnow.del.peer`` Action
**************************

This is an :ref:`Action <config-action>` to remove a known peer from the internal allowed peers list.

.. code-block:: yaml

    espnow:
      on_new_peer:
        - espnow.add.peer: it->mac_address()
        - espnow.del.peer: it->mac_address()

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the espnow component to set.
- **mac_address (**Required**, MAC Address): The MAC address that needs to be added to the list of allowed peers.


See Also
--------

- :apiref:`espnow/espnow.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
