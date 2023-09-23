Statistics
==========

.. seo::
    :description: Instructions for setting up a Statistics Sensor

The ``statistics`` sensor platform quickly generates summary statistics from another sensor’s measurements. See :ref:`statistics-descriptions` for information about the available summary statistics.

The component calculates statistics over a sliding window or a resettable continuous window. See :ref:`statistics-window_types` for details about each possible type.

Each summary statistic sensor is optional, and the component stores the measurement information only necessary for the enabled sensors. The component uses external memory on ESP32 boards if available.

As an alternative to this component, you could use :ref:`sensor-filters` to compute some of the available summary statistics over a sliding window. In contrast, this component allows you to generate multiple summary statistics from the same source sensor. Additionally, it calculates them more efficiently than sensors filters.

To use the component, first, provide the source sensor and then configure the window settings and the desired statistics.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: statistics
        source_id: source_measurement_sensor_id
        window:
          type: sliding
          window_size: 15
          send_every: 5
          send_first_at: 3
        statistics:
          - type: count
            name: "Count of Valid Sensor Measurements"         
          - type: duration
            name: "Sample Duration"
          - type: max
            name: "Sensor Maximum"   
          - type: min
            name: "Sensor Minimum"
          - type: mean
            name: "Sensor Average"
          - type: quadrature
            name: "Sensor Quadrature"
          - type: since_argmax
            name: "Time Since Last Maximum of Sensor"
          - type: since_argmin
            name: "Time Since Last Minimum of Sensor"          
          - type: std_dev
            name: "Sensor Sample Standard Deviation"
          - type: trend
            name: "Sensor Trend"          

      # Use any other sensor component to gather statistics for
      - platform: ...
        id: source_measurement_sensor_id

Configuration Variables
-----------------------

- **window** (**Required**, Window Schema): The configuration for the window of sensor measurements.

    - **type** (**Required**, enum): One of ``sliding``, ``continuous``, or ``continuous_long_term``.
    - All other options from :ref:`statistics-sliding_options` or :ref:`statistics-continuous_options`.

- **weight_type** (*Optional*, enum): How each measurement is weighted, one of ``simple`` or ``duration``. Defaults to ``simple``.
- **group_type** (*Optional*, enum): The type of the set of sensor measurements, one of ``sample`` or ``population``. Defaults to ``sample``.


- **statistics** (*Optional*, list): A list of the statistic sensors.

    - **type** (**Required**, enum): One of ``count``, ``duration``, ``max``, ``mean``, ``min``, ``quadrature``, ``since_argmax``, ``since_argmin``, ``std_dev``, or ``trend``.
    - **time_unit** (*Optional* - only for ``duration``, ``quadrature``, ``since argmax``, ``since argmin``, and ``trend`` types, enum): The time unit used for the statistics calculation, one of
      ``ms``, ``s``, ``min``, ``h`` or ``d``. Defaults to ``s``.
    - All options from :ref:`Sensor <config-sensor>`.  

- **on_update** (*Optional*, :ref:`Automation <automation>`): List of actions to be performed after all sensors have updated. See :ref:`statistics-on_update_trigger`.

.. _statistics-sliding_options:

``sliding`` window type options
*******************************

- **window_size** (**Required**, int): The number of *chunks* over which to calculate the summary statistics when pushing out a value.
- **chunk_size** (*Optional*, int): The number of *measurements* to be stored in a chunk before inserting into the window. Note that only one of ``chunk_size`` and ``chunk_duration`` may be configured. If neither are configured, ``chunk_size`` defaults to ``1``.
- **chunk_duration** (*Optional*, :ref:`config-time`): The duration of *measurements* to be stored in a chunk before inserting into the window. Note, only one of ``chunk_size`` and ``chunk_duration`` may be configured. If neither are configured, ``chunk_size`` defaults to ``1``.
- **send_every** (*Optional*, int): How often the sensor statistics should be pushed out. For example, if set to 15, then the statistic sensors will publish updates every 15 *chunks*. Defaults to ``1``.
- **send_first_at** (*Optional*, int): By default, the first *chunk's* statistics on boot is immediately
  published. With this parameter you can specify how many *chunks* should be collected before the first statistics are sent.
  Must be less than or equal to ``send_every``
  Defaults to ``1``.

.. _statistics-continuous_options:

``continuous`` and ``continuous_long_term`` window type options
***************************************************************

