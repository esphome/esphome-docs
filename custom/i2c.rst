Custom I²C Device
=================

Lots of devices communicate using the I²C protocol. If you want to integrate
a device into ESPHome that uses this protocol you can pretty much use almost
all Arduino-based code because the ``Wire`` library is also available in ESPHome.

The following firmware example writes a constant value to a slave register inside an un-timed loop:

.. code-block:: cpp

    #include "esphome.h"

    class MyCustomComponent : public Component {
     public:
      void setup() override {
        // Initialize the device. Usually Wire.begin() will be called in here,
        // though that call is unnecessary if you have an 'i2c:' entry in your config

        Wire.begin();
      }
      void loop() override {
        // Example: write the value 0x42 to register 0x78 of device with address 0x21
        Wire.beginTransmission(0x21);
        Wire.write(0x78);
        Wire.write(0x42);
        Wire.endTransmission();
      }
    };


Dashboard Interfacing: I²C Write
--------------------------------
It may be useful to write to the slave register via I²C using a numerical input from the dashboard. For example, the following yaml code snippet captures a user-supplied numerical input in the range 1--255:

.. code-block:: yaml

    number:
        - platform: template
        name: "Input 1"
        optimistic: true
        min_value: 1
        max_value: 255
        initial_value: 20
        step: 1
        mode: box
        id: input_1
        icon: "mdi:counter"
        
We want to write this number to a ``REGISTER_ADDRESS`` on the slave device via I²C. The Arduino-based looping code shown above is modified following the guidance in :doc:`Custom Sensor Component </components/sensor/custom>`.
 
.. code-block:: cpp

    #include "esphome.h"
 
    const uint16_t I2C_ADDRESS = 0x21;
    const uint16_t REGISTER_ADDRESS = 0x78; 
    const uint16_t POLLING_PERIOD = 15000; //milliseconds
    char temp = 20; //Initial value of the register

    class MyCustomComponent : public PollingComponent {
     public:
      MyCustomComponent() : PollingComponent(POLLING_PERIOD) {}
      float get_setup_priority() const override { return esphome::setup_priority::BUS; } //Access I2C bus

      void setup() override {
        //Add code here as needed
        Wire.begin();
        }
  
      void update() override {  
      char register_value = id(input_1).state; //Read the number set on the dashboard
      //Did the user change the input?
      if(register_value != temp){
            Wire.beginTransmission(I2C_ADDRESS);
            Wire.write(REGISTER_ADDRESS);
            Wire.write(register_value);
            Wire.endTransmission();
            temp = register_value; //Swap in the new value
            }
            }
    };
        
The ``Component`` class has been replaced with ``PollingComponent`` and the free-running ``loop()`` is changed to the  ``update()`` method with period set by ``POLLING_PERIOD``. The numerical value from the dashboard is accessed with its ``id`` tag and its state is set to the byte variable that we call ``register_value``.  To prevent an I²C write on every iteration, the contents of the register are stored in ``temp`` and checked for a change. Configuring the hardware with ``get_setup_priority()`` is explained in :doc:`Step 1 </components/sensor/custom>`.

Dashboard Interfacing: I²C Read
--------------------------------
To read and display data from a sensor that is slave on the I²C bus, it is instantiated as explained in :doc:`Step 2 </components/sensor/custom>`. In the  yaml file below, three register values on the slave are made available to the dashboard:

.. code-block:: yaml

    sensor:
    - platform: custom
    lambda: |-
        auto my_sensor = new MyCustomComponent();
        App.register_component(my_sensor);
        return {my_sensor->register_value_1,my_sensor->register_value_2,my_sensor->register_value_3};

    sensors:
    - name: "Data 1 Display" 
    - name: "Data 2 Display"
    - name: "Data 3 Display"

The timed polling loop is modified to periodically retrieve three sequential data bytes beginning at ``REGISTER_ADDRESS``. Three pointers are defined to publish the data bytes:

.. code-block:: cpp

    #include "esphome.h"

    const uint16_t I2C_ADDRESS = 0x21;
    const uint16_t REGISTER_ADDRESS = 0x78;
    const uint16_t POLLING_PERIOD = 15000; //milliseconds
    static char Data_array[3];

    class MyCustomComponent : public PollingComponent {
        public:
        Sensor *register_value_1 = new Sensor();
        Sensor *register_value_2 = new Sensor();
        Sensor *register_value_3 = new Sensor();
    MyCustomComponent() : PollingComponent(update_interval) {}  
    float get_setup_priority() const override { return esphome::setup_priority::BUS; } //Access I2C bus

    void setup() override {
    //Add code here as needed
    Wire.begin();
    }

    void update() override { 
    // Read 3 bytes in sequence starting at REGISTER_ADDRESS
        Wire.beginTransmission(I2C_ADDRESS);
        Wire.write(REGISTER_ADDRESS);
        Wire.endTransmission(); // End write; starting register address is now specified
        Wire.requestFrom(I2C_ADDRESS, 3); 
        //Could also do this in a loop
        Data_array[0]=Wire.read(); 
        Data_array[1]=Wire.read(); 
        Data_array[2]=Wire.read();       
        //Publish the sensor data on the Home Assistant GUI
        register_value_1->publish_state(Data_array[0]);
        register_value_2->publish_state(Data_array[1]);
        register_value_3->publish_state(Data_array[2]);
        }
      };

See Also
--------

- :ghedit:`Edit`
