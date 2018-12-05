OTA Update Component
====================

.. seo::
    :description: Instructions for setting up Over-The-Air (OTA) updates for ESPs to upload firmwares remotely.
    :image: system-update.png
    :keywords: Xiaomi, Mi Flora, BLE, Bluetooth

With the OTA (Over The Air) update component you can upload your
firmware binaries to your node without having to use an USB cable for
uploads. esphomeyaml natively supports this through its ``run`` and
``upload`` helper scripts.

.. note::
  Please be aware that ESP8266 modules must be reset after a serial 
  upload before OTA can work.
  When you are trying to conduct an OTA update and receive an error message
  ``Bad Answer: ERR: ERROR[11]: Invalid bootstrapping`` the reason is
  very likely that power-cycling the ESP module is required once after
  the serial upload.
  

Optionally, you can also define a password to use for OTA updates so
that an intruder isn’t able to upload any firmware to the ESP without
having hardware access to it. This password is also hashed
automatically, so an intruder can’t extract the password from the
binary.

esphomelib also supports an “OTA safe mode”. If for some reason your
node gets into a boot loop, esphomelib will automatically try to detect
this and will go over into a safe mode after 10 unsuccessful boot
attempts. In that mode, all components are disabled and only Serial
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

.. note::

    If you get errors like

    .. code::

        ERROR [esphomeyaml.espota] Failed
        ERROR [esphomeyaml.espota] Host livingroom.local Not Found

    when attempting to upload via OTA, please try setting a :ref:`manual IP for WiFi <wifi-manual_ip>`.

See Also
--------

- :doc:`API Reference </api/core/ota>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/ota.rst>`__

.. disqus::
