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
  or downloaded as ``Legacy format`` from the esphome HA addon. **Do not use** ``firmware-factory.bin`` or ``Modern format``.

See Also
--------

- :doc:`/components/ota`
- :ghedit:`Edit`
