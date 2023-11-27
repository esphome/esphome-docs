ESP32 Bluetooth Low Energy Beacon
=================================

.. seo::
    :description: Instructions for setting up Bluetooth Low Energy iBeacons using the BLE feature on ESP32s.
    :image: bluetooth.svg

The ``esp32_ble_beacon`` component creates a Bluetooth Low Energy Beacon with your ESP32 device.
Beacons are BLE devices that repeatedly just send out a pre-defined packet of data. This packet
can then be received by devices like smartphones and can then be used to track a phone's location.

.. warning::

    The BLE software stack on the ESP32 consumes a significant amount of RAM on the device.
    
    **Crashes are likely to occur** if you include too many additional components in your device's
    configuration. Memory-intensive components such as :doc:`/components/voice_assistant` and other
    audio components are most likely to cause issues.

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_beacon:
      type: iBeacon
      uuid: 'c29ce823-e67a-4e71-bff2-abaa32e77a98'

Configuration variables:
------------------------

- **type** (**Required**): The type of beacon to create, currently only supports ``iBeacon``.
- **uuid** (**Required**): The `universally unique identifier <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__
  to identify the beacon.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for code generation.

Advanced options:

- **major** (*Optional*, int): The iBeacon major identifier of this beacon. Usually used to
  group beacons, for example for grouping all beacons in the same building, but has no effect if
  the BLE receiver doesn't use it. Defaults to ``10167``.
- **minor** (*Optional*, int): The iBeacon minor identifier of this beacon. Usually used to
  identify beacons within an iBeacon group. Defaults to ``61958``.
- **min_interval** (*Optional*, :ref:`config-time`): The iBeacon minimum transmit interval in milliseconds from 20 to 10240.
  Setting this less than ``max_interval`` gives the BLE hardware a better chance to avoid
  collisions with other BLE transmissions. Defaults to the iBeacon specification's defined interval: ``100ms``.
- **max_interval** (*Optional*, :ref:`config-time`): The iBeacon maximum transmit interval in milliseconds from 20 to 10240.
  Setting this greater than ``min_interval`` gives the BLE hardware a better chance to avoid
  collisions with other BLE transmissions. Defaults to the iBeacon specification's defined interval: ``100ms``.
- **measured_power** (*Optional*, int): The RSSI of the iBeacon as measured 1 meter from the device.
  This is used to calibrate the ranging calculations in iOS. The procedure for setting this value can
  be found in Apple's `Getting Started with iBeacon PDF <https://developer.apple.com/ibeacon/Getting-Started-with-iBeacon.pdf>`__
  under the heading *Calibrating iBeacon*. Between -128 to 0. Defaults to ``-59``.
- **tx_power** (*Optional*, int): The transmit power of the iBeacon in dBm.
  One of -12, -9, -6, -3, 0, 3, 6, 9. Defaults to ``3dBm``.

Setting Up
----------

First, you'll need to set up the configuration for ESPHome. Just copy the configuration above and
change the UUID to something unique. For example, you can copy this randomly generated UUID:

.. raw:: html

    <input type="text" id="ble-uuid" onclick="this.focus();this.select()" style="width: 240px;" readonly="readonly">
    <script>
      // https://stackoverflow.com/a/105074/8924614
      function guid() {
        function s4() {
          return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
      }
      document.getElementById("ble-uuid").value = guid();
    </script>

Then, just compile and flash the ESP32.

When everything is set up correctly, you should see a show up using your iBeacon scanner of choice. On iPhones,
this should already work from the Bluetooth screen (not tested), on Android, you will need to use an app like
`"Beacon Scanner" <https://play.google.com/store/apps/details?id=com.bridou_n.beaconscanner>`__ by Nicolas Bridoux.

For using these beacons to track the location of your phone, you will need to use another app. For example, I used
`this guide by the owntracks <https://owntracks.org/booklet/features/beacons/>`__ app to let my Home Automation system
know when I'm home or away. Another nice Android app is `Beacon MQTT <https://turbo-lab.github.io/android-beacon-mqtt/>`__.
It can work with multiple beacons simultaneously.

.. figure:: images/esp32_ble_beacon-ibeacon.png
    :align: center
    :width: 75.0%

See Also
--------

- :doc:`esp32_ble_tracker`
- :doc:`binary_sensor/ble_presence`
- :apiref:`esp32_ble_beacon/esp32_ble_beacon.h`
- `ESP32 BLE for Arduino <https://github.com/nkolban/ESP32_BLE_Arduino>`__ by `Neil Kolban <https://github.com/nkolban>`__.
- :ghedit:`Edit`
