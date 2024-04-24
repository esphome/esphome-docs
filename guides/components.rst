The Components
==============

EspHome is fully build up round components. Each component can be fully configurated through the YAML configuration file.
This YAML file is just to configurate one device. Everything the compiler needs to know how it needs to build the firmware
needs to be writen in this document. There are just two required components needed to get your first script running.
First de  :ref:`esphome: <components/esphome>` component, this tells the compiler what the name and the basic compile
directives are. The second component you cant without is selecting one of the supported :ref:`devices: <devices>`,
without the compiler does not know for which microcontroller the firmware needs to be build.

Now you are ready to add as many components till the mememory is full. Below are some components that could be useful
for you. The others can be find on the index page. Just browse the monthly growing list of posible options.

Before you are going to dig in it is best to read the :doc:`this section <guides/automations>` first. This explains more about
automations and templates etc..

The next step
-------------
When you only the above two components added to your YAML script there is no way yet to communicate with the device.
So you need to decide how you want to communicate with the device, lucky we have troughed about that and offer a couple of
ways to do this via :ref:`network options <network-hardware>` with :doc:`Native API <components/api>` :doc:`MQTT <components/mqtt>`.
Or the difficult way using :ref:`bluetooth <bluetooth-ble>` or the :ref:`hardware peripheral <hardware-peripheral-interfaces-busses>`.

.. _automation-networkless:

Does ESPHome Work Without a Network Connection
------------------------------------------------

YES! Every thing you define in ESPHome are executed on the ESP itself and will continue to
work even if the WiFi network is down or the MQTT server is not reachable.

There is one caveat though: ESPHome automatically reboots if no connection to the MQTT broker can be
made. This is because the ESPs typically have issues in their network stacks that require a reboot to fix.
You can adjust this behavior (or even disable automatic rebooting) using the ``reboot_timeout`` option
in the :doc:`wifi component </components/wifi>` and :doc:`mqtt component </components/mqtt>`.
(Beware that effectively disables the reboot watchdog, so you will need to power cycle the device
if it fails to connect to the network without a reboot)


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
        pin: GPIO16
        on_multi_click: !include { file: on-multi-click.yaml, vars: { id: 1 } } # inline syntax
      - platform: gpio
        id: button2
        pin: GPIO4
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
      sda: GPIO21
      scl: GPIO22
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

.. _config-globals:

Global Variables
----------------

In some cases you might require to share a global variable across multiple lambdas. For example,
global variables can be used to store the state of a garage door.

.. code-block:: yaml

    # Example configuration entry
    globals:
      - id: my_global_int
        type: int
        restore_value: no
        initial_value: '0'
      # Example for global string variable
      - id: my_global_string
        type: std::string
        restore_value: yes
        max_restore_data_length: 24
        initial_value: '"Global value is"'

   # In an automation
   on_press:
     then:
       - lambda: |-
           if (id(my_global_int) > 5) {
             // global value is greater than 5
             id(my_global_int) += 1;
           } else {
             id(my_global_int) += 10;
           }

           ESP_LOGD(TAG, "%s: %d", id(my_global_string).c_str(), id(my_global_int));

Configuration variables:

- **id** (**Required**, :ref:`config-id`): Give the global variable an ID so that you can refer
  to it later in :ref:`lambdas <config-lambda>`.
- **type** (**Required**, string): The C++ type of the global variable, for example ``bool`` (for ``true``/``false``),
  ``int`` (for integers), ``float`` (for decimal numbers), ``int[50]`` for an array of 50 integers, etc.
- **restore_value** (*Optional*, boolean): Whether to try to restore the state on boot up.
  Be careful: on the ESP8266, you only have a total of 96 bytes available for this! Defaults to ``no``.
  This will use storage in "RTC memory", so it won't survive a power-cycle unless you use the ``esp8266_restore_from_flash`` option to save to flash. See :doc:`esp8266_restore_from_flash </components/esphome>` for details.
- **max_restore_data_length** (*Optional*, integer): Only applies to variables of type ``std::string``.  ESPHome will allocate enough space for this many characters,
  plus single character of overhead. Strings longer than this will not be saved. The max value of this variable is 254 characters, and the default is 63 characters.
- **initial_value** (*Optional*, string): The value with which to initialize this variable if the state
  can not be restored or if state restoration is not enabled. This needs to be wrapped in quotes! Defaults to
  the C++ default value for this type (for example ``0`` for integers).

.. _globals-set_action:

Action *globals.set*
********************

This :ref:`Action <config-action>` allows you to change the value of a :ref:`global <config-globals>`
variable without having to go through the lambda syntax.

.. code-block:: yaml

    on_...:
      - globals.set:
          id: my_global_var
          value: '10'

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The :ref:`config-id` of the global variable to set.
- **value** (**Required**, :ref:`templatable <config-templatable>`): The value to set the global
  variable to.

.. _script:

Scripts
-------

With the ``script:`` component you can define a list of steps in a central place, and then
execute the script with a single call.

.. code-block:: yaml

    # Example configuration entry
    script:
      - id: my_script
        then:
          - switch.turn_on: my_switch
          - delay: 1s
          - switch.turn_off: my_switch


Configuration variables:

