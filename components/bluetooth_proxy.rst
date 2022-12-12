Bluetooth Proxy
===============

.. seo::
    :description: Instructions for setting up the Bluetooth Proxy in ESPHome.
    :image: bluetooth.svg

Home Assistant can expand its Bluetooth reach by communicating through the Bluetooth proxy component in ESPHome.
The Individual device integrations in Home Assistant (such as BTHome) will receive the data from the Bluetooth
Integration in Home Assistant which automatically aggregates all ESPHome bluetooth proxies with any USB Bluetooth
Adapters you might have. This exceptional feature offers fault tolerant connection between the Bluetooth devices
and Home Assistant.

If you're looking to create an ESPHome node that is just a Bluetooth Proxy, see
our `Bluetooth Proxy installer <https://esphome.github.io/bluetooth-proxies/>`__ website.

.. note::

    The Bluetooth proxy of ESPHome provides Home Assistant with a maximum number of 3 simultaneous active connections.
    Devices which maintain a *continuous active* connection will consume one of these constantly, whilst devices which
    do *periodic disconnections and reconnections* will permit using more than 3 of them (on a statistical basis).
    Passively broadcasted sensor data (that is advertised by certain devices without active connections) is received
    separately from these, and is not limited to a specific number.
    
    Not all devices are supported and ESPHome does not decode or keep a list. To find out if your device is supported,
    please search for it in the `Home Assistant Integrations <https://www.home-assistant.io/integrations/>`__ list.

Configuration:
--------------

.. code-block::

    bluetooth_proxy:

- **active** (*Optional*, boolean): Enables proxying active connections. Defaults to ``false``. Requires Home Assistant 2022.10 or later.

- **cache_services** (*Optional*, boolean): Enables caching services in NVS flash storage which significantly speeds up active connections. Defaults to ``true`` when using the ESP-IDF framework.

The Bluetooth proxy depends on :doc:`esp32_ble_tracker` so make sure to add that to your configuration.

.. note::

    Bluetooth proxy requires Home Assistant 2022.9 or later.

Improving reception performance
-------------------------------

Use a board with an Ethernet connection to the network, to offload ESP32's radio module from WiFi traffic, this gains performance on Bluetooth side.
To maximize the chances of catching advertisements of the sensors, you can set ``interval`` equal to ``window`` in :doc:`/components/esp32_ble_tracker` scan parameter settings:

.. code-block:: yaml

    esp32_ble_tracker:
      scan_parameters:
        interval: 1100ms
        window: 1100ms

Avoid placing the ESP node in racks, close to routers/switches or other network equipment as EMI interference will degrade Bluetooth signal reception. For best results put as far away as possible, at least 3 meters distance from any other such equipment. Place your ESPHome devices close to the Bluetooth devices that you want to interact with for the best experience.

See Also
--------

- :doc:`esp32_ble_tracker`
- :apiref:`bluetooth_proxy/bluetooth_proxy.h`
- BTHome `<https://bthome.io/>`__
- :ghedit:`Edit`
