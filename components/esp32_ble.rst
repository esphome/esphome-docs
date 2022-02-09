BLE Component
=============

.. seo::
    :description: Instructions for setting up Bluetooth LE in ESPHome.
    :image: bluetooth.svg

The ``esp32_ble`` component in ESPHome sets up the Bluetooth LE stack on the device so that a :doc:`esp32_ble_server`
can run.

.. code-block:: yaml

    # Example configuration

    esp32_ble:


No configuration variables.

Advertisement
-------------

``esp32_ble`` handles Bluetooth LE Advertisement configuration, that is used to let nearby devices know about the
instance. Besides basic things like the device name and MAC address, this message can hold up to 31 byte of arbitrary
payload. This portion of advertisement message is called manufacturer data, and used in ultra-low energy setups for
distributing low quantities of information without need to establish a connection.

By default this section is empty but can be set via ``esp32_ble`` API:

.. code-block:: cpp

    void BLEAdvertising::set_manufacturer_data(uint8_t *data, uint16_t size);

It takes the pointer to a byte array that must be at most 31 byte long, and the size of it, that must be at most 31.

Once the data is set, it's now possible to start advertisement via another API function:

.. code-block:: cpp

    void BLEAdvertising::start();

The above function needs to be called after every change to the manufacturer data - even if the pointer doesn't change.

When serializing data into bytes it's important to ensure it's packed and unpacked in the same way (e.g., same
endianness). Assuming that all devices involved in the setup share the same architecture, it's possible to use
primitive struct packing for serialization.

Both the server and clients would need to share the message definition, so we need to define it a common header file
like ``structs.h`` within esphome directory, next to the configuration YAML files.

.. code-block:: cpp

    typedef struct payload {

      time_t   timestamp;
      uint16_t kitchen_co2;

    } __attribute__((packed)) payload_t;


    typedef struct manufacturer_data {

      uint16_t   company_id;
      payload_t  data;

    } manufacturer_data_t;

The ``ble-server.yaml`` would setup advertising as shown in example below (non-essential parts omitted for brevity):

.. code-block:: yaml

    esphome:
      name: ble-server
      includes:
      - structs.h

    esp32_ble:
        id: ble

    interval:
      - interval: 10seconds
        then:
          - lambda: |-
              ESP_LOGD("advertisement", "Refreshing advertisement");

              // We allocate single instance in memory and refresh it in place
              static manufacturer_data_t* advertisement = new manufacturer_data_t;

              // Assuming there is a time component configured with identifier ntp
              advertisement->data.timestamp = id(ntp).now().timestamp;

              // Assuming there is a sensor component configured with identifier kitchen_co2
              advertisement->data.kitchen_co2 = (uint16_t) id(kitchen_co2).state;

              if (advertisement->company_id == 0) { // Execute once after boot for initial setup
                  ESP_LOGD("advertisement", "Initializing advertisement");

                  advertisement->company_id = 0xFFFF; // 0xFFFF reserved for local testing and non-commercial use
                  id(ble).get_advertising()->set_manufacturer_data((uint8_t*) advertisement, sizeof(manufacturer_data_t));

                  ESP_LOGD("main", "Advertisement initialized");
              }

              // Force esp_ble to use new data
              id(ble).get_advertising()->start();

              ESP_LOGD("advertisement", "Advertisement refreshed");

Finally, ``ble-client.yaml`` could consume the data using :doc:`esp32_ble_tracker` and decode it usign shared structs:

.. code-block:: yaml

    esphome:
      name: ble-client
      includes:
      - structs.h

    esp32_ble_tracker:

      scan_parameters:
        active: false

      on_ble_manufacturer_data_advertise:
        - mac_address: !secret ble_server_mac_address
          manufacturer_id: FFFF // same value as used in the server
          then:
            - lambda: |-
                payload_t* message = (payload_t*) x.data();
                
                ESP_LOGD(
                  "advertisement", "Received: time=%ld, kitchen_co2=%hu.",
                  message->timestamp, message->kitchen_co2
                );


See Also
--------

- :doc:`esp32_ble_server`
- :doc:`esp32_improv`
- :apiref:`esp32_ble/ble.h`
- :ghedit:`Edit`
