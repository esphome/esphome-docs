Custom UART Text Sensor
=======================

.. seo::
    :description: Instructions for setting up a custom uart text sensor.
    :image: language-cpp.png

Lots of devices communicate using the UART protocol. If you want to read 
lines from uart to a Text Sensor you can do so using this code example.

With this you can use automations or lambda to set switch or sensor states.

.. code-block:: cpp

    #include "esphome.h"

    class UartReadLineSensor : public Component, public UARTDevice, public TextSensor {
     public:
      UartReadLineSensor(UARTComponent *parent) : UARTDevice(parent) {}    

      void setup() override {
        // nothing to do here
      }    

      int readline(int readch, char *buffer, int len)
      {
        static int pos = 0;
        int rpos;
      
        if (readch > 0) {
          switch (readch) {
            case '\n': // Ignore new-lines
              break;
            case '\r': // Return on CR
              rpos = pos;
              pos = 0;  // Reset position index ready for next time
              return rpos;
            default:
              if (pos < len-1) {
                buffer[pos++] = readch;
                buffer[pos] = 0;
              }
          }
        }
        // No end of line has been found, so return -1.
        return -1;
      }    

      void loop() override {
        const int max_line_length = 80;
        static char buffer[max_line_length];
        while (available()) {
          if(readline(read(), buffer, max_line_length) > 0) {
            publish_state(buffer);
          }
        }
      }
    };

(Store this file in your configuration directory, for example ``uart_read_line_sensor.h``)
    
And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphome:
      includes:
        - uart_read_line_sensor.h
    
    logger:
      level: VERBOSE #makes uart stream available in esphome logstream
      baud_rate: 0 #disable logging over uart

    uart:
      id: uart_bus
      tx_pin: D0
      rx_pin: D1
      baud_rate: 9600

    text_sensor:
    - platform: custom
      lambda: |-
        auto my_custom_sensor = new UartReadLineSensor(id(uart_bus));
        App.register_component(my_custom_sensor);
        return {my_custom_sensor};
      text_sensors:
        id: "uart_readline"

Example usage
-------------

Here is an example switch using the uart text sensor to set switch state.

Here we use interval to request status from the device. The response will be stored in uart text sensor.
Then the switch uses the text sensor state to set its own state.

.. code-block:: yaml

    switch:
      - platform: template
        name: "Switch"
        lambda: |-
          if (id(uart_readline).state == "*POW=ON#") {
            return true;
          } else if(id(uart_readline).state == "*POW=OFF#") {
            return false;
          } else {
            return {};
          }
        turn_on_action:
          - uart.write: "\r*pow=on#\r"
        turn_off_action:
          - uart.write: "\r*pow=off#\r"
    
    interval:
      - interval: 10s
        then:
          - uart.write: "\r*pow=?#\r"

See Also
--------

- :doc:`/components/uart`
- :doc:`/custom/uart`
- :ghedit:`Edit`
