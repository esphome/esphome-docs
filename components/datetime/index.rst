Datetime Component
==================

.. seo::
    :description: Instructions for setting up datetime components in ESPHome.
    :image: folder-open.svg

ESPHome has support for components to create a datetime entity. A datetime entity
currently represents a date that can be set by the user/frontend.

.. note::

    Requires Home Assistant 2024.4 or newer.

.. _config-datetime:

Base Datetime Configuration
---------------------------

All datetime in ESPHome have a name and an optional icon.

.. code-block:: yaml

    # Example datetime configuration
    name: Date to check

    # Optional variables:
    icon: "mdi:calendar-alert"

Configuration variables:

- **name** (**Required**, string): The name for the datetime.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the datetime to use that name, you can set ``name: None``.

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
                  ESP_LOGD("main", "Updated hour is later or equal to 12");
                } else {
                  ESP_LOGD("main", "Updated hour is earlier than 12");
                }

Configuration variables: See :ref:`Automation <automation>`.

.. _datetime-date_set_action:

``datetime.date.set`` Action
****************************

This is an :ref:`Action <config-action>` for setting a datetime date state.
The ``date`` provided can be in one of 3 formats:

.. code-block:: yaml

    # String date
    - datetime.date.set:
        id: my_date
        date: "2023-12-04"

    # Individual date parts
    - datetime.date.set:
        id: my_date
        date:
          year: 2023
          month: 12
          day: 4

    # Using a lambda
    - datetime.date.set:
        id: my_date
        date: !lambda |-
          // Return an ESPTime struct
          return {.day_of_month: 4, .month: 12, .year: 2023};

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the datetime to set.
- **date** (**Required**, string, date parts, :ref:`templatable <config-templatable>`):
  The value to set the datetime to.



.. _datetime-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all datetimes to do some
advanced stuff (see the full API Reference for more info).

- ``.make_call()``: Make a call for updating the datetime value.

  .. code-block:: cpp

      // Within lambda, set the date to 2024-02-25
      auto call = id(my_date).make_call();
      call.set_date("2024-02-25");
      call.perform();

  Check the API reference for information on the methods that are available for
  the ``DateCall`` object.

- ``.year``: Retrieve the current year of the ``date``. It will be ``0`` if no value has been set.
- ``.month``: Retrieve the current month of the ``date``. It will be ``0`` if no value has been set.
- ``.day``: Retrieve the current day of the ``date``. It will be ``0`` if no value has been set.
- ``.state_as_esptime()``: Retrieve the current value of the datetime as a :apistruct:`ESPTime` object.

  .. code-block:: cpp

      // For example, create a custom log message when a value is received:
      ESP_LOGI("main", "Value of my datetime: %04d-%02d-%02d", id(my_date).year, id(my_date).month, id(my_date).day);

See Also
--------

- :apiref:`DateTimeBase <datetime/datetime_base.h>`
- :apiref:`DateEntity <datetime/date_entity.h>`
- :apiref:`DateCall <datetime/date_entity.h>`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
