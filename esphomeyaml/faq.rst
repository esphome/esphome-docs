Frequently Asked Questions
==========================

What's the difference between esphomelib and esphomeyaml?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

That's no good. Here are some steps that resolve some problems:

-  **Update platformio** Some errors are caused by platformio not having the latest version. Try running
   ``platformio update`` in your terminal.
-  **Clean the platformio cache**: Sometimes the build cache leaves behind some weird artifacts. Try running
   ``platformio run -d <NAME_OF_NODE> -t clean``.
-  **Try with the latest Arduino framework version**:
   See `this </esphomeyaml/components/esphomeyaml.html#using-the-latest-arduino-framework-version>`__.
-  **Still an error?** Please file a bug report over in the `esphomelib issue tracker <https://github.com/OttoWinter/esphomelib/issues>`__.
   I will take a look at it as soon as I can. Thanks!

How do I update to the latest version?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simple. Run:

.. code:: bash

    pip2 install -U esphomeyaml


Does esphomelib support [this device/feature]?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If it's not in `the docs </esphomeyaml/index.html>`__, it's probably sadly not
supported. However, I'm always trying to add support for new features, so feel free to create a feature
request in the `esphomelib issue tracker <https://github.com/OttoWinter/esphomelib/issues>`__. Thanks!

I have a question... How can I contact you?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sure! I'd be happy to help :) You can contact me here:

-  `Discord <https://discord.gg/KhAMKrd>`__
-  `Home Assistant Community Forums <https://community.home-assistant.io/t/esphomelib-library-to-greatly-simplify-home-assistant-integration-with-esp32>`__
-  `esphomelib <https://github.com/OttoWinter/esphomelib/issues>`__ and
   `esphomeyaml <https://github.com/OttoWinter/esphomeyaml/issues>`__ issue trackers. Preferably only for issues and
   feature requests.
-  Alternatively, also under my e-mail address contact (at) otto-winter.com

My node keeps reconnecting randomly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jep, that's a known issue. However, it seems to be very low-level and I don't really know
how to solve it. I'm working on possible work-arounds for the issue but currently I do
not have a real solution.

