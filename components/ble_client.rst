BLE Client
==========

.. seo::
    :description: Configuration of the BLE client on ESP32.
    :image: bluetooth.svg

The ``ble_client`` component enables connections to Bluetooth
Low Energy devices in order to query and control them. This
component does not expose any sensors or output components itself,
but merely manages connections to them for use by other components.

.. note::

    The BLE software stack on the ESP32 consumes a significant
    amount of RAM on the device. As such, you may experience
    frequent crashes due to out-of-memory if you enable many
    other components.

    A maximum of three devices is supported due to limitations in the
    ESP32 BLE stack. If you wish to connect more devices, use additional
    ESP32 boards.

    This component does not (yet) support devices that require
    security settings (eg connecting with a PIN).

    Currently, devices connected with the client cannot be
    supported by other components based on :doc:`/components/esp32_ble_tracker`
    as they listen to advertisements which are only sent by devices
    without an active connection.

Despite the last point above, the ``ble_client`` component requires
the ``esp32_ble_tracker`` component in order to discover available
client devices.

.. code-block:: yaml

    esp32_ble_tracker:

    ble_client:
      - mac_address: FF:FF:20:00:0F:15
        id: itag_black

Configuration variables:
------------------------

- **mac_address** (**Required**, MAC Address): The MAC address of the BLE device to connect to.
- **id** (**Required**, :ref:`config-id`): The ID to use for code generation, and for reference by dependent components.

Automations:

- **on_connect** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the client connects to a device. See :ref:`ble_client-on_connect`.
- **on_disconnect** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the client disconnects from a device. See :ref:`ble_client-on_disconnect`.

BLE Client Automation
---------------------

.. _ble_client-on_connect:

``on_connect``
**************

This automation is triggered when the client connects to the BLE device.

.. code-block:: yaml

    ble_client:
      - mac_address: 11:22:33:44:55:66
        id: ble_itag
        on_connect:
          then:
            - lambda: |-
                ESP_LOGD("ble_client_lambda", "Connected to BLE device");

.. _ble_client-on_disconnect:

``on_disconnect``
*****************

This automation is triggered when the client disconnects from a BLE device.

.. code-block:: yaml

    ble_client:
      - mac_address: 11:22:33:44:55:66
        id: ble_itag
        on_disconnect:
          then:
            - lambda: |-
                ESP_LOGD("ble_client_lambda", "Disconnected from BLE device");

.. _ble_client-ble_write_action:

``ble_client.ble_write`` Action
-------------------------------

This action triggers a write to a specified BLE characteristic. The write is attempted in
a best-effort fashion and will only succeed if the ``ble_client``'s  connection has been
established and the peripheral exposes the expected BLE service and characteristic.

Example usage:

.. code-block:: yaml

    ble_client:
      - mac_address: 11:22:33:44:55:66
        id: my_ble_client

    switch:
      - platform: template
        name: "My Switch"
        turn_on_action:
          - ble_client.ble_write:
              id: my_ble_client
              service_uuid: F61E3BE9-2826-A81B-970A-4D4DECFABBAE
              characteristic_uuid: 6490FAFE-0734-732C-8705-91B653A081FC
              # List of bytes to write.
              value: [0x01, 0xab, 0xff]

BLE Overview
------------
This section gives a brief overview of the Bluetooth LE architecture
to help with understanding this and the related components. There are
plenty of more detailed references online.

BLE uses the concept of a *server* and a *client*. In simple terms,
the server is implemented on the device providing services, usually
these are the devices such as heart monitors, tags, weather stations,
etc. The client connects to the server and makes use of its services.
The client will often be an app on a phone, or in the case of ESPHome,
it's the ESP32 device.

When a client connects to a server, the client queries for *services*
provided by the server. Services expose categories of functionality
on the server. These might be well defined and supported services,
such as the Battery Level service, Device Information or Heart Rate.
Or they might be custom services designed just for that device. For
example the button on cheap iTags uses a custom service.

Each service then defines one or more *characteristics* which are
typically the discrete values of that service. For example for the
Environmental Sensor service characteristics exposed include the
Wind Speed, Humidity and Rainfall. Each of these may be read-only
or read-write, depending on their functionality.

A characteristic may also expose one or more *descriptors*, which carry
further information about the characteristic. This could be things
like the units, the valid ranges, and whether notifications (see below)
are enabled.

BLE also supports *notifications*. A client continuously polling for
updates could consume a lot of power, which is undesirable for a
protocol that's designed to be low energy. Instead, a server can push
updates to the client only when they change. Depending on their purpose
and design, a characteristic may allow for notifications to be sent. The
client can then enable notifications by setting the configuration
descriptor for the characteristic.

