Changelog
=========

Version 1.7.0
-------------

- The :doc:`/esphomeyaml/components/deep_sleep` now has a ``wakeup_pin_mode`` option for the ESP32. This option
  can be used to tell esphomelib what to do if the wakeup pin is already in the wakeup level when attempting
  to enter deep sleep.
- There are two new triggers available now: :ref:`esphomeyaml.on_boot <esphomeyaml-on_boot>` and
  :ref:`esphomeyaml.on_shutdown <esphomeyaml-on_shutdown>` with which you can do some advanced cleanup/setup
  on boot and shutdown of the node.

Breaking Changes
~~~~~~~~~~~~~~~~

- Fixed the :doc:`SHT3x-D </esphomeyaml/component/sensor/sht3xd>` component and removed the ``accuracy``
  parameter. The accuracy now defaults to ``HIGH``.