- **window_size** (**Required**, int): The number of *chunks* after which all statistics are reset. Set to ``0`` to disable automatic resets.
- **chunk_size** (*Optional*, int): The number of *measurements* to be stored in a chunk before inserting into the window. Note that only one of ``chunk_size`` and ``chunk_duration`` may be configured. If neither are configured, ``chunk_size`` defaults to ``1``.
- **chunk_duration** (*Optional*, :ref:`config-time`): The duration of *measurements* to be stored in a chunk before inserting into the window. Note that only one of ``chunk_size`` and ``chunk_duration`` may be configured. If neither are configured, ``chunk_size`` defaults to ``1``.
- **send_every** (*Optional*, int): How often the sensor statistics should be pushed out. For example, if set to 15, then the statistic sensors will publish updates every 15 *chunks*. Set to ``0`` to disable automatic sensor publication. Defaults to ``1``.
- **send_first_at** (*Optional*, int): By default, the first *chunk's* statistics on boot is immediately
  published. With this parameter you can specify how many *chunks* should be collected before the first statistics are sent.
  Must be less than or equal to ``send_every``.
  Defaults to ``1``.
- **restore** (*Optional*, boolean): Whether to store the intermediate statistics on the device so that they can be restored upon power cycle or reboot. Cannot be enabled if the ``trend`` sensor is configured. Warning: this option can wear out your flash. Defaults to ``false``.

Detailed Descriptions
---------------------

Weight Types
*************

You can configure the weight type to equally weigh each sensor measurement using ``simple`` or weigh each measurement by its duration using ``duration``. If your sensor updates have a consistent update interval, then ``simple`` should work well. If your sensor is not updated consistently, then choose the ``duration`` type. Note that with the ``duration`` type, the component does not insert a sensor measurement into the window until it receives another sensor measurement; i.e., there is a delay of one measurement. This delay is necessary to determine each measurement’s duration.

Group Types
***********

You can configure whether the component considers the set of sensor measurements to be a population or a sample using the ``population`` or ``sample`` type respectively. This setting affects the standard deviation ``std_dev`` sensor. For sliding windows or continuous windows that reset the ``sample`` type is usually appropriate. If you use a ``continuous`` or ``continuous_long_term`` window type without automatic reset, you should most likely use the ``population`` type.

.. _statistics-descriptions:

Statistic Sensors
*****************

- ``count`` sensor:

  - Counts the number of sensor measurements in the window that are not ``NaN``.
  - By default, its ``state_class`` is ``total_increasing``.
  - By default, it inherits ``entity_category`` from the source sensor.     

- ``duration`` sensor:

  - Gives the sum of the durations between each measurements' timestamps in the window.
  - By default, its ``state_class`` is ``measurement``, and its ``device_class`` is ``duration``.
  - By default, it inherits ``entity_category`` from the source sensor.     
  - The ``unit_of_measurement`` is the configured ``time_unit``.

- ``max`` sensor:

  - The maximum value of measurements from the source sensor in the window.
  - By default, its ``state_class`` is ``measurement``.  
  - By default, it inherits ``accuracy_decimals``, ``device_class``, ``entity_category``, ``icon``, and ``unit_of_measurement`` from the source sensor.

- ``mean`` sensor:

  - The mean/average value of measurements from the source sensor in the window.
  - By default, its ``state_class`` is ``measurement``.  
  - By default, it inherits ``accuracy_decimals``, ``device_class``, ``entity_category``, ``icon``, and ``unit_of_measurement`` from the source sensor.

- ``min`` sensor:

  - The minimum value of measurements from the source sensor in the window.
  - By default, its ``state_class`` is ``measurement``.  
  - By default, it inherits ``accuracy_decimals``, ``device_class``, ``entity_category``, ``icon``, and ``unit_of_measurement`` from the source sensor.

- ``quadrature`` sensor type:
  
  - The area under the values of the measurements from the source sensor in the window.
  - By default, its ``state_class`` is ``total``.
  - By default, it inherits ``entity_category`` from the source sensor.
  - By default, it uses 2 more ``accuracy_decimals`` than the source sensor.
  - The ``unit_of_measurement`` is the source sensor's unit multiplied by the configured ``time_unit``. For example, if the source sensor is in ``W`` and ``time_unit`` is in hours, the unit is ``Wh``.

- ``since_argmax`` sensor:

  - The timespan since the most recent maximum value in the window.
  - By default, its ``state_class`` is ``measurement``, and its ``device_class`` is ``duration``.
  - By default, it inherits ``entity_category`` from the source sensor.  
  - The ``unit_of_measurement`` is the configured ``time_unit``.

