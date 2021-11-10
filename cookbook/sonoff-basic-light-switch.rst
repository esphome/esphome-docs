DIY Light switch using a Sonoff Basic
=====================================

.. seo::
    :description: An example of how to integrate a light switch into Home Assistant using ESPHome
    :image: sonoff_light_switch.png
    :keywords: Relay, Sonoff Basic, Sonoff Dual Dual R1, Light, HASS, Home Assistant, ESPHome

.. note::

    This is a DIY solution, and you will need to have some knowledge of electrical wiring and enough
    capabilities to do this work safely.

    The author, and the ESPHome team, take no responsibility for any actions, injuries or outcomes
    from following this guide.

    In some countries you may need specific qualifications before you can carry out such work in
    a residential property.

Background
----------

Moving your entire house to smart lighting can end up being very expense, for instance if you have a
light fitting with 5 lamps in it that's 5 expensive smart bulbs to buy just for one room! Smart bulbs
clearly have some great advantages, dimmable, colour temperature or even full colour changing. What
if all you're after is a cost effective way to turn them on and off?

The ideal solution would be to replace the light switch with one that can be controlled by home
assistant, whilst retaining the ease of use of a standard light that would also continue to work if
the network went down, or Home Assistant failed etc.

It turns out Sonoff do exactly this product, it called a T1-UK (other country options available),
however you soon found the touch aspect of them might not 'feel right' and certainly might not get the
approval of other members of your household. However if this solution appeals to you, check out the
:doc:`Cookbook guide for T1/T2/T3</cookbook/sonoff-t1-3>`

The other option to consider is a standard '2 way' light switch (like you might have on an upstairs
/ downstairs control in your house) but using relays for the second switch. For many this will have
the disadvantage that if you remotely changed the light status the switch is then 'upside down'.

The Solution
------------

Use a 'retractive' style light switch. That is one that is spring loaded and so always returns to the
'off' position. It's effectively a push button, that looks like a light switch. Combining this with a
Sonoff Basic gives you the ideal solution for somewhere around £5. That's much cheaper than buying lots
of expensive smart bulbs, but of course you only get on / off control.

You will have several potential hurdles to overcome:

1. The first is that you do need to have a neutral at the location of the Sonoff. Many houses will not have
   this as standard at the light switch.

2. You need enough space to accommodate your Sonoff Basic at your chosen location.

If you're lucky most of the locations will have plasterboard walls, and you will be able to simply drop a neutral
wire down the inside of the wall to the lights switch (where you locate the Sonoff).

Also, if you have plasterboard walls, most of the light switch back boxes are the plastic dry lining style boxes.
This can come in useful because if you remove the PCB from the plastic case it actually fits in the back box nicely.

.. warning::

    If you plan to take the PCB out of the plastic case you need to make sure it's properly insulated, and that the back
    box is deep enough to hold the PCB as well as the switch. You should also insulate the PCB, for instance by dropping it
    in a heavy duty glue lined heat shrink sleeve.

    **The PCB has mains electricity flowing through it, if you are in any doubt about your capabilities do not attempt to do
    this.**

If you have a light switch in a brick wall, an option might be to place the Sonoff Basic above the light in the ceiling void,
and use the cable that ran from the light to the switch as a low voltage cable to connect the Sonoff GPIO.

.. warning::

    If you are going to reuse existing wiring to connect to the GPIO, you must make sure it's connected directly to the switch
    and does not have mains voltage on it from another circuit.

Implementation
--------------

So having established the pitfalls that you need to overcome lets crack on with making this work.

Please make sure you have read up about :doc:`the Sonoff Basic and how to flash it with ESPHome </devices/sonoff_basic>`.
As that won't be covered here.Also make sure you know your way around a soldering iron and can find the relevant information
about the location of the GPIO pins on the Sonoff Basic if you need to.

If you have a Sonoff Basic V1 devices GPIO14 is already presented on a pin header on the PCB next to the programming pins.
On the V2 and V3 PCBs, there is a solder pad underneath the PCB that will let you get at this GPIO.

You have 2 choices when it comes to picking which GPIO to use. GPIO0 or GPIO14. GPIO0 is used by the push button switch on the
the PCB so you will need to locate the right pin on the switch and solder a wire onto it if you're going to use that one. Whichever
one you pick, you will also need to use the ground or 0V pin for the other side of the switch. Once you have soldered your wires
into place, a handy tip is to add a drop of glue over the wire, a little way away from the solder joint, so give some strain relief
to the joint.

Now you have a pair of wires from the GPIO and 0V to your retractive switch lets look at the code.

.. code-block:: yaml

    esphome:
      name: my_ls
      platform: ESP8266
      board: esp01_1m

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password

    logger:

    api:

    ota:

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO14
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_1
        on_press:
          then:
            - light.toggle: light_1

      - platform: status
        name: "My LS Status"

    output:
      - platform: gpio
        pin: GPIO12
        id: relay_1

    light:
      - platform: binary
        name: "My Light"
        id: light_1
        output: relay_1

    status_led:
      pin:
        number: GPIO13
        inverted: yes

In the above code block, there is a *secrets.yaml* file so that you have just one place to change WiFi
details for all your devices.

Although not visible day to day, there is also the status LED configured so that it can be used when setting
up / debugging. Also a configured binary sensor to give status in case you want to perform an action / alert
if the light switch disconnects for any reason.

.. note::

    If you wanted to use a pull cord switch (in a bathroom for instance) that works like a standard switch and
    changes state each pull (as opposed to a retractive switch that you press and let go) then you can change
    a single line *on_press:* to *on_state:* which will trigger the light toggle every time the state of the
    switch changes.

    If you do this it's important that you do not use GPIO0, otherwise if the device reboots and the switch happens
    to be in the closed state the Sonoff will boot into flash mode and not work.



See Also
--------

- :doc:`/cookbook/sonoff-light-switch`
- :doc:`/guides/automations`
- :doc:`/devices/sonoff_basic`
