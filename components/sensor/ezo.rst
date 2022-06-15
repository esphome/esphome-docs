EZO sensor circuits
===================

.. seo::
    :description: Instructions for setting up EZO sensor circuits in esphome
    :image: ezo-ph-circuit.png
    :keywords: ezo ph ec rtd sensor circuit esphome

The ``ezo`` sensor platform allows you to use your EZO sensor circuits with
ESPHome. The :ref:`I²C Bus <i2c>` is
required to be set up in your configuration for this sensor to work.
All embedded solutions from EZO can be found `here <https://atlas-scientific.com/embedded-solutions/>`__.
If a certain command is not supported by default, it can be executed with

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

.. _evo_lambda_calls:

lambda calls
------------

From :ref:`lambdas <config-lambda>`, you can interacte with the sensor in various ways. For any ``get`` command a trigger will be called with the information retrieved from the sensor. See :ref:`evo_callbacks`.

- ``set_i2c()``: Set I2C mode

  .. code-block:: cpp

      id(ph_ezo).set_i2c();


- ``get_device_information()``: Sensor retrieves calibration and triggers ``on_device_information:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_device_information();


- ``set_sleep()``:  Put the device to sleep

  .. code-block:: cpp

      id(ph_ezo).set_sleep();


- ``get_slope()``: Sensor retrieves slope and triggers ``on_slope:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_slope();


- ``set_tempcomp_value(float temp)``: Send the given temperature (in Celcius) to the sensor.

  .. code-block:: cpp

      id(ph_ezo).set_tempcomp_value(id(rtd_ezo).state);


- ``set_t(std::string value)``: Send the given temperature (in Celcius) to the sensor.

  .. code-block:: cpp

      id(ph_ezo).set_t("27.00");


- ``get_t()``: Sensor retrieves temperature compensation value (in Celcius) and triggers ``on_t:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_t();


- ``set_calibration(std::string point, std::string value)``: Sets calibration. Point is one of "low,mid,high". Refer to the datasheet for more information

  .. code-block:: cpp

      id(ph_ezo).set_calibration("mid", "7.00");


- ``get_calibration()``: Sensor retrieves calibration and triggers ``on_calibration:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_calibration();


- ``clear_calibration()``: Clears calibration

  .. code-block:: cpp

      id(ph_ezo).clear_calibration();


- ``get_led_state()``: Sensor LED state and triggers ``on_led:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_led_state();


- ``set_led_state(bool on)``: Sensor LED on or off

  .. code-block:: cpp

      id(ph_ezo).set_led_state(true);


- ``send_custom(const std::string &payload, uint16_t delay_ms = 300, bool response_expected = false)``: Runs a custom command. This sends exactly what is in ``payload``. Optionally you can set a ``delay`` and if a response is expected that should be parsed. Defaults to ``false`` for custom commands.

  .. code-block:: cpp

      // Run a custom command to turn on the LED
      id(ph_ezo).send_custom("L,1");


.. _evo_callbacks:

Callbacks
---------

- **on_led:** : Triggered when the result of ``get_led_state()`` is ready
- **on_device_information:** : Triggered when the result of ``get_device_information()`` is ready
- **on_slope:** : Triggered when the result of ``get_slope()`` is ready
- **on_calibration:** : Triggered when the result of ``get_calibration()`` is ready
- **on_t:** : Triggered when the result of ``get_t()`` is ready
- **on_custom:** : Triggered when the result of ``get_custom()`` is ready


See Also
--------

- :ref:`sensor-filters`
- :apiref:`ezo/ezo.h`
- :ghedit:`Edit`
