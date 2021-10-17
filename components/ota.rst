OTA Update Component
====================

.. seo::
    :description: Instructions for setting up Over-The-Air (OTA) updates for ESPs to upload firmwares remotely.
    :image: system-update.png
    :keywords: Xiaomi, Mi Flora, BLE, Bluetooth

With the OTA (Over The Air) update component you can upload your
firmware binaries to your node without having to use a USB cable for
uploads. ESPHome natively supports this through its ``run`` and
``upload`` helper scripts.

ESPHome also has an "OTA safe mode". If for some reason your
node gets into a boot loop, ESPHome will automatically try to detect
this and will go over into a safe mode after the configured unsuccessful boot
attempts (Defaults to ``10``). In that mode, all components are disabled and only Serial
Logging+WiFi+OTA are initialized, so that you can upload a new binary.

.. code-block:: yaml

    # Example configuration entry
    ota:
      safe_mode: True
      password: VERYSECURE

Configuration variables:
------------------------

-  **safe_mode** (*Optional*, boolean): Whether to enable safe mode.
   Defaults to ``True``.
-  **password** (*Optional*, string): The password to use for updates.
-  **port** (*Optional*, int): The port to use for OTA updates. Defaults
   to ``3232`` for the ESP32 and ``8266`` for the ESP8266.
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
-  **reboot_timeout** (*Optional*, :ref:`time <config-time>`): The amount of time to wait before rebooting when in
   safe mode. Defaults to ``5min``.
-  **num_attempts** (*Optional*, int): The number of attempts to wait before entering safe mode. Defaults to ``10``.

.. note::

    Please be aware that ESP8266 modules must be reset after a serial
    upload before OTA can work.
    When you are trying to conduct an OTA update and receive an error message
    ``Bad Answer: ERR: ERROR[11]: Invalid bootstrapping`` the reason is
    very likely that power-cycling the ESP module is required once after
    the serial upload.

Updating the password:
----------------------

Since the password is used both for compiling and uploading the regular ``esphome <file> run``
won't work of course. This issue can be worked around by executing the operations separately
through an ``on_boot`` trigger:

.. code-block:: yaml

    esphome:
      on_boot:
        - lambda: |-
            id(my_ota).set_auth_password("New password");
    ota:
      password: "Old password"
      id: my_ota

See Also
--------

- :apiref:`ota/ota_component.h`
- :ghedit:`Edit`
