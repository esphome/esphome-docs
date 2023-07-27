Statistics
==========

.. seo::
    :description: Instructions for setting up a Statistics Sensor

The ``statistics`` sensor platform quickly generates summary statistics from another sensor’s measurements. See :ref:`statistics-description` for information about the available summary statistics.

The component calculates statistics over a sliding window or a resettable continuous window. See :ref:`window-types` for details about each possible type.

Each summary statistic sensor is optional, and the component stores the measurement information only necessary for the enabled sensors. The component uses external memory on ESP32 boards if available. See :ref:`external_memory` for details.

You could also use :ref:`sensor-filters` to compute some of the available summary statistics over a sliding window. In contrast, this component allows you to generate multiple summary statistics from the same source sensor. Additionally, it calculates them more efficiently than sensors filters.

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
        average_type: time_weighted
        group_type: sample
        count:
          name: "Count of Valid Sensor Measurements"         
        duration:
          name: "Sample Duration"
        max:
          name: "Sensor Maximum"   
        min:
          name: "Sensor Minimum"
        mean:
          name: "Sensor Average"
        since_argmax:
          name: "Time Since Last Maximum of Sensor"
        since_argmin:
          name: "Time Since Last Minimum of Sensor"          
        std_dev: 
          name: "Sensor Sample Standard Deviation"
        trend:
          name: "Sensor Trend"          

      # Use any other sensor component to gather statistics for
      - platform: ...
        id: source_measurement_sensor_id

Configuration variables:
------------------------

- **type** (**Required**, enum): One of ``sliding``, ``chunked_sliding``, ``continuous``, or ``chunked_continuous``.
- **average_type** (*Optional*, enum): How each measurement is weighted, one of ``simple`` or ``time_weighted``. Defaults to ``simple``.
- **group_type** (*Optional*, enum): The type of the set of sensor measurements, one of ``sample`` or ``population``. Defaults to ``sample``.
- **time_unit** (*Optional*, enum): The time unit used for the trend sensor, one of
  ``ms``, ``s``, ``min``, ``h`` or ``d``. Defaults to ``s``.

- **count** (*Optional*): The information for the count sensor.

  - **name** (**Required**, string): The name for the count sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.  

- **duration** (*Optional*): The information for the duration sensor.

  - **name** (**Required**, string): The name for the duration sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.    

- **max** (*Optional*): The information for the maximum sensor.

  - **name** (**Required**, string): The name for the maximum sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **mean** (*Optional*): The information for the mean (average) sensor.

  - **name** (**Required**, string): The name for the mean sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **min** (*Optional*): The information for the minimum sensor.

  - **name** (**Required**, string): The name for the minimum sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **since_argmax** (*Optional*): The information for the since argmax sensor.

  - **name** (**Required**, string): The name for the since argmax sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.  

- **since_argmin** (*Optional*): The information for the since argmin sensor.

  - **name** (**Required**, string): The name for the since argmin sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.  

- **std_dev** (*Optional*): The information for the standard deviation sensor.

  - **name** (**Required**, string): The name for the standard deviation sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **trend** (*Optional*): The information for the trend sensor.

  - **name** (**Required**, string): The name for the trend sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.


``sliding`` window type options:
********************************

- **window_size** (**Required**, int): The number of *measurements* over which to calculate the summary statistics when pushing out a
  value.
- **send_every** (*Optional*, int): How often the sensor statistics should be pushed out. For example, if set to 15, then the statistic sensors will publish updates every 15 *measurements*. Defaults to ``1``.
- **send_first_at** (*Optional*, int): By default, the first *measurement's* statistics on boot is immediately
  published. With this parameter you can specify how many *measurements* should be collected before the first statistics are sent.
  Must be less than or equal to ``send_every``
  Defaults to ``1``.

``chunked_sliding`` window type options:
****************************************

- **window_size** (**Required**, int): The number of *chunks* over which to calculate the summary statistics when pushing out a value.
- **chunk_size** (*Optional*, int): The number of *measurements* to be stored in a chunk before inserting into the window. Note that exactly one of ``chunk_size`` or ``chunk_duration`` must be present.
- **chunk_duration** (*Optional*, :ref:`config-time`): The duration of *measurements* to be stored in a chunk before inserting into the window. Note that exactly one of ``chunk_size`` or ``chunk_duration`` must be present.
- **send_every** (*Optional*, int): How often the sensor statistics should be pushed out. For example, if set to 15, then the statistic sensors will publish updates every 15 *chunks*. Defaults to ``1``.
- **send_first_at** (*Optional*, int): By default, the first *chunk's* statistics on boot is immediately
  published. With this parameter you can specify how many *chunks* should be collected before the first statistics are sent.
  Must be less than or equal to ``send_every``
  Defaults to ``1``.


