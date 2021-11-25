MQTT Client Component
=====================

.. seo::
    :description: Instructions for setting up the MQTT client to communicate with the local network in ESPHome.
    :image: mqtt.png
    :keywords: MQTT

The MQTT Client Component sets up the MQTT connection to your broker.
If you are connecting to Home Assistant, you may prefer to use the native API,
in which case this is not needed.

.. warning::

    If you enable MQTT and you do *not* use the "native API" for Home Assistant, you must
    remove the ``api:`` line from your ESPHome configuration, otherwise the ESP will
    reboot every 15 minutes because no client connected to the native API.

.. code-block:: yaml

    # Example configuration entry
    mqtt:
      broker: 10.0.0.2
      username: livingroom
      password: MyMQTTPassword

Configuration variables:
------------------------

- **broker** (**Required**, string): The host of your MQTT broker.
- **port** (*Optional*, int): The port to connect to. Defaults to 1883.
- **username** (*Optional*, string): The username to use for
  authentication. Empty (the default) means no authentication.
- **password** (*Optional*, string): The password to use for
  authentication. Empty (the default) means no authentication.
- **client_id** (*Optional*, string): The client id to use for opening
  connections. See :ref:`mqtt-defaults` for more information.
- **discovery** (*Optional*, boolean): If Home Assistant automatic
  discovery should be enabled. Defaults to ``true``.
- **discovery_retain** (*Optional*, boolean): Whether to retain MQTT
  discovery messages so that entities are added automatically on Home
  Assistant restart. Defaults to ``true``.
- **discovery_prefix** (*Optional*, string): The prefix to use for Home
  Assistant’s MQTT discovery. Should not contain trailing slash.
  Defaults to ``homeassistant``.
- **use_abbreviations** (*Optional*, boolean): Whether to use
  `Abbreviations <https://www.home-assistant.io/docs/mqtt/discovery/>`__
  in discovery messages. Defaults to ``true``.
- **topic_prefix** (*Optional*, string): The prefix used for all MQTT
  messages. Should not contain trailing slash. Defaults to
  ``<APP_NAME>``.
- **log_topic** (*Optional*, :ref:`mqtt-message`): The topic to send MQTT log
  messages to.
- **birth_message** (*Optional*, :ref:`mqtt-message`): The message to send when
  a connection to the broker is established. See :ref:`mqtt-last_will_birth` for more information.
- **will_message** (*Optional*, :ref:`mqtt-message`): The message to send when
  the MQTT connection is dropped. See :ref:`mqtt-last_will_birth` for more information.
- **shutdown_message** (*Optional*, :ref:`mqtt-message`): The message to send when
  the node shuts down and the connection is closed cleanly. See :ref:`mqtt-last_will_birth` for more information.
- **ssl_fingerprints** (*Optional*, list): Only on ESP8266. A list of SHA1 hashes used
  for verifying SSL connections. See :ref:`mqtt-ssl_fingerprints`
  for more information.
- **reboot_timeout** (*Optional*, :ref:`config-time`): The amount of time to wait before rebooting when no
  MQTT connection exists. Can be disabled by setting this to ``0s``. Defaults to ``15min``.
- **keepalive** (*Optional*, :ref:`config-time`): The time
  to keep the MQTT socket alive, decreasing this can help with overall stability due to more
  WiFi traffic with more pings. Defaults to 15 seconds.
- **on_message** (*Optional*, :ref:`Automation <automation>`): An action to be
  performed when a message on a specific MQTT topic is received. See :ref:`mqtt-on_message`.
- **on_json_message** (*Optional*, :ref:`Automation <automation>`): An action to be
  performed when a JSON message on a specific MQTT topic is received. See :ref:`mqtt-on_json_message`.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _mqtt-message:

MQTTMessage
-----------

With the MQTT Message schema you can tell ESPHome how a specific MQTT message should be sent.
It is used in several places like last will and birth messages or MQTT log options.

.. code-block:: yaml

    # Simple:
    some_option: topic/to/send/to

    # Disable:
    some_option:

    # Advanced:
    some_option:
      topic: topic/to/send/to
      payload: online
      qos: 0
      retain: true


Configuration options:

-  **topic** (**Required**, string): The MQTT topic to publish the message.
-  **payload** (**Required**, string): The message content. Will be filled by the actual payload with some
   options, like log_topic.
-  **qos** (*Optional*, int): The `Quality of
   Service <https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels>`__
   level of the topic. Defaults to 0.
