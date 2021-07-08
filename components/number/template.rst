Template Number
===============

.. seo::
    :description: Instructions for setting up template numbers with ESPHome.
    :image: description.png

The ``template`` number platform allows you to create a number with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    number:
      - platform: template
        name: "Template number"
        update_interval: never
        min_value: 0
        max_value: 100
        step: 1

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the number.
- **min_value** (**Required**, float): The minimum value this number can be.
- **max_value** (**Required**, float): The maximum value this number can be.
- **step** (**Required**, float): The granularity with which the number can be set.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the number.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests to set the number value.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  number. Defaults to ``60s``.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template number will immediately update the reported state.
  Defaults to ``false``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-number>`.

``number.set`` Action
----------------------------------

You can also publish a state to a template number from elsewhere in your YAML file
with the :ref:`number-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`template/number/template_number.h`
- :ghedit:`Edit`
