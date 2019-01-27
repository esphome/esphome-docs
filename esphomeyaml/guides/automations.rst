.. _automation:

Automations And Templates
=========================

.. seo::
    :description: Getting started guide for automations in esphomelib.
    :image: auto-fix.png

Automations and templates are two very powerful concepts of esphomelib/yaml. Automations
allow you to perform actions under certain conditions and templates are a way to easily
customize everything about your node without having to dive into the full esphomelib C++
API.

Let's begin with an example to explain these concepts. Suppose you have this configuration file:

.. code-block:: yaml

    switch:
      - platform: gpio
        pin: GPIO3
        name: "Living Room Dehumidifier"

    binary_sensor:
      - platform: gpio
        pin: GPIO4
        name: "Living Room Dehumidifier Toggle Button"

With this file you can already perform some basic tasks. You can control the ON/OFF state
of the dehumidifier in your living room from Home Assistant's front-end. But in many cases,
controlling everything strictly from the frontend is quite a pain. That's why you have
decided to also install a simple push button next to the dehumidifier on pin GPIO4.
A simple push on this button should toggle the state of the dehumidifier.

You *could* write an automation to do this task in Home Assistant's automation engine, but
ideally the IoT should work without an internet connection and should not break with
the MQTT server being offline.

That's why, starting with esphomelib 1.7.0, there's a new automation engine. With it, you
can write some basic (and also some more advanced) automations using a syntax that is
hopefully a bit easier to read and understand than Home Assistant's.

For example, this configuration would achieve your desired behavior:

.. code-block:: yaml

    switch:
      - platform: gpio
        pin: GPIO3
        name: "Living Room Dehumidifier"
        id: dehumidifier1

    binary_sensor:
      - platform: gpio
        pin: GPIO4
        name: "Living Room Dehumidifier Toggle Button"
        on_press:
          then:
            - switch.toggle: dehumidifier1



Woah, hold on there. Please explain what's going on here! Sure :) Let's step through what's happening here.

.. code-block:: yaml

    switch:
       - platform: gpio
         # ...
         id: dehumidifier1

First, we have to give the dehumidifier an :ref:`config-id` so that we can
later use it inside our awesome automation.

.. code-block:: yaml

    binary_sensor:
      - platform: gpio
        # ...
        on_press:

We now attach a special attribute ``on_press`` to the toggle button. This part is called a "trigger". In this example,
the automation in the next few lines will execute whenever someone *begins* to press the button. Note the terminology
follows what you would call these events on mouse buttons. A *press* happens when you begin pressing the button/mouse.
There are also other triggers like ``on_release``, ``on_click`` or ``on_double_click`` available.


.. code-block:: yaml

    # ...
    on_press:
      then:
        - switch.toggle: dehumidifier1

.. _config-action:

Actions
-------

Now comes the actual automation block. With ``then``, you tell esphomeyaml what should happen when the press happens.
Within this block, you can define several "actions". For example, ``switch.toggle`` and the line after that form an
action. Each action is separated by a dash and multiple actions can be executed in series by just adding another ``-``
like so:

.. code-block:: yaml

    # ...
    on_press:
      then:
        - switch.toggle: dehumidifier1
        - delay: 2s
        - switch.toggle: dehumidifier1

With this automation, a press on the push button would cause the dehumidifier to turn on/off for 2 seconds, and then
cycle back to its original state. Similarly you can have a single trigger with multiple automations:

.. code-block:: yaml

    # ...
    on_press:
      - then:
          - switch.toggle: dehumidifier1
      - then:
          - light.toggle: dehumidifier_indicator_light

    # Same as:
    on_press:
      then:
        - switch.toggle: dehumidifier1
        - light.toggle: dehumidifier_indicator_light


As a last example, let's make our dehumidifier smart: Let's make it turn on automatically when the humidity a sensor
reports is above 65% and make it turn off again when it reaches 50%

.. code-block:: yaml

    sensor:
      - platform: dht
        humidity:
          name: "Living Room Humidity"
          on_value_range:
            - above: 65.0
              then:
                - switch.turn_on: dehumidifier1
            - below: 50.0
              then:
                - switch.turn_off: dehumidifier1
        temperature:
          name: "Living Room Temperature"

That's a lot of indentation 😉 ``on_value_range`` is a special trigger for sensors that triggers when the value output
of the sensor is within a certain range. In the first example, this range is defined as "any value above or including
65.0", and the second one refers to once the humidity reaches 50% or below.

Now that concludes the introduction into automations in esphomeyaml. They're a powerful tool to automate almost
everything on your device with an easy-to-use syntax. For the cases where the "pure" YAML automations don't work,
esphomelib has another extremely powerful tool to offer: Templates.

