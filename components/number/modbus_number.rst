Modbus Number
=============

.. seo::
    :description: Instructions for setting up a modebus_controller device sensor.
    :image: modbus_controller.png

The ``modbus_controller`` platform creates a Number from a modbus_controller and a modbus sensor.
A Modbus Number is always connected to a :doc:`Modbus Sensor </components/sensor/modbus_sensor>`.When the Number is updated a modbus write command is created using the address and register type of the modbus_sensor.
If the command succeeds the connected sensor is updated with the new value.

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **modbus_controller_id** (**Required**): type of the modbus register.
- **modbus_sensor_id**: (**Required**): start address of the first register in a range
- **min_value** (**Optional**, float): The minimum value this number can be.
- **max_value** (**Optional**, float): The maximum value this number can be.
- **step** (**Optional**, float): The granularity with which the number can be set. Defaults to 1
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): Lambda called before send.
  Lambda is evaluated before the modbus write command is created. 
- **multiply** (**Optional**, float): multiply the new value with this factor before sending the requests. Ignored if lambda is defined.


All other options from :ref:`Number <config-number>`.


**Parameters passed into the lambda**

- **x** (float): The float value to be sent to the modbus device

- **payload** (`std::vector<uint16_t>&payload`): empty vector for the payload. The lamdba can add 16 bit raw modbus register words.
      note: because the response contains data for all registers in the same range you have to use `data[item->offset]` to get the first response byte for your sensor.
- **item** (const pointer to a SensorItem derived object):  The sensor object itself.

Possible return values for the lambda:

 - ``return <FLOATING_POINT_NUMBER>;`` the new value for the sensor.
 - ``return <anything>; and fill payload with data`` if the payload is added from the lambda then these 16 bit words will be sent
 - ``return {};`` if you don't want write the command to the device (or do it from the lambda).

**Example**

.. code-block:: yaml

    sensor:
      - platform: modbus_controller
        modbus_controller_id: epever
        id: battery_capacity
        address: 0x9001
        name: "Battery Capacity"
        register_type: holding
        value_type: U_WORD

    number:
      - platform: modbus_controller
        modbus_controller_id: epever
        modbus_sensor_id: epever      
        id: battery_capacity_number
        name: "Battery Cap Number"
        lambda: !lambda |-
          ESP_LOGD("main lambda","Modbus Number incoming value = %f",x);
          uint16_t b_capacity = x ; 
          // add the payload directly 
          payload.push_back(b_capacity);
          // ignored because payload is set
          return x * 1.0 ;
        # ignored because lambda is defined
        multiply: 100.0


See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_sensor`
- :doc:`/components/binary_sensor/modbus_binarysensor`
- :doc:`/components/switch/modbus_switch`
- :doc:`/components/text_sensor/modbus_textsensor`
- :doc:`/components/output/modbus_output`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
