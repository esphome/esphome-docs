esphomelib
==========

.. meta::
    :google-site-verification: qclmMpSERA2uy_ZceVgL6ijwkeEHer75LEPyyTQnK4E

.. seo::
    :description: esphomelib Homepage - Reimagining DIY Home Automation. esphomelib is a framework that tries to provide the best possible use experience for using ESP8266 and ESP32 microcontrollers for Home Automation.
    :image: logo-full.png

.. image:: /esphomeyaml/images/logo-full.svg

What is esphomelib?
-------------------

Esphomelib is a framework for creating custom firmwares for your WiFi-enabled
ESP microcontrollers. Its primary focus is making the process to get your ESP
running as simple as possible, with many helper tools to ensure you will have the
best user experience.

Esphomelib is split up into two main parts: esphomelib, the C++ framework backing the entire
framework, and esphomeyaml, a tool that automatically creates firmwares for you just
from simple configuration files - so **no programming experience required**!

.. imgtable::

    Esphomeyaml Component Index, /esphomeyaml/index, logo.svg
    Getting Started, /esphomeyaml/index.html#guides, download.svg
    Esphomelib API Reference, /api/index, puzzle.svg

esphomeyaml will:

 * Read your configuration file and warn you about potential errors (like using the invalid pins.)
 * Create a custom C++ sketch file for you using esphomeyaml's powerful C++ generation engine.
 * Compile the sketch file for you using `platformio <https://platformio.org/>`__.
 * Upload the binary to your ESP via Over the Air updates.
 * If you're using `Home Assistant <https://www.home-assistant.io/>`__, esphomelib
   will automatically add all components to the home assistant UI.

Features
--------

 * **No programming experience required:** just edit YAML configuration files like you're used to with Home Assistant.
 * **Smart:**
 * **Fast and efficient:** Written in C++ and keeps memory consumption to a minimum.
 * **Small binaries:** Only the sensors/devices you actually use will appear in the binary.
 * **Made for Home Assistant:** Almost all Home Assistant features are supported out of the box. Including RGB lights and many more.
 * **Powerful logging engine:** View colorful logs and debug issues remotely.
 * **Automations:** Using esphomeyaml's :ref:`automation engine <automation>`, you can have automations run on the ESP
   with an intuitive script syntax.
 * **Flexible:** Use `esphomelib <https://github.com/OttoWinter/esphomelib>`__'s powerful core to create custom sensors/outputs.
 * **It's Open Source 😺**


.. toctree::
    :hidden:

    esphomeyaml/index
    web-api/index
    api/index
    misc/index