- ``since_argmin`` sensor:

  - The timespan since the most recent minimum value in the window.
  - By default, its ``state_class`` is ``measurement``, and its ``device_class`` is ``duration``.
  - By default, it inherits ``entity_category`` from the source sensor.    
  - The ``unit_of_measurement`` is the configured ``time_unit``.

- ``std_dev`` sensor:

  - The standard deviation of measurements from the source sensor in the window.
  - If ``group_type`` is ``sample``, and ``weight_type`` is ``simple``, then it uses Bessel's correction to give an unbiased estimator.
  - If ``group_type`` is ``sample``, and ``weight_type`` is ``duration``, then it uses reliability weights to give an unbiased estimator.  
  - By default, its ``state_class`` is ``measurement``.  
  - By default, it inherits ``device_class``, ``entity_category``, ``icon``, and ``unit_of_measurement`` from the source sensor.
  - By default, it uses 2 more ``accuracy_decimals`` than the source sensor.

- ``trend`` sensor:

  - Gives the slope of the line of best fit for the source sensor measurements in the window versus their timestamps.
  - Cannot be enabled if the ``window`` configuration option ``restore`` is set to true.
  - By default, its ``state_class`` is ``measurement``.  
  - By default, it inherits ``entity_category`` from the source sensor.
  - By default, it uses 2 more ``accuracy_decimals`` than the source sensor.
  - The ``unit_of_measurement`` is the source sensor's unit divided by the configured ``time_unit``. For example, if the source sensor is in ``Pa`` and ``time_unit`` is in seconds, the unit is ``Pa/s``.

.. note::

    The trend sensor may be unstable over a small set of sensor measurements, especially if the sensor is noisy. To avoid this, use a trend sensor on large windows; e.g., 50 or more sensor measurements. Or, apply a smoothing filter like an exponential moving average to the source sensor.
  
.. _statistics-window_types:

Window Types
************

There are two categories of windows. The first category is a sliding window. A sliding window has a pre-defined capacity of ``window_size`` measurements. The component inserts sensor measurements until it has inserted ``window_size`` total. When full, this component removes the oldest measurement in the window and then inserts the newwest senesor measurement.

The second category is a continuous window. This category of windows has a pre-defined capacity of ``window_size`` measurements. The component inserts sensor measurements until it inserts ``window_size`` total. Then, this component removes **all** of the sensor measurements in the window. If ``window_size`` is set to ``0``, then the window is **never** reset.

Instead of inserting individual measurements, the component can first combine several sensor measurements into a chunk. When this chunk exceeds ``chunk_size`` sensor measurements or ``chunk_duration`` time has passed, this component adds that chunk to the window. This approach saves memory for sliding windows, as memory does not hold every individual sensor measurement but only stores several sensor measurements combined into the chunk. For continuous windows, this improves accuracy for significantly large windows.

If you want to collect statistics from a significant number of measurements (potentially unlimited), use a ``continuous_long_term`` type. It uses slightly more memory and is slightly slower but is numerically more accurate than a ``continuous`` type. A ``continuous`` type uses very little memory and is extremely fast. However, it may lose accuracy with significantly large windows. A rough rule of thumb is to use ``continuous_long_term`` if you are collecting data that include more than several thousand measurements.

Example Window Configurations
-----------------------------

One Minute Window Published Every Minute
****************************************

Suppose you want statistics over the last minute updated once every minute.

.. code-block:: yaml

    # Statistics over last minute sent every minute
    sensor:
      - platform: statistics
        window:
          type: continuous
          window_size: 1          # resets window after 1 chunk of 1 minute duration
          chunk_duration: 1min
          send_every: 1
        # ...

One Hour Window Published Every Minute
**************************************

Suppose you want statistics over the last hour, updated once per minute.

.. code-block:: yaml

    # Statistics over last hour sent every minute
    sensor:
      - platform: statistics
        window:
          type: sliding
          window_size: 60         # 60 chunks that are 1 minute each is 1 hour
          chunk_duration: 1min
          send_every: 1
        # ...

All-Time Window Published Every 15 minutes
******************************************

Suppose you want statistics for all time, with updates every 15 minutes.

.. code-block:: yaml

    # All time statistics
    sensor:
      - platform: statistics
        window:
          type: continuous_long_term
          window_size: 0          # disables automatic resets
          chunk_duration: 15min
          send_every: 1
          restore: true           # periodically saves statistics to flash to recover on power loss or reboot
        # ...

    preferences:
      flash_write_interval: 1h    # writes statistics to flash every hour to avoid unnecessary writes      

