Web Server Component
====================

.. seo::
    :description: Instructions for setting up a web server in ESPHome.
    :image: http.svg
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

    Example web server frontend (Version 1)
    
Version 2:
----------
.. figure:: /components/images/web_server-v2.png 

    Web Components (Version 2)

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

- **include_internal** (*Optional*, boolean): Whether ``internal`` entities should be displayed on the
  web interface. Defaults to ``false``.
- **ota** (*Optional*, boolean): Turn on or off the OTA feature inside webserver. Strongly not suggested without enabled authentication settings. Default: `true`
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **version** (*Optional*, string): 1 or 2. Version 1 displays as a table. Version 2 uses web components and has more functionality. Default: `2`
- **app** (*Optional*): Enables inlining (embedding) and serving static files from flash.

  - **source** (**Required**, local directory): Path to local directory containing static files to inline (embed) and serve under ``/app/`` URL prefix.

.. note::

    Example web_server configuration using HTTP authentication:

    .. code-block:: yaml

        # Example configuration entry
        web_server:
          port: 80
          auth:
            username: admin
            password: !secret web_server_password
            
    Example web_server configuration using version 1 (previous behaviour):

    .. code-block:: yaml

        # Example configuration entry
        web_server:
          port: 80
          version: 1
          
    Example web_server configuration using version 2  - no internet/intranet required:

    .. code-block:: yaml

        # Example configuration entry
        web_server:
          local: true
          
    All of the assets are inlined, compressed and served from flash

Here be Dragons
===============
    
The following assume copies of the files with local paths - which are config dependant.

Example web_server version 1 configuration with CSS and JS included from esphome-docs.
CSS and JS URL's are set to empty value, so no internet access is needed for this device to show it's web interface.
Force to turn off OTA function because the missing authentication.

.. code-block:: yaml

    # Example configuration entry V1
    web_server:
      port: 80
      ota: false
      css_include: "../../../esphome-docs/_static/webserver-v1.min.css"
      js_include: "../../../esphome-docs/_static/webserver-v1.min.js"
      js_url: ""

Example web_server version 2 configuration with JS included from a local file.

CSS and JS URL's are set to empty value, so no internet access is needed for this device to show it's web interface.
V2 embeds the css within the js file so is not required, however you could include your own CSS.

.. code-block:: yaml

    # Example configuration entry V2
    web_server:
      js_include: "./v2/www.js"
      js_url: ""
      version: 2


Copy https://oi.esphome.io/v2/www.js to a V2 folder in your yaml folder.
        

Serving static files or web applications
========================================

:doc:`/web-api/index` provides a powerful REST and Event Source API that can be used for managing various aspects
of an ESPHome device. The default web server interface provides a generic web page for interfacing with the device,
but sometimes a more tailored made solution is needed (e.g. displaying real-time charts, exposing only a subset of
switches, etc.).

Web application configuration of ``web_server`` component allows for inlining (embedding) of web application
files (HTML, Javascript, CSS) into flash storage of a device and serving them directly from the device under
``/app/`` URL prefix.

Example ``web_server`` configuration for embedding and serving static files from local ``www`` directory:

.. code-block:: yaml

    # Example configuration entry
    web_server:
      app:
        source: www

The above configuration block will inline (embed) all files from the local directory ``www`` and serve them under
``/app/`` URL prefix - for example:

- local file ``www/index.html`` will be accessible by visiting ``http://<node_name>.local/app/index.html``
- local file ``www/app.js`` will be accessible by visiting ``http://<node_name>.local/app/app.js``


Media (MIME) types
------------------

Web browsers expect web servers to serve static files with ``Content-Type`` header containing IANA Media Type
(MIME type) for the particular file. ESPHome will try to auto-detect files' media types based on the list
of known file extensions. The location of the list is dependent on the operating system: registry on Windows,
``/etc/mime.types`` on Unix-like systems). See https://docs.python.org/3.8/library/mimetypes.html for details.

ESPHome will output the detected media type for a file when adding the file to firmware:

