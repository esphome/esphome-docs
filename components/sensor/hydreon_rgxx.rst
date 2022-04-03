Hydreon Rain Sensor
===================

.. seo::
    :description: Instructions for setting up Hydreon rain sensors
    :image: hydreon_rg9.jpg
    :keywords: hydreon

The ``hydreon_rgxx`` sensor platform allows you to use rain sensors by Hydreon. Currently supported are the RG-9 and RG-15 (`rainsensors <https://rainsensors.com/products/model-comparison/>`_) sensors.
These optical rain sensors use a UART connection at 3.3V. The :ref:`UART <uart>` is
required to be set up in your configuration for this sensor to work.


.. figure:: images/hydreon_rg9_full.jpg
    :align: center
    :width: 50.0%

    Hydreon RG-9 Rain Sensor. Image by `Hydreon <https://rainsensors.com/products/rg-9/>`_.

.. code-block:: yaml

    # Example RG-9 entry
    
    uart:
      rx_pin: GPIO16
      tx_pin: GPIO17
      baud_rate: 9600

    sensor:
      - platform: hydreon_rgxx
        model: "RG_9"
        update_interval: 60s
        moisture:
          name: "rain"
          expire_after: 120s  
          
    binary_sensor:
      - platform: hydreon_rgxx
        too_cold:
          name: "too cold"

.. code-block:: yaml

    # Example RG-15 entry

    uart:
      rx_pin: GPIO16
      tx_pin: GPIO17
      baud_rate: 9600

    sensor:
      - platform: hydreon_rgxx
        model: "RG_15"
        update_interval: 60s
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

- **model**: (**Required**, int): Specify which rain sensor you have connected. Must be either ``RG_9`` or ``RG_15``.

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

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.


See Also
--------

- :ref:`sensor-filters`
- :doc:`../binary_sensor/hydreon_rgxx`
- `Hydreon RG-9 <https://rainsensors.com/products/rg-9/>`__
- `Hydreon RG-15 <https://rainsensors.com/products/rg-15/>`__
- `RG-15 V1.000 manual <https://rainsensors.com/wp-content/uploads/sites/3/2020/07/rg-15_instructions_sw_1.000.pdf>`__
- `RG-9 V1.000 manual <https://rainsensors.com/wp-content/uploads/sites/3/2021/03/2020.08.25-rg-9_instructions.pdf>`__
- :ghedit:`Edit`
