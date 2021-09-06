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
        comment: Living room ESP32 controller
        platform: ESP32
        board: nodemcu-32s

.. _esphome-configuration_variables:

Configuration variables:
------------------------

- **name** (**Required**, string): This is the name of the node. It
  should always be unique in your ESPHome network. May only contain lowercase
  characters, digits and hyphens. See :ref:`esphome-changing_node_name`.
- **platform** (**Required**, string): The platform your board is on,
  either ``ESP32`` or ``ESP8266``. See :ref:`esphome-arduino_version`.
- **board** (**Required**, string): The board ESPHome should
  specify for PlatformIO. For the ESP32, choose the appropriate one
  from `this list <http://docs.platformio.org/en/latest/platforms/espressif32.html#boards>`__
  and use `this list <http://docs.platformio.org/en/latest/platforms/espressif8266.html#boards>`__
  for ESP8266-based boards. *This only affects pin aliases and some internal settings*, if unsure
  choose the generic board option!

Advanced options:

- **arduino_version** (*Optional*): The version of the Arduino framework to link the project against.
  See :ref:`esphome-arduino_version`.
- **build_path** (*Optional*, string): Customize where ESPHome will store the build files
  for your node. By default, ESPHome puts all PlatformIO project files under a folder ``<NODE_NAME>/``,
  but you can customize this behavior using this option.
- **flash_write_interval** (*Optional*, :ref:`config-time`): Customize the frequency in which data is
  flushed to the flash. This setting helps to prevent rapid changes to a component from being quickly
  written to the flash and wearing it out. Defaults to ``1min``. See :ref:`esphome-flash_write_interval` for more info.
- **platformio_options** (*Optional*, mapping): Additional options to pass over to PlatformIO in the
  platformio.ini file. See :ref:`esphome-platformio_options`.
- **includes** (*Optional*, list of files): A list of C[++] files to include in the main (auto-generated) sketch file
  for custom components. The paths in this list are relative to the directory where the YAML configuration file
  is in. Should have file extension ``.h`` - See :ref:`esphome-includes` for more info.
- **libraries** (*Optional*, list of libraries): A list of `platformio libraries <https://platformio.org/lib>`__
  to include in the project. See `platformio lib install <https://docs.platformio.org/en/latest/userguide/lib/cmd_install.html>`__.
- **comment** (*Optional*, string): Additional text information about this node. Only for display in UI.
- **name_add_mac_suffix** (*Optional*, boolean): Appends the last 6 bytes of the mac address of the device to
  the name in the form ``<name>-aabbcc``. Defaults to ``false``.
  See :ref:`esphome-mac_suffix`.

- **project** (*Optional*): ESPHome Creator's Project information. See :ref:`esphome-creators_project`.

  - **name** (**Required**, string): Name of the project
  - **version** (**Required**, string): Version of the project

ESP8266 Options:

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

ESPHome uses the Arduino framework internally to handle all low-level interactions like
initializing the WiFi driver and so on. Unfortunately, every Arduino framework version often
has its own quirks and bugs, especially concerning WiFi performance. With the ``arduino_version``
option you can tell ESPHome which Arduino framework to use for compiling.

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

For the ESP8266, you currently can manually pin the Arduino version to these values (see the full
list of Arduino frameworks `here <https://github.com/esp8266/Arduino/releases>`__):

* `2.7.4 <https://github.com/esp8266/Arduino/releases/tag/2.7.4>`__ (default)
* `2.7.3 <https://github.com/esp8266/Arduino/releases/tag/2.7.3>`__
* `2.7.2 <https://github.com/esp8266/Arduino/releases/tag/2.7.2>`__
* `2.7.1 <https://github.com/esp8266/Arduino/releases/tag/2.7.1>`__
* `2.7.0 <https://github.com/esp8266/Arduino/releases/tag/2.7.0>`__
* `2.6.3 <https://github.com/esp8266/Arduino/releases/tag/2.6.3>`__
* `2.6.2 <https://github.com/esp8266/Arduino/releases/tag/2.6.2>`__
* `2.6.1 <https://github.com/esp8266/Arduino/releases/tag/2.6.1>`__
* `2.5.2 <https://github.com/esp8266/Arduino/releases/tag/2.5.2>`__
* `2.5.1 <https://github.com/esp8266/Arduino/releases/tag/2.5.1>`__
* `2.5.0 <https://github.com/esp8266/Arduino/releases/tag/2.5.0>`__
* `2.4.2 <https://github.com/esp8266/Arduino/releases/tag/2.4.2>`__
* `2.4.1 <https://github.com/esp8266/Arduino/releases/tag/2.4.1>`__
* `2.4.0 <https://github.com/esp8266/Arduino/releases/tag/2.4.0>`__
* `2.3.0 <https://github.com/esp8266/Arduino/releases/tag/2.3.0>`__

For the ESP32, there are these Arduino `framework versions <https://github.com/espressif/arduino-esp32/releases>`__:

