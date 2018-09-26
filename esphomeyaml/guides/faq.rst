Frequently Asked Questions
==========================

Tips for using esphomeyaml
--------------------------

1. esphomeyaml supports (most of) Home Assistant's YAML configuration directives like
   ``!include``, ``!secret``. So you can store all your secret WiFi passwords and so on
   in a file called ``secrets.yaml`` within the directory where the configuration file is.

2. If you want to see how esphomeyaml interprets your configuration, run

   .. code:: bash

       esphomeyaml livingroom.yaml config

3. To view the logs from your node without uploading, run

   .. code:: bash

       esphomeyaml livingroom.yaml logs

4. If you have changed the name of the node and want to update over-the-air, just specify
   ``--upload-port`` when running esphomeyaml. For example:

   .. code:: bash

       esphomeyaml livingroom.yaml run --upload-port 192.168.178.52

5. You can always find the source esphomeyaml generates under ``<NODE_NAME>/src/main.cpp``. It's even
   possible to edit anything outside of the ``AUTO GENERATED CODE BEGIN/END`` lines for creating
   :doc:`custom sensors </esphomeyaml/components/sensor/custom>`.


.. |secret| replace:: ``!secret``
.. _secret: https://www.home-assistant.io/docs/configuration/secrets/
.. |include| replace:: ``!include``
.. _include: https://www.home-assistant.io/docs/configuration/splitting_configuration/

What's the difference between esphomelib and esphomeyaml?
---------------------------------------------------------

`esphomelib <https://github.com/OttoWinter/esphomelib>`__ is a C++ framework
around Arduino for creating custom firmwares for ESP8266/ESP32 devices. So with
esphomelib, you need to write C++ code.

`esphomeyaml <https://github.com/OttoWinter/esphomeyaml>`__ is a tool, written in python,
that creates source code that uses the esphomelib framework. It does this by parsing in
a YAML file and generating a C++ source file, compiling it and uploading the binary to the
device. It is meant to be a powerful yet user-friendly engine for creating custom
firmwares for ESP8266/ESP32 devices. Ideally, it should enable users to use a single command
to do everything they want to do with their device without messing around with build systems and so on.

The nice part of the esphomelib/esphomeyaml combo is that you can easily edit the source code
esphomeyaml generates and insert your own custom components such as sensors in it. So, if for example
a sensor you really want to use, is not supported, you can easily `create a custom component
<https://github.com/OttoWinter/esphomelib/wiki/Custom-Sensor-Component>`__ for it.

Because esphomeyaml runs on a host with lots of resources (as opposed to the ESP node itself),
esphomeyaml will in the future also be able to do some really powerful stuff. I have some ideas
like having an automatic schematic creator or a simple `blockly-like <https://developers.google.com/blockly/>`__
in mind that will hopefully make the user-experience of using ESP32/ESP8266 nodes a lot easier.

Help! Something's not working!1!
--------------------------------

That's no good. Here are some steps that resolve some problems:

-  **Update platformio** Some errors are caused by platformio not having the latest version. Try running
   ``platformio update`` in your terminal.
-  **Clean the platformio cache**: Sometimes the build cache leaves behind some weird artifacts. Try running
   ``platformio run -d <NAME_OF_NODE> -t clean``.
-  **Try with the latest Arduino framework version**:
   See :ref:`this <esphomeyaml-arduino_version>`.
-  **Still an error?** Please file a bug report over in the `esphomelib issue tracker <https://github.com/OttoWinter/esphomelib/issues>`__.
   I will take a look at it as soon as I can. Thanks!

How to submit an issue report
-----------------------------

First of all, thank you very much to everybody submitting issue reports! While I try to test esphomelib/yaml as much as
I can using my own hardware, I don't own every single device type and mostly only do tests with my own home automation
system. When doing some changes in the core, it can quickly happen that something somewhere breaks. Issue reports are a
great way for me to track and (hopefully) fix issues, so thank you!

For me to fix the issue the quickest, there are some things that would be really helpful:

1.  How do you use esphomelib? Through esphomeyaml or directly through C++ code?
2.  If it's a build/upload issue: What system are you compiling/uploading things from? Windows, POSIX, from docker?
3.  A snippet of the code/configuration file used is always great for a better understanding of the issue.
4.  If it's an i2c or hardware communication issue please also try setting the
    :ref:`log level <logger-log_levels>` to ``VERY_VERBOSE`` as it provides helpful information
    about what is going on.

You can find the issue tracker here https://github.com/OttoWinter/esphomelib/issues

How do I update to the latest version?
--------------------------------------

It's simple. Run:

.. code:: bash

    pip2 install -U esphomeyaml
    # From docker:
    docker pull ottowinter/esphomeyaml:latest

And in HassIO, there's a simple UPDATE button when there's an update available as with all add-ons

How do I use the latest bleeding edge version?
----------------------------------------------

First, a fair warning that the latest bleeding edge version is not always stable and might have issues.
If you find some, please do however report them if you have time :)

Installing the latest bleeding edge version of esphomelib is also quite easy. It's most often required
if there was a bug somewhere and I didn't feel like building & pushing a whole new release out (this often
takes up to 2 hours!). To install the dev version of esphomeyaml:

