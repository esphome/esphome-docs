Configuration Types
===================

.. seo::
    :description: Documentation of different configuration types in ESPHome
    :image: settings.svg

ESPHome’s configuration files have several configuration types. This
page describes them.

.. _config-id:

ID
--

Quite an important aspect of ESPHome are “IDs”. They are used to
connect components from different domains. For example, you define an
output component together with an ID and then later specify that same ID
in the light component. IDs should always be unique within a
configuration and ESPHome will warn you if you try to use the same
ID twice.

Because ESPHome converts your configuration into C++ code and the
IDs are in reality just C++ variable names, they must also adhere to
C++’s naming conventions. `C++ Variable
names <https://venus.cs.qc.cuny.edu/~krishna/cs111/lectures/D3_C++_Variables.pdf>`__
…

-  … must start with a letter and can end with numbers.
-  … must not have a space in the name.
-  … can not have special characters except the underscore (“_“).
-  … must not be a keyword.


.. note::

    These IDs are used only within ESPHome and are not translated to Home Assistant's Entity ID.


.. _config-pin:

Pin
---

ESPHome always uses the **chip-internal GPIO numbers**. These
internal numbers are always integers like ``16`` and can be prefixed by
``GPIO``. For example to use the pin with the **internal** GPIO number 16,
you could type ``GPIO16`` or just ``16``.

Most boards however have aliases for certain pins. For example the NodeMCU
ESP8266 uses pin names ``D0`` through ``D8`` as aliases for the internal GPIO
pin numbers. Each board (defined in :doc:`ESPHome section </components/esphome>`)
has their own aliases and so not all of them are supported yet. For example,
for the ``D0`` (as printed on the PCB silkscreen) pin on the NodeMCU ESP8266
has the internal GPIO name ``GPIO16``, but also has an alias ``D0``. So using
either one of these names in your configuration will lead to the same result.

.. code-block:: yaml

    some_config_option:
      pin: GPIO16

    some_config_option:
      # alias on the NodeMCU ESP8266:
      pin: D0

.. _config-pin_schema:

Pin Schema
----------

In some places, ESPHome also supports a more advanced “pin schema”.

.. code-block:: yaml

    some_config_option:
      # Basic:
      pin: GPIOXX

      # Advanced:
      pin:
        number: GPIOXX
        inverted: true
        mode:
          input: true
          pullup: true

Configuration variables:

-  **number** (**Required**, pin): The pin number.
-  **inverted** (*Optional*, boolean): If all read and written values
   should be treated as inverted. Defaults to ``false``.
-  **allow_other_uses** (*Optional*, boolean): If the pin is also specified elsewhere in the configuration.
   By default multiple uses of the same pin will be flagged as an error. This option will suppress the error and is
   intended for rare cases where a pin is shared between multiple components. Defaults to ``false``.

-  **mode** (*Optional*, string or mapping): Configures the pin to behave in different
   modes like input or output. The default value depends on the context.
   Accepts either a shorthand string or a mapping where each feature can be individually
   enabled/disabled:

   - **input** (*Optional*, boolean): If true, configure the pin as an input.
   - **output** (*Optional*, boolean): If true, configure the pin as an output.
   - **pullup** (*Optional*, boolean): Activate internal pullup resistors on the pin.
   - **pulldown** (*Optional*, boolean): Activate internal pulldown resistors on the pin.
   - **open_drain** (*Optional*, boolean): Set the pin to open-drain (as opposed to push-pull).
     The active pin state will then result in a high-impedance state.

   For compatibility some shorthand modes can also be used.

   - ``INPUT``
   - ``OUTPUT``
   - ``OUTPUT_OPEN_DRAIN``
   - ``ANALOG``
   - ``INPUT_PULLUP``
   - ``INPUT_PULLDOWN``
   - ``INPUT_OUTPUT_OPEN_DRAIN``

Advanced options:

