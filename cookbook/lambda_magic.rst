Lambda Magic
============

.. seo::
    :description: Recipes for various interesting things you can do with Lambdas in ESPHome
    :image: language-cpp.svg

Here are a couple recipes for various interesting things you can do with :ref:`Lambdas <config-lambda>` in ESPHome.
These things don't need external or custom components, and show how powerful :ref:`Lambda <config-lambda>` usage can be.

Send UDP commands
-----------------

There are various network devices which can be commanded with UDP packets containing command strings.
You can send such UDP commands from ESPHome using a Lambda in a script.

.. code-block:: yaml

	script:
	- id: send_udp
	  parameters:
		msg: string
		host: string
		port: int
	  then:
		- lambda: |-
			  int sock = ::socket(AF_INET, SOCK_DGRAM, 0);
			  struct sockaddr_in destination, source;

			  destination.sin_family = AF_INET;
			  destination.sin_port = htons(port);
			  destination.sin_addr.s_addr = inet_addr(host.c_str());

			  //you can remove the next 4 lines if you don't want to set the source port for outgoing packets
			  source.sin_family = AF_INET;
			  source.sin_addr.s_addr = htonl(INADDR_ANY);
			  source.sin_port = htons(64998); //source port number
			  bind(sock, (struct sockaddr*)&source, sizeof(source));

			  int n_bytes = ::sendto(sock, msg.c_str(), msg.length(), 0, reinterpret_cast<sockaddr*>(&destination), sizeof(destination));
			  ESP_LOGD("lambda", "Sent %s to %s:%d in %d bytes", msg.c_str(), host.c_str(), port, n_bytes);
			  ::close(sock);

	button:
	- platform: template
	  id: button_udp_sender
	  name: "Send UDP Command"
	  on_press:
		- script.execute:
			id: send_udp
			msg: "Hello World!"
			host: "192.168.1.10"
			port: 5000

Tested on both `arduino` and `esp-idf` platforms.

Custom UART Text Sensor
-----------------------

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

**Example usage**

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
- :ref:`lambda <config-lambda>`
- :ref:`automation`

- :ghedit:`Edit`
