Shelly Dimmer
============

.. seo::
    :description: Instructions for setting up a Shelly Dimmer 2.
    :image: shellydimmer2.jpg
    
The ``shelly_dimmer`` component adds support for the dimming and power-metering functionality that can be found the [Shelly Dimmer 2](https://shelly.cloud/knowledge-base/devices/shelly-dimmer-2/). The interaction with mains is done via an STM32 microcontroller that is flashed with an [open source firmware](https://github.com/jamesturton/shelly-dimmer-stm32).
A detailed analysis of the Shelly Dimmer 2 hardware is given [here](https://github.com/arendst/Tasmota/issues/6914).

.. figure:: images/shellydimmer2.jpg
    :align: center
    :width: 40.0%


An example of a configuration of this component:
.. code-block:: yaml

    # the serial port is occupied with the communication to the microcontroller --> disable logging
    logger:
      baud_rate: 0

    light:
      - platform: shelly_dimmer
        name: Shelly Dimmer 2 Light
        id: thislight
        power:
          name: Shelly Dimmer 2 Light Power
        voltage:
          name: Shelly Dimmer 2 Light Voltage
        current:
          name: Shelly Dimmer 2 Light Current
        max_brightness: 500


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the light.
- **leading_edge** (**Optional**, boolean): (Dimming mode)[https://en.wikipedia.org/wiki/Dimmer#Solid-state_dimmer]: "true" means leading edge, "false" (default) is trailing edge.
- **min_brightness** (**Optional**, int): Minimum brightness value on a scale from 0..1000, the default is 0.
- **max_brightness** (**Optional**, int): Maximum brightness value on a scale from 0..1000, the default is 1000.
- **nrst_pin** (**Optional**, :ref:`config-pin`): Pin connected with "NRST" of STM32. The  default is "GPIO5".
- **boot0_pin** (**Optional**, :ref:`config-pin`): Pin connected with "BOOT0" of STM32. The  default is "GPIO4".
- **current** (**Optional**): Sensor of the current in Amperes. All options from
  :ref:`Sensor <config-sensor>`.
- **voltage** (**Optional**): Sensor of the voltage in Volts. Only accurate if neutral is connected. All options from :ref:`Sensor <config-sensor>`.
- **power** (**Optional**): Sensor of the active power in Watts. Only accurate if neutral is connected. All options from :ref:`Sensor <config-sensor>`.
- **firmware**  (**Optional**, string) Version string of the [firmware](https://github.com/jamesturton/shelly-dimmer-stm32) that will be flashed on the microcontroller. The default is "51.5".
- All other options from :ref:`Light <config-light>`.


See Also
--------

- :doc:`/components/light/index`
- :apiref:`shelly_dimmer/light/shelly_dimmer.h`
- :ghedit:`Edit`
