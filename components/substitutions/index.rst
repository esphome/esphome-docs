Substitutions
=============

.. seo::
    :description: How to use substitutions in ESPHome
    :image: settings.svg

ESPHome has a powerful way to reduce repetition in configuration files: substitutions.
With substitutions, you can have a single generic source file for all nodes of one kind and
substitute expressions in as required.

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
-----------------------

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
-----------------------------

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
--------------------------

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

See Also
--------

- :doc:`ESPHome index </index>`
- :doc:`/guides/getting_started_command_line`
- :doc:`/guides/faq`
- :ghedit:`Edit`