``continuous`` window type options:
***********************************

- **window_size** (*Optional*, int): The number of *measurements* after which all statistics are reset. Set to ``0`` to disable automatic resets. Note that at least one of ``window_duration`` and ``window_size`` must be configured. If both are configured, whichever causes a reset first will do so.
- **window_duration** (*Optional*, :ref:`config-time`): Time duration after which all statistics are reset. Note that at least one of ``window_duration`` and ``window_size`` must be configured. If both are configured, whichever causes a reset first will do so.
- **send_every** (*Optional*, int): How often the sensor statistics should be pushed out. For example, if set to 15, then the statistic sensors will publish updates every 15 *measurements*. Set to ``0`` to disable automatic sensor publication. Defaults to ``1``.
- **send_first_at** (*Optional*, int): By default, the first *measurement's* statistics on boot is immediately
  published. With this parameter you can specify how many *measurements* should be collected before the first statistics are sent.
  Must be less than or equal to ``send_every``.
  Defaults to ``1``.

``chunked_continuous`` window type options:
*******************************************

- **window_size** (*Optional*, int): The number of *chunks* after which all statistics are reset. Set to ``0`` to disable automatic resets. Note that at least one of ``window_duration`` and ``window_size`` must be configured. If both are configured, whichever causes a reset first will do so.
- **window_duration** (*Optional*, :ref:`config-time`): Time duration after which all statistics are reset. Note that at least one of ``window_duration`` and ``window_size`` must be configured. If both are configured, whichever causes a reset first will do so.
- **chunk_size** (*Optional*, int): The number of *measurements* to be stored in a chunk before inserting into the window. Note that exactly one of ``chunk_size`` or ``chunk_duration`` must be present.
- **chunk_duration** (*Optional*, :ref:`config-time`): The duration of *measurements* to be stored in a chunk before inserting into the window. Note that exactly one of ``chunk_size`` or ``chunk_duration`` must be present.
- **send_every** (*Optional*, int): How often the sensor statistics should be pushed out. For example, if set to 15, then the statistic sensors will publish updates every 15 *chunks*. Set to ``0`` to disable automatic sensor publication. Defaults to ``1``.
- **send_first_at** (*Optional*, int): By default, the first *chunk's* statistics on boot is immediately
  published. With this parameter you can specify how many *chunks* should be collected before the first statistics are sent.
  Must be less than or equal to ``send_every``.
  Defaults to ``1``.
- **restore** (*Optional*, boolean): Whether to store the intermediate statistics on the device so that they can be restored upon power cycle or reboot. Warning: this option can wear out your flash. Defaults to ``false``.

.. _window-types:

Window Types
------------

There are two categories of windows. The first category is a sliding window. A sliding window has a pre-defined capacity of ``window_size`` measurements. The component inserts sensor measurements until it has inserted ``window_size`` total. Before this component inserts another sensor measurement, it removes the oldest measurement in the window.

The second category is a continuous window. This category of windows has a pre-defined capacity of ``window_size`` measurements or a pre-defined duration ``window_duration``. The component inserts sensor measurements until it inserts ``window_size`` total or the difference between the timestamps of the oldest and most recent sensor measurements exceeds ``window_duration``. Then, this component removes **all** of the sensor measurements in the window.

Instead of inserting individual measurements, the component can combine several sensor measurements into a chunk. When this chunk exceeds ``chunk_size`` sensor measurements or ``chunk_size`` duration, this component adds that chunk to the window. This approach saves memory for sliding windows, as memory does not hold every individual sensor measurement but only stores several sensor measurements combined. For continuous windows, this improves accuracy for significantly large windows.

If you want to collect statistics from a significant number of measurements (potentially unlimited), use a ``chunked_continuous`` type. It uses slightly more memory and is slower but is numerically accurate. A ``continuous`` type uses very little memory and is extremely fast. However, it can lose accuracy with significantly large windows.

.. list-table:: Sliding Window Type Comparison
    :header-rows: 1 

    * - 
      - ``sliding``
      - ``chunked_sliding``
    * - Capacity set by count
      - yes
      - yes
    * - Capacity set by duration
      - no
      - indirectly
    * - Memory usage
      - low to high (depends on window size)
      - low (if chunk size is large) to medium (if chunk size is small)
    * - CPU usage
      - very low
      - very low
    * - Accurate Long-Term
      - yes
      - yes



