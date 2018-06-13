.. _automation:

Automations And Templates
=========================

Automations and templates are two very powerful concepts of esphomelib/yaml. Automations
allow you to perfom actions under certain conditions and templates are a way to easily
customize everything about your node without having to dive into the full esphomelib C++
API.

Let's begin with an example to explain these concepts. Suppose you have this configuration file:

.. code:: yaml

    switch:
      - platform: gpio
        pin: GPIO3
        name: "Living Room Dehumidifer"

    binary_sensor:
      - platform: gpio
        pin: GPIO4
        name: "Living Room Dehumidifer Toggle Button"

With this file you can already perform some basic tasks. You can control the ON/OFF state
of the dehumidifer in your livingroom from Home Assistant's front-end. But in many cases,
controlling everything strictly from the frontend is quite a pain. That's why you have
decided to also install a simple push button next to the dehumidifer on pin GPIO4.
A simple push on this button should toggle the state of the dehumidifer.

You *could* write an automation to do this task in Home Assistant's automation engine, but
ideally the IoT should work without an internet connection and should not break without
the MQTT server being online.

That's why, starting with esphomelib 1.7.0, there's a new automation engine. With it, you
can write some basic (and also some more advanced) automations using a syntax that is
hopefully a bit easier to read and understand than Home Assistant's.

For example, this configuration would achieve your desired behavior:

.. code:: yaml

    switch:
      - platform: gpio
        pin: GPIO3
        name: "Living Room Dehumidifier"
        id: dehumidifier1

    binary_sensor:
      - platform: gpio
        pin: GPIO4
        name: "Living Room Dehumidifer Toggle Button"
        on_press:
          then:
            - switch.toggle:
                id: dehumidifier1



Woah, hold on there. Please explain what's going on here! Sure :) Let's step through what's happening here.

.. code:: yaml

    switch:
       - platform: gpio
         # ...
         id: dehumidifier1

First, we have to give the dehumidifier an :ref:`config-id` so that we can
later use it inside our awesome automation.

.. code:: yaml

    binary_sensor:
      - platform: gpio
        # ...
        on_press:

We now attach a special attribute ``on_press`` to the toggle button. This part is called a "trigger". In this example,
the automation in the next few lines will execute whenever someone *begins* to press the button. Note the terminology
follows what you would call these events on mouse buttons. A *press* happens when you begin pressing the button/mouse.
There are also other triggers like ``on_release``, ``on_click`` or ``on_double_click`` available.


.. code:: yaml

    # ...
    on_press:
      then:
        - switch.toggle:
            id: dehumidifier1

.. _config-action:

Actions
^^^^^^^

Now comes the actual automation block. With ``then``, you tell esphomeyaml what should happen when the press happens.
Within this block, you can define several "actions". For example, ``switch.toggle`` and the line after that form an
action. Each action is separated by a dash and multiple actions can be executed in series by just adding another ``-``
like so:

.. code:: yaml

    # ...
    on_press:
      then:
        - switch.toggle:
            id: dehumidifier1
        - delay: 2s
        - switch.toggle:
            id: dehumidifier1

With this automation, a press on the push button would cause the dehumidifier to turn on/off for 2 seconds, and then
cycle back to its original state. Similarly you can have a single trigger with multiple automations:

.. code:: yaml

    # ...
    on_press:
      - then:
          - switch.toggle:
              id: dehumidifier1
      - then:
          - light.toggle:
              id: dehumidifier_indicator_light

    # Same as:
    on_press:
      then:
        - switch.toggle:
            id: dehumidifier1
        - light.toggle:
            id: dehumidifier_indicator_light


As a last example, let's make our dehumidifier smart: Let's make it turn on automatically when the humidity a sensor
reports is above 65% and make it turn off again when it reaches 50%

.. code:: yaml

    sensor:
      - platform: dht
        humidity:
          name: "Living Room Humidity"
          on_value_range:
            - above: 65.0
              then:
                - switch.turn_on:
                    id: dehumidifier1
            - below: 50.0
              then:
                - switch.turn_off:
                    id: dehumidifier1
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
^^^^^^^^^^^^^^^^^^^

With templates inside esphomelib, you can do almost *everything*. If for example you want to only perform a certain
automation if a certain complex formula evaluates to true, you can do that with templates. Let's look at an example
first:

