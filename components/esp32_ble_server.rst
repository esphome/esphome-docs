BLE Server
==========

.. seo::
    :description: Instructions for setting up Bluetooth LE GATT Server in ESPHome.
    :image: bluetooth.svg

The ``esp32_ble_server`` component in ESPHome sets up a simple BLE GATT server that exposes the device name,
manufacturer and board. This component allows other components to create their own services to expose
data and control.

.. warning::

    The BLE software stack on the ESP32 consumes a significant amount of RAM on the device.
    
    **Crashes are likely to occur** if you include too many additional components in your device's
    configuration. Memory-intensive components such as :doc:`/components/voice_assistant` and other
    audio components are most likely to cause issues.

.. code-block:: yaml

    # Example configuration

    esp32_ble_server:
      manufacturer: "Orange"
      manufacturer_data: [0x4C, 0, 0x23, 77, 0xF0 ]


Configuration variables:
------------------------

- **manufacturer** (*Optional*, string): The name of the manufacturer/firmware creator. Defaults to ``ESPHome``.
- **model** (*Optional*, string): The model name of the device. Defaults to the friendly name of the ``board`` chosen
  in the :ref:`core configuration <esphome-configuration_variables>`.
- **manufacturer_data** (*Optional*, list of bytes): The manufacturer-specific data to include in the advertising
  packet. Should be a list of bytes, where the first two are the little-endian representation of the 16-bit
  manufacturer ID as assigned by the Bluetooth SIG.
- **services** (*Optional*, list of :ref:`esp32_ble_server-service`): A list of services to expose on the BLE GATT server.

.. _esp32_ble_server-service:

Service Configuration
---------------------

Services are the main way to expose data and control over BLE. Services communicate with the client through characteristics. Each service can have multiple characteristics.

.. code-block:: yaml

    esp32_ble_server:
        services:
            - uuid: 2a24b789-7aab-4535-af3e-ee76a35cc42d
            advertise: false
            characteristics:
                - uuid: cad48e28-7fbe-41cf-bae9-d77a6c233423
                properties:
                    - read
                value: "Hello, World!"


Configuration variables:

- **uuid** (*Required*, string, int): The UUID of the service. If it is a string, it should be in the format ``xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx``.
- **advertise** (*Optional*, boolean): If the service should be advertised. Defaults to ``false``.
- **num_handles** (*Optional*, int): The number of handles to allocate for this service. Defaults to the optimal number of handles based on the number of characteristics and descriptors in the service.
- **characteristics** (*Optional*, list of :ref:`esp32_ble_server-characteristic`): A list of characteristics to expose in this service.

.. _esp32_ble_server-characteristic:

Characteristic Configuration
----------------------------

Characteristics expose data and control for a BLE service. Characteristics can have multiple descriptors to provide additional information about the characteristic. Each characteristic can have multiple descriptors.

.. code-block:: yaml

    esp32_ble_server:
        services:
            # ...
            characteristics:
                - id: test_characteristic
                uuid: cad48e28-7fbe-41cf-bae9-d77a6c233423
                properties:
                    - read
                value: "Hello, World!"
                descriptors:
                    - uuid: 2901
                    value: "Hello, World Descriptor!"


Configuration variables:

- **id** (*Optional*, string): An ID to refer to this characteristic in automations.
- **uuid** (*Required*, string, int): The UUID of the characteristic. If it is a string, it should be in the format ``xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx``.
- **properties** (*Required*, list of string): The properties of the characteristic. Can be ``read``, ``write``, ``notify``, ``broadcast``, ``indicate``, ``write_nr``.
- **value** (*Optional*, string, int, float, boolean, list of bytes): The initial value of the characteristic. Defaults to an empty string.
- **descriptors** (*Optional*, list of :ref:`esp32_ble_server-descriptor`): A list of descriptors to expose in this characteristic.
- **on_write** (*Optional*, :ref:`Automation <automation>`): An action to be performed when the characteristic is written to. The characteristic must have the ``write`` property. See :ref:`esp32_ble_server-characteristic-on_write`.

.. _esp32_ble_server-descriptor:

Descriptor Configuration
------------------------

Descriptors are optional and are used to provide additional information about a characteristic.

.. code-block:: yaml

    esp32_ble_server:
        services:
            - uuid: # ...
            characteristics:
                - uuid: # ...
                descriptors:
                    - uuid: 2901
                    value: "Hello, World Descriptor!"


Configuration variables:

- **uuid** (*Required*, string, int): The UUID of the descriptor. If it is a string, it should be in the format ``xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx``.
- **max_length** (*Optional*, int): The maximum length of the descriptor. Defaults to 0, which means the maximum length is calculated based on the initial value.
- **value** (*Optional*, string, int, float, boolean, list of bytes): The value of the descriptor. Defaults to an empty string.

.. _esp32_ble_server-characteristic-on_write:

``on_write`` Trigger
--------------------

With this configuration option you can write complex automations that are triggered when a characteristic is written to.

.. code-block:: yaml

    esp32_ble_server:
        services:
            - uuid: # ...
            characteristics:
                # ...
                properties:
                    - write
                on_write:
                    then:
                    - lambda: |-
                        ESP_LOGD("BLE", "Received: %s", x.c_str());


``ble_server.characteristic_set_value`` Action
----------------------------------------------

This action sets the value of a characteristic.

.. code-block:: yaml

    on_...:
      then:
        - ble_server.characteristic_set_value:
            id: test_write_characteristic
            value: !lambda 'return "Hello, World!";'


Configuration variables:

- **id** (*Required*, string): The ID of the characteristic to set the value of.
- **value** (*Required*, string, :ref:`templatable <config-templatable>`): The value to set the characteristic to.


See Also
--------

- :doc:`esp32_ble`
- :doc:`esp32_improv`
- :apiref:`esp32_ble/ble.h`
- :ghedit:`Edit`
