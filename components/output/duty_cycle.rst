Duty Cycle Output
===========================

.. seo::
    :description: Instructions for setting up duty cycle outputs for GPIO pins.
    :image: percent.svg

Similar to PWM, The Duty Cycle Output platform allows you to control GPIO pins by 
pulsing them on/off over a given time period. It could be used to control a 
heating element through a relay where a fast PWM update cycle would not be appropriate.

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: duty_cycle
        pin: D1
        id: my_duty_cycle
        period: 15s


Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to pulse.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **period** (**Required**, frequency): The duration of each cycle. (i.e. a 10s 
  period at 50% duty would result in the pin being turned on for 5s, then off for 5s)
- All other options from :ref:`Output <config-output>`.
