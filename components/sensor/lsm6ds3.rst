LSM6DS3 Accelerometer/Gyroscope/Temperature Sensor
==================================================

.. seo::
    :description: Instructions for setting up LSM6DS3 Accelerometer and Gyroscope sensors.

The ``lsm6ds3`` sensor platform allows you to use your LSM6DS3 Accelerometer/Gyroscope
(`datasheet <https://cdn.sparkfun.com/assets/learn_tutorials/4/1/6/AN4650_DM00157511.pdf>`__)
sensors with ESPHome. The :ref:`I²C Bus <i2c>` is
required to be set up in your configuration for this sensor to work.

This component only does basic sensor reading, and is not setup to support on chip event
detection with gpio interrupts. It does support power management.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: lsm6ds3
        address: 0x6A
        accel_x:
          name: "LSM6DS3 Accel X"
        accel_y:
          name: "LSM6DS3 Accel Y"
        accel_z:
          name: "LSM6DS3 Accel z"
        gyro_x:
          name: "LSM6DS3 Gyro X"
        gyro_y:
          name: "LSM6DS3 Gyro Y"
        gyro_z:
          name: "LSM6DS3 Gyro z"
        temperature:
          name: "LSM6DS3 Temperature"
        high_perf: false
        sample_accl_rate: 13
        sample_gyro_rage: 13
        power_save: true

Configuration variables:
------------------------

- **address** (*Optional*, int): Manually specify the I²C address of the sensor. Defaults to ``0x6A``.
- **accel_x** (*Optional*): Use the X-Axis of the Accelerometer. All options from
  :ref:`Sensor <config-sensor>`.
- **accel_y** (*Optional*): Use the Y-Axis of the Accelerometer. All options from
  :ref:`Sensor <config-sensor>`.
- **accel_z** (*Optional*): Use the Z-Axis of the Accelerometer. All options from
  :ref:`Sensor <config-sensor>`.
- **gyro_x** (*Optional*): Use the X-Axis of the Gyroscope. All options from
  :ref:`Sensor <config-sensor>`.
- **gyro_y** (*Optional*): Use the Y-Axis of the Gyroscope. All options from
  :ref:`Sensor <config-sensor>`.
- **gyro_z** (*Optional*): Use the Z-Axis of the Gyroscope. All options from
  :ref:`Sensor <config-sensor>`.
- **temperature** (*Optional*): Use the internal temperature of the sensor. All options from
  :ref:`Sensor <config-sensor>`.
- **high_perf** (*Optional*): Use high performance sampling, has larger power draw. Defaults to ``false``
- **sample_accl_rate** (*Optional*): Samples per second of the acceleration, one of 13, 26, 52, 104, 208, 416, 833, 1660,
  3330, 6660, 13330. Defaults to 13
- **sample_gyro_rate** (*Optional*): Samples per second of the gyroscope, one of 13, 26, 52, 104, 208, 416, 833, 1660.
  Defaults to 13
- **power_save** (*Optional*): Use on chip power saving features, at the expense of latency. Defaults to true.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

See Also
--------

- :ref:`sensor-filters`
- :doc:`template`
- :apiref:`lsm6ds3/lsm6ds3.h`
- :ghedit:`Edit`