- **drive_strength** (*Optional*, string): On ESP32s with esp-idf framework the pad drive strength,
  i.e. the maximum amount of current can additionally be set. Defaults to ``20mA``.
  Options are ``5mA``, ``10mA``, ``20mA``, ``40mA``.
- **ignore_strapping_warning** (*Optional*, boolean): Certain pins on ESP32s are designated *strapping pins* and are read
  by the chip on reset to configure initial operation, e.g. to enable bootstrap mode.
  Using such pins for I/O should be avoided and ESPHome will warn if I/O is configured on a strapping pin.

  For more detail see :ref:`strapping-warnings`.

  If you are *absolutely* sure that you are using a strapping pin for I/O in a way that will not cause problems,
  you can suppress the warning by setting this option to ``true`` in the pin configuration.

.. _config-time:

Time
----

In lots of places in ESPHome you need to define time periods.
There are several ways of doing this. See below examples to see how you can specify time periods:

.. code-block:: yaml

    some_config_option:
      some_time_option: 1000us  # 1000 microseconds = 1ms
      some_time_option: 1000ms  # 1000 milliseconds
      some_time_option: 1.5s  # 1.5 seconds
      some_time_option: 0.5min  # half a minute
      some_time_option: 2h  # 2 hours

      # Make sure you wrap these in quotes
      some_time_option: '2:01'  # 2 hours 1 minute
      some_time_option: '2:01:30'  # 2 hours 1 minute 30 seconds

      # 10ms + 30s + 25min + 3h
      some_time_option:
        milliseconds: 10
        seconds: 30
        minutes: 25
        hours: 3
        days: 0

      # for all 'update_interval' options, also
      update_interval: never  # never update
      update_interval: 0ms  # update in every loop() iteration

.. _config-substitutions:

Substitutions
-------------

Starting with version 1.10.0, ESPHome has a powerful new way to reduce repetition in configuration files:
Substitutions. With substitutions, you can have a single generic source file for all nodes of one kind and
substitute expressions in.

.. code-block:: yaml

    substitutions:
      devicename: livingroom
      upper_devicename: Livingroom

    esphome:
      name: $devicename
      # ...

    sensor:
    - platform: dht
      # ...
      temperature:
        name: ${upper_devicename} Temperature
      humidity:
        name: ${upper_devicename} Humidity

In the top-level ``substitutions`` section, you can put as many key-value pairs as you want. Before
validating your configuration, ESPHome will automatically replace all occurrences of substitutions
by their value. The syntax for a substitution is based on bash and is case-sensitive: ``$substitution_key`` or
``${substitution_key}`` (same).

Two substitution passes are performed allowing compound replacements.

.. code-block:: yaml

    substitutions:
      foo: yellow
      bar_yellow_value: !secret yellow_secret
      bar_green_value: !secret green_secret

    something:
      test: ${bar_${foo}_value}

.. _YAML-insertion-operator:

YAML insertion operator
***********************

Additionally, you can use the YAML insertion operator ``<<`` syntax to create a single YAML file from which a number
of nodes inherit:

.. code-block:: yaml

    # In common.yaml
    esphome:
      name: $devicename
      # ...

    sensor:
    - platform: dht
      # ...
      temperature:
        name: ${upper_devicename} Temperature
      humidity:
        name: ${upper_devicename} Humidity

.. code-block:: yaml

    # In nodemcu1.yaml
    substitutions:
      devicename: nodemcu1
      upper_devicename: NodeMCU 1

    <<: !include common.yaml

.. tip::

    To hide these base files from the dashboard, you can

    - Place them in a subdirectory (dashboard only shows files in top-level directory)
    - Prepend a dot to the filename, like ``.base.yaml``

.. _substitute-include-variables:

Substitute !include variables
*****************************

ESPHome's ``!include`` accepts a list of variables that can be substituted within the included file.

.. code-block:: yaml

    binary_sensor:
      - platform: gpio
        id: button1
        pin: GPIOXX
        on_multi_click: !include { file: on-multi-click.yaml, vars: { id: 1 } } # inline syntax
      - platform: gpio
        id: button2
        pin: GPIOXX
        on_multi_click: !include
          # multi-line syntax
          file: on-multi-click.yaml
          vars:
            id: 2

