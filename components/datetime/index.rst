Datetime Component
==================

.. seo::
    :description: Instructions for setting up datetime components in ESPHome.
    :image: folder-open.svg

ESPHome has support for components to create a datetime entity. A datetime entity 
represents a date and time, only date or only a time which can be set by the user/frontend.

.. note::

    Not implemented in Home Assistant Core yet

.. _config-datetime:

Base Datetime Configuration
---------------------------

All datetime in ESPHome have a name and an optional icon.

.. code-block:: yaml

    # Example datetime configuration
    name: Time to switch light on

    # Optional variables:
    icon: "mdi:lightbulb-on"

Configuration variables:

- **name** (**Required**, string): The name for the datetime.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the datetime to use that name, you can set ``name: None``.

- **time_id** (*Optional*, :ref:`Time Component <config-time-component>`)
- **on_time** (*Optional*, :ref:`Automation <automation>`)

  .. note::

      If you add an ``on_time`` automation you need to specify a valid ``time id``.

- **icon** (*Optional*, icon): Manually set the icon to use for the datetime in the frontend.
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
- **mode** (*Optional*, string): Defines how the datetime should be displayed in the frontend.
  Only ``"auto"`` supported at the moment
  Defaults to ``"auto"``.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`datetime-on_value`.
- **on_time** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the date/time value matches the date/time from the specified ``time_id`` component.
  See :ref:`datetime-on_time`

MQTT Options:

- All other options from :ref:`MQTT Component <config-mqtt-component>`.

Datetime Automation
-------------------

You can access the most recent state as a string of the datetime in :ref:`lambdas <config-lambda>` using
``id(datetime_id).state``. 
You can also access it as a ``ESPTime`` object by ``id(datetime_id).state_as_time``

.. _datetime-on_value:

``on_value``
************

This automation will be triggered when a new value is published. In :ref:`Lambdas <config-lambda>`
you can get the value as a ESPTime object from the trigger with ``x``.

.. code-block:: yaml

    datetime:
      - platform: template
        # ...
        on_value:
          then:
            - lambda: |-
                if(x.hour >= 12) {
                  ESP_LOGD("main", "Picked time is greater than 12");
                } else {
                  ESP_LOGD("main", "Picked time is smaler than 12");
                }

Configuration variables: See :ref:`Automation <automation>`.

.. _datetime-on_time:

``on_time``
***********

This automation is triggered when the stored date/time matches the current date/time of the 
specified ``time_id`` component.
If only a date is provided, the automation will trigger once on the specified date
at 00:00:01.
The same applies if the provided time does not include seconds. So it will trigger once
on the first second of the specified minute.

.. code-block:: yaml

    datetime:
      - platform: template
        # ...
        on_time:
          - switch.turn_on:
              id: my_switch

Configuration variables: See :ref:`Automation <automation>`.

.. _datetime-has_date_condition:

``datetime.has_date`` Condition
*******************************

This condition passes if the state of the given dateime has a date set.

.. code-block:: yaml

    # in a trigger:
    on_...:
      if:
        condition:
          ndatetime.has_date:
            id: my_datetime
        then:
          - script.execute: my_script

.. _datetime-has_time_condition:

``datetime.has_date`` Condition
*******************************

This condition passes if the state of the given dateime has a time set.

.. code-block:: yaml

    # in a trigger:
    on_...:
      if:
        condition:
          datetime.has_time:
            id: my_datetime
        then:
          - script.execute: my_script

.. _datetime-set_action:

``datetime.set`` Action
***********************

This is an :ref:`Action <config-action>` for setting a datetime state.

.. code-block:: yaml

    - datetime.set:
        id: my_datetime
        value: "2023-12-04 15:35"

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the number to set.
- **value** (**Required**, string, :ref:`templatable <config-templatable>`):
  The value to set the datetime to.



.. _datetime-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all datetimes to do some
advanced stuff (see the full API Reference for more info).

- ``.make_call()``: Make a call for updating the datetime value.

  .. code-block:: cpp

      // Within lambda, set the datetime to 2024-02-25 10:20
      auto call = id(my_number).make_call();
      call.set_value("2024-02-25 10:20");
      call.perform();

  Check the API reference for information on the methods that are available for
  the ``DatetimeCall`` object.

- ``.state``: Retrieve the current value of the datetime. Is ``""`` if no value has been read or set.
- ``.state_as_time``: Retrieve the current value of the datetime as a ``ESPTime`` objekt. 
  Is ``.is_valid()`` will return ``false`` if no value has been read or set.

  .. code-block:: cpp

      // For example, create a custom log message when a value is received:
      ESP_LOGI("main", "Value of my datetime: %s", id(my_datetime).state);

See Also
--------

- :apiref:`Datetime <datetime/datetime.h>`
- :apiref:`DatetimeCall <datetime/datetime_call.h>`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
