Improv via BLE
==============

.. seo::
    :description: Instructions for setting up Improv via BLE in ESPHome.
    :image: improv-social.png

The ``esp32_improv`` component in ESPHome implements the open `Improv standard <https://www.improv-wifi.com/>`__
for configuring Wi-Fi on an ESP32 device by using Bluetooth Low Energy (BLE) to receive the credentials.

The ``esp32_improv`` component will automatically set up the :doc:`BLE Server <esp32_ble>`.

.. warning::

    The BLE software stack on the ESP32 consumes a significant amount of RAM on the device.
    
    **Crashes are likely to occur** if you include too many additional components in your device's
    configuration. Memory-intensive components such as :doc:`/components/voice_assistant` and other
    audio components are most likely to cause issues.

.. code-block:: yaml

    # Example configuration entry
    wifi:
      # ...

    esp32_improv:
      authorizer: binary_sensor_id


Configuration variables:
------------------------

- **authorizer** (**Required**, :ref:`config-id`): A :doc:`binary sensor <binary_sensor/index>` to authorize with.
  Also accepts ``none``/``false`` to skip authorization.
- **authorized_duration** (*Optional*, :ref:`config-time`): The amount of time until authorization times out and needs
  to be re-authorized. Defaults to ``1min``.
- **status_indicator** (*Optional*, :ref:`config-id`): An :doc:`output <output/index>` to display feedback to the user.
- **identify_duration** (*Optional*, :ref:`config-time`): The amount of time to identify for. Defaults to ``10s``.
- **wifi_timeout** (*Optional*, :ref:`config-time`): The amount of time to wait before starting the improv service after Wi-Fi
  is no longer connected. Defaults to ``1min``.

Status Indicator
----------------

The ``status_indicator`` has the following patterns:

- solid: The improv service is active and waiting to be authorized.
- blinking once per second: The improv service is awaiting credentials.
- blinking 3 times per second with a break in between: The identify command has been used by the client.
- blinking 5 times per second: Credentials are being verified and saved to the device.
- off: The improv service is not running.

See Also
--------

- :doc:`wifi`
- :doc:`improv_serial`
- :doc:`captive_portal`
- `Improv Wi-Fi <https://www.improv-wifi.com/>`__
- :apiref:`esp32_improv/esp32_improv_component.h`
- :ghedit:`Edit`