.. _config-lambda:

Templates (Lambdas)
-------------------

With templates inside esphomelib, you can do almost *everything*. If for example you want to only perform a certain
automation if a certain complex formula evaluates to true, you can do that with templates. Let's look at an example
first:

.. code-block:: yaml

    binary_sensor:
      - platform: gpio
        name: "Cover End Stop"
        id: top_end_stop
    cover:
      - platform: template
        name: Living Room Cover
        lambda: !lambda |-
          if (id(top_end_stop).state) {
            return cover::COVER_OPEN;
          } else {
            return cover::COVER_CLOSED;
          }

What's happening here? First, we define a binary sensor (with the id ``top_end_stop``) and then a
:doc:`template cover </esphomeyaml/components/cover/template>`. The *state* of the template cover is
controlled by a template, or "lambda". In lambdas you're effectively writing C++ code and therefore the
name lambda is used instead of Home Assistant's "template" lingo to avoid confusion. But before you go
shy away from using lambdas because you just hear C++ and think oh noes, I'm not going down *that* road:
Writing lambdas is not that hard! Here's a bit of a primer:

First, you might have already wondered what the ``lambda: !lambda |-`` part is supposed to mean. ``!lambda``
tells esphomeyaml that the following block is supposed to be interpreted as a lambda, or C++ code. Note that
here, the ``lambda:`` key would actually implicitly make the following block a lambda so in this context,
you could have just written ``lambda: |-``.

Next, there's the weird ``|-`` character combination. This effectively tells the YAML parser to treat the following
**indented** (!) block as plaintext. Without it, the YAML parser would attempt to read the following block as if
it were made up of YAML keys like ``cover:`` for example. (You may also have seen variations of this like ``>-``
or just ``|`` or ``>``. There's a slight difference in how these different styles deal with whitespace, but for our
purposes we can ignore that).

With ``if (...) { ... } else { ... }`` we create a *condition*. What this effectively says that if the thing inside
the first parentheses evaluates to ``true``` then execute the first block (in this case ``return cover::COVER_OPEN;``,
or else evaluate the second block. ``return ...;`` makes the code block give back a value to the template. In this case,
we're either *returning* ``cover::COVER_OPEN`` or ``cover::COVER_CLOSED`` to indicate that the cover is closed or open.

Finally, ``id(...)`` is a helper function that makes esphomeyaml fetch an object with the supplied ID (which you defined
somewhere else, like ``top_end_stop```) and let's you call any of esphomelib's many APIs directly. For example, here
we're retrieving the current state of the end stop using ``.state`` and using it to construct our cover state.

.. note::

    esphomeyaml (currently) does not check the validity of lambda expressions you enter and will blindly copy
    them into the generated C++ code. If compilation fails or something else is not working as expected
    with lambdas, it's always best to look at the generated C++ source file under ``<NODE_NAME>/src/main.cpp``.

.. tip::

    To store local variables inside lambdas that retain their value across executions, you can create ``static``
    variables like so. In this example the variable ``num_executions`` is incremented by one each time the
    lambda is executed and the current value is logged.

    .. code-block:: yaml

        lambda: |-
          static int num_executions = 0;
          ESP_LOGD("main", "I am at execution number %d", num_executions);
          num_executions += 1;

.. _config-templatable:

Bonus: Templating Actions
*************************

Another feature of esphomeyaml is that you can template almost every parameter for actions in automations. For example
if you have a light and want to set it to a pre-defined color when a button is pressed, you can do this:

.. code-block:: yaml

    on_press:
      then:
        - light.turn_on:
            id: some_light_id
            transition_length: 0.5s
            red: 0.8
            green: 1.0
            blue: !lambda |-
              // The sensor outputs values from 0 to 100. The blue
              // part of the light color will be determined by the sensor value.
              return id(some_sensor).state / 100.0;

Every parameter in actions that has the label "templatable" in the docs can be templated like above, using
all of the usual lambda syntax.

.. _config-globals:

Bonus 2: Global Variables
*************************

In some cases you might require to share a global variable across multiple lambdas. For example,
global variables can be used to store the state of a garage door.

.. code-block:: yaml

    # Example configuration entry
    globals:
      - id: my_global_int
        type: int
        restore_value: no
        initial_value: '0'

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

           ESP_LOGD(TAG, "Global value is: %d", id(my_global_int));

Configuration options:

- **id** (**Required**, :ref:`config-id`): Give the global variable an ID so that you can refer
  to it later in :ref:`lambdas <config-lambda>`.
- **type** (**Required**, string): The C++ type of the global variable, for example ``bool`` (for ``true``/``false``),
  ``int`` (for integers), ``float`` (for decimal numbers), ``int[50]`` for an array of 50 integers, etc.
