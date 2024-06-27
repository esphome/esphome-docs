ESPHome OTA Updates
===================

.. seo::
    :description: Instructions for setting up ESPHome's Over-The-Air (OTA) platform to allow remote updating of devices.
    :image: system-update.svg

.. _config-ota_esphome:

ESPHome's Over-The-Air (OTA) platform allows you to remotely install modified/updated firmware binaries onto your
ESPHome devices over their network (Wi-Fi or Ethernet) interface.

This platform is used by both the ESPHome dashboard as well as the command line interface (CLI) (via
``esphome run ...``) to install firmware onto supported devices.

In addition to OTA updates, ESPHome also supports a "safe mode" to help with recovery if/when updates don't work as
expected. This is automatically enabled by this component, but it may be disabled if desired. See
:doc:`/components/safe_mode` for details.

.. code-block:: yaml

    # Example configuration entry
    ota:
      - platform: esphome
        safe_mode: true
        password: !secret ota_password

Configuration variables:
------------------------

-  **password** (*Optional*, string): The password to use for updates.
-  **port** (*Optional*, int): The port to use for OTA updates. Defaults:

   - ``3232`` for the ESP32
   - ``8266`` for the ESP8266
   - ``2040`` for the RP2040
   - ``8892`` for Beken chips
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
-  **version** (*Optional*, int): Version of OTA protocol to use. Version 2 is more stable. To downgrade to legacy
   ESPHome, the device should be updated with OTA version 1 first. Defaults to ``2``.
-  All :ref:`automations <automation>` supported by :doc:`/components/ota/index`.

.. note::

    After a serial upload, ESP8266 modules must be reset before OTA updates will work. If you attempt to perform an OTA
    update and receive the error message ``Bad Answer: ERR: ERROR[11]: Invalid bootstrapping``, the ESP module/board
    must be power-cycled.

Updating the Password
---------------------

Changing an Existing Password
*****************************

Since the configured password is used for both compiling and uploading, the regular ``esphome run <file>`` command
won't work. This issue can be worked around by executing the operations separately with an ``on_boot`` trigger:

.. code-block:: yaml

    esphome:
      on_boot:
        - lambda: |-
            id(my_ota).set_auth_password("New password");

    ota:
      - platform: esphome
        id: my_ota
        password: "Old password"

After this trick has been used to change the password, the ``on_boot`` trigger may be removed and the old password
replaced with the new password in the ``ota:`` section.

Adding a Password
*****************

If OTA is already enabled without a password, simply add a ``password:`` line to the existing ``ota:`` config block.

See Also
--------

- :apiref:`ota/ota_component.h`
- :doc:`/components/ota/index`
- :doc:`/components/ota/http_request`
- :doc:`/components/safe_mode`
- :ghedit:`Edit`
