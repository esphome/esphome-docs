BLE Component
=============

.. seo::
    :description: Instructions for setting up Bluetooth LE in ESPHome.
    :image: bluetooth.svg

The ``esp32_ble`` component in ESPHome sets up the Bluetooth LE stack on the device so that a :doc:`esp32_ble_server`
can run.

.. warning::

    The BLE software stack on the ESP32 consumes a significant amount of RAM on the device.
    
    **Crashes are likely to occur** if you include too many additional components in your device's
    configuration. Memory-intensive components such as :doc:`/components/voice_assistant` and other
    audio components are most likely to cause issues.

.. code-block:: yaml

    # Example configuration

    esp32_ble:
      io_capability: keyboard_only

Configuration variables:
------------------------

- **io_capability** (*Optional*, enum): The IO capability of this ESP32, used for securely connecting to other BLE devices. Defaults to ``none``.

    - ``none`` - No IO capability (Connections that require PIN code authentication will fail)
    - ``keyboard_only`` - Only a keyboard to enter PIN codes (or a fixed PIN code)
    - ``display_only`` - Only a display to show PIN codes
    - ``keyboard_display`` - A keyboard and a display
    - ``display_yes_no`` - A display to show PIN codes and buttons to confirm or deny the connection

See Also
--------

- :doc:`esp32_ble_server`
- :doc:`esp32_improv`
- :apiref:`esp32_ble/ble.h`
- :ghedit:`Edit`
