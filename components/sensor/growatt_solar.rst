Growatt Solar
=============

.. seo::
    :description: Instructions for setting up a Growatt inverter reading on modbus.
    :image: growatt.jpg
    :keywords: Growatt, Ginverter

The ``Growatt Inverter`` sensor platform allows you to use growatt inverter data reading on modbus with ESPHome.

.. figure:: images/growatt.jpg
    :align: center
    :width: 50.0%

    Growatt Logo

The communication with this integration is done over a :ref:`UART bus <uart>` using :ref:`Modbus <modbus>`.
You must therefore have a ``uart:`` entry in your configuration with both the TX and RX pins set
to some pins on your board and the baud rate set to 9600.

.. code-block:: yaml

    # Example configuration entry
    uart:
      - id: gw_uart
        baud_rate: 9600
        tx_pin: GPIO1
        rx_pin: GPIO3

    modbus:
      uart_id: gw_uart
      flow_control_pin: GPIO4

    sensor:
      - platform: growatt_solar
        update_interval: 10s
        protocol_version: RTU
        
        inverter_status:
          name: "Growatt Status Code"

        phase_a:
          voltage:
              name: "Growatt Voltage Phase A"
          current:
              name: "Growatt Current Phase A"
          active_power:
              name: "Growatt Power Phase A"
        phase_b:
          voltage:
              name: "Growatt Voltage Phase B"
          current:
              name: "Growatt Current Phase B"
          active_power:
              name: "Growatt Power Phase B"
        phase_c:
          voltage:
              name: "Growatt Voltage Phase C"
          current:
              name: "Growatt Current Phase C"
          active_power:
              name: "Growatt Power Phase C"

        pv1:
          voltage:
              name: "Growatt PV1 Voltage"
          current:
              name: "Growatt PV1 Current"
          active_power:
              name: "Growatt PV1 Active Power"

        pv2:
          voltage:
              name: "Growatt PV2 Voltage"
          current:
              name: "Growatt PV2 Current"
          active_power:
              name: "Growatt PV2 Active Power"

        active_power:
          name: "Growatt Grid Active Power"

        pv_active_power:
          name: "Growatt PV Active Power"

        frequency:
          name: "Growatt Frequency"

        energy_production_day:
          name: "Growatt Today's Generation"
          
        total_energy_production:
          name: "Growatt Total Energy Production"

        inverter_module_temp:
          name: "Growatt Inverter Module Temp"




Configuration variables:
------------------------

- **inverter_status** (*Optional*): Status code of the inverter (0: waiting, 1: normal, 3:fault)

- **protocol_version** (*Optional*): Version of the protocol used by your inverter. 
  Old inverters use RTU (default). Newer ones use RTU2 (e.g. MIC, MIN, MAX series)

- **phase_a** (*Optional*): The group of exposed sensors for Phase A/1.

  - **current** (*Optional*): Use the current value of the sensor in amperes. All options from
    :ref:`Sensor <config-sensor>`.
  - **voltage** (*Optional*): Use the voltage value of the sensor in volts.
    All options from :ref:`Sensor <config-sensor>`.
  - **active_power** (*Optional*): Use the (active) power value of the sensor in watts. All options
    from :ref:`Sensor <config-sensor>`.

- **phase_b** (*Optional*): The group of exposed sensors for Phase B/2 on applicable inverters.

  - All options from **phase_a**

- **phase_c** (*Optional*): The group of exposed sensors for Phase C/3 on applicable inverters.

  - All options from **phase_a**

- **pv1** (*Optional*): The group of exposed sensors for Photo Voltaic 1.

  - **current** (*Optional*): Use the current value of the sensor in amperes. All options from
    :ref:`Sensor <config-sensor>`.
  - **voltage** (*Optional*): Use the voltage value of the sensor in volts.
    All options from :ref:`Sensor <config-sensor>`.
  - **active_power** (*Optional*): Use the (active) power value of the sensor in watts. All options
    from :ref:`Sensor <config-sensor>`.

- **pv2** (*Optional*): The group of exposed sensors for Photo Voltaic 2.

  - All options from **pv1**

- **active_power** (*Optional*): Use the (active) power value for the Grid in watts. All options
  from :ref:`Sensor <config-sensor>`.

- **pv_active_power** (*Optional*): Use the (active) power value of PVs in total in watts. All options
  from :ref:`Sensor <config-sensor>`.

- **frequency** (*Optional*): Use the frequency value of the sensor in hertz.
  All options from :ref:`Sensor <config-sensor>`.
- **energy_production_day** (*Optional*): Use the export active energy value for same day of the
  sensor in kilo watt hours. All options from :ref:`Sensor <config-sensor>`.
- **total_energy_production** (*Optional*): Use the total exported energy value of the sensor in
  kilo watt hours. All options from :ref:`Sensor <config-sensor>`.
- **inverter_module_temp** (*Optional*): Use the inverter module temperature value of the sensor in
  degree celsius. All options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :ghedit:`Edit`
