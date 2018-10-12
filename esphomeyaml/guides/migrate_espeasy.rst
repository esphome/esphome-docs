Migrating from ESPEasy
======================

Migrating from previous ESPEasy setups is very easy. You just need to have
esphomeyaml create a binary for you and then upload that in the ESPEasy web interface.

Getting Binary
--------------

First follow the guides for the :ref:`different supported devices <devices>` and create a configuration
file. Then, generate and download the binary:

- **Using the HassIO add-on/dashboard**: Just click the ``COMPILE`` button, wait for
  the compilation to end and press the ``DOWNLOAD BINARY`` button.

  .. figure:: images/download_binary.png

- **Using the command line**: run ``esphomeyaml livingroom.yaml compile`` (replacing
  ``livingroom.yaml`` with your configuration file of course) and navigate to the
  ``<NODE_NAME>/.pioenvs/<NODE_NAME>/`` folder. There you will find a ``firmware.bin`` file,
  this is the binary you will upload.

Uploading Binary
----------------

To upload the binary, navigate to the ESPEasy web interface and enter the
"Tools " section.

.. figure:: images/espeasy_ota.png
    :align: center
    :width: 60.0%

Press "Load" under Firmware, then select the binary you previously downloaded and upload
the binary. If everything succeeds, you should now have esphomelib on your node 🎉.

.. note::

    With esphomelib, you in most cases won't need to worry about the available flash size, as
    the binary only ever includes the code that you are actually using.

Happy Hacking!

See Also
--------

- :doc:`/esphomeyaml/devices/nodemcu_esp8266`
- :doc:`/esphomeyaml/devices/nodemcu_esp32`
- :doc:`/esphomeyaml/devices/esp8266`
- :doc:`/esphomeyaml/devices/esp32`
- :doc:`/esphomeyaml/devices/sonoff_s20`
- :doc:`/esphomeyaml/devices/sonoff_4ch`
- :doc:`migrate_espurna`
- :doc:`migrate_sonoff_tasmota`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/guides/migrate_espeasy.rst>`__

.. disqus::
