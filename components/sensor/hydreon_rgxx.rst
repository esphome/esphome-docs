Hydreon Rain Sensor
===================

.. seo::
    :description: Instructions for setting up Hydreon rain sensors
    :image: hydreon_rg9.jpg
    :keywords: ina219

The ``hydreon_rgxx`` sensor platform allows you to use rain sensors by Hydreon. Currently supported are the RG-9 (`rainsensors.com <https://rainsensors.com/products/rg-9/>`) and RG-15 (`rainsensors.com <https://rainsensors.com/products/rg-15/`) sensors.
These optical rain sensors use a UART connection at 3.3V. The :ref:`UART <uart>` is
required to be set up in your configuration for this sensor to work.


.. figure:: images/hydreon_rg9.jpg
    :align: center
    :width: 50.0%

    Hydreon RG-9 Rain Sensor.

.. code-block:: yaml

		uart:
			rx_pin: GPIO16
			tx_pin: GPIO17
			baud_rate: 9600

    # Example RG-9 entry
		sensor:
			- platform: hydreon_rgxx
				model: "RG_9"
				moisture:
					name: "Rain"
					expire_after: 30s	

.. code-block:: yaml

		uart:
			rx_pin: GPIO16
			tx_pin: GPIO17
			baud_rate: 9600

    # Example RG-15 entry
		sensor:
			- platform: hydreon_rgxx
				model: "RG_15"
				acc:
					name: "rain"
				eventacc:
					name: "rain event"
				totalacc:
					name: "rain total"
				rint:
					name: "rain intensity"

Configuration variables:
------------------------

- **address** (*Optional*, int): Manually specify the I²C address of the sensor. Defaults to ``0x40``.
- **shunt_resistance** (*Optional*, float): The value of the shunt resistor on the board for current calculation.
  Defaults to ``0.1 ohm``.
- **max_voltage** (*Optional*, float): The maximum bus voltage you are expecting. ESPHome will use this to
  configure the sensor optimally. Defaults to ``32V`` (the max).
- **max_current** (*Optional*, float): The maximum current you are expecting. ESPHome will use this to
  configure the sensor optimally. Defaults to ``3.2A``.
- **current** (*Optional*): Use the current value of the sensor in amperes. All options from
  :ref:`Sensor <config-sensor>`.
- **power** (*Optional*): Use the power value of the sensor in watts. All options from
  :ref:`Sensor <config-sensor>`.
- **bus_voltage** (*Optional*): Use the bus voltage (voltage of the high side contact) value of the sensor in V.
  All options from :ref:`Sensor <config-sensor>`.
- **shunt_voltage** (*Optional*): Use the shunt voltage (voltage across the shunt resistor) value of the sensor in V.
  All options from :ref:`Sensor <config-sensor>`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.


See Also
--------

- :ref:`sensor-filters`
- :doc:`ina3221`
- :apiref:`ina219/ina219.h`
- `INA291 Arduino Library <https://github.com/adafruit/Adafruit_INA219>`__ by `Adafruit <https://www.adafruit.com/>`__
- :ghedit:`Edit`
