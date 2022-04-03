Kalman filter-based sensor fusion
=================================

.. seo::
    :description: Instructions for setting up a kalman_combinator sensor

The ``kalman_combinator`` sensor platform allows you to filter one or several
sensors into one with a reduced error. If using a single sensor as data source,
it acts like a :ref:`sensor-filter-exponential_moving_average` filter. With
multiple sensors, it combines their values based on their respective standard
deviation.

The ``unit_of_measurement``, ``device_class``, ``entity_category``, ``icon``, and
``accuracy_decimals`` properties are by default inherited from the first sensor.
``state_class`` is explicitly not inherited, because ``total_increasing`` states
could still decrease when multiple sensors are used.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: kalman_combinator
        name: "Temperature"
        unit_of_measurement: °C
        process_std_dev: 0.001
        sources:
          - source: temperature_sensor_1
            error: 1.0
          - source: temperature_sensor_2
            error: !lambda |-
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

  - **source** (**Required**, :ref:`config-id` of a :doc:`/components/sensor/index`): The
    sensor that is used as sample source
  - **error** (**Required**, float, :ref:`templatable <config-templatable>`): The standard deviation of the
    sensor's measurements. If implemented as a template, the measurement is in
    parameter ``x``.

- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :apiref:`kalman_combinator/kalman_combinator.h`
- :ghedit:`Edit`
