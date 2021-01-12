.. _nextion_text_sensor:

Nextion Text Sensor Component
===============================

.. seo::
    :description: Instructions for setting up Nextion text sensor.
    :image: nextion.jpg
    :alt: nextion display

The ``nextion`` text sensor platform supports intergers. It can be a component or variable in the Nextion display.
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
      hass_component_name: textoutput.txt
      nextion_component_name: text0

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **nextion_id** (*Optional*, :ref:`config-id`): The ID of the Nextion display.
- **nextion_component_name** (*Optional*, string): The name of the Nextion component.
- **nextion_variable_name** (*Optional*, string): The name of the Nextion variable. Any value over ``0`` is considerd to be **on**
- **update_interval** (*Optional*, :ref:`config-time`):  The duration to update the sensor
- **hass_component_name** (*Optional*, :ref:`config-time`):  Sets the HASS name. It will watch for changes this HASS entity and update the Nextion sensor accordingly.
- All other options from :ref:`Text Sensor <config-text_sensor>`.

**Only one** *nextion_component_name* **or** *nextion_variable_name* **can be set**

See :ref:`nextion_text_sensor_how_things_update` for additional information

Globals
*******
The Nextion does not retain data on Nextion page changes. Additionaly if a page is changed and the **nextion_component_name** does not exist on that page then
nothing will be updated. To get around this the Nextion components can be changed to have a vscope of ``global``. If this is set then the **nextion_component_name**
should be prefixed with the page name (page0/page1).

*Example*

  ``nextion_component_name: page0.text0``

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods do some
advanced stuff (see the full API Reference for more info).

.. _nextion_text_sensor_set_state:

- ``set_state(std::string state)``: Set the state :ref:`sensor-lambda_calls`

.. _nextion_text_sensor_update:

- ``update()``: Poll from the Nextion :ref:`sensor-lambda_calls`


.. _nextion_text_sensor_how_things_update:

How things Update
-----------------
A Nextion component with and interger value (.val) or Nextion variable will be automatically polled if **update_interval** is set.
To have the Nextion send the data you can use the :ref:`nextion_custom_text_sensor_protocol` for this. Add the :ref:`nextion_custom_text_sensor_protocol` to the 
component or function you want to trigger the send. Typically this is in *Touch Press Event* but some components, like a slider, should have it 
set in the *Touch Release Event* to capture all the changes. Since this is a custom protocol it can be sent from anywhere (timers/functions/componenets)
in the Nextion. 

.. note::

There is no need to check the *Send Component ID* for the *Touch Press Event* or *Touch Release Event*
since this will be sending the real value to esphome.


On startup esphome will retrieve the value from the Nextion for any component even if **update_interval** is set or not.

Using the above yaml example:  
  - "text0" will poll the Nextion for ``text0.txt`` value and set the state accordingly.  

    - :ref:`nextion_text_sensor_set_state` 
    - :ref:`nextion_text_sensor_update` 

.. _nextion_custom_text_sensor_protocol:

Nextion Custom Sensor Protocol
------------------------------
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
- ``prints "text0",0`` Sends the name that matches **nextion_component_name** or **nextion_variable_name**
- ``printh 00`` Sends a NULL
- ``prints text0.txt,0`` The actual text to send. For a variable use the Nextion variable name ``text0`` with out ``.txt``
- ``printh 00`` Sends a NULL
- ``printh FF FF FF`` Nextion command ack


See Also
--------

- :doc:`/components/display/nextion`
- :doc:`index`
- :apiref:`nextion/nextion_textsensor.h`
- :ghedit:`Edit`

