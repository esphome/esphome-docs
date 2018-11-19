PMSX003 Particulate Matter Sensor
=================================

.. seo::
    :description: Instructions for setting up PMSX003 Particulate matter sensors
    :image: pmsx003.png

.. warning::

    This integration is experimental as I don't have the hardware to test it (yet).
    If you can verify it works (or if it doesn't), notify me on `discord <https://discord.gg/KhAMKrd>`__.

The ``pmsx003`` sensor platform allows you to use your PMS5003, PMS7003, ... particulate matter
(`datasheet <http://www.aqmd.gov/docs/default-source/aq-spec/resources-page/plantower-pms5003-manual_v2-3.pdf>`__)
sensors with esphomelib.

As the communication with the PMSX003 is done using UART, you need
to have an :ref:`UART bus <uart>` in your configuration with the ``rx_pin`` connected to the SEND/TX pin
(may also be called the RX pin, depending on the model) of the PMS. Additionally, you need to set the baud rate to 9600.

This platform supports three sensor types, which you need to specify using the ``type:`` configuration
value:

- ``PMSX003`` for generic PMS5003, PMS7003, ...; these sensors support ``pm_1_0``, ``pm_2_5`` and ``pm_10_0`` output.
- ``PMS5003T`` for PMS5003T. These support ``pm_2_5``, ``temperature`` and ``humidity``.
- ``PMS5003ST`` for PMS5003ST. These support ``pm_2_5``, ``temperature``, ``humidity`` and ``formaldehyde``.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: GPIO23

    sensor:
      - platform: pmsx003
        type: PMX003
        pm_1_0:
          name: "Particulate Matter <1.0µm Concentration"
        pm_2_5:
          name: "Particulate Matter <2.5µm Concentration"
        pm_10_0:
          name: "Particulate Matter <10.0µm Concentration"

Configuration variables:
------------------------

- **pm_1_0** (*Optional*): Use the concentration of particulates of size less than 1.0µm in µg per cubic meter.
  All options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.
- **pm_2_5** (*Optional*): Use the concentration of particulates of size less than 2.5µm in µg per cubic meter.
  All options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.
- **pm_10_0** (*Optional*): Use the concentration of particulates of size less than 10.0µm in µg per cubic meter.
  All options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.
- **temperature** (*Optional*): Use the temperature value in °C for the ``PMS5003T`` and ``PMS5003ST``.
  All options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.
- **humidity** (*Optional*): Use the humidity value in % for the ``PMS5003T`` and ``PMS5003ST``.
  All options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.
- **formaldehyde** (*Optional*): Use the formaldehyde (HCHO) concentration in µg per cubic meter for the ``PMS5003ST``.
  All options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

See Also
--------

- :ref:`sensor-filters`
- :doc:`API Reference </api/sensor/pmsx003>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/pmsx003.rst>`__

.. disqus::
