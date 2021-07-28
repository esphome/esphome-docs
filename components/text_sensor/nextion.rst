.. _nextion_text_sensor:

Nextion Text Sensor Component
===============================

.. seo::
    :description: Instructions for setting up Nextion text sensor.
    :image: nextion.jpg    

The ``nextion`` text sensor platform supports text strings. It can be a component or variable in the Nextion display.
It is best to set the components vscope to global in the Nextion Editor. This way the component will be available
if the page is shown or not. 

See :doc:`/components/display/nextion` for setting up the display

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: nextion
        id: nextion1
        # ...

    text_sensor:
    - platform: nextion
      nextion_id: nextion1
      name: text0
      id: text0
      update_interval: 4s
      component_name: text0

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **nextion_id** (*Optional*, :ref:`config-id`): The ID of the Nextion display.
- **component_name** (*Optional*, string): The name of the Nextion component.
- **variable_name** (*Optional*, string): The name of the Nextion variable. Any value over ``0`` is considerd to be **on**
- **update_interval** (*Optional*, :ref:`config-time`): The duration to update the sensor. If using a :ref:`nextion_custom_text_sensor_protocol` this should not be used
- **background_color** (*Optional*, :ref:`config-color`):  The background color
- **foreground_color** (*Optional*, :ref:`config-color`):  The foreground color
- **font_id** (*Optional*, uint8_t):  The font id for the component
- **visible** (*Optional*, boolean ):  Visible or not
- All other options from :ref:`Text Sensor <config-text_sensor>`.

**Only one** *component_name* **or** *variable_name* **can be set**

See :ref:`nextion_text_sensor_how_things_update` for additional information

Globals
*******
The Nextion does not retain data on Nextion page changes. Additionally, if a page is changed and the **component_name** does not exist on that page then
nothing will be updated. To get around this, the Nextion components can be changed to have a vscope of ``global``. If this is set, then the **component_name**
should be prefixed with the page name (page0/page1 or whatever you have changed it to).

*Example*

``component_name: page0.text0``

.. _nextion_text_sensor_lambda_calls:

Lambda Calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods to access
some more advanced functions (see the full :apiref:`nextion/text_sensor/nextion_textsensor.h` for more info).

.. _nextion_text_sensor_set_state:

- ``set_state(bool value, bool publish, bool send_to_nextion)``: Set the state to **value**. Publish the new state to HASS. Send_to_Nextion is to publish the state to the Nextion.

.. _nextion_text_sensor_update:

- ``update()``: Poll from the Nextion

.. _nextion_text_sensor_settings:

- ``set_background_color(Color color)``: Sets the background color to **Color**
- ``set_foreground_color(Color color)``: Sets the background color to **Color**
- ``set_visible(bool visible)`` : Sets visible or not. If set to false, no updates will be sent to the component

.. _nextion_text_sensor_how_things_update:

How things Update
-----------------
A Nextion component with an integer value (.val) or Nextion variable will be automatically polled if **update_interval** is set.
To have the Nextion send the data you can use the :ref:`nextion_custom_text_sensor_protocol` for this. Add the :ref:`nextion_custom_text_sensor_protocol` to the 
component or function you want to trigger the send. Typically this is in *Touch Press Event* but some components, like a slider, should have it 
set in the *Touch Release Event* to capture all the changes. Since this is a custom protocol it can be sent from anywhere (timers/functions/componenets)
in the Nextion. 

.. note::

    There is no need to check the *Send Component ID* for the *Touch Press Event* or *Touch Release Event*
    since this will be sending the real value to esphome.

Using the above yaml example:  
  - "text0" will poll the Nextion for ``text0.txt`` value and set the state accordingly.  

    - :ref:`Lambda Calls <nextion_text_sensor_lambda_calls>`.  

.. note::

    No updates will be sent to the Nextion if it is sleeping. Once it wakes, the components will be updated. If a component is invisible, :code:`visible(false)`, then it won't update until it is set to be visible.


.. _nextion_custom_text_sensor_protocol:

Nextion Custom Text Sensor Protocol
-----------------------------------
All lines are required

.. code-block:: c++

    printh 92
    prints "text0",0
    printh 00
    prints text0.txt,0
    printh 00
    printh FF FF FF

*Explanation*

- ``printh 92`` Tells the library this is text sensor
- ``prints "text0",0`` Sends the name that matches **component_name** or **variable_name**
- ``printh 00`` Sends a NULL
- ``prints text0.txt,0`` The actual text to send. For a variable use the Nextion variable name ``text0`` with out ``.txt``
- ``printh 00`` Sends a NULL
- ``printh FF FF FF`` Nextion command ack


See Also
--------

- :doc:`/components/display/nextion`
- :doc:`index`
- :apiref:`nextion/text_sensor/nextion_textsensor.h`
- :ghedit:`Edit`
