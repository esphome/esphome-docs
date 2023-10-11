Grove TB6612FNG Motor Drive
===========================

.. seo::
    :description: Instructions for setting up Grove TB6612FNG Motor Driver  in ESPHome.
    :image: grove_tb6612fng.jpg

The Grove TBB6612FNG a runs over  I²C bus and has the capability to control DC and Stepper motors.
At the current stage of implementation only DC motor is implemented.

.. figure:: images/grove_tb6612fng.jpg
    :align: center
    :width: 50.0%

.. code-block:: yaml

    # Example configuration grove motor
    grove_tb6612fng:
        id: test_motor
        name: motor_outside
        address: 0x14

    # Example switch trigger
    switch:
      - platform: template
        name: open_vent
        id: open_vent
        optimistic: True
        on_turn_on:
          then:
            - grove_tb6612fng.run:
                channel: 1
                speed: 255
                direction: BACKWARD
                id: test_motor
            - delay: 10s
            - switch.turn_on: stop_motor
            - switch.turn_off:  open_vent

Configuration variables:
************************

- **id** (**Required**, :ref:`config-id`): The id to use for this TB6612FNG component.
- **address** (*Optional*, int): The I²C address of the driver.
  Defaults to ``0x14``.
- **name** (**Required**, boolean): The name of the component

.. grove_tb6612fng.run:

``grove_tb6612fng.run`` Action
------------------------------

Set the motor to spin by defining the direction and speed of the rotation, speed is a range from 0 to 255

.. code-block:: yaml

    on_...:
      then:
        - grove_tb6612fng.run:
            channel: 1
            speed: 255
            direction: BACKWARD
            id: test_motor


.. grove_tb6612fng.stop:


``grove_tb6612fng.stop`` Action
-------------------------------

Set the motor to stop motion but wont stop to spin in case there is a force pulling down, you would want to use break action if this is your case

.. code-block:: yaml

    on_...:
      then:
        - grove_tb6612fng.stop:
            channel: 1



.. grove_tb6612fng.break:


``grove_tb6612fng.break`` Action
--------------------------------

Set the motor channel to be on break mode which it ensure the wheel wont spin even if forced or pushed

.. code-block:: yaml

    on_...:
      then:
        - grove_tb6612fng.break:
            channel: 1
            id: test_motor

.. grove_tb6612fng.standby:

``grove_tb6612fng.standby`` Action
----------------------------------

Set the board to be on standby when is not used for a long time which reduces power consumptions and any jerking motion when stationary

.. code-block:: yaml

    on_...:
      then:
        - grove_tb6612fng.standby
            id: test_motor

.. grove_tb6612fng.no_standby:

``grove_tb6612fng.no_standby`` Action
-------------------------------------

Set the board to be awake, every esphome is restarted the default mode is set to standby to ensure the motor wont spin accidentally

.. code-block:: yaml

    on_...:
      then:
        - grove_tb6612fng.no_standby
            id: test_motor


See Also
--------

- :ref:`i2c`
- :doc:`switch/gpio`
- :ghedit:`Edit`
