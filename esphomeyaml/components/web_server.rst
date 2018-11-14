Web Server Component
====================

.. seo::
    :description: Instructions for setting up a web server in esphomelib.
    :image: http.svg
    :keywords: web server, http, REST API

The ``web_server`` component creates a simple web server on the node that can be accessed
through any browser and a simple `REST API`_. Please note that enabling this component
will take up *a lot* of memory and can lead to problems, especially on the ESP8266.

To navigate to the web server in your browser, either use the IP address of the node or
use ``<node_name>.local/`` (note the trailing forward slash) via mDNS.

To conserve flash size, the CSS and JS files used on the root page to show a simple user
interface are hosted by esphomelib.com. If you want to use your own service, use the
``css_url`` and ``js_url`` options in your configuration.

.. _REST API: /web-api/index.html

.. figure:: /esphomeyaml/components/images/web_server.png
    :align: center

    Example web server frontend.

.. code:: yaml

    # Example configuration entry
    web_server:
      port: 80

Configuration variables:
------------------------

- **port** (*Optional*, int): The port the web server should open its socket on.
- **css_url** (*Optional*, url): The URL that should be used for the CSS stylesheet. Defaults
  to https://esphomelib.com/_static/webserver-v1.min.css (updates will go to ``v2``, ``v3``, etc).
- **js_url** (*Optional*, url): The URL that should be used for the JS script. Defaults
  to https://esphomelib.com/_static/webserver-v1.min.js.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. note::

    Starting with version 1.9.0, you can also upload firmware files OTA with the web server.

See Also
--------

- :doc:`API Reference </api/core/web-server>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/web_server.rst>`__

.. disqus::