Each service, characteristic, and descriptor is identified by a
unique identifier (UUID) that may be between 16 and 128 bits long.
A client will typically identify a device's capabilities based on
the UUIDs.

Once the connection is established, referencing each
service/characteristic/descriptor by the full UUID would take a
considerable portion of the small (~23 byte) packet. So the
characteristics and descriptors also provide a small 2-byte
*handle* (alias) to maximize available data space.

Setting Up Devices
------------------

Whilst the component can connect to most BLE devices (that do not
require authentication/pin), useful functionality is only obtained
through dependent components, such as :doc:`/components/sensor/ble_client`.
See the documentation for these components for details on setting up
specific devices.

In order to use the ``ble_client`` component, you need to enable the
:doc:`/components/esp32_ble_tracker` component. This will also allow you to discover
the MAC address of the device.

When you have discovered the MAC address of the device, you can add it
to the ``ble_client`` stanza.

If you then build and upload this configuration, the ESP will listen for
the device and attempt to connect to it when it is discovered. The component
will then query the device for all available services and characteristics and
display them in the log:

.. code-block:: text

    [18:24:56][D][ble_client:043]: Found device at MAC address [FC:58:FA:B1:F8:93]
    [18:24:56][I][ble_client:072]: Attempting BLE connection to fc:58:fa:b1:f8:93
    [18:24:56][I][ble_client:097]: [fc:58:fa:b1:f8:93] ESP_GATTC_OPEN_EVT
    [18:24:57][I][ble_client:143]: Service UUID: 0x1800
    [18:24:57][I][ble_client:144]:   start_handle: 0x1  end_handle: 0x5
    [18:24:57][I][ble_client:305]:  characteristic 0x2A00, handle 0x3, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A01, handle 0x5, properties 0x2
    [18:24:57][I][ble_client:143]: Service UUID: 0x1801
    [18:24:57][I][ble_client:144]:   start_handle: 0x6  end_handle: 0x6
    [18:24:57][I][ble_client:143]: Service UUID: 0x180A
    [18:24:57][I][ble_client:144]:   start_handle: 0x7  end_handle: 0x19
    [18:24:57][I][ble_client:305]:  characteristic 0x2A29, handle 0x9, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A24, handle 0xb, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A25, handle 0xd, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A27, handle 0xf, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A26, handle 0x11, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A28, handle 0x13, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A23, handle 0x15, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A2A, handle 0x17, properties 0x2
    [18:24:57][I][ble_client:305]:  characteristic 0x2A50, handle 0x19, properties 0x2
    [18:24:57][I][ble_client:143]: Service UUID: F000FFC0045140-00B0-0000-0000-000000
    [18:24:57][I][ble_client:144]:   start_handle: 0x1a  end_handle: 0x22
    [18:24:57][I][ble_client:305]:  characteristic F000FFC1045140-00B0-0000-0000-000000, handle 0x1c, properties 0x1c
    [18:24:57][I][ble_client:343]:    descriptor 0x2902, handle 0x1d
    [18:24:57][I][ble_client:343]:    descriptor 0x2901, handle 0x1e
    [18:24:57][I][ble_client:305]:  characteristic F000FFC2045140-00B0-0000-0000-000000, handle 0x20, properties 0x1c
    [18:24:57][I][ble_client:343]:    descriptor 0x2902, handle 0x21
    [18:24:57][I][ble_client:343]:    descriptor 0x2901, handle 0x22
    [18:24:57][I][ble_client:143]: Service UUID: 0xFFE0
    [18:24:57][I][ble_client:144]:   start_handle: 0x23  end_handle: 0x26
    [18:24:57][I][ble_client:305]:  characteristic 0xFFE1, handle 0x25, properties 0x10
    [18:24:57][I][ble_client:343]:    descriptor 0x2902, handle 0x26
    [18:24:57][I][ble_client:143]: Service UUID: 0x1802
    [18:24:57][I][ble_client:144]:   start_handle: 0x27  end_handle: 0x29
    [18:24:57][I][ble_client:305]:  characteristic 0x2A06, handle 0x29, properties 0x4


The discovered services can then be used to enable and configure other
ESPHome components, for example Service UUID 0xFFE0 is used for iTag style
keychain button events, used by the :doc:`/components/sensor/ble_client` component.

See Also
--------

- :doc:`/components/sensor/ble_client`
- :ref:`Automation <automation>`
- :apiref:`ble_client/ble_client.h`
- :ghedit:`Edit`
