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

.. _select-on_value:

``on_value``
************

This automation will be triggered when a new option is published. In :ref:`Lambdas <config-lambda>`
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

This is an :ref:`Action <config-action>` for setting a select state.

.. code-block:: yaml

    - select.set:
        id: my_select
        option: "Happy"

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the select to set.
- **option** (**Required**, string, :ref:`templatable <config-templatable>`):
  The option to set the select to.

.. _select-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all selects to do some
advanced stuff (see the full API Reference for more info).

- ``make_call()``: Set the select option.

  .. code-block:: cpp

      // Within lambda, select the "Happy" option.
      auto call = id(my_select).make_call();
      call.set_option("Happy");
      call.perform();

- ``.state``: Retrieve the current option of the select.

  .. code-block:: cpp

      // For example, create a custom log message when an option is selected:
      ESP_LOGI("main", "Option of my select: %s", id(my_select).state.c_str());

See Also
--------

- :apiref:`select/select.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
