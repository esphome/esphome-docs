Sim800L Component
=================

.. seo::
    :description: Instructions for setting up the SIM800L gsm module to send and receive SMS in ESPHome.
    :image: sim800l.png
    :keywords: SMS SIM800L GSM

The ``SIM800L`` Component provides the ability to send and receive SMS text messages. The device must be
connected via a :doc:`UART bus </components/uart>` supporting both receiving and transmitting line.

The uart bus must be configured at the same speed of the module which is by default 9600bps. Either hardware
or software uarts are supported. If you are using the hardware uart in the ESP8266, make sure you disable
the  :doc:`logger`.

.. note::

    This module requires a custom power supply between 3.8v and 4.2v that can handle  current pikes up
    to 2 amps, it will not work by powering from the same 3.3v power source of the ESP. However you can
    connect TX and RX lines directly without any level shifter.

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
      id: sim800l1
      on_sms_received:
        - logger.log:
            format: "Received '%s' from %s"
            args: [ 'message.c_str()', 'sender.c_str()' ]

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the UART hub.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **on_sms_received** (*Optional*, :ref:`Automation <automation>`): An action to be
  performed when a sms is received. See :ref:`sim800l-on_sms_received`.

.. _sim800l-on_sms_received:

``on_sms_received`` Trigger
---------------------------

With this configuration option you can write complex automations whenever a sms message
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
            id: sim800l1
            recipient: '+15551234567'
            message: Hello there

        # Templated:
        - sim800l.send_sms:
            id: sim800l1
            recipient: !lambda |-
              if (id(reed_switch).state) return "+15551234567";
              else return "15551234568";
            message: !lambda |-
              return id(reed_switch).state ? "Door is now OPEN" : "Hey door just CLOSED";

Configuration options:

- **id** (*Required*, string): The ID of the SIM800L
- **recipient** (*Required*, string, :ref:`templatable <config-templatable>`): The message recipient.
  number. Make sure to use quotes if the number starts with a `+` or the parser will remove it.
- **message** (*Required*, string, :ref:`templatable <config-templatable>`): The message content.

.. note::

    This action can also be written in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        id(sim800l1).send_sms("+15551234567", "The message content");

See Also
--------

- :apiref:`sim800l/sim800l.h`
- :doc:`/components/uart`
- :ghedit:`Edit`
