Havells Solar
=============

.. seo::
    :description: Instructions for setting up Havells inverter reading on modbus.
    :image: havellsgti5000d_s.jpg
    :keywords: Havells Enviro, Havells GTI

The ``Havells Inverter`` sensor platform allows you to use Havells inverter data reading on modbus
(`website <https://www.havells.com/en/consumer/solar/solar-on-grid-inverter-and-solutions/solar-on-grid-inverter.html>`__)
with ESPHome.

.. figure:: images/havellsgti5000d.jpg
    :align: center
    :width: 50.0%

    Havells On Grid Solar Inverter.

The communication with this component is done via a :ref:`UART <uart>` using :ref:`Modbus <modbus>`.
You must therefore have a ``uart:`` and ``modbus:`` entry in your configuration with both the TX and RX pins set
to some pins on your board and the baud rate set to 9600.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: havells_solar
        update_interval: 60s
        phase_a:
          voltage:
              name: "HAVELLS Phase A Voltage"
          current:
              name: "HAVELLS Phase A Current"
        phase_b:
          voltage:
              name: "HAVELLS Voltage Phase B"
          current:
              name: "HAVELLS Current Phase B"
        phase_c:
          voltage:
              name: "HAVELLS Voltage Phase C"
          current:
              name: "HAVELLS Current Phase C"
        pv1:
          voltage:
              name: "HAVELLS PV1 Voltage"
          current:
              name: "HAVELLS PV1 Current"
          active_power:
              name: "HAVELLS PV1 Active Power"
          voltage_sampled_by_secondary_cpu:
              name: "HAVELLS PV1 Voltage Sampled By Slave CPU"
          insulation_of_p_to_ground:
              name: "HAVELLS PV1 Insulation Of +VE To Ground"
        pv2:
          voltage:
              name: "HAVELLS PV2 Voltage"
          current:
              name: "HAVELLS PV2 Current"
          active_power:
              name: "HAVELLS PV2 Active Power"
          voltage_sampled_by_secondary_cpu:
              name: "HAVELLS PV2 Voltage Sampled By Slave CPU"
          insulation_of_p_to_ground:
              name: "HAVELLS PV2 Insulation Of +VE To Ground"
        active_power:
          name: "HAVELLS Active Power"
        reactive_power:
          name: "HAVELLS Reactive Power"
        frequency:
          name: "HAVELLS Frequency"
        energy_production_day:
          name: "HAVELLS Today's Generation"
        total_energy_production:
          name: "HAVELLS Total Energy Production"
        total_generation_time:
          name: "HAVELLS Total Generation Time"
        today_generation_time:
          name: "HAVELLS Today Generation Time"
        inverter_module_temp:
          name: "HAVELLS Inverter Module Temp"
        inverter_inner_temp:
          name: "HAVELLS Inverter Inner Temp"
        inverter_bus_voltage:
          name: "HAVELLS Inverter BUS Voltage"
        insulation_of_pv_n_to_ground:
          name: "HAVELLS Insulation Of PV- To Ground"
        gfci_value:
          name: "HAVELLS GFCI Value"
        dci_of_r:
          name: "HAVELLS DCI Of R"
        dci_of_s:
          name: "HAVELLS DCI Of S"
        dci_of_t:
          name: "HAVELLS DCI Of T"



Configuration variables:
------------------------

- **phase_a** (*Optional*): The group of exposed sensors for Phase A/1.

  - **current** (*Optional*): Use the current value of the sensor in amperes. All options from
    :ref:`Sensor <config-sensor>`.
  - **voltage** (*Optional*): Use the voltage value of the sensor in volts.
    All options from :ref:`Sensor <config-sensor>`.

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
  - **voltage_sampled_by_secondary_cpu** (*Optional*): Use the photo voltiac's voltage sampled by
    slave CPU value of the sensor in volts. All options from :ref:`Sensor <config-sensor>`.
  - **insulation_of_p_to_ground** (*Optional*): Use the insulation of photo voltiac's +ve terminal to
    ground value of the sensor in kilo ohms. All options from :ref:`Sensor <config-sensor>`.

- **pv2** (*Optional*): The group of exposed sensors for Photo Voltaic 2.

  - All options from **pv1**

- **active_power** (*Optional*): Use the (active) power value of the sensor in watts. All options
  from :ref:`Sensor <config-sensor>`.
- **reactive_power** (*Optional*): Use the reactive power value of the sensor in VAR. All
  options from :ref:`Sensor <config-sensor>`.
- **frequency** (*Optional*): Use the frequency value of the sensor in hertz.
  All options from :ref:`Sensor <config-sensor>`.
- **energy_production_day** (*Optional*): Use the export active energy value for same day of the
  sensor in kilo watt hours. All options from :ref:`Sensor <config-sensor>`.
- **total_energy_production** (*Optional*): Use the total exported energy value of the sensor in
  kilo watt hours. All options from :ref:`Sensor <config-sensor>`.
- **total_generation_time** (*Optional*): Use the total generation time value of the sensor in
  hours. All options from :ref:`Sensor <config-sensor>`.
- **today_generation_time** (*Optional*): Use the day generation time value for same day of the
  sensor in minutes. All options from :ref:`Sensor <config-sensor>`.
- **inverter_module_temp** (*Optional*): Use the inverter module temperature value of the sensor in
  degree celsius. All options from :ref:`Sensor <config-sensor>`.
- **inverter_inner_temp** (*Optional*): Use the inverter inner temperature value of the sensor in
  degree celsius. All options from :ref:`Sensor <config-sensor>`.
- **inverter_bus_voltage** (*Optional*): Use the inverter bus voltage value of the sensor in volts.
  All options from :ref:`Sensor <config-sensor>`.
- **insulation_of_pv_n_to_ground** (*Optional*): Use the insulation  of  photo  voltiacs's
  -ve terminal to ground value of the sensor in kilo ohms. All options from :ref:`Sensor <config-sensor>`.
- **gfci_value** (*Optional*): Use the GFCI value of the sensor.
  All options from :ref:`Sensor <config-sensor>`.
- **dci_of_r** (*Optional*): Use the DCI of R value of the sensor.
  All options from :ref:`Sensor <config-sensor>`.
- **dci_of_s** (*Optional*): Use the DCI of S value of the sensor.
  All options from :ref:`Sensor <config-sensor>`.
- **dci_of_t** (*Optional*): Use the DCI of T value of the sensor.
  All options from :ref:`Sensor <config-sensor>`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **address** (*Optional*, int): The address of the sensor if multiple sensors are attached to
  the same UART bus. You will need to set the address of each device manually. Defaults to ``1``.

See Also
--------

- :ref:`sensor-filters`
- :ghedit:`Edit`
