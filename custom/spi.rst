Custom SPI Device
=================

.. esphome:component-definition::
   :alias: spi
   :category: additional-custom-components
   :friendly_name: Custom SPI Component
   :toc_group: Additional Custom Components
   :toc_image: language-cpp.svg

Lots of devices communicate using the SPI protocol. If you want to integrate
a device into ESPHome that uses this protocol you can pretty much use almost
all Arduino-based code because the ``SPI`` library is also available in ESPHome.

See the other custom component guides for how to register components and make
them publish values.

Please refer to the SPI library docs for more information.

.. code-block:: cpp

    #include "esphome.h"

    class MyCustomComponent : public Component {
     public:
      void setup() override {
        SPI.pins(SCK_PIN, MISO_PIN, MOSI_PIN, CS_PIN);
        SPI.begin();
      }
      void loop() override {
        SPI.beginTransaction(...)

        SPI.write(0x42);
      }
    };

See Also
--------

- :ghedit:`Edit`
