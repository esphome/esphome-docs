Kalman filter-based sensor fusion
=================================

.. seo::
    :description: Instructions for setting up a kalman_combinator sensor

The ``kalman_combinator`` sensor platform allows you to filter one or several
sensors into one with a reduced error. If using a single sensor as data source,
it acts like a :ref:`sensor-filter-exponential_moving_average` filter. With
multiple sensors, it combines their values based on their respective standard
deviation.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: kalman_combinator
        name: "Temperature"
        unit_of_measurement: °C
        process_std_dev: 0.001
        sources:
          - source: temperature_sensor_1
            error: 1.
          - source: temperature_sensor_2
            error_function: |-
              return 0.5 + std::abs(x - 25) * 0.023

Configuration variables:
------------------------

- **process_std_dev** (**Required**, float): The standard deviation of the
  measurement's change per second (e.g. ``1/3600 = 0.000277`` if the
  temperature usually changes at most by one Kelvin per hour). A low value here
  will place high importance on the current state and be slow to respond to
  changes in the measured samples. A high value will update faster, but also be
  more noisy.
- **std_dev** (*Optional*, :ref:`Sensor <config-sensor>`): A sensor
  that publishes the current standard deviation of the state with each update.
- **sources** (**Required**, list): A list of sensors to use as source. Each
  source must have either **error** or **error_function** set. These work like
  the **process_std_dev** parameter, with low values marking accurate data.

  - **sensor** (**Required**, ID of a :doc:`/components/sensor/index`): The
    sensor that is used as sample source
  - **error** (*Optional*, float): The standard deviation of the sensor's
    measurements.
  - **error_function** (*Optional*, lambda): A lambda that returns the
    standard deviation of a single sample, based on the sample value ``x``.

- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :apiref:`kalman_combinator/kalman_combinator.h`
- :ghedit:`Edit`
