Eastron SDM Energy Monitor
==========================

.. seo::
    :description: Instructions for setting up SDM power monitors.
    :image: images/sdm220m-full.png
    :keywords: SDM220M, SDM220, SDM630

The ``sdm_meter`` sensor platform allows you to use Eastron SDM modbus energy monitors
(`website <http://www.eastrongroup.com/product_detail.php?id=170&menu1=&menu2=>`__)
with ESPHome.

.. figure:: images/sdm220m-full.png
    :align: center
    :width: 50.0%

    SDM220M Energy Monitor.

The communication with this integration is done over a :ref:`UART bus <uart>` using :ref:`Modbus <modbus>`.
You must therefore have a ``uart:`` entry in your configuration with both the TX and RX pins set
to some pins on your board and the baud rate set to 9600.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: D1
      tx_pin: D2
      baud_rate: 9600
      stop_bits: 1

    sensor:
      - platform: sdm_meter
        phase_a:
          current:
            name: "SDM220M Current"
          voltage:
            name: "SDM220M Voltage"
          active_power:
            name: "SDM220M Power"
          power_factor:
            name: "SDM220M Power Factor"
          apparent_power:
            name: "SDM220M Apparent Power"
          reactive_power:
            name: "SDM220M Reactive Power"
          phase_angle:
            name: "SDM220M Phase Angle"
        frequency:
          name: "SDM220M Frequency"
        import_active_energy:
          name: "SDM220M Import Active Energy"
        export_active_energy:
          name: "SDM220M Export Active Energy"
        import_reactive_energy:
          name: "SDM220M Import Reactive Energy"
        export_reactive_energy:
          name: "SDM220M Export Reactive Energy"
        update_interval: 60s


Configuration variables:
------------------------

- **phase_a** (*Optional*): The group of exposed sensors for Phase A/1.

  - **current** (*Optional*): Use the current value of the sensor in amperes. All options from
    :ref:`Sensor <config-sensor>`.
  - **voltage** (*Optional*): Use the voltage value of the sensor in volts.
    All options from :ref:`Sensor <config-sensor>`.
  - **active_power** (*Optional*): Use the (active) power value of the sensor in watts. All options
    from :ref:`Sensor <config-sensor>`.
  - **power_factor** (*Optional*): Use the power factor value of the sensor.
    All options from :ref:`Sensor <config-sensor>`.
  - **apparent_power** (*Optional*): Use the apparent power value of the sensor in VA. All
    options from :ref:`Sensor <config-sensor>`.
  - **reactive_power** (*Optional*): Use the reactive power value of the sensor in VAR. All
    options from :ref:`Sensor <config-sensor>`.
  - **phase_angle** (*Optional*): Use the phase angle value of the sensor in degree. All options
    from :ref:`Sensor <config-sensor>`.

- **phase_b** (*Optional*): The group of exposed sensors for Phase B/2 on applicable meters. eg: SDM630

  - All options from **phase_a**

- **phase_c** (*Optional*): The group of exposed sensors for Phase C/3 on applicable meters. eg: SDM630

  - All options from **phase_a**

- **frequency** (*Optional*): Use the frequency value of the sensor in hertz.
  All options from :ref:`Sensor <config-sensor>`.
- **import_active_energy** (*Optional*): Use the import active energy value of the sensor in watt
  hours. All options from :ref:`Sensor <config-sensor>`.
- **export_active_energy** (*Optional*): Use the export active energy value of the sensor in watt
  hours. All options from :ref:`Sensor <config-sensor>`.
- **import_reactive_energy** (*Optional*): Use the import reactive energy value of the sensor in
  volt amps reactive hours. All options from :ref:`Sensor <config-sensor>`.
- **export_reactive_energy** (*Optional*): Use the export reactive energy value of the sensor in
  volt amps reactive hours. All options from :ref:`Sensor <config-sensor>`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **address** (*Optional*, int): The address of the sensor if multiple sensors are attached to
  the same UART bus. You will need to set the address of each device manually. Defaults to ``1``.

See Also
--------

- :ref:`sensor-filters`
- :apiref:`sdm220m/sdm220m.h`
- :ghedit:`Edit`
