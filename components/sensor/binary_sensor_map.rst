Binary Sensor Map
=================

.. seo::
    :description: Instructions for setting up a Binary Sensor Map
    :image: binary_sensor_map.jpg

The ``binary_sensor_map`` sensor platform allows you to map :doc:`binary sensor </components/binary_sensor/index>`
to values. Depending on the state of each binary sensor, its associated value in this platform's configuration will 
be published according to this sensor's type.

This sensor is used for combining binary sensors' ``ON`` or ``OFF`` states into a numerical value. Some use cases include 
touch devices and Bayesian probabilities for an event.

This platform currently supports three measurement types: ``BAYESIAN``, ``GROUP``, and ``SUM``.
You need to specify which type of mapping you want with the ``type:`` configuration value:

When using the ``BAYESIAN`` type, add your binary sensors as ``observations`` to the binary sensor map. 
When using the ``GROUP`` or ``SUM`` type, add your binary sensors as ``channels`` to the binary sensor map. 
The binary sensor map then publishes a value depending on the type of the binary sensor map and the parameters 
specified with each observation or channel. The maximum amount of observations or channels supported is 64.

- ``BAYESIAN`` This type mimics the Home Assistant's `Bayesian sensor <https://www.home-assistant.io/integrations/bayesian/>`__. The sensor itself requires setting its own ``prior`` probability, which represents the likelihood that the sensor's event is true, ignoring all external influences. Each channel has its own ``prob_given_true`` and ``prob_given_false``. The ``prob_given_true`` parameter represents the probability (between 0 and 1) that the channel's ``binary_sensor`` is ``true`` when the overall Bayesian sensor should be ``true``. The ``prob_given_false`` parameter represents the probability that the channel's ``binary_sensor`` is ``true`` when the  overall Bayesian sensor should be ``false``. An :doc:`/components/binary_sensor/analog_threshold` can be used to convert this sensor's published output to a binary output by using setting an appropriate threshold.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: binary_sensor_map
        id: bayesian_prob
        name: 'Bayesian Event Probability'
        type: bayesian
        prior: 0.4
        channels:
          - binary_sensor: bit0
            prob_given_true: 0.9
            prob_given_false: 0.2
          - binary_sensor: bit1
            prob_given_true: 0.6
            prob_given_false: 0.1

    binary_sensor:
      - platform: gpio
        pin: 4
        id: bit0
      - platform: gpio
        pin: 5
        id: bit1

      - platform: analog_threshold
        name: "Bayesian Event Predicted State"
        sensor_id: bayesian_prob
        threshold: 0.6


- ``GROUP`` Each channel has its own value. The sensor publishes the average value of all active
  binary sensors or ``NAN`` if no sensors are active.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: binary_sensor_map
        id: group_0
        name: 'Group Map 0'
        type: GROUP
        channels:
          - binary_sensor: touchkey0
            value: 0
          - binary_sensor: touchkey1
            value: 10
          - binary_sensor: touchkey2
            value: 20
          - binary_sensor: touchkey3
            value: 30

    # Example binary sensors using MPR121 component
    mpr121:
      id: mpr121_first
      address: 0x5A

    binary_sensor:
      - platform: mpr121
        channel: 0
        id: touchkey0
      # ...
      
- ``SUM`` Each channel has its own value. The sensor publishes the sum of all active
  binary sensors values or ``0`` if no sensors are active.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: binary_sensor_map
        id: group_0
        name: 'Group Map 0'
        type: sum
        channels:
          - binary_sensor: bit0
            value: 1
          - binary_sensor: bit1
            value: 2
          - binary_sensor: bit2
            value: 4
          - binary_sensor: bit3
            value: 8

    binary_sensor:
      - platform: gpio
        pin: 4
        id: bit0

      - platform: gpio
        pin: 5
        id: bit1

      - platform: gpio
        pin: 6
        id: bit2

      - platform: gpio
        pin: 7
        id: bit3
      # ...

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **type** (**Required**, string): The sensor type. Should be one of: ``BAYESIAN``, ``GROUP``, or ``SUM``.
- **prior** (**Required for BAYESIAN type**, float between 0 and 1): The prior probability of the Bayesian event.
- **channels** (**Required**): A list of channels that are mapped to certain values.

  - **binary_sensor** (**Required**): The id of the :doc:`binary sensor </components/binary_sensor/index>`
    to add as a channel for this sensor.
  - **value** (**Required**): The value this channel should report when its binary sensor is active.
- **observations** (**Required for BAYESIAN type**): A list of observations that influence the probability of the Bayesian event.

  - **binary_sensor** (**Required**): The id of the :doc:`binary sensor </components/binary_sensor/index>`
    to add as a channel for this sensor.
  - **prob_given_true** (**Required**, float between 0 and 1): Assuming the Bayesian event is true, the probability this sensor is true.
  - **prob_given_false** (**Required**, float between 0 and 1): Assuming the Bayesian event is false, the probability this sensor is true.

- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :doc:`/components/binary_sensor/mpr121`
- :doc:`/components/binary_sensor/analog_threshold`
- :ref:`sensor-filters`
- :apiref:`binary_sensor_map/binary_sensor_map.h`
- `Bayesian sensor in Home Assistant <https://www.home-assistant.io/integrations/bayesian/>`__
- :ghedit:`Edit`
