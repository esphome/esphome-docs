OTA via HTTP Update Component
=============================

.. seo::
    :description: Instructions for setting up Over-The-Air (OTA) updates for ESPs to download firmwares remotely by HTTP.
    :image: system-update.svg

With the OTA (Over The Air) via HTTP update component, your devices can install updated firmware on their own.
To use it, in your device's configuration, you specify a URL from which the device will download the binary
file (firmware). To trigger the update, an ESPHome :ref:`action <config-action>` is used which initiates the
download and installation of the new firmware. Once complete, the device is rebooted, invoking the new firmware.

Since the device functions as an HTTP(S) client, it can be on a foreign network or behind a firewall. This mechanism
is primarily useful with either standalone or MQTT-only devices.

.. code-block:: yaml

    # Example configuration entry
    ota_http:

    button:
      - platform: template
        name: "Firmware update"
        on_press:
          then:
            - ota_http.flash:
                md5_url: http://example.com/firmware.md5
                url: http://example.com/firmware.bin
            - logger.log: "This message should be not displayed because the device reboots"

Configuration variables:
------------------------

- **esp8266_disable_ssl_support** (*Optional*, boolean): Disables SSL support on the ESP8266 when set to ``true``.
  **Only available on ESP8266.** Defaults to ``false``. See :ref:`esphome-esp8266_disable_ssl_support` for more information.
- **exclude_certificate_bundle** (*Optional*, boolean): When set to ``true``, the default ESP x509 certificate bundle
  is excluded from the build. This certificate bundle includes the complete list of root certificates from Mozilla's
  NSS root certificate store. Defaults to ``false``.
  **Only available when using the ESP-IDF framework; must be explicitly set to true when using the Arduino framework.**
- **safe_mode** (*Optional*, boolean, string): Flash at boot time. Defaults to ``fallback``.
    Valid values:
        - ``no``: Never attempt to flash at boot time.
        - ``yes``: Always flash at boot time.
        - ``fallback``: Retry at boot time if OTA fails.
- **watchdog_timeout** (*Optional*, :ref:`config-time`): Change the watchdog timeout during flash operation.
  Can be useful on slow certificate validation, or if the http server is behind a slow proxy.
  **Only available on ESP32 and RP2040**.

.. warning::

    Setting ``exclude_certificate_bundle`` to ``true`` **reduces security** when using HTTPS connections!

    Without the certificate bundle, the remote HTTPS server cannot be verified, opening the update process up to
    man-in-the-middle attacks. To maximize security, this option should **only** be enabled when the device does
    not have sufficient memory to store the certificate bundle, when a custom CA/self-signed certificate is used
    or when the Arduino framework is used.

.. note::

    You can obtain the ``firmware.bin`` from either:

    - **ESPHome dashboard** (HA add-on): download in *"Legacy format"*
    - **ESPHome CLI**: the directory ``.esphome/build/project/.pioenvs/project/firmware.bin``

      ...where *"project"* is the name of your ESPHome device/project.

    You **cannot** use ``firmware-factory.bin`` or *"Modern format"* with ``ota_http``.

.. _ota_http-flash_action:

``ota_http.flash`` Action
-------------------------

This action triggers the download and installation of the updated firmware from the configured URL.
As it's an ESPHome :ref:`action <config-action>`, it may be used in any ESPHome automation(s).

.. code-block:: yaml

    on_...:
      then:
        - ota_http.flash:
            md5_url: http://example.com/firmware.md5
            url: https://example.com/firmware.bin
        - logger.log: "This message should be not displayed because the device reboots"

        # Templated:
        - ota_http.flash:
            md5_url: !lambda return id(text_sensor_md5).state;
            url: !lambda return id(text_sensor_url).state;
        - logger.log: "This message should be not displayed because the device reboots"

Configuration variables:
------------------------

- **md5_url** (**Required**, string, :ref:`templatable <config-templatable>`):
  The URL of the file containing an `MD5sum <https://en.wikipedia.org/wiki/Md5sum>`_ of the firmware file
  pointed to by ``url`` (below).
- **url** (**Required**, string, :ref:`templatable <config-templatable>`):
  The URL of the binary file containing the (new) firmware to be installed.

.. note::

    - Basic authentication is supported with **https://username:password@example.com/firmware.bin**.  `username`
      and `password` must be `URL-encoded <https://en.wikipedia.org/wiki/Percent-encoding>`_  if they include
      special characters.

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

See Also
--------

- :doc:`/components/ota`
- :doc:`/components/http_request`
- :ghedit:`Edit`
