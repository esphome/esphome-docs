Telegram Bot
============

.. seo::
    :description: Instructions for setting up Telegram Bot for ESPHome.
    :image: telegram_bot.png

Use Telegram on your mobile or desktop device to send and receive messages or commands to/from your ESPHome device.

The ``telegram_bot`` component uses the :doc:`/components/http_request` component to make requests to `Telegram Bot API <https://core.telegram.org/bots/api>`__.

.. note::

    First you need to create your bot and get a bot token: `Telegram Bot Account <https://core.telegram.org/bots>`__

Then setup a component:

.. code-block:: yaml

    # Example configuration entry
    telegram_bot:
      id: chatbot
      token: <BOT_TOKEN>
      allowed_chat_ids:
        - <CHAT_ID>

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **token** (**Required**, string): Bot authorization token.
- **allowed_chat_ids** (*Optional*, list): A list of allowed chat ids.
- **scan_interval** (*Optional*, :ref:`config-time`): The interval for requesting new messages from the API server.
- **on_message** (*Optional*, :ref:`Automation <automation>`): An action to be
  performed when a message is received. See :ref:`telegram_bot-on_message`.

A variable ``x`` of type :apistruct:`telegram_bot::Message` is passed to the automation.

.. code-block:: cpp

    struct Message {
      std::string id;
      std::string text;
      std::string chat_id;
      std::string chat_title;
      std::string from_id;
      std::string from_name;
      std::string date;
      std::string type;
      int update_id;
    };

.. _telegram_bot-on_message:

``on_message`` Trigger
----------------------

With this configuration option you can write complex automations whenever an
message is received. To use the message content, use a :ref:`lambda <config-lambda>`
template, the message payload is available under the name ``x`` inside that lambda.

.. code-block:: yaml

    telegram_bot:
      # ...
      on_message:
        - type: message
          message: '/light'
          then:
            - switch.toggle: some_switch

Configuration variables:

- **type** (*Optional*, string): Message type. Avaliable types:
  ``message``, ``channel_post``, ``callback_query``. More information
  in `Telegram Bot API Documentation <https://core.telegram.org/bots/api#available-types>`__.
- **message** (*Optional*, string): Filter messages by text.

Telegram Bot Actions
--------------------

Component supports several :ref:`actions <config-action>` that can be used to send messages.

.. _telegram_bot-send_message:

``telegram_bot.send_message`` Action
************************************

This :ref:`action <config-action>` sends a text message.

.. code-block:: yaml

    on_...:
      - telegram_bot.send_message:
          chat_id: <CHAT_ID>
          message: !lambda |-
            return 'Telegram Message';
          inline_keyboard:
            - text: Toggle Light
              callback_data: '/light'

Configuration variables:

- **chat_id** (**Required**, string, :ref:`templatable <config-templatable>`): Chat ID to send message.
- **message** (**Required**, string, :ref:`templatable <config-templatable>`): Message to send.
- **inline_keyboard** (*Optional*, list): Inline keyboard data, see :ref:`telegram_bot-inline_keyboard`.

.. _telegram_bot-inline_keyboard:

Inline Keyboard
***************

`Telegram Inline Keyboard Documentation <https://core.telegram.org/bots#inline-keyboards-and-on-the-fly-updating>`__

.. code-block:: yaml

    on_...:
      - telegram_bot.send_message:
          # ...
          inline_keyboard:
            - text: Toggle Light
              callback_data: '/light'
            - text: Google
              url: 'https://google.com/'

Configuration variables:

- **text** (**Required**, string): Text for keyboard button.
- **url** (*Optional*, string): URL to navigate this button.
- **callback_data** (*Optional*, string): Command to send to bot by this button. See :ref:`telegram_bot-on_message`.

.. _telegram_bot-answer_callback_query:

``telegram_bot.answer_callback_query`` Action
*********************************************

This :ref:`action <config-action>` answers callback query.

.. code-block:: yaml

    telegram_bot:
      # ...
      on_message:
        - message: '/open'
          type: callback_query
          then:
            telegram_bot.answer_callback_query:
              callback_query_id: !lambda "return x.id;"
              message: 'Answer to /open command'

Configuration variables:

- **callback_query_id** (**Required**, string, :ref:`templatable <config-templatable>`): Callback query ID to answer. See :ref:`telegram_bot-inline_keyboard`.
- **message** (**Required**, string, :ref:`templatable <config-templatable>`): Message to send.


See Also
--------

- :doc:`index`
- :apiref:`telegram_bot/telegram_bot.h`
- :ghedit:`Edit`