- **restore_value** (*Optional*, boolean): Whether to try to restore the state on boot up.
  Be careful: on the ESP8266, you only have a total of 96 bytes available for this! Defaults to ``no``.
- **initial_value** (*Optional*, string): The value with which to initialize this variable if the state
  can not be restored or if state restoration is not enabled. This needs to be wrapped in quotes! Defaults to
  the C++ default value for this type (for example ``0`` for integers).

.. _automation-networkless:

Do Automations Work Without a Network Connection
************************************************

YES! All automations you define in esphomelib are execute on the ESP itself and will continue to
work even if the WiFi network is down or the MQTT server is not reachable.

There is one caveat though: esphomelib automatically reboots if no connection to the MQTT broker can be
made. This is because the ESPs typically have issues in their network stacks that require a reboot to fix.
You can adjust this behavior (or even disable automatic rebooting) using the ``reboot_timeout`` option
in the :doc:`wifi component </esphomeyaml/components/wifi>` and :doc:`mqtt component </esphomeyaml/components/mqtt>`.

All Triggers
------------

- :ref:`mqtt.on_message <mqtt-on_message>` / :ref:`mqtt.on_json_message <mqtt-on_json_message>`
- :ref:`sensor.on_value <sensor-on_value>` / :ref:`sensor.on_raw_value <sensor-on_raw_value>` / :ref:`sensor.on_value_range <sensor-on_value_range>`
- :ref:`binary_sensor.on_press <binary_sensor-on_press>` / :ref:`binary_sensor.on_release <binary_sensor-on_release>` / :ref:`binary_sensor.on_state <binary_sensor-on_state>`
- :ref:`binary_sensor.on_click <binary_sensor-on_click>` / :ref:`binary_sensor.on_double_click <binary_sensor-on_double_click>` / :ref:`binary_sensor.on_multi_click <binary_sensor-on_multi_click>`
- :ref:`esphomeyaml.on_boot <esphomeyaml-on_boot>` / :ref:`esphomeyaml.on_shutdown <esphomeyaml-on_shutdown>` / :ref:`esphomeyaml.on_loop <esphomeyaml-on_loop>`
- :ref:`pn532.on_tag <pn532-on_tag>`
- :ref:`time.on_time <time-on_time>`
- :ref:`interval.interval <interval>`

All Actions
-----------

- :ref:`delay <delay_action>`
- :ref:`lambda <lambda_action>`
- :ref:`if <if_action>` / :ref:`while <while_action>`
- :ref:`component.update <component-update_action>`
- :ref:`script.execute <script-execute_action>` / :ref:`script.stop <script-stop_action>`
- :ref:`logger.log <logger-log_action>`
- :ref:`homeassistant.service <api-homeassistant_service_action>`
- :ref:`mqtt.publish <mqtt-publish_action>` / :ref:`mqtt.publish_json <mqtt-publish_json_action>`
- :ref:`switch.toggle <switch-toggle_action>` / :ref:`switch.turn_off <switch-turn_off_action>` / :ref:`switch.turn_on <switch-turn_on_action>`
- :ref:`light.toggle <light-toggle_action>` / :ref:`light.turn_off <light-turn_off_action>` / :ref:`light.turn_on <light-turn_on_action>`
- :ref:`cover.open <cover-open_action>` / :ref:`cover.close <cover-close_action>` / :ref:`cover.stop <cover-stop_action>`
- :ref:`fan.toggle <fan-toggle_action>` / :ref:`fan.turn_off <fan-turn_off_action>` / :ref:`fan.turn_on <fan-turn_on_action>`
- :ref:`output.turn_off <output-turn_off_action>` / :ref:`output.turn_on <output-turn_on_action>` / :ref:`output.set_level <output-set_level_action>`
- :ref:`deep_sleep.enter <deep_sleep-enter_action>` / :ref:`deep_sleep.prevent <deep_sleep-prevent_action>`

.. _config-condition:

All Conditions
--------------

- :ref:`lambda <lambda_condition>`
- :ref:`and <and_condition>` / :ref:`or <or_condition>`
- :ref:`binary_sensor.is_on <binary_sensor-is_on_condition>` / :ref:`binary_sensor.is_off <binary_sensor-is_off_condition>`
- :ref:`switch.is_on <switch-is_on_condition>` / :ref:`switch.is_off <switch-is_off_condition>`
- :ref:`sensor.in_range <sensor-in_range_condition>`

.. _delay_action:

``delay`` Action
----------------

This action delays the execution of the next action in the action list by a specified
time period.

