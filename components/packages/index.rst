Packages
========

.. seo::
    :description: How to use packages in ESPHome
    :image: settings.svg

When you have many ESPHome devices (or are producing and distributing them at scale), a common need tends to surface:
configuration modularization. You'll likely want to break your configuration into common (groups of) elements, building
it into reusable pieces which can subsequently be used by many/all devices. Only unique pieces of your configuration
remain in any given device's YAML configuration file.

This can be accomplished with ESPHome's ``packages`` feature.

All definitions from packages will be merged with your device's main configuration in a non-destructive way. This
allows overriding (parts of) configuration contained in the package(s). Substitutions in your main configuration will
override substitutions with the same name in a package.

Dictionaries are merged key-by-key. Lists of components are merged by component ID (if specified). Other lists are
merged by concatenation. All other configuration values are replaced with the later value.

Local Packages
--------------

Consider the following example where the author put common pieces of configuration (like Wi-Fi and I²C) into base files
and then extends it with some device-specific configuration in the main configuration.

Note how the piece of configuration describing ``api`` component in ``device_base.yaml`` gets merged with the services
definitions from main configuration file.

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

Remote/Git Packages
-------------------

Packages can also be loaded from a Git repository by utilizing the correct configuration syntax.
:doc:`/components/substitutions/index` can be used inside the remote packages which allows users to override
them locally with their own substitution value.

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
---------------------

Since packages are incorporated using the ``!include`` system, variables can be provided to them. This means that
packages can be used as *templates*, allowing complex or repetitive configurations to be stored in a package file
and then incorporated into the configuration more than once.

Packages may also contain a ``defaults`` block which provides subsitutions for variables not provided by the
``!include`` block.

As an example, if the configuration needed to support three garage doors using the ``gpio`` switch platform and the
``time_based`` cover platform, it could be constructed like this:

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

To make changes or add additional configuration to included configurations, ``!extend config_id`` can be used, where
``config_id`` is the ID of the configuration to modify.

For example, to set a specific update interval on a common uptime sensor that is shared between configurations:

.. code-block:: yaml

    packages:
      common: !include common.yaml

    sensor:
      - id: !extend uptime_sensor
        update_interval: 10s

Remove
------

To remove existing entries from included configurations, ``!remove [config_id]`` can be used, where ``config_id`` is
the ID of the entry to modify.

For example, to remove a common uptime sensor that is shared between configurations:

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
- :doc:`/guides/getting_started_command_line`
- :doc:`/guides/faq`
- :ghedit:`Edit`
