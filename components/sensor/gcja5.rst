Panasonic SN-GCJA5 Particulate Matter Sensor
============================================

.. seo::
    :description: Instructions for setting up Panasonic SN-GCJA5 Particulate matter sensors
    :image: gcja5.svg

The ``gcja5`` sensor platform allows you to use your Panasonic SN-GCJA5 laser based particulate matter sensor
(`datasheet <https://na.industrial.panasonic.com/products/sensors/air-quality-gas-flow-sensors/lineup/laser-type-pm-sensor/series/123557/model/123559>`__)
sensors with ESPHome.

As the communication with the GCJA5 is done using UART, you need
to have an :ref:`UART bus <uart>` in your configuration with the ``rx_pin`` connected to the SEND/TX. Additionally, you need to set the baud rate to 9600, and you
MUST have ``EVEN`` parity.

The sensor itself will push values every second. You may wish to :ref:`filter <sensor-filters>` this value to reduce the amount of data you are ingesting.
The sensor will internally track changes to the Laser Diode and Photo Diode over time to adjust and ensure accuracy.
Based on continous runtime, the sensor is rated to last at least 5 years.

.. code-block:: yaml

    # Example configuration entry

    sensor:
      - platform: gcja5
        pm_1_0:
          name: "Particulate Matter <1.0µm Concentration"
        pm_2_5:
          name: "Particulate Matter <2.5µm Concentration"
        pm_10_0:
          name: "Particulate Matter <10.0µm Concentration"

Configuration variables:
------------------------

- **pm_1_0** (*Optional*): Mass of particles with a diameter of 1 micrometres or less (μg/m^3).
  All options from :ref:`Sensor <config-sensor>`.
- **pm_2_5** (*Optional*): Mass of particles with a diameter of 2.5 micrometres or less (μg/m^3).
  All options from :ref:`Sensor <config-sensor>`.
- **pm_10_0** (*Optional*): Mass of particles with a diameter of 10 micrometres or less (μg/m^3).
  All options from :ref:`Sensor <config-sensor>`.
- **pm_10_0** (*Optional*): Mass of particles with a diameter of 10 micrometres or less (μg/m^3).
  All options from :ref:`Sensor <config-sensor>`.
- **pmc_0_3** (*Optional*): Count of particles with diameter > 0.3 um in 0.1 L of air (#/0.1L).
  All options from :ref:`Sensor <config-sensor>`.
- **pmc_0_5** (*Optional*): Count of particles with diameter > 0.5 um in 0.1 L of air (#/0.1L).
  All options from :ref:`Sensor <config-sensor>`.
- **pmc_1_0** (*Optional*): Count of particles with diameter > 1 um in 0.1 L of air (#/0.1L).
  All options from :ref:`Sensor <config-sensor>`.
- **pmc_2_5** (*Optional*): Count of particles with diameter > 2.5 um in 0.1 L of air (#/0.1L).
  All options from :ref:`Sensor <config-sensor>`.
- **pmc_5_0** (*Optional*): Count of particles with diameter > 5 um in 0.1 L of air (#/0.1L).
  All options from :ref:`Sensor <config-sensor>`.
- **pmc_10_0** (*Optional*): Count of particles with diameter > 10 um in 0.1 L of air (#/0.1L).
  All options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :doc:`/components/sensor/gcja5`
- :ref:`sensor-filters`
- :apiref:`gcja5/gcja5.h`
- :ghedit:`Edit`
