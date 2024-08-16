Template Number
===============

.. seo::
    :description: Instructions for setting up template numbers with ESPHome.
    :image: description.svg

The ``template`` number platform allows you to create a number with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    number:
      - platform: template
        name: "Template number"
        optimistic: true
        min_value: 0
        max_value: 100
        step: 1

Configuration variables:
------------------------

- **min_value** (**Required**, float): The minimum value this number can be.
- **max_value** (**Required**, float): The maximum value this number can be.
- **step** (**Required**, float): The granularity with which the number can be set.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the current value of the number.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests to set the
  number value. The new value is available to lambdas in the ``x`` variable.
- **update_interval** (*Optional*, :ref:`config-time`): The interval on which to update the number
  by executing the ``lambda``. Defaults to ``60s``.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template number will immediately update the reported state.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **restore_value** (*Optional*, boolean): Saves and loads the state to RTC/Flash.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **initial_value** (*Optional*, float): The value to set the state to on setup if not
  restored with ``restore_value``.
  Cannot be used with ``lambda``. Defaults to ``min_value``.
- All other options from :ref:`Number <config-number>`.

``number.set`` Action
---------------------

You can also set the number for the template number from elsewhere in your YAML file
with the :ref:`number-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`template/number/template_number.h`
- :ghedit:`Edit`
