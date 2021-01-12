.. _nextion_sensor:

Nextion Sensor Component
========================

.. seo::
    :description: Instructions for setting up Nextion sensor.
    :image: nextion.jpg    

The ``nextion`` sensor platform supports intergers. It can be a component or variable in the Nextion display.
It is best to set the components vscope to global in the Nextion Editor. This way the component will be available
if the page is shown or not. 

.. note::

    The Nextion can receive an interger but it can only send 3 bytes for a negative integer. The range if using the :ref:`nextion_custom_sensor_protocol` is:
        -16777215 to 4294967295

See :doc:`/components/display/nextion` for setting up the display

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: nextion
        id: nextion1
        # ...

    sensor:
      - platform: nextion        
        name: "Current Humidity"
        nextion_component_name: humidity # pageX.humidity for a global
        nextion_precision: 1
        update_interval: 4s
      - platform: nextion
        nextion_id: nextion1        
        name: "Current Temperature"
        nextion_variable_name: temperature
        hass_component_name: sensor.temperature

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **nextion_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the Nextion display.
- **nextion_component_name** (*Optional*, string): Manually specify the name of the Nextion component.
- **nextion_variable_name** (*Optional*, string): Manually specify the name of the Nextion variable.
- **update_interval** (*Optional*, :ref:`config-time`):  The duration to update the sensor
- **nextion_precision** (*Optional*, uint8_t):  This is for Nextion float components. This sets 
  the precision that the component is set to. This typically is the ``vvs1`` setting of the component.                                                         
- **hass_component_name** (*Optional*, :ref:`config-time`):  Sets the HASS name. It will watch for changes this HASS entity and update the Nextion sensor accordingly.
- All other options from :ref:`Sensor <config-sensor>`.

**Only one** *nextion_component_name* **or** *nextion_variable_name* **can be set**

See :ref:`nextion_sensor_how_things_update` for additional information

Globals
*******
The Nextion does not retain data on Nextion page changes. Additionaly if a page is changed and the **nextion_component_name** does not exist on that page then
nothing will be updated. To get around this the Nextion components can be changed to have a vscope of ``global``. If this is set then the **nextion_component_name**
should be prefixed with the page name (page0/page1).

*Example*

``nextion_component_name: page0.humidity``

.. _nextion_sensor_lambda_calls:

Lambda Calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods do some
advanced stuff (see the full API Reference for more info).

.. _nextion_sensor_set_state:

- ``set_state(int value)``: Set the state :ref:`sensor-lambda_calls`

.. _nextion_sensor_update:

- ``update()``: Poll from the Nextion :ref:`sensor-lambda_calls`

.. _nextion_sensor_how_things_update:

How things Update
-----------------
A Nextion component with and interger value (.val) or Nextion variable will be automatically polled if **update_interval** is set.
To have the Nextion send the data you can use the :ref:`nextion_custom_sensor_protocol` for this. Add the :ref:`nextion_custom_sensor_protocol` to the 
component or function you want to trigger the send. Typically this is in *Touch Press Event* but some components, like a slider, should have it 
set in the *Touch Release Event* to capture all the changes. Since this is a custom protocol it can be sent from anywhere (timers/functions/componenets)
in the Nextion. 

.. note::

    There is no need to check the *Send Component ID* for the *Touch Press Event* or *Touch Release Event*
    since this will be sending the real value to esphome.

On startup esphome will retrieve the value from the Nextion for any component even if **update_interval** is set or not.

Using the above yaml example:
  - "Current Humidity" will poll the Nextion for the ``humidity.val`` value and set the sensor accordingly.
  - "Current Temperature" will NOT poll the Nextion. Either the Nextion will need to use the :ref:`nextion_custom_sensor_protocol` or use a lambda:

    - :ref:`Lambda Calls <nextion_sensor_lambda_calls>`.  

.. _nextion_custom_sensor_protocol:

Nextion Custom Sensor Protocol
------------------------------
All lines are required

.. code-block:: c++

    printh 91
    prints "temperature",0
    printh 00
    prints temperature.val,0
    printh FF FF FF

*Explanation*

- ``printh 91`` Tells the library this is a sensor (int) data
- ``prints "temperature",0`` Sends the name that matches **nextion_component_name** or **nextion_variable_name**
- ``printh 00`` Sends a NULL
- ``prints temperature.val,0`` The actual value to send. For a variable use the Nextion variable name ``temperature`` with out ``.val``
- ``printh FF FF FF`` Nextion command ack


See Also
--------

- :doc:`/components/display/nextion`
- :doc:`index`
- :apiref:`nextion/nextion_sensor.h`
- :ghedit:`Edit`

