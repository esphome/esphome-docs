Web Server Component
====================

.. seo::
    :description: Instructions for setting up a web server in ESPHome.
    :image: http.svg
    :keywords: web server, http, REST API

The ``web_server`` component creates a simple web server on the node that can be accessed
through any browser and a simple :ref:`api-rest`. Please note that enabling this component
will take up *a lot* of memory and may decrease stability, especially on ESP8266.

.. figure:: /components/images/web_server.png
    :align: center
    :width: 86.0%

    Web server version 1


.. figure:: /components/images/web_server-v2.png
    :align: center
    :width: 86.0%

    Web server version 2


To navigate to the web server in your browser, either use the IP address of the node or
use ``<node_name>.local/`` (note the trailing forward slash) via mDNS.


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
- **auth** (*Optional*): Enables a simple *Digest* authentication with username and password.

  - **username** (**Required**, string): The username to use for authentication.
  - **password** (**Required**, string): The password to check for authentication.

- **include_internal** (*Optional*, boolean): Whether ``internal`` entities should be displayed on the
  web interface. Defaults to ``false``.
- **enable_private_network_access** (*Optional*, boolean): Enables support for
  `Private Network Access <https://wicg.github.io/private-network-access>`__ and the
  `Private Network Access Permission Prompt <https://wicg.github.io/private-network-access/#permission-prompt>`__.
  Defaults to ``true``.
- **log** (*Optional*, boolean): Turn on or off the log feature inside webserver. Defaults to ``true``.
- **ota** (*Optional*, boolean): Turn on or off the OTA feature inside webserver. Strongly not suggested without enabled authentication settings. Defaults to ``true``. Cannot be used with the ``esp-idf`` framework.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **local** (*Optional*, boolean): Include supporting javascript locally allowing it to work without internet access. Defaults to ``false``.
- **version** (*Optional*, string): ``1`` or ``2``. Version 1 displays as a table. Version 2 uses web components and has more functionality. Defaults to ``2``.

To conserve flash size, the CSS and JS files used on the root page to show a simple user
interface are hosted by esphome.io. If you want to use your own service, use the
``css_url`` and ``js_url`` options in your configuration.

Example configurations:
-----------------------

Enabling HTTP authentication:

.. code-block:: yaml

    # Example configuration entry
    web_server:
      port: 80
      auth:
        username: !secret web_server_username
        password: !secret web_server_password

Use version 1 user interface:

.. code-block:: yaml

    # Example configuration entry
    web_server:
      port: 80
      version: 1

No internet/intranet required on the clients (all assets are inlined, compressed and served from flash):

.. code-block:: yaml

    # Example configuration entry
    web_server:
      local: true


Advanced usage
--------------

The following assume copies of the files with local paths - which are config dependant.

Example ``web_server`` version 1 configuration with CSS and JS included from esphome-docs.
CSS and JS URL's are set to empty value, so no internet access is needed for this device to show it's web interface.
Force to turn off OTA function because the missing authentication.

.. code-block:: yaml

    web_server:
      port: 80
      version: 1
      ota: false
      css_include: "../../../esphome-docs/_static/webserver-v1.min.css"
      css_url: ""
      js_include: "../../../esphome-docs/_static/webserver-v1.min.js"
      js_url: ""

Example ``web_server`` version 2 configuration with JS included from a local file.
CSS and JS URL's are set to empty value, so no internet access is needed for this device to show it's web interface.
V2 embeds the css within the js file so is not required, however you could include your own CSS.

.. code-block:: yaml

    # Example configuration entry v2
    web_server:
      js_include: "./v2/www.js"
      js_url: ""
      version: 2

Copy https://oi.esphome.io/v2/www.js to a V2 folder in your yaml folder.


See Also
--------

- :ref:`api-event-source`
- :ref:`api-rest`
- :apiref:`web_server/web_server.h`
- :doc:`prometheus`
- :ghedit:`Edit`
