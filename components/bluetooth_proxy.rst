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

.. code-block::

    bluetooth_proxy:

No configuration variables.

See Also
--------

- :doc:`esp32_ble_tracker`
- :apiref:`bluetooth_proxy/bluetooth_proxy.h`
- :ghedit:`Edit`
