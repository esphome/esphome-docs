OTA Update via HTTP Request Component
=====================================

.. seo::
    :description: Instructions for setting up Over-The-Air (OTA) updates for ESPs to download firmwares remotely by HTTP.
    :image: system-update.svg

With the OTA (Over The Air) via HTTP Request update component, your devices can install updated firmware on their own.
To use it, in your device's configuration, you specify a URL from which the device will download the binary
file (firmware). To trigger the update, an ESPHome :ref:`action <config-action>` is used which initiates the
download and installation of the new firmware. Once complete, the device is rebooted, invoking the new firmware.

Since the device functions as an HTTP(S) client, it can be on a foreign network or behind a firewall. This mechanism
is primarily useful with either standalone or MQTT-only devices.

.. code-block:: yaml

    # Example configuration entry
    ota:
      - platform: http_request

    # OTA updade trigerred by a button
    button:
      - platform: template
        name: Firmware update
        on_press:
          then:
            - ota_http_request.flash:
                md5_url: http://example.com/firmware.md5
                url: http://example.com/firmware.bin
            - logger.log: "This message should be not displayed because the device reboots"


Configuration variables:
------------------------

- **esp8266_disable_ssl_support** (*Optional*, boolean): When set to ``true``, HTTPS/SSL support is excluded from the
  build, resulting in a smaller binary. HTTPS connections will not be possible. **Only available on ESP8266.** Defaults
  to ``false``. See :ref:`esphome-esp8266_disable_ssl_support` for more information.
- **verify_ssl** (*Optional*, boolean): When set to ``true``, SSL/TLS certificate validity will be verified upon
  connection. To accomplish this, ESP-IDF's default ESP x509 certificate bundle is included in the build. This
  certificate bundle includes the complete list of root certificates from Mozilla's NSS root certificate store.
  Defaults to ``true``. **May only be set to true when using the ESP-IDF framework; must be explicitly set to false
  when using the Arduino framework.**
- **watchdog_timeout** (*Optional*, :ref:`config-time`): Change the watchdog timeout during flash operation.
  May be useful on slow connections or connections with high latency. **Do not change this value unless you are
  experiencing device reboots due to watchdog timeouts;** doing so may prevent the device from rebooting due to a
  legitimate problem. **Only available on ESP32 and RP2040**.

.. warning::

    Setting ``verify_ssl`` to ``false`` **reduces security** when using HTTPS connections!

    Without the certificate bundle, certificates used by the remote HTTPS server cannot be verified, opening the update
    process up to man-in-the-middle attacks.
    
    To maximize security, do not set ``verify_ssl`` to ``false`` *unless:*
    
    - the device does not have sufficient memory to store the certificate bundle
    - a custom CA/self-signed certificate is used, or
    - the Arduino framework is used

.. note::

    You can obtain the ``firmware.bin`` from either:

    - **ESPHome dashboard** (HA add-on): download in *"Legacy format"*
    - **ESPHome CLI**: the directory ``.esphome/build/project/.pioenvs/project/firmware.bin``

      ...where *"project"* is the name of your ESPHome device/project.

    You **cannot** use ``firmware-factory.bin`` or *"Modern format"* with ``ota_http_request``.

.. _ota_http_request-flash_action:

``ota_http_request.flash`` Action
---------------------------------

This action triggers the download and installation of the updated firmware from the configured URL.
As it's an ESPHome :ref:`action <config-action>`, it may be used in any ESPHome automation(s).

.. code-block:: yaml

    on_...:
      then:
        - ota_http_request.flash:
            md5_url: http://example.com/firmware.md5
            url: https://example.com/firmware.bin
        - logger.log: "This message should be not displayed because the device reboots"

Configuration variables:
------------------------

- **md5** (*Optional*, string, :ref:`templatable <config-templatable>`): The
  `MD5sum <https://en.wikipedia.org/wiki/Md5sum>`_ of the firmware file pointed to by ``url`` (below). May not be used
  with ``md5_url`` (below); must be specified if ``md5_url`` is not.
- **md5_url** (*Optional*, string, :ref:`templatable <config-templatable>`): The URL of the file containing an
  `MD5sum <https://en.wikipedia.org/wiki/Md5sum>`_ of the firmware file pointed to by ``url`` (below). May not be used
  with ``md5`` (above); must be specified if ``md5`` is not.
- **url** (**Required**, string, :ref:`templatable <config-templatable>`): The URL of the binary file containing the
  (new) firmware to be installed.
- **username** (*Optional*, string, :ref:`templatable <config-templatable>`): The username to use for HTTP basic
  authentication.
- **password** (*Optional*, string, :ref:`templatable <config-templatable>`): The password to use for HTTP basic
  authentication.

.. note::

    - ``username`` and ``password`` must be `URL-encoded <https://en.wikipedia.org/wiki/Percent-encoding>`_  if they
      include special characters.

    - The `MD5sum <https://en.wikipedia.org/wiki/Md5sum>`_ of the firmware binary file is an ASCII file (also known
      as "plain text", typically found in files with a ``.txt`` extension) consisting of 32 lowercase hexadecimal
      characters. It can be obtained and saved to a file with the following command(s):

      - On macOS:

        .. code-block:: shell

            md5 -q firmware.bin > firmware.md5

      - On most Linux distributions:

        .. code-block:: shell

            md5sum firmware.bin > firmware.md5

      - On Windows/PowerShell:

        .. code-block:: shell

            (Get-FileHash -Path firmware.bin -Algorithm md5).Hash.ToLower() | Out-File -FilePath firmware.md5 -Encoding ASCII

      This will generate the MD5 hash of the ``firmware.bin`` file and write the resulting hash value to the
      ``firmware.md5`` file. The ``md5_url`` configuration variable should point to this file on the web server.
      It is used by the OTA updating mechanism to ensure the integrity of the (new) firmware as it is installed.
      
      **If, for any reason, the MD5sum provided does not match the MD5sum computed as the firmware is installed, the
      device will continue to use the original firmware and the new firmware is discarded.**

See Also
--------

- :doc:`/components/ota`
- :doc:`/components/http_request`
- :ghedit:`Edit`
