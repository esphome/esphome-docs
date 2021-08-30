Native API Component
====================

.. seo::
    :description: Instructions for setting up the native ESPHome API for communication with Home Assistant.
    :image: server-network.png
    :keywords: Native API, ESPHome, Home Assistant

The ESPHome native API is used to communicate with clients directly, with a highly-optimized
network protocol. Currently, only the ESPHome tool and Home Assistant use this native API.

After adding an ``api:`` line to your ESPHome configuration you can go to the Home Assistant
web interface and navigate to the "Integrations" screen in the "Configuration" panel. Then wait
for the ESPHome device to show up under the discovered section (can take up to 5 minutes) or add
the device manually by choosing "ESPHome" from the integration overview and entering
"<NODE_NAME>.local" or the IP address of the unit in the "Host" field.

The ESPHome native API is based on a custom TCP protocol using protocol buffers. You can find
the protocol data structure definitions here: https://github.com/esphome/esphome/blob/dev/esphome/components/api/api.proto
A Python library that implements this protocol is `aioesphomeapi <https://github.com/esphome/aioesphomeapi>`__.

.. code-block:: yaml

    # Example configuration entry
    api:
      password: 'MyPassword'

Configuration variables:
------------------------

- **port** (*Optional*, integer): The port to run the API Server on. Defaults to ``6053``.
- **password** (*Optional*, string): The password to protect the API Server with. Defaults to no password.
- **services** (*Optional*, list): A list of user-defined services. See :ref:`api-services`.
- **reboot_timeout** (*Optional*, :ref:`time <config-time>`): The amount of time to wait before rebooting when no
  client connects to the API. This is needed because sometimes the low level ESP functions report that
  the ESP is connected to the network, when in fact it is not - only a full reboot fixes it.
  Can be disabled by setting this to ``0s``. Defaults to ``15min``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _api-homeassistant_service_action:

``homeassistant.service`` Action
--------------------------------

When using the native API with Home Assistant, you can create Home Assistant service
calls straight from ESPHome :ref:`Automations <automation>`.

.. code-block:: yaml

    # In some trigger
    on_...:
      # Simple
      - homeassistant.service:
          service: notify.html5
          data:
            title: Button was pressed
      # With templates and variables
      - homeassistant.service:
          service: notify.html5
          data:
            title: New Humidity
          data_template:
            message: The humidity is {{ my_variable }}%.
          variables:
            my_variable: |-
              return id(my_sensor).state;

Configuration options:

- **service** (**Required**, string): The Home Assistant `Service <https://www.home-assistant.io/docs/scripts/service-calls/>`__
  to call.
- **data** (*Optional*, mapping): Optional *static* data to pass along with the service call.
- **data_template** (*Optional*, mapping): Optional template data to pass along with the service call.
  This is evaluated on the Home Assistant side with Home Assistant's templating engine.
- **variables** (*Optional*, mapping): Optional variables that can be used in the ``data_template``.
  Values are :ref:`lambdas <config-lambda>` and will be evaluated before sending the request.

Data structures are not possible, but you can create a script in Home Assistant and call with all
the parameters in plain format.

.. code-block:: yaml

    # Home Assistant Configuration
    script:
      ...
      set_light_rgb:
        alias: 'ESPHome RGB light set'
        sequence:
        - service: light.turn_on
          data_template:
            entity_id: '{{ light_name }}'
            rgb_color:
            - '{{ red }}'
            - '{{ green }}'
            - '{{ blue }}'

Then in ESPHome

.. code-block:: yaml

    # In some trigger
    on_...:
      - homeassistant.service:
          service: script.set_light_rgb
          data:
            light_name: 'my_light'
            red: '255'
            green: '199'
            blue: '71'

.. _api-services:

User-defined Services
---------------------

It is also possible to get data from Home Assistant to ESPHome with user-defined services.
When you declare services in your ESPHome YAML file, they will automatically show up in
Home Assistant and you can call them directly.

.. code-block:: yaml

    # Example configuration entry
    api:
      services:
        - service: start_laundry
          then:
            - switch.turn_on: relay
            - delay: 3h
            - switch.turn_off: relay