.. list-table:: Continuous Window Type Comparison
    :header-rows: 1

    * -
      - ``continuous``
      - ``chunked_continuous``
    * - Capacity set by count
      - yes
      - yes
    * - Capacity set by duration
      - yes
      - yes
    * - Memory usage
      - very low
      - very low to low (depends on window size)
    * - CPU usage
      - very low
      - low
    * - Accurate Long-Term
      - potentially no (for large window sizes)
      - yes


.. _statistics-description:

Statistics Description
----------------------

- ``count`` sensor:

  - Counts the number of sensor measurements in the window that are not ``NaN``.
  - By default, its ``state_class`` is ``total``.
  - By default, it inherits ``entity_category`` and ``icon`` from the source sensor.     

- ``duration`` sensor:

  - Gives the sum of the durations between each measurements' timestamps in the window.
  - By default, its ``state_class`` is ``measurement``, and its ``device_class`` is ``duration``.
  - By default, it inherits ``entity_category`` and ``icon`` from the source sensor.     
  - The ``unit_of_measurement`` is millseconds (ms).

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

- ``since_argmax`` sensor:

  - The timespan since the most recent maximum value in the window.
  - By default, its ``state_class`` is ``measurement``, and its ``device_class`` is ``duration``.
  - By default, it inherits ``entity_category`` and ``icon`` from the source sensor.  
  - The ``unit_of_measurement`` is millseconds (ms).

- ``since_argmin`` sensor:

  - The timespan since the most recent minimum value in the window.
  - By default, its ``state_class`` is ``measurement``, and its ``device_class`` is ``duration``.
  - By default, it inherits ``entity_category`` and ``icon`` from the source sensor.    
  - The ``unit_of_measurement`` is millseconds (ms).

- ``std_dev`` sensor:

  - The standard deviation of measurements from the source sensor in the window.
  - If ``group_type`` is ``sample``, and ``average_type`` is ``simple``, then it uses Bessel's correction to give an unbiased estimator.
  - If ``group_type`` is ``sample``, and ``average_type`` is ``time_weighted``, then it uses reliability weights to give an unbiased estimator.  
  - By default, its ``state_class`` is ``measurement``.  
  - By default, it inherits ``device_class``, ``entity_category``, ``icon``, and ``unit_of_measurement`` from the source sensor.
  - By default, it uses 2 more ``accuracy_decimals`` than the source sensor.

- ``trend`` sensor:

  - Gives the slope of the line of best fit for the source sensor measurements in the window versus their timestamps.
  - By default, its ``state_class`` is ``measurement``.  
  - By default, it inherits ``entity_category`` and ``icon`` from the source sensor.
  - By default, it uses 2 more ``accuracy_decimals`` than the source sensor.
  - The ``unit_of_measurement`` is the source sensor's unit divided by the configured ``time_unit``. For example, if the source sensor is in ``Pa`` and ``time_unit`` is in seconds, the unit is ``Pa/s``.
  
General Advice
--------------

Average Types
*************

You can configure the average type to equally weigh each sensor measurement using ``simple`` or weigh each measurement by its duration using ``time_weighted``. If your sensor updates have a consistent update interval, then ``simple`` should work well. If your sensor is not updated consistently, then choose the ``time_weighted`` type. Note that with the ``time_weighted`` type, the component does not insert a sensor measurement into the window until it receives another sensor measurement; i.e., there is a delay of one measurement. This delay is necessary to determine each measurement’s duration.


.. _external_memory:

External Memory
***************

If you use an ESP32 board with external memory, then this component will automatically store sensor measurements in the external memory. Just add ``psram:`` to your configuration.

.. code-block:: yaml

    # Example external memory configuration
    psram:

    sensor:
      - platform: statistics
      ...

Group Types
***********

You can configure whether the component considers the set of sensor measurements to be a population or a sample using the ``population`` or ``sample`` type respectively. This setting affects the standard deviation ``std_dev`` sensor. For sliding windows or continuous windows that reset the ``sample`` type is appropriate. If you use a ``chunked_continuous`` window type without automatic reset, you should most likely use the ``population`` type.

Trend Sensor
************

The trend sensor may be unstable over a small set of sensor measurements, especially if the sensor is noisy. To avoid this, use a trend sensor on large windows; e.g., 50 or more sensor measurements. Or, apply a smoothing filter like an exponential moving average to the source sensor.

