OTA HTTP Update Component
=========================

.. seo::
    :description: Instructions for setting up Over-The-Air (OTA) updates for ESPs to download firmwares remotely by HTTP.
    :image: system-update.svg

With the OTA HTTP (Over The Air HTTP) update component your device can download a firmware by HTTP and flash it.
As the device is in client mode, it can be on a foreign network, or behind a firewall. It is primary useful with mqtt only devices.

.. code-block:: yaml

    # Example configuration entry
    ota_http:
        esp8266_disable_ssl_support: no # `no` by default. 
        safe_mode: false # `false` by default

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

-  **safe_mode** (*Optional*, boolean): Will retry to flash at boot time if the ota fail.
   Defaults to ``false``.

ESP8266 Options:

- **esp8266_disable_ssl_support** (*Optional*, boolean): Whether to include SSL support on ESP8266s.
  Defaults to ``no``. See :ref:`esphome-esp8266_disable_ssl_support` for more info


.. note::

    The file ``firmware.bin`` can be found at ```.esphome/build/xxxx/.pioenvs/xxx/firmware.bin`` if esphome CLI is used, 
    or downloaded as ``Legacy format`` from the esphome HA addon. ota_http currently **Doesn't works** with ``firmware-factory.bin`` or ``Modern format``.

 .. _ota_http-flash_action:

``ota_http.flash`` Action
-------------------------

Flash the device with a remote http firmware using this :ref:`action <config-action>` in automations.

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

Configuration options:

-  **url** (**Required**, string, :ref:`templatable <config-templatable>`):
    The url of the firwmare. Basic auth is allowed with **https://user:password@example.com/firmware.bin**.
-  **verify_ssl** (*Optional*, boolean, :ref:`templatable <config-templatable>`): 
    If the ssl certficiate must be verified or not. Must be explicitly set to ``false`` if using **https**. 
    See :ref:`http_request-get_action` for more infos.


See Also
--------

- :doc:`/components/ota`
- :doc:`/components/http_request`
- :ghedit:`Edit`
