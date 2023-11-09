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


    button:
      - platform: template
        name: "Firmware update"
        on_press:
          then:
            - ota_http.flash:
                url: http://example.com/firmware.bin
            - logger.log: "This message should be not displayed(reboot)"

.. note::

    The file ``firmware.bin`` can be found at ```.esphome/build/xxxx/.pioenvs/xxx/firmware.bin`` if esphome CLI is used, 
    or downloaded as ``Legacy format`` from the esphome HA addon. ota_http currently **Doesn't works** with ``firmware-factory.bin`` or ``Modern format``.

 .. _ota_http-flash_action:

``ota_http.flash`` Action
-------------------------

Flash the device with a remote http firmware using this action in automations.

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
    The url of the firwmare.
-  **verify_ssl** (*Optional*, boolean, :ref:`templatable <config-templatable>`): 
    If the ssl certficiate must be verified or not. Must be explicitely set to ``false`` if using **https**.


See Also
--------

- :doc:`/components/ota`
- :ghedit:`Edit`
