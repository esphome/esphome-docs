Nextion Touch Component
=======================

.. seo::
    :description: Instructions for setting up Nextion touch binary sensors.
    :image: nextion.jpg

The ``nextion`` binary sensor platform lets you track when a component on the display is
touched or not. The binary sensor will turn on when the component with the given component and page id is
pressed on, and will turn off as soon as the finger is released.

See :doc:`/components/display/nextion` for setting up the display

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: nextion
        # ...

    binary_sensor:
      - platform: nextion
        page_id: 0
        component_id: 2
        name: "Nextion Component 2 Touch"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **page_id** (**Required**, int): The ID of the page the component is on. Use ``0`` for the default page.
- **component_id** (**Required**, int): The ID (the number, not name!) of the component to track.
- **nextion_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the Nextion display.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

Dual State Push Button:
-----------------------

To enable to use the Dual State Push Button some code has to be added in the Nextion editor. In the configuration above only the push on
the screen is registered. So touching the object is on and releasing the object is off. This works well with a push button but not with a Dual 
state push button.

The following code can be added in the Nextion Editor to the configuration of the Dual State Push button:

.. code-block:: c

    printh 65 // 65 is the ID to register the PRESS / RELEASE of a item  
    printh 00 // Page ID
    printh 03 // ITEM ID could be replaced with prints ID.val,1
    prints bt0.val,1 // Where bt0 the id of the button is = equal to id in configuration
    printh FF FF FF

See Also
--------

- :doc:`/components/display/nextion`
- :doc:`/components/sensor/nextion`
- :doc:`/components/switch/nextion`
- :doc:`index`
- :apiref:`nextion/nextion.h`
- :ghedit:`Edit`
