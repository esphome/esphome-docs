ESPHome OTA Updates
===================

.. seo::
    :description: Instructions for setting up ESPHome's Over-The-Air (OTA) platform to allow remote updating of devices.
    :image: system-update.svg

.. _config-ota:

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
-  **on_begin** (*Optional*, :ref:`Automation<automation>`): An action to be performed when an OTA update is started.
   See :ref:`ota-on_begin`.
-  **on_progress** (*Optional*, :ref:`Automation<automation>`): An action to be performed (approximately each second)
   while an OTA update is in progress. See :ref:`ota-on_progress`.
-  **on_end** (*Optional*, :ref:`Automation<automation>`): An action to be performed after a successful OTA update.
   See :ref:`ota-on_end`.
-  **on_error** (*Optional*, :ref:`Automation<automation>`): An action to be performed after a failed OTA update.
   See :ref:`ota-on_error`.
-  **on_state_change** (*Optional*, :ref:`Automation<automation>`): An action to be performed when an OTA update state
   change happens. See :ref:`ota-on_state_change`.
-  **version** (*Optional*, int): Version of OTA protocol to use. Version 2 is more stable. To downgrade to legacy
   ESPHome, the device should be updated with OTA version 1 first. Defaults to ``2``.

.. note::

    After a serial upload, ESP8266 modules must be reset before OTA updates will work. If you attempt to perform an OTA
    update and receive the error message ``Bad Answer: ERR: ERROR[11]: Invalid bootstrapping``, the ESP module/board
    must be power-cycled.

OTA Automations
---------------

The OTA component provides various automations that can be used to provide feedback during the OTA update process.
When using these automation triggers, note that:

- OTA updates block the main application loop while in progress. You won't be able to represent state changes using
  components that update their output only from within their ``loop()`` method. Explained differently: if you try to
  display the OTA progress using component X, but the update only appears after the OTA update finished, then component
  X cannot be used for providing OTA update feedback.
- Your automation action(s) must not consume any significant amount of time; if they do, OTA updates may fail.

.. _ota-on_begin:

``on_begin``
************

This automation will be triggered when an OTA update is started.

.. code-block:: yaml

    ota:
      on_begin:
        then:
          - logger.log: "OTA start"

.. _ota-on_progress:

``on_progress``
***************

Using this automation, it is possible to report on the OTA update progress. It will be triggered repeatedly during the
OTA update. You can get the actual progress percentage (a value between 0 and 100) from the trigger with variable ``x``.

.. code-block:: yaml

    ota:
      on_progress:
        then:
          - logger.log:
              format: "OTA progress %0.1f%%"
              args: ["x"]

.. _ota-on_end:

``on_end``
**********

This automation will be triggered when an OTA update has completed successfully, immediately before the device is
rebooted.

Because the update has completed, you can safely use (an) automation action(s) that takes some time to complete. If,
for example, you want to flash an LED, multiple pauses/delays would be required to make the LED blink a few times,
before the reboot. The OTA update can't fail at this point because it is already complete.

.. code-block:: yaml

    ota:
      on_end:
        then:
          - logger.log: "OTA end"

.. _ota-on_error:

``on_error``
************

This automation will be triggered when an OTA update has failed. You can get the internal error code with variable ``x``.

Just like for :ref:`ota-on_end`, you can safely use an automation that takes some time to complete as the OTA update
process has already finished.

.. code-block:: yaml

    ota:
      on_error:
        then:
          - logger.log:
              format: "OTA update error %d"
              args: ["x"]

.. _ota-on_state_change:

``on_state_change``
*******************

This automation will be triggered on every state change. You can get the actual state with variable ``state``, which
will contain one of values for the ``OTAState`` enum. These values are:

-  ``ota::OTA_STARTED``
-  ``ota::OTA_IN_PROGRESS`` *(will be called repeatedly during the update)*
-  ``ota::OTA_COMPLETED``
-  ``ota::OTA_ERROR``

.. code-block:: yaml

    ota:
      on_state_change:
        then:
          - if:
              condition:
                lambda: return state == ota::OTA_STARTED;
              then:
                - logger.log: "OTA start"

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
- :doc:`/components/button/safe_mode`
- :doc:`/components/switch/safe_mode`
- :doc:`/components/ota_http_request`
- :ghedit:`Edit`