- **id** (**Required**, :ref:`config-id`): The :ref:`config-id` of the script. Use this
  to interact with the script using the script actions.
- **mode** (*Optional*, string): Controls what happens when a script is
  invoked while it is still running from one or more previous invocations. Default to ``single``.

    - ``single``: Do not start a new run. Issue a warning.
    - ``restart``: Start a new run after first stopping previous run.
    - ``queued``: Start a new run after previous runs complete.
    - ``parallel``: Start a new, independent run in parallel with previous runs.

- **max_runs** (*Optional*, int): Allows limiting the maxiumun number of runs when using script
  modes ``queued`` and ``parallel``, use value ``0`` for unlimited runs. Defaults to ``0``.
- **parameters** (*Optional*, :ref:`Script Parameters <script-parameters>`): A script can define one
  or more parameters that must be provided in order to execute. All parameters defined here are
  mandatory and must be given when calling the script.
- **then** (**Required**, :ref:`Action <config-action>`): The action to perform.

.. _script-parameters:

Script Parameters
*****************

Scripts can be defined with parameters. The arguments given when calling the script can be used within
the script's lambda actions. To define the parameters, add the parameter names under `parameters:` key
and specify the data type for that parameter.

Supported data types:

* `bool`: A boolean true/false. C++ type: `bool`
* `int`: An integer. C++ type: `int32_t`
* `float`: A floating point number. C++ type: `float`
* `string`: A string. C++ type: `std::string`

Each of these also exist in array form:

* `bool[]`: An array of boolean values. C++ type: `std::vector<bool>`
* Same for other types.

.. code-block:: yaml

    script:
      - id: blink_light
        parameters:
          delay_ms: int
        then:
          - light.turn_on: status_light
          # The param delay_ms is accessible using a lambda
          - delay: !lambda return delay_ms;
          - light.turn_off: status_light

.. _script-execute_action:

Actions
*******

*script.execute*
~~~~~~~~~~~~~~~~

This action executes the script. The script **mode** dictates what will happen if the
script was already running.

.. code-block:: yaml

    # in a trigger:
    on_...:
      then:
        - script.execute: my_script

        # Calling a non-parameterised script in a lambda
        - lambda: id(my_script).execute();

        # Calling a script with parameters
        - script.execute:
            id: blink_light
            delay_ms: 500

        # Calling a parameterised script inside a lambda
        - lambda: id(blink_light)->execute(1000);

.. _script-stop_action:

*script.stop*
~~~~~~~~~~~~~

This action allows you to stop a given script during execution. If the
script is not running, it does nothing.
This is useful if you want to stop a script that contains a
``delay`` action, ``wait_until`` action, or is inside a ``while`` loop, etc.
You can also call this action from the script itself, and any subsequent action
will not be executed.

.. code-block:: yaml

    # Example configuration entry
    script:
      - id: my_script
        then:
          - switch.turn_on: my_switch
          - delay: 1s
          - switch.turn_off: my_switch

    # in a trigger:
    on_...:
      then:
        - script.stop: my_script

or as lambda

.. code-block:: yaml

    lambda: 'id(my_script).stop();'

.. _script-wait_action:

*script.wait*
~~~~~~~~~~~~~

This action suspends execution of the automation until a script has finished executing.

Note: If no script is executing, this will continue immediately. If multiple instances
of the script are running in parallel, this will block until all of them have terminated.

.. code-block:: yaml

    # Example configuration entry
    script:
      - id: my_script
        then:
          - switch.turn_on: my_switch
          - delay: 1s
          - switch.turn_off: my_switch

    # in a trigger:
    on_...:
      then:
        - script.execute: my_script
        - script.wait: my_script

This can't be used in a lambda as it would block all functioning of the device.  The script wouldn't even get to run.

.. _script-is_running_condition:

Conditions
**********

*script.is_running*
~~~~~~~~~~~~~~~~~~~

This :ref:`condition <config-condition>` allows you to check if a given script is running.
In case scripts are run in ``parallel``, this condition only tells you if at least one script
of the given id is running, not how many. Not designed for use with :ref:`while <while_action>`, instead try :ref:`script.wait <script-wait_action>`.

.. code-block:: yaml

    on_...:
      if:
        condition:
          - script.is_running: my_script
        then:
          - logger.log: Script is running!

or as lambda

.. code-block:: yaml

    lambda: |-
        if (id(my_script).is_running()) {
            ESP_LOGI("main", "Script is running!");
        }

.. _interval:

Intervals
---------

This component allows you to run actions at fixed time intervals.
For example if you want to toggle a switch every minute, you can use this component.
Please note that it's possible to achieve the same thing with the :ref:`time.on_time <time-on_time>`
trigger, but this technique is more light-weight and user-friendly.

.. code-block:: yaml

    # Example configuration entry
    interval:
      - interval: 1min
        then:
          - switch.toggle: relay_1


If a startup delay is configured, the first execution of the actions will not occur before at least that time
after boot.

Configuration variables:

- **interval** (**Required**, :ref:`config-time`): The interval to execute the action with.
- **startup_delay** (*Optional*, :ref:`config-time`): An optional startup delay - defaults to zero.
- **then** (**Required**, :ref:`Action <config-action>`): The action to perform.
