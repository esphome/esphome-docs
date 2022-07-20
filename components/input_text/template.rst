Template Input Text
===================

.. seo::
    :description: Instructions for setting up template input texts with ESPHome.
    :image: description.svg

The ``template`` input text platform allows you to create a input text with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    input_text:
      - platform: template
        name: Greeting
        icon: "mdi:text"
        initial_value: "Welcome Home"
        entity_category: config


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the input text.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests to set the
  input text value. The new value is available to lambdas in the ``x`` variable.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template input text will immediately update the reported state.
- **restore_value** (*Optional*, boolean): Saves and loads the state to RTC/Flash.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **initial_value** (*Optional*, float): The value to set the state to on setup if not
  restored with ``restore_value``.
  Cannot be used with ``lambda``. Defaults to ``min_value``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Input Text <config-input_text>`.

``input_text.set`` Action
-------------------------

You can also set the input text for the template input text from elsewhere in your YAML file
with the :ref:`input_text-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`template/input_text/template_input_text.h`
- :ghedit:`Edit`
