Template Select
===============

.. seo::
    :description: Instructions for setting up Template Select(s) with ESPHome.
    :image: description.png

The ``Template`` Select platform allows you to create a Select with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    select:
      - platform: template
        name: "Template select"
        update_interval: never
        options:
          - one
          - two
          - three
        initial_option: two


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the Select.
- **options** (**Required**, list): The list of options this Select has.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new option of the Select.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests to set the Select option.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  Select ``lambda``. Defaults to ``60s``.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the Template Select will immediately update the reported state.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **restore_value** (*Optional*, boolean): Saves and loads the state to RTC/Flash.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **initial_option** (*Optional*, string): The option to set the option to on setup if not
  restored with ``restore_value``.
  Cannot be used with ``lambda``. Defaults to the first option in the ``options`` list.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Select <config-select>`.

``select.set`` Action
----------------------------------

You can also set an option to a Template Select from elsewhere in your YAML file
with the :ref:`select-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`template/select/template_select.h`
- :ghedit:`Edit`