For example with the configuration seen above, after uploading you will see a service
called ``esphome.livingroom_start_laundry`` (livingroom is the node name) which you can
then call.

Additionally, you can also transmit data from Home Assistant to ESPHome with this method:

.. code-block:: yaml

    # Example configuration entry
    api:
      services:
        - service: start_effect
          variables:
            my_brightness: int
            my_effect: string
          then:
            - light.turn_on:
                id: my_light
                brightness: !lambda 'return my_brightness;'
                effect: !lambda 'return my_effect;'

Using the ``variables`` key you can tell ESPHome which variables to expect from Home Assistant.
For example the service seen above would be executed with something like this:

.. code-block:: yaml

    # Example Home Assistant Service Call
    service: esphome.livingroom_start_effect
    data_template:
      my_brightness: "{{ states.brightness.state }}"
      my_effect: "Rainbow"

Then each variable you define in the ``variables`` section is accessible in the automation
triggered by the user-defined service through the name you gave it in the variables section
(note: this is a local variable, so do not wrap it in ``id(...)`` to access it).

There are currently 4 types of variables:

- bool: A boolean (ON/OFF). C++ type: ``bool``
- int: An integer. C++ type: ``int``/``int32_t``
- float: A floating point number. C++ type: ``float``
- string: A string. C++ type: ``std::string``

Each of these also exist in array form:

- bool[]: An array of boolean values. C++ type: ``std::vector<bool>``
- ... - Same for other types.

.. _api-connected_condition:

``api.connected`` Condition
---------------------------

This :ref:`Condition <config-condition>` checks if at least one client is connected to the ESPHome
native API. Please note client not only includes Home Assistant, but also ESPHome's OTA log output
if logs are shown remotely.

.. code-block:: yaml

    on_...:
      if:
        condition:
          api.connected:
        then:
          - logger.log: API is connected!


Advantages over MQTT
--------------------

The ESPHome native API has many advantages over using MQTT for communication with Home
Automation software (currently only Home Assistant). But MQTT is a great protocol and will
never be removed. Features of native API (vs. MQTT):

- **Much more efficient:** ESPHome encodes all messages in a highly optimized format with
  protocol buffers - for example binary sensor state messages are about 1/10 of the size.
- **One-click configuration:** ESPHome just needs one click to set up in Home Assistant -
  no more messing around with retained MQTT discovery messages and alike.
- **One less single point of failure:** In the ESPHome native API each ESP is its own server.
  With MQTT, when the broker shuts off nothing can communicate anymore.
- **Stability:** Since ESPHome has far more control over the protocol than with MQTT,
  it's really easy for us to roll out stability improvements.
- **Low Latency:** The native API is optimized for very low latency, usually this is only
  a couple of milliseconds and far less than can be noticed by the eye.


.. _api-homeassistant_event_action:

``homeassistant.event`` Action
------------------------------

When using the native API with Home Assistant, you can create events in the Home Assistant event bus
straight from ESPHome :ref:`Automations <automation>`.

.. code-block:: yaml

    # In some trigger
    on_...:
      # Simple
      - homeassistant.event:
          event: esphome.button_pressed
          data:
            title: Button was pressed

Configuration options:

- **event** (**Required**, string): The event to create - must begin with ``esphome.``
- **data** (*Optional*, mapping): Optional *static* data to pass along with the event.
- **data_template** (*Optional*, mapping): Optional template data to pass along with the event.
  This is evaluated on the Home Assistant side with Home Assistant's templating engine.
- **variables** (*Optional*, mapping): Optional variables that can be used in the ``data_template``.
  Values are :ref:`lambdas <config-lambda>` and will be evaluated before sending the request.


.. _api-homeassistant_tag_scanned_action:

``homeassistant.tag_scanned`` Action
------------------------------------

When using the native API with Home Assistant, you can push tag_scanned to Home Assistant
straight from ESPHome :ref:`Automations <automation>`.

.. code-block:: yaml

    # In some trigger
    on_...:
      # Simple
      - homeassistant.tag_scanned: some-tag

Configuration options:

- **tag** (**Required**, :ref:`templatable <config-templatable>`, string): The id of the scanned tag

See Also
--------

- :apiref:`api/api_server.h`
- :ghedit:`Edit`