.. code:: yaml

    binary_sensor:
      - platform: gpio
        name: "Cover End Stop"
        id: top_end_stop
    cover:
      - platform: template
        name: Living Room Cover
        lambda: !lambda >-
          if (id(top_end_stop).value) {
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

First, you might have already wondered what the ``lambda: !lambda >-`` part is supposed to mean. ``!lambda``
tells esphomeyaml that the following block is supposed to be interpreted as a lambda, or C++ code. Note that
here, the ``lambda:`` key would actually implicitly make the following block a lambda so in this context,
you could have just written ``lambda: >-``.

Next, there's the weird ``>-`` character combination. This effectively tells the YAML parser to treat the following
**indented** (!) block as plaintext. Without it, the YAML parser would attempt to read the following block as if
it were made up of YAML keys like ``cover:`` for example. (You may also have seen variations of this like ``|-``
or just ``|`` or ``>``. There's a slight difference in how these different styles deal with whitespace, but for our
purposes we can ignore that).

With ``if (...) { ... } else { ... }`` we create a *condition*. What this effectively says that if the thing inside
the first parentheses evaluates to ``true``` then execute the first block (in this case ``return cover::COVER_OPEN;``,
or else evaluate the second block. ``return ...;`` makes the code block give back a value to the template. In this case,
we're either *returning* ``cover::COVER_OPEN`` or ``cover::COVER_CLOSED`` to indicate that the cover is closed or open.

Finally, ``id(...)`` is a helper function that makes esphomeyaml fetch an object with the supplied ID (which you defined
somewhere else, like ``top_end_stop```) and let's you call any of esphomelib's many APIs directly. For example, here
we're retrieving the current state of the end stop using ``.value`` and using it to construct our cover state.

.. note::

    esphomeyaml (currently) does not check the validity of lambda expressions you enter and will blindly copy
    them into the generated C++ code. If compilation fails or something else is not working as expected
    with lambdas, it's always best to look at the generated C++ source file under ``<NODE_NAME>/src/main.cpp``.

.. _config-templatable:

Bonus: Templating Actions
^^^^^^^^^^^^^^^^^^^^^^^^^

Another feature of esphomeyaml is that you can template almost every parameter for actions in automations. For example
if you have a light and want to set it to a pre-defined color when a button is pressed, you can do this:

.. code:: yaml

    on_press:
      then:
        - light.turn_on:
            id: some_light_id
            transition_length: 0.5s
            red: 0.8
            green: 1.0
            blue: !lambda >-
              # The sensor outputs values from 0 to 100. The blue
              # part of the light color will be determined by the sensor value.
              return id(some_sensor).value / 100.0;

Every parameter in actions that has the label "templatable" in the docs can be templated like above, using
all of the usual lambda syntax.

All Triggers
~~~~~~~~~~~~

- :ref:`mqtt.on_message <mqtt-on_message>`
- :ref:`sensor.on_value <sensor-on_value>`
- :ref:`sensor.on_value_range <sensor-on_value_range>`
- :ref:`sensor.on_raw_value <sensor-on_raw_value>`
- :ref:`binary_sensor.on_press <binary_sensor-on_press>`
- :ref:`binary_sensor.on_release <binary_sensor-on_release>`
- :ref:`binary_sensor.on_click <binary_sensor-on_click>`
- :ref:`binary_sensor.on_double_click <binary_sensor-on_double_click>`
- :ref:`esphomeyaml.on_boot <esphomeyaml-on_boot>`
- :ref:`esphomeyaml.on_shutdown <esphomeyaml-on_shutdown>`

All Actions
~~~~~~~~~~~

- :ref:`delay <delay_action>`
- :ref:`lambda <lambda_action>`
- :ref:`mqtt.publish <mqtt-publish_action>`
- :ref:`switch.toggle <switch-toggle_action>`
- :ref:`switch.turn_off <switch-turn_off_action>`
- :ref:`switch.turn_on <switch-turn_on_action>`
- :ref:`light.toggle <light-toggle_action>`
- :ref:`light.turn_off <light-turn_off_action>`
- :ref:`light.turn_on <light-turn_on_action>`
- :ref:`cover.open <cover-open_action>`
- :ref:`cover.close <cover-close_action>`
- :ref:`cover.stop <cover-stop_action>`
- :ref:`fan.toggle <fan-toggle_action>`
- :ref:`fan.turn_off <fan-turn_off_action>`
- :ref:`fan.turn_on <fan-turn_on_action>`

.. _delay_action:

Delay Action
~~~~~~~~~~~~

This action delays the execution of the next action in the action list by a specified
time period.

.. code:: yaml

   on_...:
     then:
        - switch.turn_on:
            id: relay_1
        - delay: 2s
        - switch.turn_off:
            id: relay_1
        # Templated, waits for 1s (1000ms) only if a reed switch is active
        - delay: !lambda "if (id(reed_switch).value) return 1000; else return 0;"

.. note::

    This is a "smart" asynchronous delay - other code will still run in the background while
    the delay is happening.

.. _lambda_action:

Lambda Action
~~~~~~~~~~~~~

This action executes an arbitrary piece of C++ code (see :ref:`Lambda <config-lambda>`).

.. code:: yaml

    on_...:
      then:
        - lambda: >-
            id(some_binary_sensor).publish_state(false);


Automation Conditions
~~~~~~~~~~~~~~~~~~~~~

Additionally, you can have a condition ``if:`` block in the automation. This will cause esphomelib
to only execute the ``then`` block if the ``if:`` block succeeds:

.. code:: yaml

    on_...:
      if:
        lambda: 'return id(some_binary_sensor).value;'
      then:
        # do something

See Also
~~~~~~~~

- :doc:`configuration-types`
- :doc:`faq`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/guides/automations.rst>`__
