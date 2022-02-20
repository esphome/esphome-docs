Sonoff NSPanel
==============

.. seo::
    :description: Instructions for using ESPHome of the Sonoff NSPanel

The Sonoff NSPanel integration allows ESPHome to control features and functionality of the NSPanel's
built in display.

.. code-block:: yaml

    nspanel:
      time_id: REPLACEME
      temperature: temperature_id
      screen_power_switch: screen_power_switch_id
      relays:
        - relay_1_id
        - relay_2_id

      widgets:
        - type: scene
          name: Test
          on_click:
            - logger.log: Test Scene tapped

        - type: empty
        ...


Configuration Variables:
------------------------

See Also
--------

- :ghsources:`esphome/components/nspanel`
- :ghedit:`Edit`
