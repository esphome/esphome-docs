Template Text
=============

.. seo::
    :description: Instructions for setting up template texts with ESPHome.
    :image: description.svg

The ``template`` text platform allows you to create a text with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    text:
      - platform: template
        name: "Template text"
        optimistic: true
        min_length: 0
        max_length: 100
        mode: text

Configuration variables:
------------------------

- **min_lenngth** (**Required**, float): The minimum length this text can be.
- **max_length** (**Required**, float): The maximum length this text can be.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the current value of the text.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests to set the
  text value. The new value is available to lambdas in the ``x`` variable.
- **update_interval** (*Optional*, :ref:`config-time`): The interval on which to update the text
  by executing the ``lambda``. Defaults to ``60s``.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template text will immediately update the reported state.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **restore_value** (*Optional*, boolean): Saves and loads the state to RTC/Flash.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **initial_value** (*Optional*, float): The value to set the state to on setup if not
  restored with ``restore_value``.
  Cannot be used with ``lambda``.
- All other options from :ref:`Text <config-text>`.


See Also
--------

- :ref:`automation`
- :apiref:`template/text/template_text.h`
- :ghedit:`Edit`