Which Continuous Window Type to Choose
**************************************

If you collect long-term statistics that include thousands (or more) of measurements, you should use the ``chunked_continuous`` window type. If you only collect statistics over a smaller set of measurements, then use the ``continuous`` window type.

Which Sliding Window Type to Choose
***********************************

Unless you need your statistics to update after every sensor measurement or you need to set the ``send_every`` option to a number that does not divide ``window_size``, you should use the ``chunked_sliding`` window type.


Example Configurations
----------------------

One Minute Window Published Every Minute
****************************************

Suppose you want to send the mean/average of a sensor’s measurements over the last minute updated once every minute.

.. code-block:: yaml

    # One minute average sent every minute
    sensor:
      - platform: statistics
        source_id: source_measurement_sensor_id
        window:
          type: continuous
          window_duration: 1min
          send_every: 1
        mean:
          name: "Sensor Mean (1 minute)"  

One Hour Window Published Every Minute
**************************************

Suppose you want to send the minimum and maximum value of a sensor’s measurements over the last hour, updated once per minute.

.. code-block:: yaml

    # Min and max in the last hour sent every minute
    sensor:
      - platform: statistics
        source_id: source_measurement_sensor_id
        window:
          type: chunked_sliding
          window_size: 60         # 60 chunks that are 1 minute each is 1 hour
          chunk_duration: 1min
          send_every: 1
        min:
          name: "Sensor Min (1 hour)"  
        max:
          name: "Sensor Max (1 hour)"

All-Time Window Published Every 15 minutes
******************************************

Suppose you want to send the mean/average of a sensor's measurements for all time, with updates every 15 minutes.

.. code-block:: yaml

    # All time mean
    sensor:
      - platform: statistics
        source_id: source_measurement_sensor_id
        window:
          type: chunked_continuous
          window_size: 0          # disables automatic resets
          chunk_duration: 15min
          send_every: 1
          restore: true           # periodically saves statistics to flash to recover on power loss or reboot
        mean:
          name: "Sensor Mean (all time)"

    preferences:
      flash_write_interval: 1h    # writes statistics to flash every hour to avoid unnecessary writes      

Day so Far Window Published Every 15 Minutes
********************************************

Suppose you want to send the mean temperature measurement so far in a day, with updates every 15 minutes.

.. code-block:: yaml

    # Mean Sensor
    sensor:
      - platform: statistics
        source_id: temperature_sensor
        id: daily_temperature_stats
        window:
          type: chunked_continuous
          window_size: 0        # we will manually reset the window
          chunk_duration: 15min
        mean:
          name: "Temperature Mean (Day so Far)"

    time:
      - platform: homeassistant
        id: homeassistant_time
        on_time:
          # force publish 1 second before midnight so we do not miss the last chunk
          - seconds: 59
            minutes: 59
            hours: 23
            then:
              - sensor.statistics.force_publish: daily_temperature_stats
          # reset window at midnight
          - seconds: 0
            minutes: 0
            hours: 0
            then:
              - sensor.statistics.reset: daily_temperature_stats

Automation Actions
------------------

``sensor.statistics.force_publish`` Action
******************************************

This :ref:`Action <config-action>` allows you to force all statistics sensors to publish an update. Note, the action may send statistics over a window larger than configured for ``chunked_sliding`` types.

.. code-block:: yaml

    on_...:
      - sensor.statistics.force_publish:  my_statistics_component  

``sensor.statistics.reset`` Action
**********************************

This :ref:`Action <config-action>` allows you to reset all the statistics by clearing all stored measurements in the window. 
For example, you could use a time-based automation to reset all the statistics sensors at midnight.

.. code-block:: yaml

    on_...:
      - sensor.statistics.reset:  my_statistics_component  

See Also
--------

- :ref:`sensor-filters`
- `DABA Lite algorithm (IBM's sliding window aggregators) <https://github.com/IBM/sliding-window-aggregators/blob/master/cpp/src/DABALite.hpp>`__
- `Linear Trend Estimation (Wikipedia) <https://en.wikipedia.org/wiki/Linear_trend_estimation>`__
- `Bessel's Correction (Wikipedia) <https://en.wikipedia.org/wiki/Bessel%27s_correction>`__
- `Reliability Weights (Wikipedia) <http://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Weighted_sample_variance>`__
- :apiref:`statistics/statistics.h`
- :ghedit:`Edit`
