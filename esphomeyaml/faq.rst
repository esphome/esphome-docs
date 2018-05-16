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

How to submit an issue report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First of all, thank you very much to everybody submitting issue reports! While I try to test esphomelib/yaml as much as
I can using my own hardware, I don't own every single device type and mostly only do tests with my own home automation
system. When doing some changes in the core, it can quickly happen that something somewhere breaks. Issue reports are a
great way for me to track and (hopefully) fix issues, so thank you!

For me to fix the issue the quickest, there are some things that would be really helpful:

1.  How do you use esphomelib? Through esphomeyaml or directly through C++ code?
2.  If it's a build/upload issue: What system are you compiling/uploading things from? Windows, POSIX, from docker?
3.  A snippet of the code/configuration file used is always great for a better understanding of the issue.
4.  If it's an i2c or hardware communication issue please also try setting the
    `log level </esphomeyaml/components/logger.html#log-levels>`__ to ``VERY_VERBOSE`` as it provides helpful information
    about what is going on.

You can find the issue tracker here https://github.com/OttoWinter/esphomelib/issues

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

