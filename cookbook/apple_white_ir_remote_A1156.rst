Apple IR Remote (A156) to control an iPod Dock
==================================

.. seo::
    :description: Instructions for setting up an infrared transmitter with ESPhome to control an iPod dock with Home Assistant
    :image: apple_ir_remote_ipod_dock.jpg
    :keywords: infrared IR remote

.. figure:: images/apple_ir_remote_ipod_dock.jpg
    :align: left
    :width: 75.0%


In this example I have used a Wemos D1 Mini and an infrared sheild to control an iPod dock from Home Assistant. 
I enjoy listening to \`Soulection Radio <https://soundcloud.com/soulection>\`__. They are two hour shows released weekly on Soundcloud on Fridays.
I download the shows and have them in the background while I work. But it's nice to automate things with Home Assistant that don't have an internet connection.


I've added this to the cookbook because the iPod remote codes were getting hard to find



Hardware configuration
----------------------

Hardware is easy! Just solder the sheild or wire up a IR transmitter LED using the Wemos D1 mini pins below:

Only four connections are needed:

- ``VCC`` - Power
- ``GND`` - Ground
- ``D3`` - GPIO for Receiver
- ``D4`` - GPIO for Transmitter


Software configuration
----------------------

We are emulating a 6 button remote so the configuration is simple:


Dumping Other IR Codes 
******************

This is only required if you want to add other codes for other remotes.

.. code-block:: yaml

		### This is only needed to dump other remote codes.
		 remote_receiver:
		   pin: D4
		   dump: all

The Configuration
******************


.. code-block:: yaml


		remote_transmitter:
		  pin: D3
		  # Infrared remotes use a 50% carrier signal
		  carrier_duty_percent: 50%
		  
		switch:
		  - platform: template
		    name: Apple Remote Volume Up Button
		    turn_on_action:
		      - remote_transmitter.transmit_nec:
		          address: 0x77E1
		          command: 0xD04E
		  - platform: template
		    name: Apple Remote Volume Down Button
		    turn_on_action:
		      - remote_transmitter.transmit_nec:
		          address: 0x77E1
		          command: 0xB04E
		  - platform: template
		    name: Apple Remote Previous Button
		    turn_on_action:
		      - remote_transmitter.transmit_nec:
		          address: 0x77E1
		          command: 0x104E
		  - platform: template
		    name: Apple Remote Next Button
		    turn_on_action:
		      - remote_transmitter.transmit_nec:
		          address: 0x77E1
		          command: 0xE04E
		  - platform: template
		    name: Apple Remote Play/Pause Button
		    turn_on_action:
		      - remote_transmitter.transmit_nec:
		          address: 0x77E1
		          command: 0x2000
		  - platform: template
		    name: Apple Remote Menu Button
		    turn_on_action:
		      - remote_transmitter.transmit_nec:
		          address: 0x77E1
		          command: 0x404E


Fast Forward and Rewind
---------
Fast Forward and Rewind aren't available yet but maybe someone can add it.



Sources of IR Codes:
---------

https://github.com/brackendawson/Appleceiver/blob/master/Appleceiver.ino

https://github.com/anton-semeniak/Esphome-TTGO-T-Display-Remote/blob/master/ttgo_menu.yaml

See Also
--------
- :ghedit:`Edit`
