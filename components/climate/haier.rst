Haier Climate Device
=====================

.. seo::
    :description: Instructions for setting up a Haier climate device
    :image: air-conditioner.svg

The ``haier`` component to control AC on the base of the hOn Haier protocol (AC that is controlled by the hOn application).

.. code-block:: yaml

    # Example configuration entry
     uart:
      baud_rate: 9600
      tx_pin: 17
      rx_pin: 16
      id: ac_port  
    
    climate:
      - platform: haier
        id: ac_port
        name: Haier AC 
        uart_id: ac_port
        wifi_signal: true               # Optional, default true, enables WiFI signal transmission from ESP to AC
        beeper: true                    # Optional, default true, disables beep on commands from ESP
        outdoor_temperature:            # Optional, outdoor temperature sensor
          name: Outdoor temperature
        visual:                         # Optional, you can use it to limit min and max temperatures in UI (not working for remote!)
          min_temperature: 16 °C
          max_temperature: 30 °C
          temperature_step: 1 °C
        supported_swing_modes:          # Optional, can be used to disable some swing modes if your AC does not support it
        - 'OFF'
        - VERTICAL
        - HORIZONTAL
        - BOTH   

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation
- **uart_id** (*Optional*, :ref:`config-id`): ID of the UART port to communicate with AC
- **name** (**Required**, string): The name of the climate device
- **wifi_signal** (*Optional*, boolean): If true - send wifi signal level to AC
- **beeper** (*Optional*, boolean): Can be used to disable beeping on commands from AC
- **outdoor_temperature** (*Optional*): Temperature sensor for outdoor temperature

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): ID of the sensor, can be used for code generation
  - All other options from :ref:`Sensor <config-sensor>`.
- **supported_swing_modes** (*Optional*, list): Can be used to disable some swing modes if your AC does not support it. Possible values: OFF (use quotes in opposite case ESPHome will convert it to False), VERTICAL, HORIZONTAL, BOTH
- All other options from :ref:`Climate <config-climate>`.

# Automations

Haier climate support some actiuons:

# climate.haier.display_on Action

This action turns the AC display on

```
on_...:
  then:
    climate.haier.display_on: device_id
```

# climate.haier.display_off Action

This action turns the AC display off

```
on_...:
  then:
    climate.haier.display_off: device_id
```

# climate.haier.beeper_on Action

This action enables beep feedback on every command sent to AC

```
on_...:
  then:
    climate.haier.beeper_on: device_id
```

# climate.haier.beeper_off Action

This action disables beep feedback on every command sent to AC (keep in mind that this will not work for IR remote commands)

```
on_...:
  then:
    climate.haier.beeper_off: device_id
```

# climate.haier.set_vertical_airflow Action

Set direction for vertical airflow if the vertical swing is disabled. Possible values: Up, Center, Down.

```
on_value:
  then:
    - climate.haier.set_vertical_airflow:
      id: device_id
      vertical_airflow: Up
```

# climate.haier.set_horizontal_airflow Action

Set direction for horizontal airflow if the horizontal swing is disabled. Possible values: Left, Center, Right.

```
on_value:
  then:
    - climate.haier.set_horizontal_airflow:
      id: device_id
      vertical_airflow: Right
```
