HTTP Request
============

.. seo::
    :description: Instructions for setting up HTTP Requests in ESPHome
    :image: connection.png
    :keywords: http, request


The ``http_request`` component lets you make HTTP/HTTPS requests.

.. note::

    This component works only with :ref:`arduino framework <esphome-arduino_version>` 2.5.0 or newer.

First, you need to setup a component:

.. code-block:: yaml

    # Example configuration entry
    http_request:
      useragent: esphome/device
      timeout: 10s

Configuration variables:
------------------------

- **useragent** (*Optional*, string): User-Agent header for requests. Defaults to ``ESPHome``.
- **timeout** (*Optional*, :ref:`time <config-time>`): Timeout for request. Defaults to ``5s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

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
      # Short form
      - http_request.get: https://esphome.io

Configuration variables:

- **url** (**Required**, string, :ref:`templatable <config-templatable>`): URL to send request.
- **headers** (*Optional*, mapping): Map of HTTP headers. Values are :ref:`templatable <config-templatable>`.
- **verify_ssl** (*Optional*, boolean): Verify the SSL certificate of the endpoint. Defaults to ``true``.

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


Body in JSON format (syntax 1)
******************************

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

Body in JSON format (syntax 2)
******************************

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

See Also
--------

- :doc:`index`
- :apiref:`http_request/http_request.h`
- :ghedit:`Edit`
