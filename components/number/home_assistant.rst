Home Assistant Number
=====================

.. seo::
        :description: Instructions for setting up Home Assistant numbers with ESPHome.
        :image: description.svg

The ``homeassistant`` number platform allows you to create a number that is synchronized
with Home Assistant. Min, Max and Step are not configurable for this platform because they are taken from the Home Assistant entity.

.. code-block:: yaml

        # Example configuration entry
        number:
            - platform: homeassistant
                name: "Home Assistant number"
                entity_id: light.my_light

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the number.
- **entity_id** (**Required**, string): The Home Assistant entity ID of the number to synchronize with.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
    Lambda to be evaluated every update interval to get the current value of the number.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
    be performed when the remote (like Home Assistant's frontend) requests to set the
    number value. The new value is available to lambdas in the ``x`` variable.
- **update_interval** (*Optional*, :ref:`config-time`): The interval on which to update the number
    by executing the ``lambda``. Defaults to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Number <config-number>`.

``number.set`` Action
---------------------

You can also set the number for the Home Assistant number from elsewhere in your YAML file
with the :ref:`number-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`homeassistant/number/homeassistant_number.h`
- :ghedit:`Edit`
