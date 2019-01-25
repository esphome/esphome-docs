Custom SPI Device
=================

Lots of devices communicate using the SPI protocol. If you want to integrate
a device into esphomelib that uses this protocol you can pretty much use almost
all Arduino-based code because the ``SPI`` library is also available in esphomelib.

See the other custom component guides for how to register components and make
them publish values.

.. code-block:: cpp

    #include "esphomelib.h"
    using namespace esphomelib;

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

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/custom/spi.rst>`__

.. disqus::
