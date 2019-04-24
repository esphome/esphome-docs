ESPHome Core Configuration
==========================

.. seo::
    :description: Instructions for setting up the core ESPHome configuration.
    :image: cloud-circle.png

Here you specify some core information that ESPHome needs to create
firmwares. Most importantly, this is the section of the configuration
where you specify the **name** of the node, the **platform** and
**board** you’re using.

.. code-block:: yaml

    # Example configuration entry
    esphome:
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
  either ``ESP32`` or ``ESP8266``. See :ref:`esphome-arduino_version`.
- **board** (**Required**, string): The board ESPHome should
  specify for platformio. For the ESP32, choose the appropriate one
  from `this list <http://docs.platformio.org/en/latest/platforms/espressif32.html#boards>`__
  and use `this list <http://docs.platformio.org/en/latest/platforms/espressif8266.html#boards>`__
  for ESP8266-based boards.

Advanced options:

- **arduino_version** (*Optional*): The version of the arduino framework to link the project against.
  See :ref:`esphome-arduino_version`.
- **build_path** (*Optional*, string): Customize where ESPHome will store the build files
  for your node. By default, ESPHome puts all platformio project files under a folder ``<NODE_NAME>/``,
  but you can customize this behavior using this option.
- **platformio_options** (*Optional*, mapping): Additional options to pass over to platformio in the
  platformio.ini file. See :ref:`esphome-platformio_options`.
- **use_custom_code** (*Optional*, boolean): Whether to configure the project for writing custom components.
  This sets up some flags so that custom code should compile correctly
- **includes** (*Optional*, list of files): A list of C[++] files to include in the main (auto-generated) sketch file
  for custom components. The paths in this list are relative to the directory where the YAML configuration file
  is in. Should have file extension ``.h``
- **libraries** (*Optional*, list of libraries): A list of `platformio libraries <https://platformio.org/lib>`__
  to include in the project. See `platformio lib install <https://docs.platformio.org/en/latest/userguide/lib/cmd_install.html>`__.

ESP8266 Options:

- **board_flash_mode** (*Optional*, string): The `SPI flash mode <https://github.com/espressif/esptool/wiki/SPI-Flash-Modes>`__
  to use for the board. One of ``qio``, ``qout``, ``dio`` and ``dout``. Defaults to ``dout``.
- **esp8266_restore_from_flash** (*Optional*, boolean): Whether to save & restore data from flash on ESP8266s.
  Defaults to ``no``. See :ref:`esphome-esp8266_restore_from_flash` for more info

Automations:

- **on_boot** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the node starts. See :ref:`esphome-on_boot`.
- **on_shutdown** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  right before the node shuts down. See :ref:`esphome-on_shutdown`.
- **on_loop** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  on each ``loop()`` iteration. See :ref:`esphome-on_loop`.

.. _esphome-arduino_version:

``arduino_version``
-------------------

ESPHome uses the arduino framework internally to handle all low-level interactions like
initializing the WiFi driver and so on. Unfortunately, every arduino framework version often
has its own quirks and bugs, especially concerning WiFi performance. With the ``arduino_version``
option you can tell ESPHome which arduino framework to use for compiling.

.. code-block:: yaml

    # Example configuration entry
    esphome:
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

* `2.5.0 <https://github.com/esp8266/Arduino/releases/tag/2.5.0>`__
* `2.4.2 <https://github.com/esp8266/Arduino/releases/tag/2.4.2>`__ (default)
* `2.4.1 <https://github.com/esp8266/Arduino/releases/tag/2.4.1>`__
* `2.4.0 <https://github.com/esp8266/Arduino/releases/tag/2.4.0>`__

For the ESP32, there are two arduino framework versions:

- `1.0.1 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.1>`__ (default).
- `1.0.0 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.0>`__.

.. _esphome-esp8266_restore_from_flash:

``esp8266_restore_from_flash``
------------------------------

With this option you can control where the state of certain components is kept on the ESP.
Components like ``light``, ``switch``, ``fan`` and ``globals`` can restore their state upon
boot.

However, by default this data is stored in the "RTC memory" section of the ESP8266s. This memory
is cleared when the ESP8266 is disconnected from power. So by default the state cannot be recovered
after power loss.

To still have these components restore their state upon power loss the state can additionally be
saved in *flash* memory by setting this option to ``true``.

Beware: The flash has a limited number of write cycles (usually around 100 000), after that
the flash section will fail. So do not use this option when you have components that update rapidly.
These include GPIO switches that are used internally (disable restoring with the ``restore_mode`` option),
certain light effects like ``random`` and the ``on_value_range`` trigger.

.. _esphome-on_boot:

``on_boot``
-----------

This automation will be triggered when the ESP boots up. By default, it is executed after everything else
is already set up. You can however change this using the ``priority`` parameter.

.. code-block:: yaml

    esphome:
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

.. _esphome-on_shutdown:

``on_shutdown``
---------------

This automation will be triggered when the ESP is about to shut down. Shutting down is usually caused by
too many WiFi/MQTT connection attempts, Over-The-Air updates being applied or through the :doc:`deep_sleep`.

.. note::

    It's not guaranteed that all components are in a connected state when this automation is triggered. For
    example, the MQTT client may have already disconnected.

.. code-block:: yaml

    esphome:
      # ...
      on_shutdown:
        then:
          - switch.turn_off: switch_1

Configuration variables: See :ref:`Automation <automation>`.

.. _esphome-on_loop:

``on_loop``
-----------

This automation will be triggered on every ``loop()`` iteration (usually around every 16 milliseconds).

.. code-block:: yaml

    esphome:
      # ...
      on_loop:
        then:
          # do something

.. _esphome-platformio_options:

``platformio_options``
----------------------

Platformio supports a number of options in its ``platformio.ini`` file. With the ``platformio_options``
parameter you can tell ESPHome what options to pass into the ``env`` section of the platformio file
(Note you can also do this by editing the ``platformio.ini`` file manually).

You can view a full list of platformio options here: https://docs.platformio.org/en/latest/projectconf/section_env.html

.. code-block:: yaml

    # Example configuration entry
    esphome:
      # ...
      platformio_options:
        upload_speed: 115200
        board_build.f_flash: 80000000L

See Also
--------

- :ghedit:`Edit`
