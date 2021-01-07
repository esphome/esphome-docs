.. _nextion_binary_sensor:

Nextion Binary Sensor Component
===============================

.. seo::
    :description: Instructions for setting up Nextion binary sensor.
    :image: nextion.jpg

The ``nextion`` binary sensor platform supports intergers. It can be a component or variable in the Nextion display.
It is best to set the components vscope to global in the Nextion Editor. This way the component will be available
if the page is shown or not. 

See :doc:`/components/display/nextion` for setting up the display

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: nextion
        id: nextion1
        # ...

    binary_sensor:
      - platform: nextion
        page_id: 0
        component_id: 8
        id: "mode"
      - platform: nextion
        id: r0_binary_sensor
        name: "Radio 0 Binary Sensor"
        nextion_component_name: r0 # pageX.r0 for a global
        update_interval: 4s
      - platform: nextion
        id: darkmode
        name: "Is Darkmode Set"
        nextion_variable_name: darkmode

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **nextion_id** (**Required**, :ref:`config-id`): The ID of the Nextion display.
- **nextion_component_name** (*Optional*, string): The name of the Nextion component.
- **nextion_variable_name** (*Optional*, string): The name of the Nextion variable. Any value over ``0`` is considerd to be **on**
- **page_id** (*Optional*, string): The ID of the page the component is on. Use ``0`` for the default page.
- **component_id** (*Optional*, string): The ID (the number, not name!) of the component to track.
- **update_interval** (*Optional*, :ref:`config-time`):  The duration to update the sensor
- All other options from :ref:`Sensor <config-sensor>`.

The Nextion will send a **page_id** and **component_id** when the *Send Component ID* check box is selected for the component. To enable 
this native event **page_id** and **component_id** are required. No :ref:`nextion_custom_binary_sensor_protocol` is required

**Only one** *nextion_component_name* **or** *nextion_variable_name* **can be set** and can not be mixed with **page_id** or **component_id**

See :ref:`nextion_binary_sensor_how_things_update` for additional information

Globals
*******
The Nextion does not retain data on Nextion page changes. Additionaly if a page is changed and the **nextion_component_name** does not exist on that page then
nothing will be updated. To get around this the Nextion components can be changed to have a vscope of ``global``. If this is set then the **nextion_component_name**
should be prefixed with the page name (page0/page1).

*Example*

  ``nextion_component_name: page0.humidity``

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods do some
advanced stuff (see the full API Reference for more info).

.. _nextion_binary_sensor_set_state:

- ``set_state(bool value)``: Set the state :ref:`sensor-lambda_calls`

.. _nextion_binary_sensor_update:

- ``update()``: Poll from the Nextion :ref:`sensor-lambda_calls`


.. _nextion_binary_sensor_how_things_update:

How things Update
-----------------
A Nextion component with and interger value (.val) or Nextion variable will be automatically polled if **update_interval** is set.
To have the Nextion send the data you can use the :ref:`nextion_custom_binary_sensor_protocol` for this. Add the :ref:`nextion_custom_binary_sensor_protocol` to the 
component or function you want to trigger the send. Typically this is in *Touch Press Event* but some components, like a slider, should have it 
set in the *Touch Release Event* to capture all the changes. Since this is a custom protocol it can be sent from anywhere (timers/functions/componenets)
in the Nextion. 

.. note::

There is no need to check the *Send Component ID* for the *Touch Press Event* or *Touch Release Event*
since this will be sending the real value to esphome.


On startup esphome will retrieve the value from the Nextion for any component even if **update_interval** is set or not.

Using the above yaml example:
  - "mode" is a touch sensor and will trigger when a user presess the component with ID ``8`` in page ``0``
  - "Radio 0 Binary Sensor" will poll the Nextion for the *r0.val* value and set the state accordingly.
  - "Is Darkmode Set" will NOT poll the Nextion. Either the Nextion will need to use the :ref:`nextion_custom_binary_sensor_protocol` or use a lambda:

    - :ref:`nextion_binary_sensor_set_state` 
    - :ref:`nextion_binary_sensor_update` 

.. _nextion_custom_binary_sensor_protocol:

Nextion Custom Sensor Protocol
------------------------------
All lines are required

.. code-block:: c++

    printh 93
    prints "r0",0
    printh 00
    prints r0.val,0
    printh FF FF FF

*Explanation*

- ``printh 93`` Tells the library this is binary sensor bool/integer data
- ``prints "r0",0`` Sends the name that matches **nextion_component_name** or **nextion_variable_name**
- ``printh 00`` Sends a NULL
- ``prints r0.val,0`` The actual value to send. For a variable use the Nextion variable name ``r0`` with out ``.val``
- ``printh FF FF FF`` Nextion command ack


See Also
--------

- :doc:`/components/display/nextion`
- :doc:`index`
- :apiref:`nextion/nextion_binarysensor.h`
- :ghedit:`Edit`

