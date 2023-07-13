Panasonic SN-GCJA5 Particulate Matter Sensor
=================================

.. seo::
    :description: Instructions for setting up Panasonic SN-GCJA5 Particulate matter sensors

The ``gcja5`` sensor platform allows you to use your Panasonic SN-GCJA5 laser based particulate matter sensor
(`datasheet <https://na.industrial.panasonic.com/products/sensors/air-quality-gas-flow-sensors/lineup/laser-type-pm-sensor/series/123557/model/123559>`__)
sensors with ESPHome.

As the communication with the GCJA5 is done using UART, you need
to have an :ref:`UART bus <uart>` in your configuration with the ``rx_pin`` connected to the SEND/TX. Additionally, you need to set the baud rate to 9600, and you
MUST have `EVEN`` parity.

The sensor itself will push values every second. You may wish to filter this value to reduce the amount of data you are ingesting.
The sensor will internally track changes to the Laser Diode and Photo Diode over time to adjust and ensure accuracy.
Based on continous runtime, the sensor is rated to last at least 5 years.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: GPIO10
      parity: EVEN
      baud_rate: 9600

    # Use a 30 second averaging filter to reduce the amount of data
    sensor:
      - platform: gcja5
        pm_1_0:
          name: "Particulate Matter <1.0µm Concentration"
          filters:
          - sliding_window_moving_average:
              window_size: 30
              send_every: 30
        pm_2_5:
          name: "Particulate Matter <2.5µm Concentration"
          filters:
          - sliding_window_moving_average:
              window_size: 30
              send_every: 30
        pm_10_0:
          name: "Particulate Matter <10.0µm Concentration"
          filters:
          - sliding_window_moving_average:
              window_size: 30
              send_every: 30

Configuration variables:
------------------------

- **pm_1_0_std** (*Optional*): Use the concentration of particulates of size less than 1.0µm in µg per cubic meter at standard particle.
  All options from :ref:`Sensor <config-sensor>`.
- **pm_2_5_std** (*Optional*): Use the concentration of particulates of size less than 2.5µm in µg per cubic meter at standard particle.
  All options from :ref:`Sensor <config-sensor>`.
- **pm_10_0_std** (*Optional*): Use the concentration of particulates of size less than 10.0µm in µg per cubic meter at standard particle.
  All options from :ref:`Sensor <config-sensor>`.
- **pm_1_0** (*Optional*): Use the concentration of particulates of size less than 1.0µm in µg per cubic meter under atmospheric environment.


See Also
--------

- :doc:`/components/sensor/gcja5`
- :ref:`sensor-filters`
- :apiref:`gcja5/gcja5.h`
- :ghedit:`Edit`
