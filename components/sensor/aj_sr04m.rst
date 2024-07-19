AJ-SR04M Ultrasonic Distance Sensor
===================================

.. seo::
    :description: Instructions for setting up ultrasonic distance measurement sensors in ESPHome.
    :image: aj_sr04m.jpg
    :keywords: ultrasonic, aj-sr04m

The ultrasonic distance sensor allows you to use simple ultrasonic
sensors like the AJ-SR04M (`User Manual <https://device.report/manual/11063803>`__) with ESPHome
to measure distances. 

Working voltage: DC 3-5.5V
Working current: 40 mA duration less than 50 us
Standby current: 2 mA
Working frequency: 40 kHz
Recent range: 20 cm
Furthest range: 600 cm
Measuring Angle: 75 degree
Resolution: about 2 mm
Working Temperature: -20~75 °C

AJ-SR04M can be operated in five modes. 
Mode selection happens by putting resistance over R19 pads.
Component supports Mode 4 - Low power Serial Mode.

Use 47KΩ at R19 to enter the Low power Serial Mode.
In this mode the sensor is in low power sleep mode and consumes 20uA.
When the trigger command(0x55) is received RX pin, the sensor wakes up,
performs distance calculation and outputs the distance over the TX line.
The sensor goes back to sleep after transmitting data.

.. figure:: images/aj_sr04m-1024x768.jpg
    :align: center
    :width: 50.0%

    AJ-SR04M Ultrasonic Distance Sensor.

.. figure:: images/aj_sr04m-mode_change.jpg
    :align: center
    :width: 80.0%

To use the sensor, first set up an :ref:`uart` with a baud rate of 9600 and connect the sensor to the specified pin.

.. code-block:: yaml

    # Example configuration entry
    uart:
      id: uart_bus
      tx_pin: D7 # Transmit pin
      rx_pin: D6 # Receive pin
      baud_rate: 9600 # Baud rate
      stop_bits: 1 # Num of stop bits
    
    sensor:
      - platform: aj_sr04m
        name: "Distance" # Name of sensor in frontend
        id: sensor_distance # Sensor ID to use in ESPHome
        update_interval: 2s # Interval to check sensor

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **uart_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`UART bus <uart>` you wish to use for this sensor.
  Use this if you want to use multiple UART buses at once.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- All other options from :ref:`Sensor <config-sensor>`.

Advanced options:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

See Also
--------

- :ref:`sensor-filters`
- :ref:`uart`
- :apiref:`aj_sr04m/aj_sr04m.h`
- :ghedit:`Edit`
