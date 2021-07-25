SDP3x Differential Pressure Sensor
=========================

.. seo::
    :description: Instructions for setting up the SDP3x Differential Pressure sensor.
    :image: images/sdp31.jpg
    :keywords: SDP3x, SDP31, SDP32

The SDP3x Differential Pressure sensor allows you to use your SDP3x
(`datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/8_Differential_Pressure/Datasheets/Sensirion_Differential_Pressure_Datasheet_SDP3x_Digital.pdf>`__,
`sparkfun <https://www.sparkfun.com/products/17874>`__)
sensors with ESPHome.

.. figure:: images/sdp31.jpg
    :align: center
    :width: 30.0%

    SDP31 Differential Pressure Sensor.
    (Credit: `Sparkfun <https://www.sparkfun.com/products/17874>`__, image cropped and compressed)

.. _Sparkfun: https://www.sparkfun.com/products/17874

To use the sensor, first set up an :ref:`I²C Bus <i2c>` and connect the sensor to the specified pins. Set the accuracy_decimals field to avoid rounding off the pressure readings, as the SDP3x sensors are designed to measure small pressure differences.

.. code-block:: yaml

    # Example configuration entry
    - platform: sdp3x
      name: "HVAC Filter Pressure drop"
      id: filter_pressure
      update_interval: 5s
      accuracy_decimals: 3

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the temperature sensor.
- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for lambdas/multiple sensors.
- **address** (*Optional*, int): The I²C address of the sensor. Defaults to 0x21.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.
- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :apiref:`sdp3x/sdp3x.h`
- :ghedit:`Edit`