.. code-block::

    INFO Adding web app file: www/index.html as app/index.html (size 2087, text/html, encoding none)


Compression
-----------

It is recommended that static web application files (HTML, Javascript, CSS, ...) are compressed to better utilize
the available flash space on a device. Determining which files to compress is beyond the scope of ESPHome as some
files compress really well (text files) while others (images) don't.

Web application inlining logic of ``web_server`` component expects the application files to be compressed by the
provider of the files and that files are marked as compressed by having a correct file extension for the chosen
compression algorithm (e.g. ``.gz`` for ``gzip`` compression). ESPHome will store compressed files in flash and
serve them in a compressed form under the name of the original (non-compressed) file with the correct setting
of HTTP ``Transfer-Encoding`` header. All modern web browsers are able to perform decompression on-the-fly and
process the file in an uncompressed form.

For example:

- local file ``www/index.html.gz`` will be accessible as ``http://<node_name>.local/app/index.html`` and ESPHome
  will set headers ``Content-Type: text/html`` and ``Transfer-Encoding: gzip`` when serving the file.

ESPHome will output the detected compression algorithm for a file when adding the file to firmware:

.. code-block::

    INFO Adding web app file: www/index.html.gz as app/index.html (size 1057, text/html, encoding gzip)

Multiple compression algorithms are detected (gzip, compress, bzip2, xz, br) but it is recommended to use ``gzip``
as it is currently the most widely supported one in web browsers.


Accessing the application (index.html)
--------------------------------------

All statically served files can be accessed directly by navigating to ``http://<node_name>.local/app/<file_name>``.

A shortcut for accessing ``index.html`` is provided by either navigating to:

- ``http://<node_name>.local/app/`` which serves ``index.html`` file if the file exists (eror 404 otherwise),
- or ``http://<node_name>.local/app`` which redirects the browser to ``http://<node_name>.local/app/`` which,
  in-turn, serves ``index.html`` file.


Example
-------

A production build of an Angular application produces the following static files in ``../dist/my_app``:

.. code-block::

    index.html
    main.14bf39656ae912e1.js
    polyfills.5902314ff3f2eac9.js
    runtime.f7d50caa802bfcbd.js
    styles.42da88a97f9b7241.css

Files are compressed using ``gzip`` compression utility by running ``gzip *.html *.css *.js``, producing:

.. code-block::

    index.html.gz
    main.14bf39656ae912e1.js.gz
    polyfills.5902314ff3f2eac9.js.gz
    runtime.f7d50caa802bfcbd.js.gz
    styles.42da88a97f9b7241.css.gz

ESPHome is configured with the following code block:

.. code-block:: yaml

    # Web app configuration
    web_server:
      app:
        source: ../dist/my_app

ESPHome ``compile`` inlines (embeds) the files in firmware and makes them available under ``/app/`` URL prefix:

.. code-block::

    INFO Adding web app file: ../dist/my_app/index.html.gz as app/index.html (size 1057, text/html, encoding gzip)
    INFO Adding web app file: ../dist/my_app/polyfills.5902314ff3f2eac9.js.gz as app/polyfills.5902314ff3f2eac9.js (size 12248, application/javascript, encoding gzip)
    INFO Adding web app file: ../dist/my_app/main.14bf39656ae912e1.js.gz as app/main.14bf39656ae912e1.js (size 154552, application/javascript, encoding gzip)
    INFO Adding web app file: ../dist/my_app/styles.42da88a97f9b7241.css.gz as app/styles.42da88a97f9b7241.css (size 23125, text/css, encoding gzip)
    INFO Adding web app file: ../dist/my_app/runtime.f7d50caa802bfcbd.js.gz as app/runtime.f7d50caa802bfcbd.js (size 669, application/javascript, encoding gzip)

Navigating browser to ``http://<node_name>.local/app/index.html`` or ``http://<node_name>.local/app/`` or ``http://<node_name>.local/app`` will
open the application.


See Also
--------

- :apiref:`web_server/web_server.h`
- :doc:`prometheus`
- :ghedit:`Edit`
