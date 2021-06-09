Midea Air Conditioner
=====================

.. seo::
    :description: Instructions for setting up a Midea climate device
    :image: air-conditioner.png

The ``midea_ac`` component creates a Midea air conditioner climate device.

This component requires a auto-loaded ``midea-dongle`` component, that use hardware UART.

.. note::

    This protocol also used by some vendors:

        - `Electrolux <https://www.electrolux.ru/>`_
        - `Qlima <https://www.qlima.com/>`_
        - `Artel <https://www.artelgroup.com/>`_
        - `Carrier <https://www.carrier.com/>`_
        - `Comfee <http://www.comfee-russia.ru/>`_
        - `Inventor <https://www.inventorairconditioner.com/>`_
        - and maybe others

    Example of hardware implementation is `Midea Open Dongle <https://github.com/dudanov/midea-open-dongle>`_ in free `KiCad <https://kicad-pcb.org>`_ format.

.. code-block:: yaml

    # Example configuration entry

    # Disable logging over UART (required)
    logger:
      baud_rate: 0

    # UART settings for Midea dongle (required)
    uart:
      tx_pin: 1
      rx_pin: 3
      baud_rate: 9600

    # Optional (if you want modify settings)
    midea_dongle:
      strength_icon: true
    
    # Main settings
    climate:
      - platform: midea_ac
        name: "My Midea AC"
        visual:
          min_temperature: 18 °C
          max_temperature: 25 °C
          temperature_step: 0.1 °C
        beeper: true
        custom_fan_modes:
          - SILENT
          - TURBO
        preset_eco: true
        preset_sleep: true
        preset_boost: true
        custom_presets:
          - FREEZE_PROTECTION
        swing_horizontal: true
        swing_both: true
        outdoor_temperature:
          name: "Temp"
        power_usage:
          name: "Power"
        humidity_setpoint:
          name: "Hum"

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **midea_dongle_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``midea_dongle`` if you want to use multiple devices.
- **name** (**Required**, string): The name of the climate device.
- **outdoor_temperature** (*Optional*): The information for the outdoor temperature
  sensor.

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.
- **power_usage** (*Optional*): The information for the current power consumption
  sensor.

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.
- **humidity_setpoint** (*Optional*): The information for the humidity indoor
  sensor (experimental).

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.
- **beeper** (*Optional*, boolean): Beeper feedback on command. Defaults to ``False``.
- **custom_fan_modes** (*Optional*, list): List of supported custom fan modes. Possible values are: SILENT, TURBO.
- **preset_eco** (*Optional*, boolean): ECO preset support. Defaults to ``False``.
- **preset_sleep** (*Optional*, boolean): SLEEP preset support. Defaults to ``False``.
- **preset_boost** (*Optional*, boolean): BOOST preset support. Defaults to ``False``.
- **custom_presets** (*Optional*, list): List of supported custom presets. Possible values are: FREEZE_PROTECTION.
- **swing_horizontal** (*Optional*, boolean): Enable **swing horizontal** option. Defaults to ``False``.
- **swing_both** (*Optional*, boolean): Enable **swing both** option. Defaults to ``False``.
- All other options from :ref:`Climate <config-climate>`.

Configuration variables of midea-dongle component:
**************************************************

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`../uart` if you want
  to use multiple UART buses.
- **strength_icon** (*Optional*, boolean): Set if your device have signal strength icon
  and you want to use this feature. By default, on connected state, icon show maximum signal quality. Defaults to ``False``.


Acknowledgments:
----------------

Thanks to the following people for their contributions to reverse engineering the UART protocol and source code in the following repositories:

* `Mac Zhou <https://github.com/mac-zhou/midea-msmart>`_
* `NeoAcheron <https://github.com/NeoAcheron/midea-ac-py>`_
* `Rene Klootwijk <https://github.com/reneklootwijk/node-mideahvac>`_

See Also
--------

- :doc:`/components/climate/index`
- :apiref:`climate/midea_ac.h`
- :ghedit:`Edit`