- In HassIO: In the esphomeyaml add-on repository there's also a second add-on called ``esphomeyaml-edge``.
  Install that and stop the stable version (both can't run at the same time without port collisions).
- From ``pip``: Run ``pip install git+git://github.com/OttoWinter/esphomeyaml.git``
- From docker: Run ``docker pull ottowinter/esphomeyaml:dev`` and use ``ottowinter/esphomeyaml:dev`` in all
  commands.

Next, if you want to use the latest version of the esphomelib C++ framework too:

.. code::

    # Sample configuration entry
    esphomeyaml:
      name: ...
      esphomelib_version: dev
      # ...

In some cases it's also a good idea to use the latest Arduino framework version. See
:ref:`this <esphomeyaml-arduino_version>`.

Does esphomelib support [this device/feature]?
----------------------------------------------

If it's not in :doc:`the docs </esphomeyaml/index>`, it's probably sadly not
supported. However, I'm always trying to add support for new features, so feel free to create a feature
request in the `esphomelib issue tracker <https://github.com/OttoWinter/esphomelib/issues>`__. Thanks!

I have a question... How can I contact you?
-------------------------------------------

Sure! I'd be happy to help :) You can contact me here:

-  `Discord <https://discord.gg/KhAMKrd>`__
-  `Home Assistant Community Forums <https://community.home-assistant.io/t/esphomelib-library-to-greatly-simplify-home-assistant-integration-with-esp32>`__
-  `esphomelib <https://github.com/OttoWinter/esphomelib/issues>`__ and
   `esphomeyaml <https://github.com/OttoWinter/esphomeyaml/issues>`__ issue trackers. Preferably only for issues and
   feature requests.
-  Alternatively, also under my e-mail address contact (at) otto-winter.com

My node keeps reconnecting randomly
-----------------------------------

Jep, that's a known issue. However, it seems to be very low-level and I don't really know
how to solve it. I'm working on possible work-arounds for the issue but currently I do
not have a real solution.

Some steps that can help with the issue:

-  Use the most recent version of th arduino framework. The platformio arduino package
   always takes some time to update and the most recent version often includes some awesome
   patches. See :ref:`esphomeyaml-arduino_version`.
-  The issue seems to be happen with cheap boards more frequently. Especially the "cheap" NodeMCU
   boards from eBay sometimes have quite bad antennas.
-  Play around with the ``keepalive`` option of the :doc:`MQTT client </esphomeyaml/components/mqtt>`, sometimes
   increasing this value helps (because it's causing more pings in the background), some other times a higher
   keepalive works better.

Devices that will (hopefully) be supported soon:
------------------------------------------------

Devices/Sensors that I've bought and will be supported at some point (ordered by priority):

-  GP2Y10 Dust Sensor
-  APDS-9960 RGB Gesture Sensor
-  MCP2301 16-Channel I/O Expander
-  MLX90614 Infrared Thermometer
-  PCF8591 ADC
-  OV2640 Camera
-  L298N H-Bridge Motor Driver
-  A4988 Stepper Motor Driver

Other features that I'm working on:

-  Multiple WiFi Networks to connect to
-  Color Temperature for Lights
-  Cameras (probably through ArduCAM)

Anything missing? I'd be happy to chat about more integrations over on the `discord channel
<https://discord.gg/KhAMKrd>`__ - no guarantees that everything will be supported though!

I can't update using OTA because of to little space, now what?
--------------------------------------------------------------

If you are using ESP8266/Sonoff devices and you have many components enabled you will probably encounter this error during OTA update:

.. code::

  ERROR [esphomeyaml.espota] Bad Answer: ERR: ERROR[4]: Not Enough Space

This is because of the limited amount of flash memory available on these devices (often just 1M). The size of the firmware data that is created by esphomeyaml depends on the number of components enabled (eg: webserver, sensors, etc). Especially the webserver component is very large.

During an OTA update the new firmware data needs to be stored on the flash chip so it can be used to replace the old firmware. However it is possible the old firmware is taking up to much space so the new firmware won't fit next to it. This makes a normal OTA update impossible. Forcing you to choose between easy updates or components.

A possible solution is to disable (large) components like webserver so the size of the firmware data stays below a certain size.

If even this doesn't work or you like to have a lot of components enabled there is a workaround that might help you out so you can have your cake and eat it too. Using a two stage OTA update.

First we temporary 'remove' (comment out) all components from the ``yaml`` file, leaving only: ``esphomeyaml``, ``ota`` and ``wifi``, example:

.. code:: yaml

    esphomeyaml:
      name: sonoff_basic
      platform: espressif8266
      board: esp01_1m
      board_flash_mode: dout

    wifi:
      ssid: '***'
      password: '***'

    ota:

    # mqtt:
    #   broker: 'mqtt'
    #   username: ''
    #   password: ''
    #
    #
    # logger:
    #
    # switch:
    # ...

This will result in really small firmware data which has a high chance of fitting the remaining space on your device. After this OTA update has succeeded you are left with a device with no functionality except OTA. Now you can re-enable all components previously commented out and perform a 'normal' OTA update again.

How to manully flash a firmware binary
--------------------------------------

See Also
--------

- :doc:`esphomeyaml index </esphomeyaml/index>`
- :doc:`contributing`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/guides/faq.rst>`__
