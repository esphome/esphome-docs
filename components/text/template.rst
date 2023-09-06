Template Text
===================

.. seo::
    :description: Instructions for setting up template texts with ESPHome.
    :image: description.svg

The ``template`` text platform allows you to create a text with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    text:
      - platform: template
        name: Greeting
        icon: "mdi:text"
        initial_value: "Welcome Home"
        entity_category: config


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the text.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests to set the
  text value. The new value is available to lambdas in the ``x`` variable.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template text will immediately update the reported state.
- **restore_value** (*Optional*, boolean): Saves and loads the state to RTC/Flash.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **initial_value** (*Optional*, float): The value to set the state to on setup if not
  restored with ``restore_value``.
- **max_restore_data_length** (*Optional*, int): The maximum string length to restore_value with ``restore_value``. 
  Longer values will not be persisted. Defaults to ``64`` characters.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`text <config-text>`.

``text.set`` Action
-------------------------

You can also set the text for the template text from elsewhere in your YAML file
with the :ref:`text-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`template/text/template_text.h`
- :ghedit:`Edit`