``on-multi-click.yaml``:

.. code-block:: yaml

    - timing: !include click-single.yaml
      then:
        - mqtt.publish:
            topic: ${device_name}/button${id}/status
            payload: single
    - timing: !include click-double.yaml
      then:
        - mqtt.publish:
            topic: ${device_name}/button${id}/status
            payload: double

.. _command-line-substitutions:

Command line substitutions
**************************

You can define or override substitutions from the command line by adding e.g. ``-s KEY VALUE``
which overrides substitution KEY and gives it value VALUE. This can be issued multiple times,
so e.g. with the following ``example.yaml`` file:

.. code-block:: yaml

    substitutions:
      name: default
      platform: ESP8266

    esphome:
      name: $name
      platform: $platform
      board: $board

and the following command:

.. code-block:: bash

    esphome -s name device01 -s board esp01_1m example.yaml config

You will get something like the following output (please note the unchanged ``platform``,
added ``board``, and overridden ``name`` substitutions):

.. code-block:: yaml

    substitutions:
      name: device01
      platform: ESP8266
      board: esp01_1m
    esphome:
      name: device01
      platform: ESP8266
      board: esp01_1m
      includes: []
      libraries: []
      esp8266_restore_from_flash: false
      build_path: device01
      platformio_options: {}
      arduino_version: espressif8266@2.2.3

We can observe here that command line substitutions take precedence over the ones in
your configuration file. This can be used to create generic 'template' configuration
files (like the ``example.yaml`` above) which can be used for multiple devices,
using substitutions which are provided on the command line.

.. _config-packages:

Packages
--------

Another way to modularize and reuse your configuration is to use packages. This feature allows
you to put common pieces of configuration in separate files and keep only unique pieces of your
config in the main yaml file. All definitions from packages will be merged with your main
config in non-destructive way so you could always override some bits and pieces of package
configuration. Substitutions in your main config will override substitutions with the same
name in a package.

Dictionaries are merged key-by-key. Lists of components are merged by component
ID if specified. Other lists are merged by concatenation. All other config
values are replaced with the later value.

Local packages
**************

Consider the following example where the author put common pieces of configuration like WiFi and
I²C into base files and extends it with some device specific configurations in the main config.

Note how the piece of configuration describing ``api`` component in ``device_base.yaml`` gets
merged with the services definitions from main config file.

.. code-block:: yaml

    # In config.yaml
    substitutions:
      node_name: mydevice
      device_verbose_name: "My Device"

    packages:
      wifi: !include common/wifi.yaml
      device_base: !include common/device_base.yaml

    api:
      services:
        - service: start_laundry
          then:
            - switch.turn_on: relay
            - delay: 3h
            - switch.turn_off: relay

    sensor:
      - platform: mhz19
        co2:
          name: "CO2"
        temperature:
          name: "Temperature"
        update_interval: 60s
        automatic_baseline_calibration: false

.. code-block:: yaml

    # In wifi.yaml
    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password
      domain: .yourdomain.lan
      fast_connect: true

.. code-block:: yaml

    # In device_base.yaml
    esphome:
      name: ${node_name}
      platform: ESP32
      board: wemos_d1_mini32
      build_path: ./build/${node_name}

    # I²C Bus
    i2c:
      sda: GPIOXX
      scl: GPIOXX
      scan: true
      frequency: 100kHz

    # Enable logging
    logger:
      level: ${log_level}

    api:
      encryption:
        key: !secret api_encryption_key
      reboot_timeout: 1h

    sensor:
      - <<: !include common/sensor/uptime.config.yaml
      - <<: !include common/sensor/wifi_signal.config.yaml
    binary_sensor:
      - <<: !include common/binary_sensor/connection_status.config.yaml

    switch:
      - <<: !include common/switch/restart_switch.config.yaml

.. _config-git_packages:

