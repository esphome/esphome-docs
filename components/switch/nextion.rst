.. _nextion_switch:

Nextion Switch Component
===============================

.. seo::
    :description: Instructions for setting up Nextion Switch.
    :image: nextion.jpg
    :alt: nextion display

The ``nextion`` switch platform supports the many switched components in the Nextion as well as integer variables. It can be a component or variable in the Nextion display.
It is best to set the components vscope to global in the Nextion Editor. This way the component will be available if the page is shown or not. 

See :doc:`/components/display/nextion` for setting up the display

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: nextion
        id: nextion1
        # ...

    switch:      
      - platform: nextion
        id: r0_switch
        name: "Radio 0 Switch"
        nextion_component_name: r0 # pageX.r0 for a global
        update_interval: 4s
      - platform: nextion
        id: darkmode
        name: "Is Darkmode Set"
        nextion_variable_name: darkmode

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **nextion_id** (*Optional*, :ref:`config-id`): The ID of the Nextion display.
- **nextion_component_name** (*Optional*, string): The name of the Nextion component.
- **nextion_variable_name** (*Optional*, string): The name of the Nextion variable. Any value over ``0`` is considerd to be **on**
- **update_interval** (*Optional*, :ref:`config-time`):  The duration to update the sensor
- All other options from :ref:`Switch <config-switch>`.

**Only one** *nextion_component_name* **or** *nextion_variable_name* **can be set**

See :ref:`nextion_switch_how_things_update` for additional information

Globals
*******
The Nextion does not retain data on Nextion page changes. Additionaly if a page is changed and the **nextion_component_name** does not exist on that page then
nothing will be updated. To get around this the Nextion components can be changed to have a vscope of ``global``. If this is set then the **nextion_component_name**
should be prefixed with the page name (page0/page1).

*Example*

``nextion_component_name: page0.r0``

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods do some
advanced stuff (see the full API Reference for more info).

.. _nextion_switch_set_state:

- ``set_state(bool value)``: Set the state :ref:`sensor-lambda_calls`

.. _nextion_switch_update:

- ``update()``: Poll from the Nextion :ref:`sensor-lambda_calls`


.. _nextion_switch_how_things_update:

How things Update
-----------------
A Nextion component with and interger value (.val) or Nextion variable will be automatically polled if **update_interval** is set.
To have the Nextion send the data you can use the :ref:`nextion_custom_switch_protocol` for this. Add the :ref:`nextion_custom_switch_protocol` to the 
component or function you want to trigger the send. Typically this is in *Touch Press Event* but some components, like a slider, should have it 
set in the *Touch Release Event* to capture all the changes. Since this is a custom protocol it can be sent from anywhere (timers/functions/componenets)
in the Nextion. 

.. note::

There is no need to check the *Send Component ID* for the *Touch Press Event* or *Touch Release Event*
since this will be sending the real value to esphome.


On startup esphome will retrieve the value from the Nextion for any component even if **update_interval** is set or not.

Using the above yaml example:  
  - "Radio 0 switch" will poll the Nextion for the ``r0.val`` value and set the state accordingly.
  - "Is Darkmode Set" will NOT poll the Nextion. Either the Nextion will need to use the :ref:`nextion_custom_switch_protocol` or use a lambda:

    - :ref:`nextion_switch_set_state` 
    - :ref:`nextion_switch_update` 

.. _nextion_custom_switch_protocol:

Nextion Custom Sensor Protocol
------------------------------
All lines are required

.. code-block:: c++

    printh 90
    prints "r0",0
    printh 00
    prints r0.val,0
    printh FF FF FF

*Explanation*

- ``printh 90`` Tells the library this is a switch bool/integer data
- ``prints "r0",0`` Sends the name that matches **nextion_component_name** or **nextion_variable_name**
- ``printh 00`` Sends a NULL
- ``prints r0.val,0`` The actual value to send. For a variable use the Nextion variable name ``r0`` with out ``.val``
- ``printh FF FF FF`` Nextion command ack


See Also
--------

- :doc:`/components/display/nextion`
- :doc:`index`
- :apiref:`nextion/nextion_switch.h`
- :ghedit:`Edit`

