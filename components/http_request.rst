HTTP Request
============

.. seo::
    :description: Instructions for setting up HTTP Requests in ESPHome
    :image: connection.svg
    :keywords: http, request


The ``http_request`` component lets you make HTTP/HTTPS requests. To do so, you need to add it to your device's configuration:

.. code-block:: yaml

    # Example configuration entry
    http_request:

.. _http_request-configuration_variables:

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **follow_redirects** (*Optional*, boolean): Enable following HTTP redirects. Defaults to ``true``.
- **redirect_limit** (*Optional*, integer): Maximum amount of redirects to follow when enabled. Defaults to ``3``.
- **timeout** (*Optional*, :ref:`config-time`): Timeout for request. Defaults to ``4.5s``.
- **useragent** (*Optional*, string): User-Agent header for requests. Defaults to
  ``ESPHome/<version> (https://esphome.io)`` where ``<version>`` is the version of ESPHome the device is running.
  For example: ``ESPHome/2024.6.0 (https://esphome.io)``
- **verify_ssl** (*Optional*, boolean): When set to ``true`` (default), SSL/TLS certificates will be validated upon
  connection; if invalid, the connection will be aborted. To accomplish this, ESP-IDF's default ESP x509 certificate
  bundle is included in the build. This certificate bundle includes the complete list of root certificates from
  Mozilla's NSS root certificate store. **May only be set to true when using the ESP-IDF framework; must be explicitly
  set to false when using the Arduino framework.**
- **watchdog_timeout** (*Optional*, :ref:`config-time`): Change the watchdog timeout during connection/data transfer.
  May be useful on slow connections or connections with high latency. **Do not change this value unless you are
  experiencing device reboots due to watchdog timeouts;** doing so may prevent the device from rebooting due to a
  legitimate problem. **Only available on ESP32 and RP2040**.

**For the ESP32 when using ESP-IDF:**

- **buffer_size_rx** (*Optional*, integer): Change HTTP receive buffer size. Defaults to ``512``.
- **buffer_size_tx** (*Optional*, integer): Change HTTP transmit buffer size. Defaults to ``512``.

**For the ESP8266:**

- **esp8266_disable_ssl_support** (*Optional*, boolean): Determines whether to include HTTPS/SSL support in the
  firmware binary. Excluding the SSL libraries from your build will result in a smaller binary, which may be
  necessary for memory-constrained devices (512 kB or 1 MB). If you see
  ``Error: ESP does not have enough space to store OTA file`` in your device's logs, you may need to enable this
  option. Defaults to ``false``. By setting this option to ``true``:

  - HTTPS connections will not be possible
  - ``verify_ssl: false`` is implied

.. warning::

    Setting ``verify_ssl`` to ``false`` **reduces security** when using HTTPS connections!

    Without the root certificate bundle, certificates used by the remote HTTPS server cannot be verified, opening the
    HTTPS connection up to person-in-the-middle attacks.

    To maximize security, do not set ``verify_ssl`` to ``false`` *unless:*

    - a custom CA/self-signed certificate is used,
    - the Arduino framework is used, or
    - the device does not have sufficient memory to store the certificate bundle

    **We strongly recommend using hardware which properly supports TLS/SSL.**

HTTP Request Actions
--------------------

The ``http_request`` component supports a number of :ref:`actions <config-action>` that can be used to send requests.

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
          on_response:
            then:
              - logger.log:
                  format: 'Response status: %d, Duration: %u ms'
                  args:
                    - response->status_code
                    - response->duration_ms
      # Short form
      - http_request.get: https://esphome.io

**Configuration variables:**

- **url** (**Required**, string, :ref:`templatable <config-templatable>`): URL to which to send the request.
- **headers** (*Optional*, mapping): Map of HTTP headers. Values are :ref:`templatable <config-templatable>`.
- **capture_response** (*Optional*, boolean): when set to ``true``, the response data will be captured and placed into
  the ``body`` variable as a ``std::string`` for use in :ref:`lambdas <config-lambda>`. Defaults to ``false``.
- **max_response_buffer_size** (*Optional*, integer): The maximum buffer size to be used to store the response.
  Defaults to ``1 kB``.
- **on_response** (*Optional*, :ref:`Automation <automation>`): An automation to perform after the request is received.

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
      # Short form
      - http_request.post: https://esphome.io

**Configuration variables:**

- **body** (*Optional*, string, :ref:`templatable <config-templatable>`): A HTTP body string to send with request.
- **json** (*Optional*, mapping): A HTTP body in JSON format. Values are :ref:`templatable <config-templatable>`.
  See :ref:`http_request-examples`.
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

**Configuration variables:**

- **method** (**Required**, string): HTTP method to use (``GET``, ``POST``, ``PUT``, ``DELETE``, ``PATCH``).
- All other options from :ref:`http_request-post_action` and :ref:`http_request-get_action`.

.. _http_request-on_response:

``on_response`` Trigger
-----------------------

This automation will be triggered when the HTTP request is complete.
The following variables are available for use in :ref:`lambdas <config-lambda>`:

- ``response`` as a pointer to ``HttpContainer`` object which contains ``content_length``, ``status_code`` and ``duration_ms``.
- ``body`` as ``std::string`` which contains the response body when ``capture_response``
  (see :ref:`http_request-get_action`) is set to ``true``.

.. code-block:: yaml

    on_...
      then:
        - http_request.get:
            url: https://esphome.io
            on_response:
              then:
                - logger.log:
                    format: "Response status: %d, Duration: %u ms"
                    args:
                      - response->status_code
                      - response->duration_ms
                - lambda: |-
                    ESP_LOGD(TAG, "Response status: %d, Duration: %u ms", response->status_code, response->duration_ms);


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

**Note:** all values of the map must be strings. It is not possible to send JSON ``boolean`` or ``numbers`` with this
syntax.

.. code-block:: yaml

    on_...:
      - http_request.post:
          url: https://esphome.io
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
In the ``json`` option you have access to a ``root`` object which represents the base object of the JSON message. You
can assign values to keys by using the ``root["KEY_NAME"] = VALUE;`` syntax as shown below.

.. code-block:: yaml

    on_...:
      - http_request.post:
          url: https://esphome.io
          json: |-
            root["key"] = id(my_sensor).state;
            root["greeting"] = "Hello World";

        # Will send:
        # {"key": 42.0, "greeting": "Hello World"}

GET values from a JSON body response
************************************

This example assumes that the server returns a response as a JSON object similar to this:
``{"status":"play","vol":"42","mute":"0"}``

If you want to retrieve the value for the ``vol`` key and assign it to a template ``sensor`` or ``number`` component
whose ``id`` is  set to ``player_volume``:

.. code-block:: yaml

    on_...:
    - http_request.get:
        url: https://esphome.io
        capture_response: true
        on_response:
          then:
            - lambda: |-
                json::parse_json(body, [](JsonObject root) -> bool {
                    id(player_volume).publish_state(root["vol"]);
                    return true;
                });


See Also
--------

- :doc:`index`
- :apiref:`http_request/http_request.h`
- :ghedit:`Edit`
