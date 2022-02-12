Analog Threshold Binary Sensor
==============================

.. seo::
    :description: Instructions for setting up an analog threshold binary sensors.
    :image: analog_threshold.svg

The ``analog_threshold`` binary sensor platform allows you to convert analog values 
(i.e. :doc:`sensor </components/sensor/index>` readings) 
into boolean values, using a threshold as a reference.

It provides some options to reduce instability when the source signal is noisy:
*hysteresis* (using different limits depending on the current state) 
and *delay* (only change after a new state has been kept a minimum time).

For example, below configuration would turn the readings of current sensor into
a binary sensor.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: analog_threshold
        name: "Garage Door Opening"
        sensor_id: motor_current_sensor
        threshold: 0.5


Configuration variables
-----------------------

-  **name** (**Required**, string): The name of the binary sensor.
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
-  **sensor_id** (**Required**, :ref:`config-id`): The ID of the source sensor.
-  **threshold** (**Required**, float or mapping): Configures the reference for comparison. Accepts either a shorthand 
   float number that will be used as both upper/lower threshold, or a mapping to define different values for each (to 
   use hysteresis).

   -  **upper** (**Required**, float): Upper threshold, that needs to be crossed to transition from ``low`` to ``high`` states.
   -  **lower** (**Required**, float): Lower threshold, that needs to be crossed to transition from ``high`` to ``low`` states.
-  **inverted** (*Optional*, boolean): If comparison against the threshold should be treated as inverted. In normal comparison,
   when the signal is greater or equal to the threshold (``high`` state) the binary sensor is consider as ``True``. 
   Defaults to ``false``.
-  **delay** (*Optional*, :ref:`config-time` or mapping): Minimum amount of time a prospective new state has to be kept
   in order to actually change the output. It can be a shorthand single value, 
   or a mapping with different delays for high and low states. Defaults to ``0ms``.

   -  **high** (**Required**, :ref:`config-time`): time delay to keep the high value before changing the binary state.
   -  **low** (**Required**, :ref:`config-time`): time delay to keep the low value before changing the binary state.

-  All other options from :ref:`Binary Sensor <config-binary_sensor>`.



See Also
--------

- :doc:`/components/binary_sensor/index`
- :doc:`/components/sensor/index`
- :ref:`automation`
- :apiref:`analog_trheshold/analog_threshold_binary_sensor.h`
- :ghedit:`Edit`
