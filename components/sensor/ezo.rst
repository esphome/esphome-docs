EZO sensor circuits
===================

.. seo::
    :description: Instructions for setting up EZO sensor circuits in esphome
    :image: ezo-ph-circuit.png
    :keywords: ezo ph ec rtd sensor circuit esphome

The ``ezo`` sensor platform allows you to use your EZO sensor circuits with
ESPHome. The :ref:`I²C Bus <i2c>` is
required to be set up in your configuration for this sensor to work.

Data sheet: (`datasheet <https://atlas-scientific.com/files/pH_EZO_Datasheet.pdf>`__)

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

- ``set_tempcomp_value(float temp)``: Send the given temperature to the sensor.

  .. code-block:: cpp

      // Within a lambda, set the temperature compensation value from the temperature sensor
      id(ph_ezo).set_tempcomp_value(id(rtd_ezo).state);


- ``set_custom(const std::string &to_send)``: Runs a custom command. This sends exactly what is in ``to_send``

  .. code-block:: cpp

      // Run a custom command to turn on the LED
      id(ph_ezo).set_custom("L,1");


- ``set_t(std::string value)``: Send the given temperature to the sensor.

  .. code-block:: cpp

      // Within a lambda, set the temperature (in celcius) compensation value from the temperature sensor.
      id(ph_ezo).set_t("27.00");


- ``get_t()``: Sensor retrieves temperature compensation value and triggers ``on_t:`` once done

  .. code-block:: cpp

      // Within a lambda, set the temperature (in celcius) compensation value from the temperature sensor.
      id(ph_ezo).get_t();


- ``set_i2c()``: Set I2C mode

  .. code-block:: cpp

      // Set I2C Mode
      id(ph_ezo).set_i2c();


- ``set_sleep()``:  Put the device to sleep

  .. code-block:: cpp

      // Put the device to sleep
      id(ph_ezo).set_sleep();


- ``get_calibration()``: Sensor retrieves calibration and triggers ``on_calibration:`` once done

  .. code-block:: cpp

      // Calibration      
      id(ph_ezo).get_calibration();

- ``set_calibration(std::string point, std::string value)``: Sets calibration. Point is one of "low,mid,high". Refer to the datasheet for more information

  .. code-block:: cpp

      id(ph_ezo).set_calibration("mid", "7.00");
      

- ``clear_calibration()``: Clears calibration

  .. code-block:: cpp

      id(ph_ezo).clear_calibration();


- ``get_device_information()``: Sensor retrieves calibration and triggers ``on_device_information:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_device_information();


- ``get_slope()``: Sensor retrieves slope and triggers ``on_slope:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_slope();


- ``get_led_state()``: Sensor LED state and triggers ``on_led:`` once done

  .. code-block:: cpp

      id(ph_ezo).get_led_state();

  
- ``set_led_state(bool on)``: Sensor LED on or off

  .. code-block:: cpp

      id(ph_ezo).set_led_state(true);


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
