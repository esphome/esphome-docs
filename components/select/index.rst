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

- **id** (*Optional*, string): Manually specify the ID for code generation. At least one of **id** and **name** must be specified.
- **name** (*Optional*, string): The name for the select. At least one of **id** and **name** must be specified.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the select to use that name, you can set ``name: None``.

- **icon** (*Optional*, icon): Manually set the icon to use for the select in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options.
  Set to ``""`` to remove the default entity category.
- If Webserver enabled, ``web_server_sorting_weight`` can be set. See :ref:`Webserver Entity Sorting <config-webserver-sorting>`.

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

This automation will be triggered whenever a value is set/published, even if the value is the same as before. In :ref:`Lambdas <config-lambda>`
you can get the value from the trigger with ``x`` and the index offset of the selected value with ``i``.

.. code-block:: yaml

    select:
      - platform: template
        # ...
        on_value:
          then:
            - logger.log:
                format: "Chosen option: %s (index %d)"
                args: ["x.c_str()", "i"]

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

.. _select-set_index_action:

``select.set_index`` Action
***************************

This is an :ref:`Action <config-action>` for setting the active option using its index offset.

.. code-block:: yaml

    - select.set_index:
        id: my_select
        index: 3

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.
- **index** (**Required**, int, :ref:`templatable <config-templatable>`):
  The index offset of the option to be activated.

When a non-existing index value is used, a warning is logged and the state of
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
- **cycle** (*Optional*, boolean): Whether or not to jump back to the first option
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
- **cycle** (*Optional*, boolean): Whether or not to jump to the last option
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

.. _select-operation_action:

``select.operation`` Action
***************************

This is an :ref:`Action <config-action>` that can be used to change the active
option in a select component (first, last, previous or next), using a generic
templatable action call.

.. code-block:: yaml

    # Using values
    - select.operation:
        id: my_select
        operation: Next
        cycle: true

    # Or templated (lambdas)
    - select.operation:
        id: my_select
        operation: !lambda "return SELECT_OP_NEXT;"
        cycle: !lambda "return true;"

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.
- **operation** (**Required**, string, :ref:`templatable <config-templatable>`): The
  operation to perform. One of ``FIRST``, ``LAST``, ``PREVIOUS`` or
  ``NEXT`` (case insensitive). When writing a lambda for this field, then return
  one of the following enum values: ``SELECT_OP_FIRST``, ``SELECT_OP_LAST``,
  ``SELECT_OP_PREVIOUS`` or ``SELECT_OP_NEXT``.
- **cycle** (*Optional*, bool, :ref:`templatable <config-templatable>`):
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

  .. code-block:: yaml

      # Check if a specific option is selected
      - if:
          condition:
            - lambda: 'return id(my_select).state == "my_option_value";'


- ``.size()``: Retrieve the number of options in the select.

  .. code-block:: cpp

      auto size = id(my_select).size();
      ESP_LOGI("main", "Select has %d options", size);

- ``.index_of(<option value>)``: Retrieve the index offset for an option value.

  .. code-block:: cpp

      auto index = id(my_select).index_of("Happy");
      if (index.has_value()) {
        ESP_LOGI("main", "'Happy' is at index: %d", index.value());
      } else {
        ESP_LOGE("main", "There is no option 'Happy'");
      }

- ``.active_index()``: Retrieve the index of the currently active option.

  .. code-block:: cpp

      auto index = id(my_select).active_index();
      if (index.has_value()) {
        ESP_LOGI("main", "Option at index %d is active", index.value());
      } else {
        ESP_LOGI("main", "No option is active");
      }

- ``.at(<index offset>)``: Retrieve the option value at a given index offset.

  .. code-block:: cpp

      auto index = 1;
      auto option = id(my_select).at(index);
      if (option.has_value()) {
        auto value = option.value();
        ESP_LOGI("main", "Option at %d is: %s", index, value);
      } else {
        ESP_LOGE("main", "Index %d does not exist", index);
      }

- ``.has_option(<option value>)``: Check if the select contains the given option value.

  .. code-block:: cpp

      auto option = "Happy";
      if (id(my_select).has_option(option)) {
        ESP_LOGI("main", "Select has option '%s'", option);
      }

- ``.has_index(<index offset>)``: Check if the select contains an option value for the given index offset.

  .. code-block:: cpp

      auto index = 3;
      if (id(my_select).has_index(index)) {
        ESP_LOGI("main", "Select has index offset %d", index);
      }


Example
-------

Setting up three options and set component state to selected option value.

.. code-block:: yaml

    select:
      - platform: template
        name: Mode
        id: mode
        options:
         - "Option1"
         - "Option2"
         - "Option3"
        initial_option: "Option1"
        optimistic: true
        set_action:
          - logger.log:
              format: "Chosen option: %s"
              args: ["x.c_str()"]


See Also
--------

- :apiref:`Select <select/select.h>`
- :apiref:`SelectCall <select/select_call.h>`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
