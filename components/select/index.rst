Select Component
================

.. seo::
    :description: Instructions for setting up select components in ESPHome.
    :image: folder-open.svg

ESPHome has support for components to create a select entity. A select entity is
basically an option list that can be set by either yaml, hardware or the user/frontend.

.. note::

    Home Assistant Core 2021.8 or higher is required for ESPHome select entities to work.

.. _config-select:

Base Select Configuration
-------------------------

All selects in ESPHome have a name and an optional icon.

.. code-block:: yaml

    # Example select configuration
    name: Livingroom Mood
    id: my_select

    # Optional variables:
    icon: "mdi:emoticon-outline"

Configuration variables:

- **name** (**Required**, string): The name for the select.
- **icon** (*Optional*, icon): Manually set the icon to use for the select in the frontend.
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

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`select-on_value`.

MQTT Options:

- All other options from :ref:`MQTT Component <config-mqtt-component>`.

Select Automation
-----------------

You can access the most recent state of the select in :ref:`lambdas <config-lambda>` using
``id(select_id).state``.
For more information on using lambdas with select, see :ref:`select-lambda_calls`.

.. _select-on_value:

``on_value``
************

This automation will be triggered when a new value is published. In :ref:`Lambdas <config-lambda>`
you can get the value from the trigger with ``x``.

.. code-block:: yaml

    select:
      - platform: template
        # ...
        on_value:
          then:
            - logger.log:
                format: "Chosen option: %s"
                args: ["x.c_str()"]

Configuration variables: See :ref:`Automation <automation>`.

.. _select-set_action:

``select.set`` Action
*********************

This is an :ref:`Action <config-action>` for setting the active option using an option value.

.. code-block:: yaml

    - select.set:
        id: my_select
        option: "Happy"

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.
- **option** (**Required**, string, :ref:`templatable <config-templatable>`):
  The option to set the select to.

When a non-existing option value is used, a warning is logged and the state of
the select is left as-is.

.. _select-next_action:

``select.next`` Action
**********************

This is an :ref:`Action <config-action>` for selecting the next option in a select component.

.. code-block:: yaml

    - select.next:
        id: my_select
        cycle: false

    # Shorthand
    - select.next: my_select

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.
- **cycle** (**Optional**, boolean): Whether or not to jump back to the first option
  of the select when the last option is currently selected. Defaults to ``true``. 

.. _select-previous_action:

``select.previous`` Action
**************************

This is an :ref:`Action <config-action>` for selecting the previous option in
a select component.

.. code-block:: yaml

    - select.previous:
        id: my_select
        cycle: true

    # Shorthand
    - select.previous: my_select

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.
- **cycle** (**Optional**, boolean): Whether or not to jump to the last option
  of the select when the first option is currently selected. Defaults to ``true``. 

.. _select-first_action:

``select.first`` Action
***********************

This is an :ref:`Action <config-action>` for selecting the first option in
a select component.

.. code-block:: yaml

    - select.first:
        id: my_select

    # Shorthand
    - select.first: my_select

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.

.. _select-last_action:

``select.last`` Action
**********************

This is an :ref:`Action <config-action>` for selecting the last option in
a select component.

.. code-block:: yaml

    - select.last:
        id: my_select

    # Shorthand
    - select.last: my_select

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.

.. _select-to_action:

``select.to`` Action
********************

This is an :ref:`Action <config-action>` that can be used to change the active
option in a select component (first, last, previous or next), using a generic
templatable action call.

.. code-block:: yaml

    # Using values
    - select.to:
        id: my_select
        to: Next
        cycle: true

    # Or templated (lambdas)
    - select.to:
        id: my_select
        to: !lambda "return SELECT_OP_NEXT;"
        cycle: !lambda "return true;"

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.
- **to** (**Required**, string, :ref:`templatable <config-templatable>`): Where
  to move the option selection to. One of ``FIRST``, ``LAST``, ``PREVIOUS`` or
  ``NEXT`` (case insensitive). When writing a lambda for this field, then return
  one of the following enum values: ``SELECT_OP_FIRST``, ``SELECT_OP_LAST``,
  ``SELECT_OP_PREVIOUS`` or ``SELECT_OP_NEXT``.
- **cycle** (**Optional**, bool, :ref:`templatable <config-templatable>`):
  Can be used for options ``NEXT`` and ``PREVIOUS`` to specify whether or not to
  wrap around the options list when respectively the last or first option in
  the select is currently active.

.. _select-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all selects to do some
advanced stuff (see the full API Reference for more info).

- ``.make_call()``: Create a call for changing the select state.

  .. code-block:: cpp

      // Within lambda, select the "Happy" option.
      auto call = id(my_select).make_call();
      call.set_option("Happy");
      call.perform();

  Check the API reference for information on the methods that are available for
  the ``SelectCall`` object. You can for example also use ``call.select_first()``
  to select the first option or ``call.select_next(true)`` to select the next
  option with the cycle feature enabled.

- ``.state``: Retrieve the currently selected option of the select.

  .. code-block:: cpp

      // For example, create a custom log message when an option is selected:
      auto state = id(my_select).state.c_str();
      ESP_LOGI("main", "Option of my select: %s", state);

- ``.get_number_of_options()``: Retrieve the number of options in the select.

  .. code-block:: cpp

      auto nr = id(my_select).get_number_of_options();
      ESP_LOGI("main", "Select has %d options", nr);

- ``.get_index_of_option(<option name>)``: Find the index offset for an option value.

  .. code-block:: cpp

      auto i = id(my_select).get_index_of_option("Happy");
      if (i.has_value()) {
        ESP_LOGI("main", "'Happy' is at index: %d", i.value());
      } else {
        ESP_LOGE("main", "There is no option 'Happy'");
      }

- ``.get_option_at(<index offset>)``: Retrieve the option value at a given index offset.

  .. code-block:: cpp

      auto index = 1;
      auto option = id(my_select).get_option_at(index);
      if (option.has_value()) {
        auto value = option.value();
        ESP_LOGI("main", "Option at %d is: %s", index, value);
      }

See Also
--------

- :apiref:`Select <select/select.h>`
- :apiref:`SelectCall <select/select_call.h>`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
