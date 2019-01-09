Native API Component
====================

.. seo::
    :description: Instructions for setting up the native ESPHome API for communication with Home Assistant.
    :image: server-network.png
    :keywords: Native API, ESPHome, Home Assistant

.. code-block:: yaml

    # Example configuration entry
    api:
      password: 'MyPassword'

Configuration variables:
------------------------

- **port** (*Optional*, integer): The port to run the API Server on. Defaults to ``6053``.
- **password** (*Optional*, string): The password to protect the API Server with. Defaults to no password.
- **reboot_timeout** (*Optional*, :ref:`time <config-time>`): The amount of time to wait before rebooting when no
  client connects to the API. This is needed because sometimes the low level ESP functions report that
  the ESP is connected to the network, when in fact it is not - only a full reboot fixes it.
  Can be disabled by setting this to ``0s``. Defaults to ``5min``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _api-mqtt_to_native:

Migrating from MQTT to Native API Setup in Home Assistant
---------------------------------------------------------

The native API is the best way to use esphomelib together with Home Assistant - it's fast,
highly efficient and requires almost zero setup (whereas MQTT requires you to set up an MQTT broker first).

If you've previously used esphomelib with Home Assistant via MQTT and have enabled MQTT discovery,
the upgrade process is unfortunately not just swapping out the ``mqtt`` for ``api`` in your configuration:
Home Assistant's `entity registry <https://developers.home-assistant.io/docs/en/entity_registry_index.html>`__ complicates
things a bit. If you don't follow these steps, all your new native API entities will have a trailing
`_2` at the end of the entity ID.

You can repeat these steps for all your nodes, or convert them over to the new native API one by one.

1. Disable MQTT discovery on ESP side. In your ESPHome configuration, set a special "clean" discovery flag:

  .. code-block:: yaml

      # In your ESPHome configuration! Not HA config!
      mqtt:
        # Other settings ...
        discovery: clean

2. Compile and upload this new firmware. All entities should now be gone from Home Assistant.

3. Go to your Home Assistant configuration folder and go to the ``.storage`` folder (might be hidden
   depending on your operating system). In there you will find a file called ``core.entity_registry`` - open
   the file with a text editor and paste the contents below


   .. raw:: html

     <textarea rows="10" cols="50" id="entity-reg-converter"></textarea>
     <button type="button" id="entity-reg-button">Convert Entity Registry</button>
     <script>
       var elem = document.getElementById("entity-reg-converter");
       elem.addEventListener("click", function() {
         elem.focus();
         elem.select();
       });
       document.getElementById("entity-reg-button").addEventListener("click", function() {
         try {
           data = JSON.parse(elem.value);
         } catch(e) {
           alert(e);
         }
         var entities = data.data.entities;
         var newEntities = [];
         for (var i = 0; i < entities.length; i++) {
           var entity = entities[i];
           if (entity.platform != "mqtt") {
             newEntities.push(entity);
           }
         }
         data.data.entities = newEntities;
         elem.value = JSON.stringify(data, null, 4);
       });
     </script>

4. Stop Home Assistant - this is necessary for the entity registry changes not to become overriden.

5. Convert the Entity Registry file above using the "Convert Entity Registry Button", and
   override the ``.storage/core.entity_registry`` file with the new contents.

6. Start Home Assistant.

7. Now you can enable the ESPHome native API (and upload the new firmware)

  .. code-block:: yaml

    # Example configuration entry
    api:

8. In Home Assistant, go to "Configuration" -> "Integrations" - if you've set up the ``discovery:`` component,
   you'll already see the ESP as a suggestion to be configured. But if you're having issues with that, you can
   always manually set up an ESPHome device using "Set up a new integration" -> "ESPHome".

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

See Also
--------

- :doc:`API Reference </api/core/native-api>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/api.rst>`__

.. disqus::
