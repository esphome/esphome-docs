Custom I²C Device
=================

.. esphome:component-definition::
   :alias: i2c
   :category: additional-custom-components
   :friendly_name: Custom I²C Component
   :toc_group: Additional Custom Components
   :toc_image: language-cpp.svg

Lots of devices communicate using the I²C protocol. If you want to integrate
a device into ESPHome that uses this protocol you can pretty much use almost
all Arduino-based code because the ``Wire`` library is also available in ESPHome.

See the other custom component guides for how to register components and make
them publish values.

.. code-block:: cpp

    #include "esphome.h"

    class MyCustomComponent : public Component {
     public:
      void setup() override {
        // Initialize the device here. Usually Wire.begin() will be called in here,
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

See Also
--------

- :ghedit:`Edit`