Day so Far Window Published Every 15 Minutes
********************************************

Suppose you want statistics so far in a day, with updates every 15 minutes.

.. code-block:: yaml

    # Statistics over day so far
    sensor:
      - platform: statistics
        window:
          type: continuous_long_term
          window_size: 0        # we will manually reset the window
          chunk_duration: 15min
          send_every: 1
        # ...

    time:
      - platform: homeassistant
        id: homeassistant_time
        on_time:
          # Force publish 1 second before midnight so we do not miss the last chunk
          - seconds: 59
            minutes: 59
            hours: 23
            then:
              - sensor.statistics.force_publish: daily_temperature_stats
          # Reset window at midnight
          - seconds: 0
            minutes: 0
            hours: 0
            then:
              - sensor.statistics.reset: daily_temperature_stats

Statistics Automation
---------------------

.. _statistics-force_publish_action:

``sensor.statistics.force_publish`` Action
******************************************

This :ref:`Action <config-action>` allows you to force all statistics sensors to publish an update. Note the action may send statistics over a different window size than configured for ``sliding`` types.

.. code-block:: yaml

    on_...:
      - sensor.statistics.force_publish: my_statistics_component  

.. _statistics-reset_action:

``sensor.statistics.reset`` Action
**********************************

This :ref:`Action <config-action>` allows you to reset all the statistics by clearing all stored measurements in the window. 
For example, you could use time-based automations to reset all the statistics sensors at midnight.

.. code-block:: yaml

    on_...:
      - sensor.statistics.reset: my_statistics_component  

.. _statistics-on_update_trigger:

``sensor.statistics.on_update`` Trigger
***************************************

This automation triggers after all the configured sensors update.  In :ref:`Lambdas <config-lambda>`, you can get the ``Aggregate`` object containing all the statistics (for the configured sensors only) from the trigger with ``x``. See :ref:`statistics-lambdas_calls` for available functions.

.. code-block:: yaml

    sensor:
      - platform: statistics
        # ...
        on_update:
          then:
            - logger.log: "Statistics sensors have all updated"


.. _statistics-lambdas_calls:

Lambdas Calls for ``Aggregate`` Objects
***************************************

The ``on_update`` trigger provides the variable ``x``, which stores the :apiref:`Aggregate Object <statistics/aggregate.h>` that contains the current statistics available based on the configured sensors. This object has many functions that access the underlying data in their native data types, which may be helpful to compute other statistics not currently available as a sensor. If you are using the ``continuous`` window type, all functions return valid statistics. For other window types, be sure to configure the required sensors noted for each function that you want to use.

  - ``compute_covariance()``: Compute the covariance of the set of measurements with respect to timestamps. It applies Bessel's correction or implements reliability weights if the group type is a sample.
  
    - returns the covariance as a ``double`` type
    - valid if ``trend`` sensor is configured

  - ``compute_quadrature()``: Compute the area under the curve of the measurements.

    - returns the area under the curve as a ``double`` type, with units of the source sensor times milliseconds
    - valid if ``mean`` and ``duration`` sensors are configured

  - ``compute_std_dev()``: Compute the standard deviation of the set of measurements. Applies Bessel's correction or implements reliability weights if the group type is a sample.

    - returns the standard deviation as a ``double`` type
    - valid if ``std_dev`` or ``trend`` sensor is configured

  - ``compute_trend()``: Compute the slope of the line of best fit.
    - returns the trend as a ``double`` type
    - valid if ``trend`` sensor is configured

  - ``compute_variance()``: Compute the variance of the set of measurements. Applies Bessel's correction or implements reliability weights if the group type is a sample.

    - returns the variance as a ``double`` type
    - valid if ``std_dev`` or ``trend`` sensor is configured

  - ``get_argmax()``: The UTC Unix time of the most recent maximum value in the set of measurements.

    - returns the UTC Unix time as a ``time_t`` type
    - valid if ``argmax`` sensor is configured

  - ``get_argmin()``: The UTC Unix time of the most recent minimum value in the set of measurements.

    - returns the UTC Unix time as a ``time_t`` type
    - valid if ``argmax`` sensor is configured

  - ``get_c2()``: From Welford's algorithm, it is used for computing covariance of the measurements and timestamps.

    - returns the value as a ``double`` type
    - valid if ``trend`` sensor is configured

  - ``get_count()``: The count of the number of measurements stored in the window.

    - returns the count as a ``size_t`` type
    - always valid

  - ``get_duration()``: The duration of measurements in the Aggregate in milliseconds.

    - returns the milliseconds as a ``uint64_t`` type
    - valid if ``duration`` sensor is configured or if the ``weight_type`` is ``duration``

  - ``get_duration_squared()``: The sum of squared durations of measurements in the Aggregate in milliseconds squared.

    - returns the milliseconds squared as a ``uint64_t`` type
    - valid if the ``weight_type`` is ``duration``

  - ``get_m2()``: From Welford's algorithm, it is used for computing variance of the measurements.

    - returns the value as a ``double`` type
    - valid if ``std_dev`` or ``trend`` sensor is configured

  - ``get_max()``: The maximum of the set of measurements.

    - returns the maximum as a ``float`` type
    - valid if ``since_argmax`` or ``max`` sensor is configured


  - ``get_mean()``: The mean of the set of measurements.

    - returns the mean as a ``double`` type
    - valid if ``mean``, ``std_dev``, or ``trend`` sensor is configured

  - ``get_min()``: The minimum of the set of measurements.

    - returns the minimum as a ``float`` type
    - valid if ``since_argmin`` or ``min`` sensor is configured

  - ``get_timestamp_m2()``: From Welford's algorithm, it is used for computing variance of the timestamps.

    - returns the value as a ``double`` type
    - valid if ``trend`` sensor is configured

  - ``get_timestamp_mean()``: The mean of the timestamps in millseconds. Note that this is normalized to ``timestamp_reference``.

    - returns the timestamp mean as a ``double`` type
    - valid if ``trend`` sensor is configured    

  - ``get_timestamp_reference()``: The reference timestamp (in millseconds) that the ``timestamp_mean`` is normalized with.

    - returns the timestamp reference as a ``uint32_t`` type
    - valid if ``trend`` sensor is configured

