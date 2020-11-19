Nextion Switch Component
========================

.. seo::
    :description: Instructions for setting up Nextion switch.
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

    switch:
      - platform: nextion
        page_id: 0
        component_id: 2
        name: "Nextion Component Switch"
        button_id: "bt0"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **page_id** (**Required**, int): The ID of the page the component is on. Use ``0`` for the default page.
- **component_id** (**Required**, int): The ID (the number, not name!) of the component to track.
- **button_id** (**Required**, string): The ID of button within the Nextion Configuration.
- **nextion_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the Nextion display.
- All other options from :ref:`Switch <config-switch>`.

Required Nextion Code:
----------------------

To enable to use the Dual State Push Button (Switch) some code has to be added in the Nextion editor. 

The following code can has to be added in the Nextion Editor to the configuration of the Dual State Push button acting as a switch:

.. code-block:: c

    printh 90
    printh 00
    printh 03
    prints bt0.val,1
    printh FF FF FF

- **printh 90** (**Required**): 90 is a special code, created to register feedback from switch
- **printh 00** (**Required**): The ID of the page the component is on.
- **printh 03** (**Required**): ITEM ID could be replaced with prints ID.val,1
- **prints bt0.val,1** (**Required**): Where bt0 the id of the button is = equal to id in configuration
- **printh FF FF FF** (**Required**): To close the string

See Also
--------

- :doc:`/components/display/nextion`
- :doc:`/components/binary_sensor/nextion`
- :doc:`/components/sensor/nextion`
- :doc:`index`
- :apiref:`nextion/nextion.h`
- :ghedit:`Edit`
