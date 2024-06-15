Safe Mode
=========

.. seo::
    :description: Instructions for setting up ESPHome's Safe Mode to help recover from repeated boot failures.
    :image: system-update.svg

Sometimes hardware and/or software doesn't behave as expected. ESPHome supports a "safe mode" to help recover from
repeated boot failures/reboot loops. After a specified number (the default is ten) of boot failures, the safe mode may
be invoked; in this mode, all components are disabled except serial logging, network (Wi-Fi or Ethernet) and the OTA
component(s). In most cases, this will temporarily mitigate the issue, allowing you a chance to correct it, perhaps by
uploading a new binary.

You can also force the invocation of safe mode by configuring a dedicated :doc:`button</components/button/safe_mode>`
or :doc:`switch</components/switch/safe_mode>` component and/or by repeatedly pressing the reset button on the board
for ``num_attempts`` times (see below).

.. code-block:: yaml

    # Example configuration entry
    safe_mode:

.. _safe_mode-configuration_variables:

Configuration variables:
------------------------

-  **disabled** (*Optional*, boolean): Set to ``true`` to disable safe_mode. :doc:`/components/ota` automatically sets
   up safe mode; this allows disabling it if/when it is not wanted.
-  **boot_is_good_after** (*Optional*, :ref:`config-time`): The amount of time after which the boot is considered successful.
   Defaults to ``1min``.
-  **num_attempts** (*Optional*, int): The number of failed boot attempts which must occur before invoking safe mode.
   Defaults to ``10``.
-  **reboot_timeout** (*Optional*, :ref:`config-time`): The amount of time to wait before rebooting when in safe mode.
   Defaults to ``5min``.
- **on_safe_mode** (*Optional*, :ref:`Automation <automation>`): An action to be performed once when safe mode is invoked.

.. warning::

    The ``on_safe_mode`` :ref:`automation <automation>` is intended for use by recovery actions **only**.
    
    As mentioned above, in safe mode, all components are disabled except serial logging, network (Wi-Fi or Ethernet)
    and OTA component(s).
    
    **All other components (for example, displays and sensors) are disabled and cannot be used.**

See Also
--------

- :apiref:`safe_mode/safe_mode.h`
- :doc:`/components/button/safe_mode`
- :doc:`/components/switch/safe_mode`
- :ghedit:`Edit`
