Custom UART Device
==================

Lots of devices communicate using the UART protocol. If you want to integrate
a device into esphomelib that uses this protocol you can pretty much use almost
all Arduino-based code because esphomelib has a nice abstraction over the UART bus.

See the other custom component guides for how to register components and make
them publish values.

.. code-block:: cpp

    #include "esphomelib.h"
    using namespace esphomelib;

    class MyCustomComponent : public Component, public UARTDevice {
     public:
      MyCustomComponent(UARTComponent *parent) : UARTDevice(parent) {}

      void setup() override {
        // nothing to do here
      }
      void loop() override {
        // Use Arduino API to read data, for example
        String line = readString();
        int i = parseInt();
        while (available()) {
          char c = read();
        }
        // etc
      }
    };

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      includes:
        - my_custom_component.h

    uart:
      id: uart_bus
      tx_pin: D0
      rx_pin: D1
      baud_rate: 9600

    custom_component:
    - lambda: |-
        auto my_custom = new MyCustomComponent(id(uart_bus));
        return {my_custom};

See Also
--------

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/custom/uart.rst>`__

.. disqus::
