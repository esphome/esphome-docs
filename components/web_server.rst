Web Server Component
====================

.. seo::
    :description: Instructions for setting up a web server in ESPHome.
    :image: http.png
    :keywords: web server, http, REST API

The ``web_server`` component creates a simple web server on the node that can be accessed
through any browser and a simple `REST API`_. Please note that enabling this component
will take up *a lot* of memory and can lead to problems, especially on the ESP8266.

To navigate to the web server in your browser, either use the IP address of the node or
use ``<node_name>.local/`` (note the trailing forward slash) via mDNS.

To conserve flash size, the CSS and JS files used on the root page to show a simple user
interface are hosted by esphome.io. If you want to use your own service, use the
``css_url`` and ``js_url`` options in your configuration.

.. _REST API: /web-api/index.html

.. figure:: /components/images/web_server.png
    :align: center

    Example web server frontend.

.. code-block:: yaml

    # Example configuration entry
    web_server:
      port: 80


Configuration variables:
------------------------

- **port** (*Optional*, int): The port the web server should open its socket on.
- **css_url** (*Optional*, url): The URL that should be used for the CSS stylesheet. Defaults
  to https://esphome.io/_static/webserver-v1.min.css (updates will go to ``v2``, ``v3``, etc). Can be set to empty string.
- **css_include** (*Optional*, local file): Path to local file to be included in web server index page.
  Contents of this file will be served as ``/0.css`` and used as CSS stylesheet by internal webserver.
  Useful when building device without internet access, where you want to use built-in AP and webserver.
- **js_url** (*Optional*, url): The URL that should be used for the JS script. Defaults
  to https://esphome.io/_static/webserver-v1.min.js. Can be set to empty string.
- **js_include** (*Optional*, local file): Path to local file to be included in web server index page.
  Contents of this file will be served as ``/0.js`` and used as JS script by internal webserver.
  Useful when building device without internet access, where you want to use built-in AP and webserver.
- **auth** (*Optional*): Enables basic authentication with username and password.

  - **username** (**Required**, string): The username to use for authentication.
  - **password** (**Required**, string): The password to check for authentication.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. note::

    Example web_server configuration using HTTP authentication:

    .. code-block:: yaml

        # Example configuration entry
        web_server:
          port: 80
          auth:
            username: admin
            password: !secret web_server_password

    Example web_server configuration with CSS and JS included from esphome-docs.
    CSS and JS URL's are set to empty value, so no internet access is needed for this device to show it's web interface.

    .. code-block:: yaml

        # Example configuration entry
        web_server:
          port: 80
          css_include: "../../../esphome-docs/_static/webserver-v1.min.css"
          css_url: ""
          js_include: "../../../esphome-docs/_static/webserver-v1.min.js"
          js_url: ""

See Also
--------

- :apiref:`web_server/web_server.h`
- :doc:`prometheus`
- :ghedit:`Edit`
