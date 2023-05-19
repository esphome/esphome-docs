A01NYUB Waterproof Ultrasonic Sensor
====================================

.. seo::
    :description: Instructions for setting up A01NYUB waterproof ultrasonic distance sensor in ESPHome.
    :image: a01nyub.jpg
    :keywords: ultrasonic, DFRobot, A01NYUB

This sensor allows you to use A01NYUB waterproof ultrasonic sensor by DFRobot 
(`datasheet <https://wiki.dfrobot.com/A01NYUB%20Waterproof%20Ultrasonic%20Sensor%20SKU:%20SEN0313>`__)
with ESPHome to measure distances. This sensor can measure
ranges between 28 centimeters and 750 centimeters with a resolution of 1 milimeter.

Since this sensor reads multiple times per second, filtering is highly recommended.

.. figure:: images/a01nyub-full.jpg
    :align: center
    :width: 50.0%

    A01NYUB Waterproof Ultrasonic Distance Sensor.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: 36
      baud_rate: 9600

    sensor:
      - platform: "a01nyub"
        name: "Rainwater Tank"
        # Tweak the filters for your application
        filters:
          - sliding_window_moving_average:
              window_size: 12
              send_every: 12
          - or:
            - throttle: "20min"
            - delta: 0.02


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- All other options from :ref:`Sensor <config-sensor>`.

Advanced options:

- **uart_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`UART bus <uart>` you wish to use for this sensor.
  Use this if you want to use multiple UART buses at once.


See Also
--------

- :ref:`sensor-filters`
- :ref:`uart`
- :doc:`template`
- :apiref:`a01nyub/a01nyub.h`
- :ghedit:`Edit`