- `1.0.6 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.6>`__ (default)
- `1.0.5 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.5>`__
- `1.0.4 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.4>`__
- `1.0.3 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.3>`__
- `1.0.2 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.2>`__
- `1.0.1 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.1>`__
- `1.0.0 <https://github.com/espressif/arduino-esp32/releases/tag/1.0.0>`__

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

.. _esphome-flash_write_interval:

``flash_write_interval``
------------------------

As all devices have a limited number of flash write cycles, this setting helps to reduce the number of flash writes
due to quickly changing components. In the past, when components such as ``light``, ``switch``, ``fan`` and ``globals``
were changed, the state was immediately committed to flash. The result of this was that the last state of these
components would always restore to its last state on power loss, however, this has the cost of potentially quickly
damaging the flash if these components are quickly changed.

A safety feature has thus been implemented to mitigate issues resulting from the limited number of flash write cycles,
the state is first stored in memory before being flushed to flash after the ``flash_write_interval`` has passed. This
results in fewer flash writes, preserving the flash health.

This behavior can be disabled by setting ``flash_write_interval`` to `0s` to immediately commit the state to flash,
however, be aware that this may lead to increased flash wearing and a shortened device lifespan!

For ESP8266, :ref:`esphome-esp8266_restore_from_flash` must also be set to true for states to be written to flash.

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

- **priority** (*Optional*, float): The priority to execute your custom initialization code. A higher value
  means a high priority and thus also your code being executed earlier. Please note this is an ESPHome-internal
  value and any change will not be marked as a breaking change. Defaults to ``-10``. Priorities (you can use any value between them too):

  - ``800.0``: This is where all hardware initialization of vital components is executed. For example setting switches
    to their initial state.
  - ``600.0``: This is where most sensors are set up.
  - ``250.0``: At this priority, WiFi is initialized.
  - ``200.0``: Network connections like MQTT/native API are set up at this priority.
  - ``-100.0``: At this priority, pretty much everything should already be initialized.

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

PlatformIO supports a number of options in its ``platformio.ini`` file. With the ``platformio_options``
parameter you can tell ESPHome what options to pass into the ``env`` section of the PlatformIO file
(Note you can also do this by editing the ``platformio.ini`` file manually).

You can view a full list of PlatformIO options here: https://docs.platformio.org/en/latest/projectconf/section_env.html

.. code-block:: yaml

    # Example configuration entry
    esphome:
      # ...
      platformio_options:
        upload_speed: 115200
        board_build.f_flash: 80000000L

.. _esphome-includes:

``includes``
------------

With ``includes`` you can include source files in the generated PlatformIO project.
All files declared with this option are copied to the project each time it is compiled.

You can always look at the generated PlatformIO project (``<CONFIG_DIR>/<NODENAME>``) to see what
is happening - and if you want you can even copy the include files directly into the ``src/`` folder.
The ``includes`` option is only a helper option that does that for you.

.. code-block:: yaml

    # Example configuration entry
    esphome:
      # ...
      includes:
        - my_switch.h

This option behaves differently depending on what the included file is pointing at:

 - If the include string is pointing at a directory, the entire directory tree is copied over
   to the src/ folder.
 - If the include string is point at a header file (.h, .hpp, .tcc) - it is copied in the src/ folder
   AND included in the main.cpp. This way the lambda code can access it.


.. _esphome-changing_node_name:

Changing ESPHome Node Name
--------------------------

Trying to change the name of a node or its address in the network?
You can do so with the ``use_address`` option of the :doc:`WiFi configuration <wifi>`.

Change the device name or address in your YAML to the new value and additionally
set ``use_address`` to point to the old address like so:

.. code-block:: yaml

    # Step 1. Changing name from test8266 to kitchen
    esphome:
      name: kitchen
      # ...

    wifi:
      # ...
      use_address: test8266.local

Now upload the updated config to the device. As a second step, you now need to remove the
``use_address`` option from your configuration again so that subsequent uploads will work again
(otherwise it will try to upload to the old address).

.. code-block:: yaml

    # Step 2
    esphome:
      name: kitchen
      # ...

    wifi:
      # ...
      # Remove or comment out use_address
      # use_address: test8266.local

The same procedure can be done for changing the static IP of a device.


.. _esphome-mac_suffix:

Adding the MAC address as a suffix to the device name
-----------------------------------------------------

Using ``name_add_mac_suffix`` allows the user to compile a single binary file to flash
many of the same device and they will all have unique names/hostnames.
Note that you will still need to create an individual YAML config file if you want to
OTA update the devices in the future.


.. _esphome-creators_project:

Project information
-------------------

This allows creators to add the project name and version to the compiled code. It is currently only
exposed via the logger, mDNS and the device_info response via the native API. The format of the name
should be ``author_name.project_name``.

.. code-block:: yaml

    # Example configuration
    esphome:
      ...
      project:
        name: "jesse.leds_party"
        version: "1.0.0"


See Also
--------

- :ghedit:`Edit`
