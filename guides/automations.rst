.. _automation:

Automations and Templates
=========================

.. seo::
    :description: Getting started guide for automations in ESPHome.
    :image: auto-fix.svg

Automations and templates are two very powerful aspects of ESPHome. Automations
allow you to perform actions under certain conditions and templates are a way to easily
customize everything about your node without having to dive into the full ESPHome C++
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

That's why, starting with ESPHome 1.7.0, there's a new automation engine. With it, you
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

First, we have to give the dehumidifier a :ref:`config-id` so that we can
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

.. _config-actions:

Actions
-------

Now comes the actual automation block. With ``then``, you tell ESPHome what should happen when the press happens.
Within this block, you can define several "actions" that will be executed sequentially.
For example, ``switch.toggle`` and the line after that form an
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


As a last example, let's make our dehumidifier smart: Let's make it turn on automatically when the humidity reported by a sensor
is above 65%, and make it turn off again when it falls below 50%:

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

That's a lot of indentation 😉 ``on_value_range`` is a special trigger for sensors that trigger when the value output
of the sensor is within a certain range. In the first example, this range is defined as "any value above or including
65.0", and the second one refers to once the humidity reaches 50% or below.

Now that concludes the introduction to automations in ESPHome. They're a powerful tool to automate almost
everything on your device with an easy-to-use syntax. For the cases where the "pure" YAML automations don't work,
ESPHome has another extremely powerful tool to offer: Templates.


.. _delay_action:

*delay*
*******

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
    the delay is happening. When using a lambda call, you should return the delay value in milliseconds.

.. _config-component-actions:

Component Actions
-----------------

.. _component-update_action:

*component.update*
******************

Using this action you can manually call the ``update()`` method of a component.

Please note that this only works with some component types and others will result in a
compile error.

.. code-block:: yaml

    on_...:
      then:
        - component.update: my_component

        # The same as:
        - lambda: 'id(my_component).update();'

.. _component-suspend_action:

*component.suspend*
*******************

Using this action you can manually call the ``stop_poller()`` method of a component.

After this action the component will stop being refreshed.

While the poller is suspendend, it's still possible to trigger on-demand updates by
using :ref:`component.update <component-update_action>`

Please note that this only works with PollingComponent types and others will result in a
compile error.

.. code-block:: yaml

    on_...:
      then:
        - component.suspend: my_component

        # The same as:
        - lambda: 'id(my_component).stop_poller();'

.. _component-resume_action:

*component.resume*
******************

Using this action you can manually call the ``start_poller()`` method of a component.

After this action the component will refresh at the original update_interval rate

This will allow the component to resume automatic update at the defined interval.

This action also allows to change the update interval, calling it without suspend,
replace the poller directly.

Please note that this only works with PollingComponent types and others will result in a
compile error.

.. code-block:: yaml

    on_...:
      then:
        - component.resume: my_component

        # The same as:
        - lambda: 'id(my_component).start_poller();'

    # Change the poller interval
    on_...:
      then:
        - component.resume:
            id: my_component
            update_interval: 15s

.. _config-conditional-actions:

Conditional Actions
-------------------

.. _if_action:

*if*
****

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


Configuration variables:

- **condition** (**Required**, :ref:`config-condition`): The condition to check which branch to take. See :ref:`Conditions <config-condition>`.
- **then** (*Optional*, :ref:`Action <config-action>`): The action to perform if the condition evaluates to true.
  Defaults to doing nothing.
- **else** (*Optional*, :ref:`Action <config-action>`): The action to perform if the condition evaluates to false.
  Defaults to doing nothing.

.. _while_action:

*while*
*******

This action is similar to the :ref:`if <if_action>` Action. The ``while`` action loops
through a block as long as the given condition is true.

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


Configuration variables:

- **condition** (**Required**): The condition to check whether to execute. See :ref:`Conditions <config-condition>`.
- **then** (**Required**, :ref:`Action <config-action>`): The action to perform until the condition evaluates to false.

.. _repeat_action:

*repeat*
********

This action allows you to repeat a block a given number of times.
For example, the automation below will flash the light five times.

.. code-block:: yaml

    on_...:
      - repeat:
          count: 5
          then:
            - light.turn_on: some_light
            - delay: 1s
            - light.turn_off: some_light
            - delay: 10s


Configuration variables:

- **count** (**Required**, int): The number of times the action should be repeated.
- **then** (**Required**, :ref:`Action <config-action>`): The action to repeat.

.. _wait_until_action:

*wait_until*
************

This action allows your automations to wait until a condition evaluates to true. (So this is just
a shorthand way of writing a ``while`` action with an empty ``then`` block.)

.. code-block:: yaml

    # In a trigger:
    on_...:
      - logger.log: "Waiting for binary sensor"
      - wait_until:
          binary_sensor.is_on: some_binary_sensor
      - logger.log: "Binary sensor is ready"


