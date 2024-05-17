OTA Update Component
====================

.. seo::
    :description: Instructions for setting up Over-The-Air (OTA) updates for ESPs to upload firmwares remotely.
    :image: system-update.svg

.. _config-ota:

With the OTA (Over The Air) update component you can upload your
firmware binaries to your node without having to use a USB cable for
uploads. ESPHome natively supports this through its ``run`` and
``upload`` helper scripts.

ESPHome also has an "OTA safe mode". If for some reason your
node gets into a boot loop, ESPHome will automatically try to detect
this and will go over into a safe mode after the configured unsuccessful boot
attempts (Defaults to ``10``). In that mode, all components are disabled and only Serial
Logging + Network(WiFi or Ethernet) + OTA are initialized, so that you can upload a new
binary. You can trigger entering safe mode by either configuring a dedicated button or
switch to do that or by pressing the reset button on the board for ``num_attempts`` times.


.. code-block:: yaml

    # Example configuration entry
    ota:
      safe_mode: true
      password: !secret ota_password

Configuration variables:
------------------------

-  **safe_mode** (*Optional*, boolean): Whether to enable safe mode.
   Defaults to ``true``.
-  **password** (*Optional*, string): The password to use for updates.
-  **port** (*Optional*, int): The port to use for OTA updates.
   Defaults:

   - ``3232`` for the ESP32
   - ``8266`` for the ESP8266
   - ``2040`` for the RP2040
   - ``8892`` for Beken chips
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
-  **reboot_timeout** (*Optional*, :ref:`config-time`): The amount of time to wait before rebooting when in
   safe mode. Defaults to ``5min``.
-  **num_attempts** (*Optional*, int): The number of attempts to wait before entering safe mode. Defaults to ``10``.
-  **on_begin** (*Optional*, :ref:`Automation<automation>`): An action to be
   performed when an OTA update is started. See :ref:`ota-on_begin`.
-  **on_progress** (*Optional*, :ref:`Automation<automation>`): An action to be
   performed (multiple times) during an OTA update. See :ref:`ota-on_progress`.
-  **on_end** (*Optional*, :ref:`Automation<automation>`): An action to be
   performed after a successful OTA update. See :ref:`ota-on_end`.
-  **on_error** (*Optional*, :ref:`Automation<automation>`): An action to be
   performed after a failed OTA update. See :ref:`ota-on_error`.
-  **on_state_change** (*Optional*, :ref:`Automation<automation>`): An action to be
   performed when an OTA update state change happens. See :ref:`ota-on_state_change`.
-  **version** (*Optional*, int): Version of OTA protocol to use. Version 2 is more stable.
   To downgrade to legacy ESPHome, the device should be updated with OTA version 1 first.
   Defaults to ``2``.

.. note::

    Please be aware that ESP8266 modules must be reset after a serial
    upload before OTA can work.
    When you are trying to conduct an OTA update and receive an error message
    ``Bad Answer: ERR: ERROR[11]: Invalid bootstrapping`` the reason is
    very likely that power-cycling the ESP module is required once after
    the serial upload.

OTA Automation
--------------

The OTA component provides various automations that can be used to provide feedback
during an OTA update. There are a few things to consider when making use of the
provided automation triggers:

-  An OTA update blocks the main loop during its operation. This means that you
   won't be able to represent state changes using components that update their
   output only from within their ``loop()`` method. Explained differently: if you
   try to display the OTA progress using component X, but the update only appears
   after the OTA update finished, then component X cannot be used for providing
   OTA update feedback.

-  Make sure that your automation actions do not take too much time, to prevent
   them from blocking the OTA update code for too long.

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

Using this automation, it is possible to report on the OTA update progress.
It will be triggered multiple times during the OTA update. You can get the actual
progress percentage (a value between 0 and 100) from the trigger with variable ``x``.

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

This automation will be triggered when an OTA update has completed successfully,
right before the device is rebooted.

Because the update has completed, you can safely use an automation action that
takes some time to complete. This can for example be useful if you want to flash
a LED or so, in which case a pause would be required to make the LED light up
for long enough, before the reboot turns it off.

.. code-block:: yaml

    ota:
      on_end:
        then:
          - logger.log: "OTA end"

.. _ota-on_error:

``on_error``
************

This automation will be triggered when an OTA update has failed. You can get
the internal error code with variable ``x``.

Just like for :ref:`ota-on_end`, you can safely use an automation that
takes some time to complete, because the OTA update is no longer busy.

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

This automation will be triggered on every state change. You can get the actual
state with variable ``state``, which will contain one of values for the OTAState
enum. These values are:

-  ``ota::OTA_STARTED``
-  ``ota::OTA_IN_PROGRESS`` (will be called multiple times during the update)
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

Updating the password:
----------------------

Changing an existing password:
******************************

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

Adding a password:
******************

If OTA is already enabled without a password, simply add a ``password:`` line to the existing
``ota:`` config block.

See Also
--------

- :apiref:`ota/ota_component.h`
- :doc:`/components/button/safe_mode`
- :doc:`/components/switch/safe_mode`
- :ghedit:`Edit`