.. code-block:: yaml

   on_...:
     then:
        - switch.turn_on: relay_1
        - delay: 2s
        - switch.turn_off: relay_1
        # Templated, waits for 1s (1000ms) only if a reed switch is active
        - delay: !lambda "if (id(reed_switch).state) return 1000; else return 0;"

.. note::

    This is a "smart" asynchronous delay - other code will still run in the background while
    the delay is happening.

.. _lambda_action:

``lambda`` Action
-----------------

This action executes an arbitrary piece of C++ code (see :ref:`Lambda <config-lambda>`).

.. code-block:: yaml

    on_...:
      then:
        - lambda: |-
            id(some_binary_sensor).publish_state(false);

.. _lambda_condition:

``lambda`` Condition
--------------------

This condition performs an arbitrary piece of C++ code (see :ref:`Lambda <config-lambda>`)
and can be used to create conditional flow in actions.

.. code-block:: yaml

    on_...:
      then:
        - if:
            condition:
              # Should return either true or false
              lambda: |-
                return id(some_sensor).state < 30;
            # ...

.. _and_condition:
.. _or_condition:

``and`` / ``or`` Condition
--------------------------

Check a combination of conditions

.. code-block:: yaml

    on_...:
      then:
        - if:
            condition:
              # Same syntax for and
              or:
                - binary_sensor.is_on: some_binary_sensor
                - binary_sensor.is_on: other_binary_sensor
            # ...

.. _if_action:

``if`` Action
-------------

This action first evaluated a certain condition (``if:``) and then either
executes the ``then:`` branch or the ``else:`` branch depending on the output of the condition.

After the chosen branch (``then`` or ``else``) is done with execution, the next action is performed.

For example below you can see an automation that checks if a sensor value is below 30 and if so
turns on a light for 5 seconds. Otherwise, the light is turned off immediately.

.. code-block:: yaml

    on_...:
      then:
        - if:
            condition:
              lambda: 'return id(some_sensor).state < 30;'
            then:
              - logger.log: "The sensor value is below 30!"
              - light.turn_on: my_light
              - delay: 5s
            else:
              - logger.log: "The sensor value is above 30!"
        - light.turn_off: my_light


Configuration options:

- **condition** (**Required**, :ref:`config-condition`): The condition to check which branch to take. See :ref:`Conditions <config-condition>`.
- **then** (*Optional*, :ref:`config-action`): The action to perform if the condition evaluates to true.
  Defaults to doing nothing.
- **else** (*Optional*, :ref:`config-action`): The action to perform if the condition evaluates to false.
  Defaults to doing nothing.

.. _while_action:

``while`` Action
----------------

This action is similar to the :ref:`if <if_action>` Action. The ``while`` action executes
a block until a given condition evaluates to false.

.. code-block:: yaml

    # In a trigger:
    on_...:
      - while:
          condition:
            binary_sensor.is_on: some_binary_sensor
          then:
          - logger.log: "Still executing"
          - light.toggle: some_light
          - delay: 5s

Configuration options:

- **condition** (**Required**): The condition to check whether to execute. See :ref:`Conditions <config-condition>`.
- **then** (**Required**, :ref:`config-action`): The action to perform until the condition evaluates to false.

.. _component-update_action:

``component.update`` Action
---------------------------

Using this action you can manually call the ``update()`` method of a component.

Please note that this only works with some component types and others will result in a
compile error.

.. code-block:: yaml

    on_...:
      then:
        - component.update: my_component

        # The same as:
        - lambda: 'id(my_component).update();'

.. _script-execute_action:

``script.execute`` Action
-------------------------

This action allows code-reuse. For example if you have multiple triggers
that perform the same exact action, you would normally have to copy the YAML lines for all
triggers.

With the ``script`` component you can define these steps in a central place, and then
execute the script with a single call.

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

.. _script-stop_action:

``script.stop`` Action
----------------------

This action allows you to stop a given script during execution. If the
script is not running, does nothing.
Please note this is only useful right now if your script contains a ``delay`` action.

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

.. _interval:

``interval``
------------

This component allows you to run actions periodically with a fixed interval.
For example if you want to toggle a switch every minute, you can use this component.
Please note that this certain cases are also possible with the :ref:`time.on_time <time-on_time>`
trigger, but this one is more light-weight and user-friendly.

.. code-block:: yaml

    # Example configuration entry
    interval:
      - interval: 1min
        then:
          - switch.toggle: relay_1

Configuration options:

- **interval** (**Required**, :ref:`config-time`): The interval to execute the action with.
- **then** (**Required**, :ref:`config-action`): The action to perform.

See Also
--------

- :doc:`configuration-types`
- :doc:`faq`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/guides/automations.rst>`__

.. disqus::
