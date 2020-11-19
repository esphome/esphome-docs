Nextion Switch Component
========================

.. seo::
    :description: Instructions for setting up Nextion sensors.
    :image: nextion.jpg

The ``nextion`` switch lets you track when a component on the display is
switched on or off. The behavior is quite similar to the Dual state push button as a binary sensor. In case a switch is used the 
``nextion`` screen will be updated if the switch is activated within Home Assistant.

See :doc:`/components/display/nextion` for setting up the display

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: nextion
        # ...

    sensor:
      - platform: nextion
        page_id: 0
        component_id: 5
        name: "Nextion Sensor"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **page_id** (**Required**, int): The ID of the page the component is on. Use ``0`` for the default page.
- **component_id** (**Required**, int): The ID (the number, not name!) of the component to track.
- **nextion_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the Nextion display.
- All other options from :ref:`Sensor <config-sensor>`.

Required Nextion Code:
----------------------

The following code can has to be added in the Nextion Editor to the configuration of the item (for example slider) you want to usa as the input for the sensor:

.. code-block:: c#

    printh 91  
    printh 00
    printh 03
    prints ht0.val,1
    printh FF FF FF

Configuration variables:
------------------------

- **printh 91** (**Required**): 91 is special code I created to register feedback from value change (for example slider)
- **printh 00** (**Required**): The ID of the page the component is on.
- **printh 03** (**Required**): ITEM ID could be replaced with prints ID.val,1
- **prints ht0.val,1** (**Required**): Where ht0 the id of the slider
- **printh FF FF FF** (**Required**): To close the string

See Also
--------

- :doc:`/components/display/nextion`
- :doc:`/components/binary_sensor/nextion`
- :doc:`/components/switch/nextion`
- :doc:`index`
- :apiref:`nextion/nextion.h`
- :ghedit:`Edit`
