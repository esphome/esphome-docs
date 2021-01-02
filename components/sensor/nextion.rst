.. _nextion_sensor:

Nextion Sensor Component
========================

.. seo::
    :description: Instructions for setting up Nextion sensor.
    :image: nextion.jpg

The ``nextion`` sensor platform supports intergers. It can be a component or variable in the Nextion display.
It is best to set the components vscope to global in the Nextion Editor. This way the component will be available
if the page is shown or not. 

See :doc:`/components/display/nextion` for setting up the display

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: nextion
        id: nextion1
        # ...

    sensor:
      - platform: nextion
        nextion_id: nextion1        
        name: "Current Humidity"
        component_name: humidity
        update_interval: 4s
      - platform: nextion
        nextion_id: nextion1        
        name: "Current Temperature"
        variable_name: temperature

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **nextion_id** (**Required**, :ref:`config-id`): Manually specify the ID of the Nextion display.
- **component_name** (*Optional*, string): Manually specify the name of the Nextion component.
- **variable_name** (*Optional*, string): Manually specify the name of the Nextion variable.
- **update_interval** (*Optional*, :ref:`config-time`):  The duration to update the sensor
- All other options from :ref:`Sensor <config-sensor>`.

**Only one** *component_name* **or** *update_interval* **can be set**

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods do some
advanced stuff (see the full API Reference for more info).

.. _nextion_sensor_publish_state:

- ``publish_state(value)``: Set the state :ref:`sensor-lambda_calls`

.. _nextion_sensor_update:

- ``update()``: Poll from the Nextion :ref:`sensor-lambda_calls`

How things Update
-----------------
A Nextion component (Number) or Nextion variable will be automatically polled if **update_interval** is set.
To have the Nextion send the data you can use the :ref:`nextion_custom_sensor_protocol` for this. Add the custom lines to the 
component you want to trigger the send. Typically this is in *Touch Press Event* but some components, like a slider, should have it 
set in the *Touch Release Event* to capture all the changes. There is no need to check the *Send Component ID* for the *Touch Press Event* or *Touch Release Event*
since this will be sending the real value to esphome. Note this can be any component or code.

On startup esphome will retrieve the value from the Nextion for any component even if **update_interval** is set or not.

Using the above yaml example:
  - "Current Humidity" will poll the Nextion for the *humidity.val* value and set the sensor accordingly.
  - "Current Temperature" will NOT poll the Nextion. Either the Nextion will need to use the :ref:`nextion_custom_sensor_protocol` or use a lambda:

    - :ref:`nextion_sensor_update` 
    - :ref:`nextion_sensor_publish_state` 

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


- **printh 91** Tells the library this is sensor (int) data
- **prints "temperature",0** Sends the name
- **printh 00** NULL
- **prints temperature.val,0** The actual value to send
- **printh FF FF FF** Nextion command ack


See Also
--------

- :doc:`/components/display/nextion`
- :doc:`index`
- :apiref:`nextion/nextion.h`
- :ghedit:`Edit`

