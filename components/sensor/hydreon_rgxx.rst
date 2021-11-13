Hydreon Rain Sensor
===================

.. seo::
    :description: Instructions for setting up Hydreon rain sensors
    :image: hydreon_rg9.jpg
    :keywords: ina219

The ``hydreon_rgxx`` sensor platform allows you to use rain sensors by Hydreon. Currently supported are the RG-9
(`rainsensors.com <https://rainsensors.com/products/rg-9/>`) and RG-15 (`rainsensors.com <https://rainsensors.com/products/rg-15/`) sensors.
These optical rain sensors use a UART connection at 3.3V. The :ref:`UART <uart>` is
required to be set up in your configuration for this sensor to work.


.. figure:: images/hydreon_rg9_full.jpg
    :align: center
    :width: 50.0%

    Hydreon RG-9 Rain Sensor.

.. code-block:: yaml
    # Example RG-9 entry
    
    uart:
      rx_pin: GPIO16
      tx_pin: GPIO17
      baud_rate: 9600

    sensor:
      - platform: hydreon_rgxx
        model: "RG_9"
        update_interval: 1s
        moisture:
          name: "rain"
          expire_after: 30s  

.. code-block:: yaml
    # Example RG-15 entry

    uart:
      rx_pin: GPIO16
      tx_pin: GPIO17
      baud_rate: 9600

    sensor:
      - platform: hydreon_rgxx
        model: "RG_15"
        update_interval: 1s
        acc:
          name: "rain"
        event_acc:
          name: "rain event"
        total_acc:
          name: "rain total"
        r_int:
          name: "rain intensity"

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

- **moisture** (*Optional*): Rain intensity level from 0-7. Only on RG-9.

  - **name** (**Required**, string): The name for the voltage sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **acc** (*Optional*): Amount of rain since last message (see `update_interval`), in `mm`. Only on RG-15.

  - **name** (**Required**, string): The name for the voltage sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **event_acc** (*Optional*): Amount of rain for this event (i.e. since it last stopped raining), in `mm`. Only on RG-15.

  - **name** (**Required**, string): The name for the voltage sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **total_acc** (*Optional*): Total amount of rain this sensor has ever measured, in `mm`. Only on RG-15.

  - **name** (**Required**, string): The name for the voltage sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **r_int** (*Optional*): Current rain intensity in `mm/h`. Only on RG-15.

  - **name** (**Required**, string): The name for the voltage sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``1s``.


See Also
--------

- :ref:`sensor-filters`
- :ghedit:`Edit`
