HTTP Request
============

.. seo::
    :description: Instructions for setting up HTTP Requests in ESPHome
    :image: connection.svg
    :keywords: http, request


The ``http_request`` component lets you make HTTP/HTTPS requests. First, you need to setup a component:

.. code-block:: yaml

    # Example configuration entry
    http_request:
      useragent: esphome/device
      timeout: 10s

Configuration variables:
------------------------

- **useragent** (*Optional*, string): User-Agent header for requests. Defaults to ``ESPHome``.
- **timeout** (*Optional*, :ref:`config-time`): Timeout for request. Defaults to ``5s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **follow_redirects** (*Optional*, boolean): Enable following HTTP redirects. Defaults to ``true``.
- **redirect_limit** (*Optional*, integer): Maximum amount of redirects to follow when enabled. Defaults to ``3``.

ESP8266 Options:

- **esp8266_disable_ssl_support** (*Optional*, boolean): Whether to include SSL support on ESP8266s.
  Defaults to ``no``. See :ref:`esphome-esp8266_disable_ssl_support` for more info

.. _esphome-esp8266_disable_ssl_support:

``esp8266_disable_ssl_support``
-------------------------------

This options allows you to disable inclusion of SSL libraries. This is required on a flash
constrained devices (512k or 1M) which does not have enough space to support
SSL and OTA concurrently. The flashing will fail with the following error
``Error: ESP does not have enough space to store OTA file``.

HTTP Request Actions
--------------------

Component support a number of :ref:`actions <config-action>` that can be used to send requests.

.. _http_request-get_action:

``http_request.get`` Action
***************************

This :ref:`action <config-action>` sends a GET request.

.. code-block:: yaml

    on_...:
      - http_request.get:
          url: https://esphome.io
          headers:
            Content-Type: application/json
          verify_ssl: false
          on_response:
            then:
              - logger.log:
                  format: 'Response status: %d, Duration: %u ms'
                  args:
                    - status_code
                    - duration_ms
      # Short form
      - http_request.get: https://esphome.io

Configuration variables:

- **url** (**Required**, string, :ref:`templatable <config-templatable>`): URL to send request.
- **headers** (*Optional*, mapping): Map of HTTP headers. Values are :ref:`templatable <config-templatable>`.
- **verify_ssl** (*Optional*, boolean): Verify the SSL certificate of the endpoint. Defaults to ``true``.
- **on_response** (*Optional*, :ref:`Automation <automation>`): An automation to perform when the request is finished.

.. note::

    Currently ESPHome **can't verify the SSL certificate** of the endpoint.
    Set ``verify_ssl: false`` to make HTTPS request.

.. _http_request-post_action:

``http_request.post`` Action
****************************

This :ref:`action <config-action>` sends a POST request.

.. code-block:: yaml

    on_...:
      - http_request.post:
          url: https://esphome.io
          headers:
            Content-Type: application/json
          json:
            key: value
          verify_ssl: false
      # Short form
      - http_request.post: https://esphome.io

Configuration variables:

- **body** (*Optional*, string, :ref:`templatable <config-templatable>`): A HTTP body string to send with request.
- **json** (*Optional*, mapping): A HTTP body in JSON format. Values are :ref:`templatable <config-templatable>`. See :ref:`http_request-examples`.
- All other options from :ref:`http_request-get_action`.

.. _http_request-send_action:

``http_request.send`` Action
****************************

This :ref:`action <config-action>` sends a request.

.. code-block:: yaml

    on_...:
      - http_request.send:
          method: PUT
          url: https://esphome.io
          headers:
            Content-Type: application/json
          body: "Some data"
          verify_ssl: false

Configuration variables:

- **method** (**Required**, string): HTTP method to use (``GET``, ``POST``, ``PUT``, ``DELETE``, ``PATCH``).
- All other options from :ref:`http_request-post_action`.

.. _http_request-on_response:

``on_response`` Trigger
-----------------------

This automation will be triggered when the HTTP request is finished and will supply these parameters:

* ``status_code`` as ``int`` - http response code
* ``duration_ms`` as ``uint32`` - time taken to complete the request

.. code-block:: yaml

    on_...
      then:
        - http_request.get:
            url: https://esphome.io
            verify_ssl: false
            on_response:
              then:
                - logger.log:
                    format: "Response status: %d, Duration: %u ms"
                    args:
                      - status_code
                      - duration_ms


.. _http_request-examples:

Examples
--------

Templatable values
******************

.. code-block:: yaml

    on_...:
      - http_request.post:
          url: !lambda |-
            return ((std::string) "https://esphome.io?state=" + id(my_sensor).state).c_str();
          headers:
            X-Custom-Header: !lambda |-
              return ((std::string) "Value-" + id(my_sensor).state).c_str();
          body: !lambda |-
            return id(my_sensor).state;


POST Body in JSON format (syntax 1)
***********************************

**Note:** all values of the map should be a strings.
It's impossible to send ``boolean`` or ``numbers`` with this syntax.

.. code-block:: yaml

    on_...:
      - http_request.post:
          url: https://esphome.io
          verify_ssl: false
          json:
            key: !lambda |-
              return id(my_sensor).state;
            greeting: "Hello World"

        # Will send:
        # {"key": "42.0", "greeting": "Hello World"}

POST Body in JSON format (syntax 2)
***********************************

**Note:** use this syntax to send ``boolean`` or ``numbers`` in JSON.

The JSON message will be constructed using the `ArduinoJson <https://github.com/bblanchon/ArduinoJson>`__ library.
In the ``json`` option you have access to a ``root`` object which will represents the base object
of the JSON message. You can assign values to keys by using the ``root["KEY_NAME"] = VALUE;`` syntax
as seen below.

.. code-block:: yaml

    on_...:
      - http_request.post:
          url: https://esphome.io
          verify_ssl: false
          json: |-
            root["key"] = id(my_sensor).state;
            root["greeting"] = "Hello World";

        # Will send:
        # {"key": 42.0, "greeting": "Hello World"}

GET values from a JSON body response
************************************

Assuming that the server returns a response in a JSON object over HTTP similar to this:
``{"status":"play","vol":"42","mute":"0"}``

If you want to retrieve the value for the ``vol`` key and assign it to a template ``sensor`` or ``number`` component (with ``id`` set to ``player_volume``):

.. code-block:: yaml

    on_...:
    - http_request.get:
        url: https://esphome.io
        on_response:
          then:
            - lambda: |-
                json::parse_json(id(http_request_data).get_string(), [](JsonObject root) {
                    id(player_volume).publish_state(root["vol"]);
                });

**Note:** don't forget to set the ``id`` for the main ``http_request`` component, to ``http_request_data``.


See Also
--------

- :doc:`index`
- :apiref:`http_request/http_request.h`
- :ghedit:`Edit`