-  **retain** (*Optional*, boolean): If the published message should
   have a retain flag on or not. Defaults to ``true``.


The ``log_topic`` has an additional configuration option:

- **level** (*Optional*, string): The log level to use for MQTT logs. See
  :ref:`logger-log_levels` for options.

.. _mqtt-using_with_home_assistant:

Using with Home Assistant
-------------------------

Using ESPHome with Home Assistant is easy, simply setup an MQTT
broker (like `mosquitto <https://mosquitto.org/>`__) and point both your
Home Assistant installation and ESPHome to that broker. Next, enable
discovery in your Home Assistant configuration with the following:

.. code-block:: yaml

    # Example Home Assistant configuration.yaml entry
    mqtt:
      broker: ...
      discovery: true

And that should already be it 🎉 All devices defined through ESPHome should show up automatically
in the entities section of Home Assistant.

When adding new entities, you might run into trouble with old entities
still appearing in Home Assistant’s front-end. This is because in order
to have Home Assistant “discover” your devices on restart, all discovery
MQTT messages need to be retained. Therefore the old entities will also
re-appear on every Home Assistant restart even though they’re in
ESPHome anymore.

To fix this, ESPHome has a simple helper script that purges stale
retained messages for you:

.. code-block:: bash

    esphome configuration.yaml clean-mqtt

With Docker:

.. code-block:: bash

    docker run --rm -v "${PWD}":/config -it esphome/esphome clean-mqtt configuration.yaml

This will remove all retained messages with the topic
``<DISCOVERY_PREFIX>/+/NODE_NAME/#``. If you want to purge on another
topic, simply add ``--topic <your_topic>`` to the command.

.. _mqtt-defaults:

Defaults
--------

By default, ESPHome will prefix all messages with your node name or
``topic_prefix`` if you have specified it manually. The client id will
automatically be generated by using your node name and adding the MAC
address of your device to it. Next, discovery is enabled by default with
Home Assistant’s default prefix ``homeassistant``.

If you want to prefix all MQTT messages with a different prefix, like
``home/living_room``, you can specify a custom ``topic_prefix`` in the
configuration. That way, you can use your existing wildcards like
``home/+/#`` together with ESPHome. All other features of ESPHome
(like availability) should still work correctly.

.. _mqtt-last_will_birth:

Last Will And Birth Messages
----------------------------

ESPHome uses the `last will
testament <https://www.hivemq.com/blog/mqtt-essentials-part-9-last-will-and-testament>`__
and birth message feature of MQTT to achieve availability reporting for
Home Assistant. If the node is not connected to MQTT, Home Assistant
will show all its entities as unavailable (a feature 😉).

.. figure:: /components/images/mqtt-availability.png
    :align: center
    :width: 50.0%

By default, ESPHome will send a retained MQTT message to
``<TOPIC_PREFIX>/status`` with payload ``online``, and will tell the
broker to send a message ``<TOPIC_PREFIX>/status`` with payload
``offline`` if the connection drops.

You can change these messages by overriding the ``birth_message`` and
``will_message`` with the following options.

.. code-block:: yaml

    mqtt:
      # ...
      birth_message:
        topic: myavailability/topic
        payload: online
      will_message:
        topic: myavailability/topic
        payload: offline

- **birth_message** (*Optional*, :ref:`mqtt-message`)
- **will_message** (*Optional*, :ref:`mqtt-message`)

If the birth message and last will message have empty topics or topics
that are different from each other, availability reporting will be
disabled.

.. _mqtt-ssl_fingerprints:

SSL Fingerprints
----------------

On the ESP8266 you have the option to use SSL connections for MQTT. This feature
will get expanded to the ESP32 once the base library, AsyncTCP, supports it. Please
note that the SSL feature only checks the SHA1 hash of the SSL certificate to verify
the integrity of the connection, so every time the certificate changes, you'll have to
update the fingerprints variable. Additionally, SHA1 is known to be partially insecure
and with some computing power the fingerprint can be faked.

To get this fingerprint, first put the broker and port options in the configuration and
then run the ``mqtt-fingerprint`` script of ESPHome to get the certificate:

.. code-block:: bash

    esphome livingroom.yaml mqtt-fingerprint
    > SHA1 Fingerprint: a502ff13999f8b398ef1834f1123650b3236fc07
    > Copy above string into mqtt.ssl_fingerprints section of livingroom.yaml

