Migrating from Sonoff Tasmota
=============================

.. seo::
    :description: Migration guide for installing ESPHome on ESPs running Sonoff Tasmota.
    :image: tasmota.png

Migrating from previous Sonoff Tasmota setups is very easy. You just need to have
ESPHome create a binary for you and then upload that in the Tasmota web interface.

Getting the Binary
------------------

First follow the guides for the :ref:`different supported devices <devices>` and create a configuration
file. Then, generate and download the binary:

- **Using the Home Assistant add-on/dashboard**: Just click the ``COMPILE``
  button, wait for the compilation to end and press the ``DOWNLOAD BINARY``
  button.

  .. figure:: images/download_binary.png

- **Using the command line**: run ``esphome livingroom.yaml compile`` (replacing
  ``livingroom.yaml`` with your configuration file of course) and navigate to the
  ``<NODE_NAME>/.pioenvs/<NODE_NAME>/`` folder. There you will find a ``firmware.bin`` file.
  This is the binary that you will upload.

Uploading the Binary
--------------------

To upload the binary, navigate to the Tasmota web interface and enter the
"Firmware Upgrade" section.

.. figure:: images/tasmota_main.png
    :align: center
    :width: 60.0%

In the "Upgrade by file upload" section, choose the binary you previously downloaded

.. figure:: images/tasmota_ota.png
    :align: center
    :width: 60.0%

If everything succeeds, you will see an "Upload Successful" message and ESPHome
will connect to the WiFi network configured in your .yaml file. 🎉

.. figure:: images/tasmota_upload.png
    :align: center
    :width: 60.0%

Happy Hacking!

.. note::

    When using the :doc:`esp8266_pwm output </components/output/esp8266_pwm>` platform and
    switching from Tasmota, you need to power-cycle the device once. After that
    the dimming functionality will work as usual and no more power cycles are required.


.. note::

    If you are using Tasmota 8+ and get an error after uploading the firmware, go to the console and type ```SetOption78 1```, then restart the device and try the firmware again.
    
See Also
--------

- :doc:`/devices/sonoff_s20`
- :doc:`/devices/sonoff_4ch`
- :doc:`/devices/sonoff`
- :doc:`/devices/nodemcu_esp8266`
- :doc:`/devices/nodemcu_esp32`
- :doc:`/devices/esp8266`
- :doc:`/devices/esp32`
- :doc:`migrate_espurna`
- :doc:`migrate_espeasy`
- :ghedit:`Edit`
