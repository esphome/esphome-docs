esphomeyaml Core Configuration
==============================

Here you specify some core information that esphomeyaml needs to create
firmwares. Most importantly, this is the section of the configuration
where you specify the **name** of the node, the **platform** and
**board** you’re using.

.. code:: yaml

    # Example configuration entry
    esphomeyaml:
        name: livingroom
        platform: ESP32
        board: nodemcu-32s

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **name** (**Required**, string): This is the name of the node. It
  should always be unique to the node and no other node in your system
  can use the same name. It can also only contain upper/lowercase
  characters, digits and underscores.
- **platform** (**Required**, string): The platform your board is on,
  either ``ESP32`` or ``ESP8266``. See :ref:`using_latest_arduino_framework`.
- **board** (**Required**, string): The board esphomeyaml should
  specify for platformio. For the ESP32, choose the appropriate one
  from `this list <http://docs.platformio.org/en/latest/platforms/espressif32.html#boards>`__
  and use `this list <http://docs.platformio.org/en/latest/platforms/espressif8266.html#boards>`__
  for ESP8266-based boards.

Advanced options:

- **library_uri** (*Optional*, string): You can manually specify the
  `version of esphomelib <https://github.com/OttoWinter/esphomelib/releases>`__ to
  use here. Accepts all parameters of `platformio lib
  install <http://docs.platformio.org/en/latest/userguide/lib/cmd_install.html#id2>`__.
  Use ``https://github.com/OttoWinter/esphomelib.git`` for the latest
  (unstable) build. Defaults to the latest stable version.
- **simplify** (*Optional*, boolean): Whether to simplify the
  auto-generated code, i.e. whether to remove unused variables, use
  ``auto`` types and so on. Defaults to ``true``.
- **use_build_flags** (*Optional*, boolean): If esphomeyaml should manually set
  build flags that specifically set what should be included in the binary. Most of
  this is already done automatically by the linker but this option can help with
  shrinking the firmware size while slowing down compilation. Defaults to ``true``.
- **build_path** (*Optional*, string): Customize where esphomeyaml will store the build files
  for your node. By default, esphomeyaml puts all platformio project files under a folder ``<NODE_NAME>/``,
  but you can customize this behavior using this option.

Automations:

- **on_boot** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the node starts. See :ref:`esphomeyaml-on_boot`.
- **on_shutdown** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  right before the node shuts down. See :ref:`esphomeyaml-on_shutdown`.

.. _using_latest_arduino_framework:

Using the latest Arduino framework version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default version of the arduino framework distributed through platformio is usually quite old
and the latest staging versions of the framework can in some cases increase stability a lot.

To use the latest version of the arduino framework with esphomeyaml, specify an URL pointing to
the staging version using the ``platform:`` parameter.

For the ESP32, this URL is https://github.com/platformio/platform-espressif32.git#feature/stage.
And for the ESP8266, the URL is https://github.com/platformio/platform-espressif8266.git#feature/stage.

.. code:: yaml

    # Example configuration entry
    esphomeyaml:
        name: livingroom
        platform: 'https://github.com/platformio/platform-espressif32.git#feature/stage'
        board: nodemcu-32s

.. _esphomeyaml-on_boot:

``on_boot``
"""""""""""

This automation will be triggered when the ESP boots up. By default, it is executed after everything else
is already set up. You can however change this using the ``priority`` parameter.

.. code:: yaml

    esphomeyaml:
      # ...
      on_boot:
        priority: -10
        # ...
        then:
          - switch.turn_off:
              id: switch_1

Configuration variables:

- **priority** (*Optional*, float): The priority to execute your custom initialization code. A higher value (for example
  positive values) mean a high priority and thus also your code being executed earlier. So for example negative priorities
  are executed very late. Defaults to ``-10``. Priorities (you can use any value between them too):

  - ``100``: This is where all hardware initialization of vital components is executed. For example setting switches
    to their initial state.
  - ``10``: At this priority, WiFi is initialized.
  - ``7.5``: MQTT initialization takes place at this priority.
  - ``0.0``: This is where most sensors are set up. They are usually set up this late so that they can dump their
    configuration in the MQTT logs.
  - ``-5.0``: The inidividual frontend counterparts for the backend components are configured at this priority
  - ``-10.0``: At this priority, pretty much everything should already be initialized.

- See :ref:`Automation <automation>`.

.. _esphomeyaml-on_shutdown:

``on_shutdown``
"""""""""""""""

This automation will be triggered when the ESP is about to shut down. Shutting down is usually caused by
too many WiFi/MQTT connection attempts, Over-The-Air updates being applied or through the :doc:`deep_sleep`.

.. note::

    It's not guaranteed that all components are in a connected state when this automation is triggered. For
    example, the MQTT client may have already disconnected.

.. code:: yaml

    esphomeyaml:
      # ...
      on_shutdown:
        then:
          - switch.turn_off:
              id: switch_1

Configuration variables: See :ref:`Automation <automation>`.

See Also
~~~~~~~~

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/esphomeyaml.rst>`__
