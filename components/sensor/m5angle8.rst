Rotary Encoder Sensor
=====================

.. seo::
    :description: Setting up the ``m5angle8`` input device with 8 potentiometers.
    :image: m5angle8.png

The ``m5angle8`` platform allows to use the [m5angle](https://docs.m5stack.com/en/unit/UNIT%208Angle) input device with ESPHome. 
It has 8 potentiometers, a switch and can individually drive 9 RGB LEDs. 

.. figure:: images/m5angle8.png
    :align: center
    :width: 75.0%

    The m5angle8 unit.

The ``m5angle8`` component communicates through an :ref:`I²C <i2c>` bus and uses a default address of 0x43. 

.. code-block:: yaml

    # Example configuration entry
    i2c:
      sda: 26
      scl: 32
      scan: false
      id: bus_external
      frequency: 200kHz
          
    m5angle8:
        i2c_id: bus_external
        id: m8_angle_base
        lights:
            id: m8_angle_leds
            name: "M5Angle Lights"
            effects:
                - addressable_rainbow: 
        knob_position_1:
            name: "M5Angle Knob 1"
        knob_position_2:
            name: "M5Angle Knob 2"
        knob_position_3:
            name: "M5Angle Knob 3"
        knob_position_4:
            name: "M5Angle Knob 4"
        knob_position_5:
            name: "M5Angle Knob 5"
        knob_position_6:
            name: "M5Angle Knob 6"
        knob_position_7:
            name: "M5Angle Knob 7"
        knob_position_8:
            name: "$M5Angle Knob 8"
        input_switch:
            name: "M5Angle Switch"

Configuration variables:
------------------------
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **i2c_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`I²C Component <i2c>` if you need
- **address** (*Optional*, int): Manually specify the I²C address of the device. Defaults to ``0x43``. 
  

- **lights** (*Optional*): Use the 9 LEDs as addressable light output.
  - All options from :ref:`Light <config-light>`.
   
- **knob_position_{1-8}** (*Optional*): Sensors for the knobs' position. If configured, it gives value of between 0-1 with 0 being the leftmost position.
 
  - **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
  - All other options from :ref:`Sensor <config-sensor>`.


- **input_switch** (*Optional*): A binary sensor of the switch on the device.
 
  - **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
  All other options from :ref:`Binary Sensor <config-binary_sensor>`.


Read positions and switch state in Lambdas
------------------------------------------

You can trigger the readout of the position of an individual knob through ``float value = id(...)->read_knob_pos(index);`` and of the switch through ``int value = id(...)->read_switch();``.
A negative return value indicates a failure to read the state. 

.. code-block:: yaml

    # Example configuration entry
    lights:
        id: m8_angle_leds
        name: "M5Angle Lights"
        effects:
            - addressable_rainbow:
            - addressable_lambda:
                name: "Indicate Values"
                update_interval: 200ms
                lambda: |-
                        ESPHSVColor hsv;
                        hsv.value = 255;
                        hsv.saturation = 240;
                        auto parent = id(m8_angle_base);
                        for (int i=0; i < 8; i++) {
                          auto kpos = parent->read_knob_pos(i);
                          if (kpos >= 0){
                            hsv.hue = kpos * 200; 
                            it[i] = hsv;
                          }
                        }
                        if (parent->read_switch() > 0)
                            hsv.hue = 20;   
                        else
                            hsv.hue = 200; 
                        it[8] = hsv;

See Also
--------

- :ref:`sensor-filters`
- :doc:`/components/binary_sensor/index`
- :doc:`/components/light/index`
- :doc:`template`
- :apiref:`m5angle8/m5angle8.h`
- :ghedit:`Edit`
