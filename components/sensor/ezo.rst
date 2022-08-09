EZO sensor circuits
===================

.. esphome:component-definition::
   :alias: ezo
   :category: sensor-miscellaneous
   :friendly_name: EZO Sensor Circuits
   :toc_group: Miscellaneous Sensors
   :toc_image: ezo-ph-circuit.png
   :descriptor: (pH)


.. seo::
    :description: Instructions for setting up EZO sensor circuits in esphome
    :image: ezo-ph-circuit.png
    :keywords: ezo ph ec rtd sensor circuit esphome

The ``ezo`` sensor platform allows you to use your EZO sensor circuits with
ESPHome. The :ref:`I²C Bus <i2c>` is
required to be set up in your configuration for this sensor to work.

.. figure:: images/ezo-ph-circuit.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    sensor:

      - platform: ezo
        id: ph_ezo
        address: 99
        unit_of_measurement: "pH"
        update_interval: 10s

      - platform: ezo
        id: rtd_ezo
        name: "RTD Temperature"
        address: 102
        accuracy_decimals: 2
        unit_of_measurement: "°C"
        update_interval: 10s


Configuration variables:
------------------------

- **address** (**Required**, int): Specify the I²C address of the sensor.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- All other options from :ref:`Sensor <config-sensor>`.

lambda calls
------------

From :ref:`lambdas <config-lambda>`, you can set the temperature compensation for the
sensors that support that option.

- ``set_tempcomp_value()``: Send the given temperature to the sensor.

  .. code-block:: cpp

      // Within a lambda, set the temperature compensation value from the temperature sensor
      id(ph_ezo).set_tempcomp_value(id(rtd_ezo).state);


See Also
--------

- :ref:`sensor-filters`
- :apiref:`ezo/ezo.h`
- :ghedit:`Edit`