.. code-block:: yaml

    mqtt:
      # ...
      ssl_fingerprints:
        - a502ff13999f8b398ef1834f1123650b3236fc07

.. _config-mqtt-component:

MQTT Component Base Configuration
---------------------------------

All components in ESPHome that do some sort of communication through
MQTT can have some overrides for specific options.

.. code-block:: yaml

    name: "Component Name"
    # Optional variables:
    retain: true
    discovery: true
    availability:
      topic: livingroom/status
      payload_available: online
      payload_not_available: offline
    state_topic: livingroom/custom_state_topic
    command_topic: livingroom/custom_command_topic

Configuration variables:

-  **name** (**Required**, string): The name to use for the MQTT
   Component.
-  **retain** (*Optional*, boolean): If all MQTT state messages should
   be retained. Defaults to ``true``.
-  **discovery** (*Optional*, boolean): Manually enable/disable
   discovery for a component. Defaults to the global default.
-  **availability** (*Optional*): Manually set what should be sent to
   Home Assistant for showing entity availability. Default derived from
   :ref:`global birth/last will message <mqtt-last_will_birth>`.
-  **state_topic** (*Optional*, string): The topic to publish state
   updates to. Defaults to
   ``<TOPIC_PREFIX>/<COMPONENT_TYPE>/<COMPONENT_NAME>/state``.
-  **command_topic** (*Optional*, string): The topic to subscribe to for
   commands from the remote. Defaults to
   ``<TOPIC_PREFIX>/<COMPONENT_TYPE>/<COMPONENT_NAME>/command``.

.. warning::

    When changing these options and you're using MQTT discovery, you will need to restart Home Assistant.
    This is because Home Assistant only discovers a device once in every Home Assistant start.

.. _mqtt-on_message:

``on_message`` Trigger
----------------------

With this configuration option you can write complex automations whenever an MQTT
message on a specific topic is received. To use the message content, use a :ref:`lambda <config-lambda>`
template, the message payload is available under the name ``x`` inside that lambda.

.. code-block:: yaml

    mqtt:
      # ...
      on_message:
        topic: my/custom/topic
        qos: 0
        then:
          - switch.turn_on: some_switch

Configuration variables:

- **topic** (**Required**, string): The MQTT topic to subscribe to and listen for MQTT
  messages on. Every time a message with **this exact topic** is received, the automation will trigger.

- **qos** (*Optional*, integer): The MQTT Quality of Service to subscribe to the topic with. Defaults
  to 0.

- **payload** (*Optional*, string): Optionally set a payload to match. Only if exactly the payload
  you specify with this option is received, the automation will be executed.

.. note::

    You can even specify multiple ``on_message`` triggers by using a YAML list:

    .. code-block:: yaml

        mqtt:
          on_message:
             - topic: some/topic
               then:
                 - # ...
             - topic: some/other/topic
               then:
                 - # ...

.. note::

    This action can also be used in :ref:`lambdas <config-lambda>`:

    .. code-block:: yaml

        mqtt:
          # Give the mqtt component an ID
          id: mqtt_client

    .. code-block:: cpp

        id(mqtt_client).subscribe("the/topic", [=](const std::string &payload) {
            // do something with payload
        });

.. _mqtt-on_json_message:

``on_json_message`` Trigger
---------------------------

With this configuration option you can write complex automations whenever a JSON-encoded MQTT
message is received. To use the message content, use a :ref:`lambda <config-lambda>`
template, the decoded message payload is available under the name ``x`` inside that lambda.

The ``x`` object is of type ``JsonObject`` by the `ArduinoJson <https://github.com/bblanchon/ArduinoJson>`__
library, and you can use all of the methods of that library to access data.

Basically, you can access elements by typing ``x["THE_KEY"]`` and save them into local variables.
Please note that it's a good idea to check if the key exists in the Json Object by calling
``containsKey`` first as the ESP will crash if an element that does not exist is accessed.

.. code-block:: yaml

    mqtt:
      # ...
      on_json_message:
        topic: the/topic
        then:
          - light.turn_on:
              id: living_room_lights

              transition_length: !lambda |-
                int length = 1000;
                if (x.containsKey("length"))
                  length = x["length"];
                return length;

              brightness: !lambda "return x["bright"];"

              effect: !lambda |-
                const char *effect = "None";
                if (x.containsKey("effect"))
                  effect = x["effect"];
                return effect;

Configuration variables:

