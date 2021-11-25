Template Output
===============

.. seo::
    :description: Instructions for setting up template outputs with ESPHome.
    :image: description.png

The ``template`` output component can be used to create templated binary and float outputs in ESPHome.

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: template
        id: outputsplit
        type: float
        write_action:
          - output.set_level:
              id: output1
              level: !lambda return state;
          - output.set_level:
              id: output2
              level: !lambda return state;

      - platform: esp8266_pwm
        id: output1
        pin: GPIO12
        inverted: true
      - platform: esp8266_pwm
        id: output2
        pin: GPIO14
        inverted: true



Configuration variables:
------------------------

- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **type** (**Required**, string): The type of output. One of ``binary`` and ``float``.
- **write_action** (**Required**, :ref:`Action <config-action>`): An automation to perform
  when the state of the output is updated.
- All other options from :ref:`Output <config-output>`.

See :apiclass:`output::BinaryOutput` and :apiclass:`output::FloatOutput`.

.. warning::

    This is an **output component** and will not be visible from the frontend. Output components are intermediary
    components that can be attached to for example lights.

.. _output-template-on_write_action:

``write_action`` Trigger
------------------------

When the state for this output is updated, the ``write_action`` is triggered.
It is possible to access the state value inside Lambdas:

.. code-block:: yaml

    - platform: template
        id: my_output
        type: float
        write_action:
          - if:
              condition:
                lambda: return ((state > 0) && (state < .4));
              then:
                - output.turn_on: button_off
                - delay: 500ms
                - output.turn_off: button_off


Complete example from the cookbook: :doc:`Sonoff Dual Light Switch</cookbook/sonoff-dual-light-switch>`.

See Also
--------

- :doc:`/components/output/index`
- :ref:`automation`
- :ghedit:`Edit`
