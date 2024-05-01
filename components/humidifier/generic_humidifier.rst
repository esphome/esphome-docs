Generic Humidifier
==================

.. seo::
    :description: Instructions for setting up Generic Humidifier component with ESPHome.
    :image: humidifier.svg

The ``generic-humidifier`` platform allows you to set up different types of humidifiers, form manufaturers or 
even humidifiers that was previously "dumb" devices.

The generic humidifier component allows user basic controls of humidifier devices, from output control, and
manufacturer defined profiles to a target humidity setting. 

.. note::

    The at the moment the automation of this component needs to be manually set using scripts.

Humidifier output profiles or modes that can be set by this component include:

- **Normal**: The general default output of a humidifier.
- **Eco**: A reduced output of a humidifier.
- **Boost**: A increased output of a humidifier.
- **Sleep**: A manufacturer designed run profile.
- **Baby**: A manufacturer designed run profile.
- **Auto**: A manufacturer designed run profile, also known as "Constant Humidity"

.. code-block:: yaml

    # Example configuration entry
    humidifier:
      - platform: generic_humidifier
        name: "Bedroom Generic Humidifier"
        sensor: my_humidity_sensor
        default_target_humidity: 55 %

        normal_action:
          - switch.turn_on: relay_2
        boost_action:
          - switch.turn_on: relay_3

Configuration variables:
------------------------

- **sensor** (**Required**, :ref:`config-id`): The sensor that is used to measure the current humidity.
- **default_target_humidity** (**Required**, float): The default target humidity for
  the control algorithm. This can be dynamically set in the frontend later.
- **normal_action** (**Required**, :ref:`Action <config-action>`): The action to call when
  the humidifier device wants to enter normal mode and increase the current humidity. 
- **eco_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the humidifier device wants to enter economy mode and decrease the current output level.
- **boost_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the humidifier device wants to enter boost mode and increase the current output level.
- **auto_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the humidifier device wants to activate the humidifier manufaturers automatic mode or a users script.
- **sleep_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the humidifier device wants to activate the humidifier manufaturers sleep mode or a users script.
- **baby_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the humidifier device wants to activate the humidifier manufaturers baby mode or a users script.  
- All other options from :ref:`Humidifier <config-humidifier>`.

See Also
--------

- :doc:`/components/humidifier/index`
- :apiref:`generic_humidifier/generic_humidifier.h`
- :ghedit:`Edit`
