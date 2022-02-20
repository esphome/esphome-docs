Sim800L Component
=================

.. seo::
    :description: Instructions for setting up the SIM800L GSM module to dial, send and receive SMS in ESPHome.
    :image: sim800l.jpg
    :keywords: SMS SIM800L GSM

The ``SIM800L`` Component provides the ability to dial, send and receive SMS text messages. The device must be
connected via a :doc:`UART bus </components/uart>` supporting both receiving and transmitting line.
The UART bus must be configured at the same speed of the module which is by default 9600bps.
The required connection wires are ``+VCC``, ``GND``, ``RX`` and ``TX``.

.. warning::

    If you are using the :doc:`logger` make sure you are not using the same pins for ``TX`` and ``RX`` or
    otherwise disable the UART logging with the ``baud_rate: 0`` option.

.. note::

    This module requires a power supply between 3.8V and 4.2V that can handle current spikes up
    to 2 amps, it will not work by powering from the same 3.3V power source of the ESP. However you can
    connect ``TX`` and ``RX`` lines directly without any level shifter.

.. figure:: images/sim800l-full.jpg
    :align: center
    :width: 60.0%

.. code-block:: yaml

    # Example configuration entry
    uart:
      baud_rate: 9600
      tx_pin: TX
      rx_pin: RX

    sim800l:
      on_sms_received:
        - logger.log:
            format: "Received '%s' from %s"
            args: [ 'message.c_str()', 'sender.c_str()' ]

    logger:
      baud_rate: 0 # disable uart logger on esp 8266

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the UART hub.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **on_sms_received** (*Optional*, :ref:`Automation <automation>`): An action to be
  performed when an SMS is received. See :ref:`sim800l-on_sms_received`.

.. _sim800l-on_sms_received:

``on_sms_received`` Trigger
---------------------------

With this configuration option you can write complex automations whenever an SMS message
is received. To use the message content, use a :ref:`lambda <config-lambda>`
template, the message content and the sender phone number are available inside that lambda
under the variables named ``message`` and ``sender`` respectively.

.. code-block:: yaml

    on_sms_received:
      - lambda: |-
          id(sms_sender).publish_state(sender);
          id(sms_message).publish_state(message);


.. _sim800l-send_sms_action:

``sim800l.send_sms`` Action
---------------------------

Send a SMS message to a phone recipient using this action in automations.

.. code-block:: yaml

    on_...:
      then:
        - sim800l.send_sms:
            recipient: '+15551234567'
            message: Hello there

        # Templated:
        - sim800l.send_sms:
            recipient: !lambda |-
              if (id(reed_switch).state) return "+15551234567";
              else return "15551234568";
            message: !lambda |-
              return id(reed_switch).state ? "Door is now OPEN" : "Hey door just CLOSED";


.. _sim800l-dial_action:

``sim800l.dial`` Action
---------------------------

Dial to a phone recipient using this action in automations.

.. code-block:: yaml

    on_...:
      then:
        - sim800l.dial:
            recipient: '+15551234567'

Configuration options:

- **recipient** (***Required**, string, :ref:`templatable <config-templatable>`): The number to dial.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID of the SIM800L if you have multiple components.

.. note::

    This action can also be written in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        id(sim800l1).dial("+15551234567");


Getting started with Home Assistant
-----------------------------------

The following code will get you up and running with a configuration updating received messages
on Home Assistant and will also setup a service so you can send messages and dial with your SIM800L.

.. code-block:: yaml

    api:
      services:
      - service: send_sms
        variables:
          recipient: string
          message: string
        then:
        - sim800l.send_sms:
            recipient: !lambda 'return recipient;'
            message: !lambda 'return message;'
      - service: dial
        variables:
          recipient: string
        then:
        - sim800l.dial:
            recipient: !lambda 'return recipient;'

    text_sensor:
    - platform: template
      id: sms_sender
      name: "Sms Sender"
    - platform: template
      id: sms_message
      name: "Sms Message"

    uart:
      baud_rate: 9600
      tx_pin: TX
      rx_pin: RX

    sim800l:
      on_sms_received:
      - lambda: |-
          id(sms_sender).publish_state(sender);
          id(sms_message).publish_state(message);

Now your latest received SMS and sender number will be displayed by the text sensors.

To trigger the automation from Home Assistant you can invoke the service with this code:

.. code-block:: yaml

    automation:
      # ...
      action:
      - service: esphome.livingroom_send_sms
        data:
          recipient: "+15551234567"
          message: "Hello World!"
      - service: esphome.livingroom_dial
        data:
          recipient: "+15551234567"


Relay management commands received from an authorized sender:

.. code-block:: yaml

    sim800l:
      on_sms_received:
      - lambda: |-
          if ( (id(sms_sender).state == "+79991234567") && ( (id(sms_message).state == "relay_1_on") OR (id(sms_message).state == "Relay_1_on") ) ) {
            id(relay_1).turn_on();
          }
    switch:
      - platform: gpio
        id: relay_1
        pin: 0


See Also
--------

- :ghsources:`esphome/components/sim800l`
- :doc:`/components/uart`
- :ghedit:`Edit`
