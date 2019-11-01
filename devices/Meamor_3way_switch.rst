Using With Meamor 3 way lightswitch
===================================

.. seo::
    :description: Instructions for putting Meamor 3 way lightswitch devices into flash mode and installing ESPHome on them.
    :image: Meamor_3way.jpg

ESPHome can also be used with Meamor 3 way wireless switches. These devices are
basically just an ESP8266 chip with 3 relays to control power output and three backlit capacitive touch buttons to control the relays.

.. note::

    This instruction is made for Meamor with the touch board 

.. figure:: images/Meamor_3way.jpg
    :align: center
    :width: 75.0%

    MEAMOR WLAN Lightswitch.

This guide will step you through setting up your Meamor 3 way lightswitch and flashing the first ESPHome firmware
with the serial interface. After that, you will be able to upload all future firmwares with the remote
Over-The-Air update process.

Specs of the Meamor:

======================================== =========================================
Weight	                                 141 g
---------------------------------------- -----------------------------------------
Measurements	                         8,6 x 8,6 x 4 cm
---------------------------------------- -----------------------------------------
Volt	                                 240 Volt
---------------------------------------- -----------------------------------------
Watt	                                 1800 Watt
---------------------------------------- -----------------------------------------
Certification	                         CE
======================================== =========================================

The only way to flash the initial ESPHome firmware is by physically opening the device up and using the UART
interface.

.. warning::

    Opening up this device can be very dangerous if not done correctly. While the device is open,
    you will be a single touch away from being electrocuted if the device is plugged in.

    So, during this *entire* guide **never ever** plug the device in. Also, you should only do this
    if you know what you're doing. If you, at any step, feel something is wrong or are uncomfortable
    with continuing, it's best to just stop for your own safety.

    It's your own responsibility to make sure everything you do during this setup process is safe.

For this guide you will need:

- Meamor 3 way lightswitch
- An USB to UART Bridge for flashing the device. These can be bought on Amazon for less than 5 dollars.
  Note that the bridge *must* be 3.3V compatible. Otherwise you will destroy your Switch.
- Jumper wires to connect the UART bridge to the header pins and to connect GPIO0 to the Ground.
- Computer running ESPHome or Hass.io add-on.
- Screwdriver to open up the Meamor 3 way lightswitch.

Have everything? Great! Then you can start.


Step 1: Opening up the Meamor 3 way lightswitch
-----------------------------------------------

The first step is to open up the Meamor 3 way lightswitch. Note that you do not have to run the original firmware
supplied with the Meamor 3 way lightswitch before doing this step.

.. warning::

    Just to repeat this: Make **absolutely sure** the device is not connected to any appliance or
    plugged in before doing this step.

While the device is not plugged in, turn the device face down and put a narrow flat screwdriver into the slot at the bottom.
With careful twisting motion detatch the face plate.

.. figure:: images/meamor_3way_opening.jpg
    :align: center
    :width: 60.0%

    Careful twisting motion.

After that, use the same screwdriver to carefully lift the top PCB off of the switch.
This PCB contains the ESP chip and what's left inside the switch body are relays.

.. figure:: images/Meamor_3way_lifttheplate.jpg
    :align: center
    :width: 75.0%

    "TOUCH BOARD" with touch pads holds the ESP chip.

Step 2: Connecting UART
-----------------------

Now we need our computer to somehow establish a data connection to the board. For this we will
have to connect the four wires on the UART to USB bridge to the UART pins of the Meamor 3 way lightswitch.
The Meamor 3 way lightswitch uses the Tuya TYWE3S-chip, which basically is a 8266 chip.

This is fairly easy for the power, as we can use the bottom two pins on the board, marked "3.3V" and "GND".
Unfortunately, you'll have to solder some wire on the "RX0", "TX0" and "GPIO0" to flash this ESP8266

.. figure:: images/Meamor_3way_inside.jpg

Now go ahead and connect these pins to your UART to USB bridge. I used a breadboard, as this makes is easier to connect
both the GND and GPIO0 to the GND-pin on the USB Bridge. 

``VCC33`` should be connected to the ``3V3`` (**not** 5V) pin of the UART bridge, ``GND`` and ``GPIO0`` to ``GND``
and the same with ``RX``/``TX``.

After flashing succesfully, you don't need the soldered wires any more, and you can remove them.


Step 3: Creating Firmware
-------------------------

