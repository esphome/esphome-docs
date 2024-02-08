Template Datetime
=================

.. seo::
    :description: Instructions for setting up template datetime with ESPHome.
    :image: description.svg

The ``template`` datetime platform allows you to create a datetime with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    datetime:
      - platform: template
        id: my_datetime
        name: Pick a Datetime
        optimistic: yes
        initial_value: "2024-01-30"
        restore_value: true

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the datetime.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the current value of the datetime.
- **set_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests to set the
  dateime value. The new value is available to lambdas in the ``x`` variable.
- **update_interval** (*Optional*, :ref:`config-time`): The interval on which to update the datetime
  by executing the ``lambda``. Defaults to ``60s``.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template datetime will immediately update the reported state.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **restore_value** (*Optional*, boolean): Saves and loads the state to RTC/Flash.
  Cannot be used with ``lambda``. Defaults to ``false``.
- **initial_value** (*Optional*, string): The value to set the state to on setup if not
  restored with ``restore_value``.
  The string needs to follow one of these formats 
  ``'%Y-%m-%d %H:%M:%S' - '%Y-%m-%d %H:%M' - '%H:%M:%S' - '%H:%M'``
  An example to set a date and time would be: ``"2023-12-04 15:35"``. 
  Only a Date: ``"2023-12-04"``. 
  Only a time, inlcuing seconds: ``"15:35:10"``.
  Cannot be used with ``lambda``. Defaults to ``"00:00:00"``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Datetime <config-datetime>`.

``datetime.set`` Action
-----------------------

You can also set the datetime for the template datetime from elsewhere in your YAML file
with the :ref:`datetime-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`template/datetime/template_datetime.h`
- :ghedit:`Edit`
