OTA HTTP Update Component
=========================

.. seo::
    :description: Instructions for setting up Over-The-Air (OTA) updates for ESPs to download firmwares remotely by HTTP.
    :image: system-update.svg

With the OTA (Over The Air) HTTP update component, your devices can install updated firmware on their own. This is achieved by configuring a URL from which the device will download the binary file and then triggering an action which causes the (new) firmware to be written to the device's flash memory. Once complete, the device is rebooted, invoking the new firmware.

As the device is in client mode, it can be on a foreign network or behind a firewall. This mechanism is primarily useful with either standalone or MQTT-only devices.

.. code-block:: yaml

    # Example configuration entry
    ota_http:

    button:
      - platform: template
        name: "Firmware update"
        on_press:
          then:
            - ota_http.flash:
                url: http://example.com/firmware.bin
                verify_ssl: false 
            - logger.log: "This message should be not displayed(reboot)"

Configuration variables:
------------------------

- **esp8266_disable_ssl_support** (*Optional*, boolean): Whether to include SSL support. **Only available on ESP8266.**
  Defaults to ``no``. See :ref:`esphome-esp8266_disable_ssl_support` for more information.
-  **safe_mode** (*Optional*, boolean, string): Flash at boot time. Defaults to ``fallback``.
    Valid values:
        - ``no``: Never attempt to flash at boot time.
        - ``yes``: Always flash at boot time.
        - ``fallback``: Retry at boot time if OTA fails.


.. note::

    The file ``firmware.bin`` can be found at ```.esphome/build/xxxx/.pioenvs/xxx/firmware.bin`` if esphome CLI is used, 
    or downloaded as ``Legacy format`` from the esphome HA addon. ota_http currently **Doesn't works** with ``firmware-factory.bin`` or ``Modern format``.

 .. _ota_http-flash_action:

``ota_http.flash`` Action
-------------------------

This action triggers the device to download and install updated firmware from the configured URL. As it's an ESPHome :ref:`action <config-action>`, it may be used in any automation(s).

.. code-block:: yaml

    on_...:
      then:
        - ota_http.flash:
            url: https://example.com/firmware.bin
            verify_ssl: false
        - logger.log: "This message should be not displayed(reboot)"

        # Templated:
        - ota_http.flash:
            url: !lambda return id(text_sensor).state;
        - logger.log: "This message should be not displayed(reboot)"

Configuration variables:

-  **url** (**Required**, string, :ref:`templatable <config-templatable>`):
    The URL of the firmware. Basic auth is supported with **https://user:password@example.com/firmware.bin**. 
    `username` and `password` must be `url-encoded <https://en.wikipedia.org/wiki/Percent-encoding>`_  if they include special characters.
-  **verify_ssl** (*Optional*, boolean, :ref:`templatable <config-templatable>`): 
    Specifies whether the SSL certificate must be verified. Must be explicitly set to ``false`` if using **https**. 
    See :ref:`http_request-get_action` for more information.


See Also
--------

- :doc:`/components/ota`
- :doc:`/components/http_request`
- :ghedit:`Edit`