The Sonoff T1 UK 3 Gang is based on the ``ESP8266`` platform (technically it's the ``ESP8285``, but for our purposes
they're the same) and is a subtype of the ``esp01_1m`` board.
With this information, you can step through the ESPHome wizard (``esphome sonoff_t1_uk_3g.yaml wizard``),
or alternatively, you can just take the below configuration file and modify it to your needs.

.. code-block:: yaml

    esphome:
      name: <NAME_OF_NODE>
      platform: ESP8266
      board: esp01_1m

    wifi:
      ssid: <YOUR_SSID>
      password: <YOUR_PASSWORD>

    api:

    logger:

    ota:

Now run ``Meamor_3way_switch.yaml compile`` to validate the configuration and
pre-compile the firmware.

.. note::

    After this step, you will be able to find the compiled binary under
    ``<NAME_OF_NODE>/.pioenvs/<NAME_OF_NODE>/firmware.bin``. If you're having trouble with
    uploading, you can also try uploading this file directly with other tools.

Step 4: Uploading Firmware
--------------------------

In order to upload the firmware, you're first going to need to get the chip into a flash mode, otherwise
the device will start up without accepting any firmware flash attempts.
To put ESP8266 into flash mode you need to connect ``GPIO0`` to ``GND`` when the device is powering up.

This is a tricky process with Meamor and the best way to do it is to use a wire with pins on either side.
To do this, while the device is UART bridge is not connected to your USB port, flip the PCB over,
take a wire and connect the second Ground hole on the PCB (red) to the third from the right bottom leg on the chip as depicted below (yellow) -
that leg is connected to the GPIO0 on ESP and plug the UART to your USB port.

Keep holding  GND and GPIO0 connected for 2-4 seconds. The Meamor should now be in a flash mode and should not blink with any LED.
The touchpads may light up.

.. code-block:: bash

    esphome meamor_3way.yaml run

If successful, you should see something like this:

.. figure:: images/sonoff_4ch_upload.png
    :align: center

Hooray 🎉! You've now successfully uploaded the first ESPHome firmware to your Meamor 3 way lightswitch. And in a moment,
you will be able to use all of ESPHome's great features with your Meamor 3 way lightswitchg. Now you can put your Meamor back together and fire up.

.. note::

    While now your meamor will start up and connect to your WiFi network if you power it up from UART it will not behave normally,
    it may flash random LEDs, turn on anf off touchpads' backlight and not react on touching touchpads. This will all be fixed once you re-assemble your Meamor and power it up from the mains power once safe to do so.

Step 5: Adding the Button, Relay and LEDs
-----------------------------------------

Now we would like the T1 UK 3 Gang to actually do something, not just connect to WiFi and pretty much sit idle.

Below you will find a table of all usable GPIO pins of the Sonoff T1 UK 3 Gang and a configuration file that exposes all
of the basic functions.

======================================== =========================================
``GPIO5``                                Touchpad #1 (inverted)
---------------------------------------- -----------------------------------------
``GPIO12``                               Touchpad #2 (inverted)
---------------------------------------- -----------------------------------------
``GPIO3``                                Touchpad #3 (inverted)
---------------------------------------- -----------------------------------------
``GPIO4``                                Relay #1 
---------------------------------------- -----------------------------------------
``GPIO15``                               Relay #2 
---------------------------------------- -----------------------------------------
``GPIO13``                               Relay #3 
---------------------------------------- -----------------------------------------
``GPIO1``                                Touchpad #1 backlight
---------------------------------------- -----------------------------------------
``GPIO16``                               Touchpad #2 backlight
---------------------------------------- -----------------------------------------
``GPIO14``                               Touchpad #3 backlight
======================================== =========================================

.. code-block:: yaml

    esphome:
      name: <NAME_OF_NODE>
      platform: ESP8266
      board: esp01_1m

    wifi:
      ssid: <YOUR_SSID>
      password: <YOUR_PASSWORD>

    api:

    logger:

    ota:

    binary_sensor:
  - platform: gpio
    pin:
      number: GPIO5
      mode: INPUT_PULLUP
      inverted: True
    name: "Tuya Touchpad 1"
    on_press:
      - switch.toggle: stand_1
      - switch.toggle: LED_1
  - platform: gpio
    pin:
      number: GPIO12
      mode: INPUT_PULLUP
      inverted: True
    name: "Tuya Touchpad 2"
    on_press:
      - switch.toggle: stand_2
      - switch.toggle: LED_2
  - platform: gpio
    pin:
      number: GPIO3
      mode: INPUT_PULLUP
      inverted: True
    name: "Tuya Touchpad 3"
    on_press:
      - switch.toggle: stand_3
      - switch.toggle: LED_3
  - platform: status
    name: "Tuya 3 switch Status"

  switch:
  - platform: gpio
    name: "Stand_1"
    id: stand_1
    pin: GPIO4
    inverted: False
    interlock: [stand_2,stand_3]
    restore_mode: RESTORE_DEFAULT_ON
  - platform: gpio
    name: "Stand_2"
    id: stand_2
    pin: GPIO15
    inverted: False
    interlock: [stand_1,stand_3]
    restore_mode: RESTORE_DEFAULT_ON
  - platform: gpio
    name: "Stand_3"
    id: stand_3
    pin: GPIO13
    inverted: False
    interlock: [stand_1,stand_2]
    restore_mode: RESTORE_DEFAULT_ON
  - platform: gpio
    name: "LED_1"
    id: LED_1
    pin: GPIO1
    inverted: False
    interlock: [LED_2,LED_3]
    restore_mode: RESTORE_DEFAULT_OFF
  - platform: gpio
    name: "LED_2"
    id: LED_2
    pin: GPIO16
    inverted: False
    interlock: [LED_1,LED_3]
    restore_mode: RESTORE_DEFAULT_OFF
  - platform: gpio
    name: "LED_3"
    id: LED_3
    pin: GPIO14
    inverted: False
    interlock: [LED_1,LED_2]
    restore_mode: RESTORE_DEFAULT_OFF


Above example also showcases an important concept of esphome: IDs and linking. In order
to make all components in esphome as much "plug and play" as possible, you can use IDs to define
them in one area, and simply pass that ID later on. 
Above example shows a setup where you can only use 1 switch at a time. Just remove the interlocks if you don't want that.

Step 6: Finishing Up
--------------------

If you're sure everything is done with the Meamor 3 way lightswitch and have double checked there's nothing that could cause a short
in the case, you can put the Meamor back together.

Now triple or even quadruple check the UART bridge is not connected to the Meamor 3 way lightswitch, then comes the time when you can
connect it.

Happy hacking!

See Also
--------

- :doc:`sonoff`
- :doc:`sonoff_4ch`
- :doc:`sonoff_s20`
- :ghedit:`Edit`
