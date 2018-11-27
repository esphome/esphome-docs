esphomeyaml Core Configuration
==============================

.. seo::
    :description: Instructions for setting up the core esphomeyaml configuration.
    :image: cloud-circle.png

Here you specify some core information that esphomeyaml needs to create
firmwares. Most importantly, this is the section of the configuration
where you specify the **name** of the node, the **platform** and
**board** you’re using.

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
        name: livingroom
        platform: ESP32
        board: nodemcu-32s

Configuration variables:
------------------------

- **name** (**Required**, string): This is the name of the node. It
  should always be unique to the node and no other node in your system
  can use the same name. It can also only contain upper/lowercase
  characters, digits and underscores.
- **platform** (**Required**, string): The platform your board is on,
  either ``ESP32`` or ``ESP8266``. See :ref:`esphomeyaml-arduino_version`.
- **board** (**Required**, string): The board esphomeyaml should
  specify for platformio. For the ESP32, choose the appropriate one
  from `this list <http://docs.platformio.org/en/latest/platforms/espressif32.html#boards>`__
  and use `this list <http://docs.platformio.org/en/latest/platforms/espressif8266.html#boards>`__
  for ESP8266-based boards.

Advanced options:

- **esphomelib_version** (*Optional*): The version of the C++ `esphomelib framework <https://github.com/OttoWinter/esphomelib>`__
  to use. See :ref:`esphomeyaml-esphomelib_version`.
- **arduino_version** (*Optional*): The version of the arduino framework to link the project against.
  See :ref:`esphomeyaml-arduino_version`.
- **build_path** (*Optional*, string): Customize where esphomeyaml will store the build files
  for your node. By default, esphomeyaml puts all platformio project files under a folder ``<NODE_NAME>/``,
  but you can customize this behavior using this option.
- **use_custom_code** (*Optional*, boolean): Whether to configure the project for writing custom components.
  This sets up some flags so that custom code should compile correctly

Automations:

- **on_boot** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the node starts. See :ref:`esphomeyaml-on_boot`.
- **on_shutdown** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  right before the node shuts down. See :ref:`esphomeyaml-on_shutdown`.
- **on_loop** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  on each ``loop()`` iteration. See :ref:`esphomeyaml-on_loop`.

.. _esphomeyaml-esphomelib_version:

``esphomelib_version``
----------------------

With the ``esphomelib_version`` parameter you can tell esphomeyaml which version of the C++ framework
to use when compiling code. For example, you can configure using the most recent (potentially unstable)
version of esphomelib straight from github. Or you can configure the use of a local copy of esphomelib
using this configuration option.

First, you can configure the use of either the latest esphomelib stable release (``latest``),
the latest development code from GitHub (``dev``), or a specific version number (``1.8.0``).

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      # ...
      # Use the latest esphomelib stable release
      esphomelib_version: latest

      # Or use the latest code from github
      esphomelib_version: dev

      # Use a specific version number
      esphomelib_version: 1.8.0

Alternatively, if you want to develop for esphomelib, you can download the
`latest code from GitHub <https://github.com/OttoWinter/esphomelib/archive/dev.zip>`__, extract the contents,
and point esphomeyaml to your local copy. Then you can modify the esphomelib to your needs or to fix bugs.

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      # ...
      # Use a local copy of esphomelib
      esphomelib_version:
        local: path/to/esphomelib

And last, you can make esphomeyaml use a specific branch/commit/tag from a remote git repository:

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      # ...
      # Use a specific commit/branch/tag from a remote repository
      esphomelib_version:
        # Repository defaults to https://github.com/OttoWinter/esphomelib.git
        repository: https://github.com/OttoWinter/esphomelib.git
        branch: master

      esphomelib_version:
        repository: https://github.com/somebody/esphomelib.git
        commit: d27bac9263e8a0a5a00672245b38db3078f8992c

      esphomelib_version:
        repository: https://github.com/OttoWinter/esphomelib.git
        tag: v1.8.0

.. _esphomeyaml-arduino_version:

``arduino_version``
-------------------

esphomelib uses the arduino framework internally to handle all low-level interactions like
initializing the WiFi driver and so on. Unfortunately, every arduino framework version often
has its own quirks and bugs, especially concerning WiFi performance. With the ``arduino_version``
option you can tell esphomeyaml which arduino framework to use for compiling.

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      # ...
      # Default: use the recommended version, usually this equals
      # the latest version.
      arduino_version: recommended

      # Use the latest stable version
      arduino_version: latest

      # Use the latest staged version from GitHub, try this if you have WiFi problems
      arduino_version: dev

      # Use a specific version
      arduino_version: 2.3.0

For the ESP8266, you currently can manually pin the arduino version to these values (see the full
list of arduino frameworks `here <https://github.com/esp8266/Arduino/releases>`__):

* `2.4.2 <https://github.com/esp8266/Arduino/releases/tag/2.4.2>`__ (the latest version)
* `2.4.1 <https://github.com/esp8266/Arduino/releases/tag/2.4.1>`__
* `2.4.0 <https://github.com/esp8266/Arduino/releases/tag/2.4.0>`__
* `2.3.0 <https://github.com/esp8266/Arduino/releases/tag/2.3.0>`__ (tasmota uses this)

.. warning::

    Over-the-Air update passwords do not work with the arduino framework
    version 2.3.0

For the ESP32, there's currently only one arduino framework version:
`1.0.0 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.0>`__.

.. _esphomeyaml-on_boot:

``on_boot``
-----------

This automation will be triggered when the ESP boots up. By default, it is executed after everything else
is already set up. You can however change this using the ``priority`` parameter.

.. code-block:: yaml

    esphomeyaml:
      # ...
      on_boot:
        priority: -10
        # ...
        then:
          - switch.turn_off: switch_1

Configuration variables:

- **priority** (*Optional*, float): The priority to execute your custom initialization code. A higher value (for example
  positive values) mean a high priority and thus also your code being executed earlier. So for example negative priorities
  are executed very late. Defaults to ``-10``. Priorities (you can use any value between them too):

  - ``100``: This is where all hardware initialization of vital components is executed. For example setting switches
    to their initial state.
  - ``50.0``: This is where most sensors are set up.
  - ``10``: At this priority, WiFi is initialized.
  - ``7.5``: MQTT initialization takes place at this priority.
  - ``-5.0``: The individual frontend counterparts for the backend components are configured at this priority
  - ``-10.0``: At this priority, pretty much everything should already be initialized.

- See :ref:`Automation <automation>`.

.. _esphomeyaml-on_shutdown:

``on_shutdown``
---------------

This automation will be triggered when the ESP is about to shut down. Shutting down is usually caused by
too many WiFi/MQTT connection attempts, Over-The-Air updates being applied or through the :doc:`deep_sleep`.

.. note::

    It's not guaranteed that all components are in a connected state when this automation is triggered. For
    example, the MQTT client may have already disconnected.

.. code-block:: yaml

    esphomeyaml:
      # ...
      on_shutdown:
        then:
          - switch.turn_off: switch_1

Configuration variables: See :ref:`Automation <automation>`.

.. _esphomeyaml-on_loop:

``on_loop``
-----------

This automation will be triggered on every ``loop()`` iteration (usually around every 16 milliseconds).

.. code-block:: yaml

    esphomeyaml:
      # ...
      on_loop:
        then:
          # do something

See Also
--------

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/esphomeyaml.rst>`__

.. disqus::