If you want to use a timeout, the term "condition" is required:

.. code-block:: yaml

    # In a trigger:
    on_...:
      - logger.log: "Waiting for binary sensor"
      - wait_until:
          condition:
            binary_sensor.is_on: some_binary_sensor
          timeout: 8s
      - logger.log: "Binary sensor might be ready"


Configuration variables:

- **condition** (**Required**): The condition to wait to become true. See :ref:`Conditions <config-condition>`.
- **timeout** (*Optional*, :ref:`config-time`): Time to wait before timing out. Defaults to never timing out.

.. _config-conditions:

Conditions
----------

Most components have there own conditions set.

.. _and_condition:
.. _or_condition:
.. _xor_condition:
.. _not_condition:

*and* / *or* / *xor* / *not*
****************************

Check a combination of conditions

.. code-block:: yaml

    on_...:
      then:
        - if:
            condition:
              # Same syntax for `and` as well as `xor` conditions
              or:
                - binary_sensor.is_on: some_binary_sensor
                - binary_sensor.is_on: other_binary_sensor
            # ...

        - if:
            condition:
              not:
                binary_sensor.is_off: some_binary_sensor

.. _for_condition:

*for*
*****

This :ref:`Condition <config-condition>` allows you to check if a given condition has been
true for at least a given amount of time.

.. code-block:: yaml

    on_...:
      if:
        condition:
          for:
            time: 5min
            condition:
              api.connected:
        then:
          - logger.log: API has stayed connected for at least 5 minutes!

Configuration variables:

- **time** (**Required**, :ref:`templatable <config-templatable>`, :ref:`config-time`):
  The time for which the condition has to have been true.
- **condition** (**Required**, :ref:`Condition <config-condition>`):
  The condition to check.


.. _config-lambda:

Lambdas
-------

With templates inside ESPHome, you can do almost *everything*. If for example you want to only perform a certain
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
            return COVER_OPEN;
          } else {
            return COVER_CLOSED;
          }

What's happening here? First, we define a binary sensor (with the id ``top_end_stop``) and then a
:doc:`template cover </components/cover/template>`. (If you're new to Home Assistant, a 'cover' is
something like a window blind, a roller shutter, or a garage door.) The *state* of the template cover is
controlled by a template, or "lambda". In lambdas you're effectively writing C++ code and therefore the
name lambda is used instead of Home Assistant's "template" lingo to avoid confusion. But before you go
shy away from using lambdas because you just hear C++ and think oh noes, I'm not going down *that* road:
Writing lambdas is not that hard! Here's a bit of a primer:

First, you might have already wondered what the ``lambda: !lambda |-`` part is supposed to mean. ``!lambda``
tells ESPHome that the following block is supposed to be interpreted as a lambda, or C++ code. Note that
here, the ``lambda:`` key would actually implicitly make the following block a lambda so in this context,
you could have just written ``lambda: |-``.

Next, there's the weird ``|-`` character combination. This effectively tells the YAML parser to treat the following
**indented** (!) block as plaintext. Without it, the YAML parser would attempt to read the following block as if
it were made up of YAML keys like ``cover:`` for example. (You may also have seen variations of this like ``>-``
or just ``|`` or ``>``. There's a slight difference in how these different styles deal with whitespace, but for our
purposes we can ignore that).

With ``if (...) { ... } else { ... }`` we create a *condition*. What this effectively says that if the thing inside
the first parentheses evaluates to ``true`` then execute the first block (in this case ``return COVER_OPEN;``,
or else evaluate the second block. ``return ...;`` makes the code block give back a value to the template. In this case,
we're either *returning* ``COVER_OPEN`` or ``COVER_CLOSED`` to indicate that the cover is closed or open.

Finally, ``id(...)`` is a helper function that makes ESPHome fetch an object with the supplied ID (which you defined
somewhere else, like ``top_end_stop``) and lets you call any of ESPHome's many APIs directly. For example, here
we're retrieving the current state of the end stop using ``.state`` and using it to construct our cover state.

.. note::

    ESPHome does not check the validity of lambda expressions you enter and will blindly copy
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

Parameter *Lambda*
******************

Another feature of ESPHome is that you can template almost every parameter for actions in automations. For example
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

.. _config-lambda-action:

Action *lambda*
***************

This action executes an arbitrary piece of C++ code (see :ref:`Lambda <config-lambda>`).

.. code-block:: yaml

    on_...:
      then:
        - lambda: |-
            id(some_binary_sensor).publish_state(false);

.. _config-lambda-condition:

Condition *lambda*
******************

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

See Also
--------

- :doc:`configuration-types`
- :doc:`faq`
- :ghedit:`Edit`
