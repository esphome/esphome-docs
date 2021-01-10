Custom SPI Device
=================

Lots of devices communicate using the SPI protocol. If you want to integrate
a device into ESPHome that uses this protocol you can pretty much use almost
all Arduino-based code because the ``SPI`` library is also available in ESPHome.

See the other custom component guides for how to register components and make
them publish values.

Please refer to the SPI library docs for more information.

.. code-block:: cpp
#include "esphome.h"


class MyCustomComponent : public Component, public spi::SPIDevice<spi::BIT_ORDER_MSB_FIRST, spi::CLOCK_POLARITY_LOW,
                                                 spi::CLOCK_PHASE_LEADING, spi::DATA_RATE_2MHZ>{
 public:
  void setup() override {
    
    this->spi_setup();
  }
  void loop() override {
    
    this->enable();
    //this->write_byte(....);
    this->disable();
  }
};

See Also
--------

- :ghedit:`Edit`