Remote/git Packages
*******************

Packages can also be loaded from a git repository by utilizing the correct config syntax.
:ref:`config-substitutions` can be used inside the remote packages which allows users to override
them locally with their own subsitution value.

.. note::

    Remote packages cannot have ``secret`` lookups in them. They should instead make use of substitutions with an
    optional default in the packaged YAML, which the local device YAML can set using values from the local secrets.

.. code-block:: yaml

    packages:
      # Git repo examples
      remote_package:
        url: https://github.com/esphome/non-existant-repo
        ref: main # optional
        files: [file1.yml, file2.yml]
        refresh: 1d # optional

      # A single file can be expressed using `file` or `files` as a string
      remote_package_two:
        url: https://github.com/esphome/non-existant-repo
        file: file1.yml # cannot be combined with `files`
        # files: file1.yml

      # shorthand form github://username/repository/[folder/]file-path.yml[@branch-or-tag]
      remote_package_three: github://esphome/non-existant-repo/file1.yml@main

Packages as Templates
*********************

Since packages are incorporated using the ``!include`` system,
variables can be provided to them.  This means that packages can be
used as `templates`, allowing complex or repetitive configurations to
be stored in a package file and then incorporated into the
configuration more than once.
Additionally packages could contain a ``defaults`` block which provides
subsitutions for variables not provided by the ``!include`` block.

As an example, if the configuration needed to support three garage
doors using the ``gpio`` switch platform and the ``time_based`` cover
platform, it could be constructed like this:

.. code-block:: yaml

    # In config.yaml
    packages:
      left_garage_door: !include
        file: garage-door.yaml
        vars:
          door_name: Left
          door_location: left
          open_switch_gpio: 25
          close_switch_gpio: 26
      middle_garage_door: !include
        file: garage-door.yaml
        vars:
          door_name: Middle
          door_location: middle
          open_switch_gpio: 27
          close_switch_gpio: 29
      right_garage_door: !include
        file: garage-door.yaml
        vars:
          door_name: Right
          door_location: right
          open_switch_gpio: 15
          close_switch_gpio: 18
          open_duration: "1min"
          close_duration: "50s"


.. code-block:: yaml

    # In garage-door.yaml
    defaults:
      open_duration: "2.1min"
      close_duration: "2min"

    switch:
      - id: open_${door_location}_door_switch
        name: ${door_name} Garage Door Open Switch
        platform: gpio
        pin: ${open_switch_gpio}

      - id: close_${door_location}_door_switch
        name: ${door_name} Garage Door Close Switch
        platform: gpio
        pin: ${close_switch_gpio}

    cover:
      - platform: time_based
        name: ${door_name} Garage Door

        open_action:
          - switch.turn_on: open_${door_location}_door_switch
        open_duration: ${open_duration}

        close_action:
          - switch.turn_on: close_${door_location}_door_switch
        close_duration: ${close_duration}

        stop_action:
          - switch.turn_off: open_${door_location}_door_switch
          - switch.turn_off: close_${door_location}_door_switch

Extend
------

To make changes or add additional configuration to included configurations ``!extend config_id`` can be used, where ``config_id`` is the ID of the configuration to modify.
For example to set a specific update interval on a common uptime sensor that is shared between configurations:

.. code-block:: yaml

    packages:
      common: !include common.yaml

    sensor:
    - id: !extend uptime_sensor
      update_interval: 10s

Remove
------

To remove existing entries from included configurations ``!remove [config_id]`` can be used, where ``config_id`` is the ID of the entry to modify.
For example to remove a common uptime sensor that is shared between configurations:

.. code-block:: yaml

    packages:
      common: !include common.yaml

    sensor:
      - id: !remove uptime_sensor

To remove captive portal for a specific device:

.. code-block:: yaml

    packages:
      common: !include common.yaml

    captive_portal: !remove

See Also
--------

- :doc:`ESPHome index </index>`
- :doc:`getting_started_command_line`
- :doc:`faq`
- :ghedit:`Edit`
