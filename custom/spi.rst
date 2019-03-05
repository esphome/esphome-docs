Custom SPI Device
=================

Lots of devices communicate using the SPI protocol. If you want to integrate
a device into ESPHome that uses this protocol you can pretty much use almost
all Arduino-based code because the ``SPI`` library is also available in ESPHome.

See the other custom component guides for how to register components and make
them publish values.

.. code-block:: cpp

    #include "esphome.h"
    using namespace esphome;

    class MyCustomComponent : public Component {
     public:
      void setup() override {
        SPI.pins(SCK_PIN, MISO_PIN, MOSI_PIN);
        SPI.begin();

        pinMode(CS_PIN, OUTPUT);
      }
      void loop() override {
        digitalWrite(CS_PIN, LOW);
        SPI.beginTransaction(...);

        SPI.write(0x42);

        digitalWrite(CS_PIN, HIGH);
      }
    };

See Also
--------

- :ghedit:`Edit`
