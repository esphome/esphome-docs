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
        id: my_date
        type: date
        name: Pick a Date
        optimistic: yes
        initial_value: "2024-01-30"
        restore_value: true

Configuration variables:
------------------------

- **type** (*Required*, enum): The type of the datetime. Can only be ``date``.
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
  restored with ``restore_value``. Can be one of:

  - A string in the format ``%Y-%m-%d``, eg: ``"2023-12-04"``.
  - An object including ``year``, ``month``, ``day``.

  .. code-block:: yaml

      initial_value:
        year: 2023
        month: 12
        day: 4

- All other options from :ref:`Datetime <config-datetime>`.

See Also
--------

- :ref:`automation`
- :apiref:`template/datetime/template_date.h`
- :ghedit:`Edit`
