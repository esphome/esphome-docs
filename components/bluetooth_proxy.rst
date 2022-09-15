Bluetooth Proxy
===============

.. seo::
    :description: Instructions for setting up the Bluetooth Proxy in ESPHome.
    :image: bluetooth.svg

Home Assistant can expand it's Bluetooth reach by communicating through
the Bluetooth proxy component in ESPHome. Place your ESPHome devices close to the
Bluetooth devices that you want to interact with for the best
experience.

If you're looking to create a device that is just a Bluetooth Proxy, see our `Bluetooth Proxy installer <https://esphome.github.io/bluetooth-proxies/>`__ website.

The Bluetooth proxy depends on :doc:`esp32_ble_tracker` so make sure to add that to your configuration.

.. note::

    Bluetooth proxy requires Home Assistant 2022.9 or later.

.. note::

    The Bluetooth proxy of ESPHome currently only provides Home Assistant with passive sensor
    data that is advertised by certain devices. Not all devices are supported and ESPHome does not decode or keep a list.
    To find out if your device is supported, please search for it in the `Home Assistant Integrations <https://www.home-assistant.io/integrations/>`__ list.

    The Individual device integrations in Home Assistant (such as BTHome) will receive the data from the Bluetooth Integration in Home Assistant
    which automatically aggregates all ESPHome bluetooth proxies with any USB Bluetooth Adapters you might have.

Configuration:
--------------

.. code-block::

    bluetooth_proxy:

No configuration variables.

See Also
--------

- :doc:`esp32_ble_tracker`
- :apiref:`bluetooth_proxy/bluetooth_proxy.h`
- :ghedit:`Edit`
