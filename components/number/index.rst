Number Component
================

.. seo::
    :description: Instructions for setting up number components in ESPHome.
    :image: folder-open.svg

ESPHome has support for components to create a number entity. A number entity is
like a sensor that can read a value from a device, but is useful when that value
can be set by the user/frontend.

.. note::

    Home Assistant Core 2021.7 or higher is required for ESPHome number entities to work.

.. _config-number:

Base Number Configuration
-------------------------

All numbers in ESPHome have a name and an optional icon.

.. code-block:: yaml

    # Example number configuration
    name: Livingroom Volume

    # Optional variables:
    icon: "mdi:volume-high"

Configuration variables:

- **name** (**Required**, string): The name for the number.
- **icon** (*Optional*, icon): Manually set the icon to use for the number in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Requires Home Assistant 2021.11 or newer.
  Set to ``""`` to remove the default entity category.
- **unit_of_measurement** (*Optional*, string): Manually set the unit
  of measurement for the number. Requires Home Assistant Core 2021.12 or newer.
- **mode** (*Optional*, string): Defines how the number should be displayed in the frontend.
  See https://developers.home-assistant.io/docs/core/entity/number/#properties
  for a list of available options. Requires Home Assistant Core 2021.12 or newer.
  Defaults to ``"auto"``.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`number-on_value`.
- **on_value_range** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a published value transition from outside to a range to inside. See :ref:`number-on_value_range`.

MQTT Options:

- All other options from :ref:`MQTT Component <config-mqtt-component>`.

Number Automation
-----------------

You can access the most recent state of the number in :ref:`lambdas <config-lambda>` using
``id(number_id).state``.

.. _number-on_value:

``on_value``
************

This automation will be triggered when a new value is published. In :ref:`Lambdas <config-lambda>`
you can get the value from the trigger with ``x``.

.. code-block:: yaml

    number:
      - platform: template
        # ...
        on_value:
          then:
            - light.turn_on:
                id: light_1
                red: !lambda "return x/255;"

Configuration variables: See :ref:`Automation <automation>`.

.. _number-on_value_range:

``on_value_range``
******************

With this automation you can observe if a number value passes from outside
a defined range of values to inside a range.
This trigger will only trigger when the new value is inside the range and the previous value
was outside the range. On startup, the last state before reboot is restored and if the value crossed
the boundary during the boot process, the trigger is also executed.

Define the range with ``above`` and ``below``. If only one of them is defined, the interval is half-open.
So for example ``above: 5`` with no below would mean the range from 5 to positive infinity.

.. code-block:: yaml

    number:
      - platform: template
        # ...
        on_value_range:
          above: 5
          below: 10
          then:
            - switch.turn_on: relay_1

Configuration variables:

- **above** (*Optional*, float): The minimum for the trigger.
- **below** (*Optional*, float): The maximum for the trigger.
- See :ref:`Automation <automation>`.

.. _number-in_range_condition:

``number.in_range`` Condition
*****************************

This condition passes if the state of the given number is inside a range.

Define the range with ``above`` and ``below``. If only one of them is defined, the interval is half-open.
So for example ``above: 5`` with no below would mean the range from 5 to positive infinity.

.. code-block:: yaml

    # in a trigger:
    on_...:
      if:
        condition:
          number.in_range:
            id: my_number
            above: 50.0
        then:
          - script.execute: my_script

Configuration variables:

- **above** (*Optional*, float): The minimum for the condition.
- **below** (*Optional*, float): The maximum for the condition.

.. _number-set_action:

``number.set`` Action
*********************

This is an :ref:`Action <config-action>` for setting a number state.

.. code-block:: yaml

    - number.set:
        id: my_number
        value: 42

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the number to set.
- **value** (**Required**, float, :ref:`templatable <config-templatable>`):
  The value to set the number to.

.. _number-increment_action:

``number.increment`` Action
***************************

This is an :ref:`Action <config-action>` for incrementing a number state.

.. code-block:: yaml

    - number.increment:
        id: my_number
        value: -10

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the number to set.
- **value** (**Required**, float, :ref:`templatable <config-templatable>`):
  The value to add to the number.

.. _number-toggle_action:

``number.toggle`` Action
************************

This is an :ref:`Action <config-action>` for toggling a number state. It requires that both min_value and max_value of the number are defined. If the current value is closer to min_value, the number will be set to max_value. If the current value is closer to max_value, the number will be set to min_valie.

.. code-block:: yaml

    - number.toggle:
        id: my_number

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the number to set.

.. _number-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all numbers to do some
advanced stuff (see the full API Reference for more info).

- ``make_call()``: Set the number value.

  .. code-block:: cpp

      // Within lambda, push a value of 42
      auto call = id(my_number).make_call();
      call.set_value(42);
      // call.set_increment(-10); // would decrement by 10
      // call.set_toggle(true); // would toggle the number between min and max value
      call.perform();

- ``.state``: Retrieve the current value of the number. Is ``NAN`` if no value has been read or set.

  .. code-block:: cpp

      // For example, create a custom log message when a value is received:
      ESP_LOGI("main", "Value of my number: %f", id(my_number).state);

See Also
--------

- :apiref:`number/number.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