- **topic** (**Required**, string): The MQTT topic to subscribe to and listen for MQTT
  messages on. Every time a message with **this exact topic** is received, the automation will trigger.

- **qos** (*Optional*, integer): The MQTT Quality of Service to subscribe to the topic with. Defaults
  to 0.

.. note::

    Due to the way this trigger works internally it is incompatible with certain actions and will
    trigger a compile failure. For example with the ``delay`` action.

.. note::

    This action can also be used in :ref:`lambdas <config-lambda>`:

    .. code-block:: yaml

        mqtt:
          # Give the mqtt component an ID
          id: mqtt_client

    .. code-block:: cpp

        id(mqtt_client).subscribe_json("the/topic", [=](JsonObject &root) {
            // do something with JSON-decoded value root
        });

.. _mqtt-publish_action:

``mqtt.publish`` Action
-----------------------

Publish an MQTT message on a topic using this action in automations.

.. code-block:: yaml

    on_...:
      then:
        - mqtt.publish:
            topic: some/topic
            payload: "Something happened!"

        # Templated:
        - mqtt.publish:
            topic: !lambda |-
              if (id(reed_switch).state) return "topic1";
              else return "topic2";
            payload: !lambda |-
              return id(reed_switch).state ? "YES" : "NO";

Configuration options:

-  **topic** (**Required**, string, :ref:`templatable <config-templatable>`):
   The MQTT topic to publish the message.
-  **payload** (**Required**, string, :ref:`templatable <config-templatable>`): The message content.
-  **qos** (*Optional*, int, :ref:`templatable <config-templatable>`): The `Quality of
   Service <https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels>`__
   level of the topic. Defaults to 0.
-  **retain** (*Optional*, boolean, :ref:`templatable <config-templatable>`): If the published message should
   have a retain flag on or not. Defaults to ``false``.


.. note::

    This action can also be written in :ref:`lambdas <config-lambda>`:

    .. code-block:: yaml

        mqtt:
          # Give the mqtt component an ID
          id: mqtt_client

    .. code-block:: cpp

        id(mqtt_client).publish("the/topic", "The Payload");

.. _mqtt-publish_json_action:

``mqtt.publish_json`` Action
----------------------------

Publish a JSON-formatted MQTT message on a topic using this action in automations.

The JSON message will be constructed using the `ArduinoJson <https://github.com/bblanchon/ArduinoJson>`__ library.
In the ``payload`` option you have access to a ``root`` object which will represents the base object
of the JSON message. You can assign values to keys by using the ``root["KEY_NAME"] = VALUE;`` syntax
as seen below.

.. code-block:: yaml

    on_...:
      then:
        - mqtt.publish_json:
            topic: the/topic
            payload: |-
              root["key"] = id(my_sensor).state;
              root["greeting"] = "Hello World";

            # Will produce:
            # {"key": 42.0, "greeting": "Hello World"}

Configuration options:

-  **topic** (**Required**, string, :ref:`templatable <config-templatable>`):
   The MQTT topic to publish the message.
-  **payload** (**Required**, :ref:`lambda <config-lambda>`): The message content.
-  **qos** (*Optional*, int): The `Quality of
   Service <https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels>`__
   level of the topic. Defaults to 0.
-  **retain** (*Optional*, boolean): If the published message should
   have a retain flag on or not. Defaults to ``false``.


.. note::

    This action can also be written in :ref:`lambdas <config-lambda>`:

    .. code-block:: yaml

        mqtt:
          # Give the mqtt component an ID
          id: mqtt_client

    .. code-block:: cpp

        id(mqtt_client).publish_json("the/topic", [=](JsonObject &root) {
          root["something"] = id(my_sensor).state;
        });

.. _mqtt-connected_condition:

``mqtt.connected`` Condition
----------------------------

This :ref:`Condition <config-condition>` checks if the MQTT client is currently connected to
the MQTT broker.

.. code-block:: yaml

    on_...:
      if:
        condition:
          mqtt.connected:
        then:
          - logger.log: MQTT is connected!

.. note::

    This action can also be written in :ref:`lambdas <config-lambda>`:

    .. code-block:: yaml

        mqtt:
          # Give the mqtt component an ID
          id: mqtt_client

    .. code-block:: cpp

        if (id(mqtt_client)->is_connected()) {
          // do something if MQTT is connected
        }

See Also
--------

- :apiref:`mqtt/mqtt_client.h`
- :ghedit:`Edit`