These raw statistics values are more accurate when you use their native data type. For example, the ``since_argmax`` and ``since_argmin`` sensors give the time since the most recent maximum or minimum value. The component actually stores the Unix UTC time (in seconds) of when the most recent extreme value occurred. Since these native integer values are so large, the float data type used for ESPHome and Home Assistant sensor values is only accurate within 1 or 2 minutes of the actual value as a result of floating point precision issues, despite this component natively storing the value accurately to the second.

Coeffecient of Determination
""""""""""""""""""""""""""""

Another use case is to compute statistics unavailable as a sensor. In this example, we calculate the linear coefficient of determination (r²) of the set of measurements and timestamps. The value of r² gives the strength of a linear relationship between two variables.

.. code-block:: yaml

    sensor:
      - platform: statistics
        source_id: source_measurement_sensor_id
        window:
          type: sliding
          window_size: 4          # 4 chunks of duration 15 seconds for a sliding window over 1 minute
          chunk_duration: 15s
          send_every: 1
        statistics: 
          - type: trend           # guarantees the covariance and variance statistics are tracked
            id: sensor_1_min_trend
        on_update:
          then:
            - lambda: |-
                double c2 = x.get_c2();   // c2/count gives covariance
                double m2 = x.get_m2();   // m2/count gives variance
                double timestamp_m2 = x.get_timestamp_m2();   // timestamp_m2/count gives variance of the timestamps

                // The linear coeffecient of determination is given by covariance^2/(variance*timestamp_variance)
                // The counts in covarance, variance, and timestamp_variance would all cancel, so we get
                double r_squared = (c2*c2)/(m2*timestamp_m2);

                // Update a template sensor with r_squared
                id(sensor_1min_r_squared).publish_state(r_squared);

      - platform: template
        name: "Sensor 1 Minute Linear Coeffecient of Determination"
        id: sensor_1min_r_squared
        update_interval: never    # the statistics component will update

See Also
--------

- :ref:`sensor-filters`
- `DABA Lite algorithm (IBM's sliding window aggregators) <https://github.com/IBM/sliding-window-aggregators/blob/master/cpp/src/DABALite.hpp>`__
- `Linear Trend Estimation (Wikipedia) <https://en.wikipedia.org/wiki/Linear_trend_estimation>`__
- `Bessel's Correction (Wikipedia) <https://en.wikipedia.org/wiki/Bessel%27s_correction>`__
- `Reliability Weights (Wikipedia) <http://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Weighted_sample_variance>`__
- `Coeffecient of Determination (Wikipedia) <https://en.wikipedia.org/wiki/Coefficient_of_determination>`__
- :apiref:`Aggregate API Reference <statistics/aggregate.h>`
- :apiref:`Statistics API Reference <statistics/statistics.h>`
- :ghedit:`Edit`
