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
  a residentaial property.

Background
----------

I was looking for a simple, cost effective, way to upgrade my lights so they could be controlled by
home assistant, whilst retaining the ease of use of a standard light that would continue to work if
the network went down, or home assistant failed etc.

I started looking at the Sonoff T1/2/3 series of switches, but soon found the touch aspect of them
didn't 'feel right' and certainly didn't get the approval of other members of the household.

I also considered a standard '2 way' light system with relays, but didn't like the idea that if you
remotely changed the light status the switch was then 'upside down'.

My Solution
-----------

I decided to use a 'retractive' style light switch. That is one that is spring loaded and so always
returns to the 'off' position. It's effectively a push button, that looks like a light switch. Combining
this with a Sonoff Basic gives you the ideal solution for somewhere around £5. Thats much cheaper than
buying lots of expensive smart lights, but of course you only get on / off control.

You will have several potential hurdles to overcome:

1. The first is that you do need to have a neutral at the location of the Sonoff. Many houses will not have
   this as standard at the light switch.

2. You need enough space to accomodate your Sonoff Basic at your chosen location.

I am lucky that in most of the locations that I wanted to use this I have plasterboard walls, and was able to simply
drop a neutral wire down the inside of the wall to the lights switch (where I have chosen to locate the Sonoff).

Also, due to haveing plasterboard walls, most of my light switch back boxes are the plastic dry lining style boxes.
This came in useful because I found that the if you remove the PCB from the plastic case it actually fits in the back
box nicely.

.. warning::

  If you plan to take the pcb out of the plastic case you need to make sure its properly insulated, and that the back
  box is deep enough to hold the PCB as well as the switch. Where I did this I have insulated by dropping it in a heavy
  glue lined heat shrink sleeve.

  **The PCB has mains electricity flowing through it, if you are in any doubt about your capabilities do not attempt to do
  this.**

There is one location where I have a light switch in a brick wall, and so was unable to pass a neutral to it, and did not
have space for the Sonoff Basic to fit behind the light switch. In this case I was able to place it above the light in the
ceiling void, and use the cable that ran from the light to the switch as a low voltage cable to connect the Sonoff GPIO.

.. warning::

  If you are going to reuse existing wiring to connect to the GPIO, you must make sure its connected directly to the switch
  and does not have mains voltage on it from another circuit.

Implementation
--------------

So having established the pitfalls that you need to overcome lets crack on with making this work.

I'm going to assume you have read up about :doc:`the Sonoff Basic and how to flash it with ESPHome </devices/sonoff_basic>`.
So I won't be covering any of that. I'm also going to assume that you know your way around a soldering iron and can find the
relevant information about the location of the GPIO pins on the Sonoff Basic if you need to.

I did this modification before ESPHome existsed, and used a different firmware, but have since upgraded all my light switches
to using ESPHome. This means that the majority of my Sonoff Basis devices as the V1 devices, and as such have GPOI14 alredy
presented on a pin header on the PCB next to the programing pins. On the V2 and V3 PCBs, these is a solder pad underneath the
PCB that will let you get at this GPIO.

You have 2 choices when it comes to picking which GPIO to use. GPIO0 or GPIO14. GPIO0 is used by the push button switch on the
the PCB so you will need to locate the right pin on the switch and solder a wire onto it if your going to use that one. Whichever
one you pick, you will also need to use the ground or 0v pin for the other side of the switch. Once you have soldered your wires
into palce, a handy tip is to add a drop of glue over the wire, a little way away from the solder joint, so give some strain relief
to the joint.

Now we have a pair of wires from the GPIO and 0v to your retractive switch we can look at the code.

.. code-block:: yaml

    esphome:
      name: my_ls
      platform: ESP8266
      board: esp01_1m

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password
      fast_connect: true

    logger:
      level: INFO

    api:

    ota:

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO14
          mode: INPUT_PULLUP
          inverted: True
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

In the above code block, I am using a *secrets.yaml* file so that I have just one place to change my wifi
details for all my devices.

The logger level INFO is required to overcome a bug that can stop the Sonoff Basic connecting to the wifi.
See `issue #455 <https://github.com/esphome/issues/issues/455>`__ for further details.

Although not visible day to day, I have also configured the status LED so that it can be used when setting
up / debugging, and configured a binary sensor to give status incase you want to perform an action / alert
if the light switch disconnects for any reason.


See Also
--------

- :doc:`/cookbook/sonoff-light-switch`
- :doc:`/guides/automations`
- :doc:`/devices/sonoff_basic`

