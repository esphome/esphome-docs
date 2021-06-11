Improv
======

.. seo::
    :description: Instructions for setting up Improv WiFi in ESPHome.
    :image: improv-social.png

The ``esp32_improv`` component in ESPHome implements the open `Improv standard <https://www.improv-wifi.com/>`__
for configuring Wi-Fi on an ESP32 device by using Bluetooth Low Energy to receive the credentials.

The ``esp32_improv`` component will automatically set up the :doc:`BLE Server <esp32_ble>`.


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

See Also
--------

- :doc:`wifi`
- :doc:`captive_portal`
- `Improv Wi-Fi <https://www.improv-wifi.com/>`__
- :apiref:`esp32_improv/esp32_improv_component.h`
- :ghedit:`Edit`
