Pylontech Battery
=================

.. seo::
    :description: Instructions for setting up Pylontech Battery in ESPHome.
    :image: pylontech.jpg

The Pylontech component allows you to pull data from Pylontech Batteries into ESPHome.
It uses :ref:`UART <uart>` for communication.

Once configured, you can use sensors as described below for your projects.

.. figure:: images/pylontech.jpg
    :align: center
    :width: 50.0%

    Pylontech Batteries

Hardware Setup
--------------

You can connect to Pylontech Batteries using the port labeled "Console".
Any connections via CAN or RS485 (e.g. to an inverter) are untouched and remain functional.

The console port offers a RS232 interface using a RJ10 or RJ45 connector.
The voltage levels are *not* TTL-compatible. A RS232 transceiver must be placed between the Batteries and the ESPHome device.
MAX3232-based transceivers have been tested and work well.

If you have multiple batteries you need to connect to the master battery's console port.

.. list-table:: Pylontech RJ45 Console Port (US2000C, US3000C)
    :header-rows: 1

    * - RJ45 Pin
      - Function
      - Connect to
    * - 3
      - Pylontech TX
      - ESPHome RX via transceiver
    * - 6
      - Pylontech RX
      - ESPHome TX via transceiver
    * - 8
      - GND
      - GND

.. figure:: images/rj45_pinout.jpg
    :align: center
    :width: 70.0%

    RJ45 pinout

.. list-table:: Pylontech RJ10 Console Pinout (US2000B)
    :header-rows: 1

    * - RJ410 Pin
      - Function
      - Connect to
    * - 2
      - Pylontech RX
      - ESPHome TX via transceiver
    * - 3
      - Pylontech TX
      - ESPHome RX via transceiver
    * - 4
      - GND
      - GND
      
Configuration
-------------

.. code-block:: yaml

    # Example configuration entry
    uart:
      - id: pylontech_uart
        tx_pin: GPIO1
        rx_pin: GPIO3
        baud_rate: 115200

    pylontech:
      - uart_id: pylontech_uart
        id: pylontech0
        update_interval: 5s


Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **id** (**Required**, :ref:`config-id`): The id to use for this Pylontech component.
- **uart_id** (*Optional*): The uart Bus ID
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.

Sensor
------

All values are reported for every Pylontech battery individually.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pylontech
        pylontech_id: pylontech0
        battery: 1
        
        voltage:
          id: bat1_voltage
          name: "Battery1 Voltage"
        current:
          id: bat1_current
          name: "Battery1 Current"
        coulomb:
          id: bat1_soc
          name: "Battery1 State of Charge"
          
          
      - platform: pylontech
        pylontech_id: pylontech0
        battery: 2
        
        voltage:
          id: bat2_voltage
          name: "Battery2 Voltage"
        current:
          id: bat2_current
          name: "Battery2 Current"
        coulomb:
          id: bat2_soc
          name: "Battery2 State of Charge"

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **pylontech_id** (**Required**): ID of the pylontech instance
- **battery** (**Required**): Which battery to monitor. 1 stands for the master battery, 2..6 for slave batteries.
- **voltage** (*Optional*): Voltage. Should be around 48V
- **current** (*Optional*): Current
- **coulomb** (*Optional*): State of Charge in percent
- **temperature** (*Optional*): Temperature
- **temperature_low** (*Optional*): Historic minimum temperature
- **temperature_high** (*Optional*): Historic maximum temperature
- **voltage_low** (*Optional*): Historic minimum voltage
- **voltage_high** (*Optional*): Historic maximum voltage
- **mos_temperature** (*Optional*): Temperature of the mosfets.

All sensors are normal sensors, so each one supports options from :ref:`Sensor <config-sensor>`.

Text Sensor
-----------

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: pylontech
        pylontech_id: pylontech0
        battery: 1
        
        base_state:
          id: bat1_base_state
          name: "Battery1 Base State"


Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **pylontech_id** (**Required**): ID of the pylontech instance
- **battery** (**Required**): Which battery to monitor. 1 stands for the master battery, 2..6 for slave batteries.
- **base_state** (*Optional*): Base state. Usually reads ``Dischg`` or ``Charge``.
- **voltage_state** (*Optional*): Voltage state. Usually reads ``Normal``.
- **current_state** (*Optional*): Current state. Usually reads ``Normal``.
- **temperature_state** (*Optional*): Temperature state. Usually reads ``Normal``.

All sensors are normal text sensors, so each one supports options from :ref:`Text Sensor <config-text_sensor>`.

Energy Monitoring
-----------------

By combining :doc:`template sensors </components/sensor/template>` and :doc:`integration sensors </components/sensor/integration>`
one can monitor the energy flowing into and out of all batteries combined, ready for `Homeassistant Energy Monitoring <https://www.home-assistant.io/docs/energy/battery/>`__.

.. code-block:: yaml

    sensor:
      - platform: template
        id: pylontech_power
        name: "Pylontech power"
        unit_of_measurement: W
        lambda: |-
          auto pwr1 = id(bat1_voltage).state * id(bat1_current).state;
          auto pwr2 = id(bat2_voltage).state * id(bat2_current).state;
          auto pwr = pwr1 + pwr2;
          id(combined_charge_power).publish_state(max(pwr, 0.0f));
          id(combined_discharge_power).publish_state(max(-pwr, 0.0f));
          return pwr;
        update_interval: 5s
        device_class: power
        state_class: measurement
        
      - platform: template
        id: combined_charge_power
      
      - platform: template
        id: combined_discharge_power
      
      - platform: integration
        name: "Pylontech charging"
        sensor: combined_charge_power
        time_unit: h
        state_class: total_increasing
        device_class: energy
        unit_of_measurement: "Wh"

      - platform: integration
        name: "Pylontech discharging"
        sensor: combined_discharge_power
        time_unit: h
        state_class: total_increasing
        device_class: energy
        unit_of_measurement: "Wh"

See Also
--------

- `Pylontech-Battery-Monitoring <https://github.com/irekzielinski/Pylontech-Battery-Monitoring>`__
- `nodered-pylontech-console-reader <https://github.com/juanhaywood/nodered-pylontech-console-reader>`__
- :ref:`uart`
- :ghedit:`Edit`
