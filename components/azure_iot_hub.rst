Azure IoT Hub
=============

.. seo::
    :description: Instructions for setting up Azure IoT Hub device telemetry in ESPHome
    :image: connection.png
    :keywords: Azure IoT Hub, Azure, REST, IoT


The ``azure_iot_hub`` component allows sending telemetry to Azure IoT Hub. It supports device-to-cloud 
messages via Azure IoT Hub REST API and automatically integrates with existing ESPHome data sources/components.
Once you add ``azure_iot_hub`` to your configuration file, sensor data will be posted to configured IoT Hub
as standard device-to-cloud telemetry messages.

To begin, please provision an Azure IoT Hub (free tier is ok but is limited in the number of telemetry messages
allowed per day, so setup sensor polling rates accordingly) and create a new IoT device to represent this
ESPHome device. Once your device is provisioned in `Azure Portal <https://portal.azure.com>`__, configure the connection.

.. code-block:: yaml

    # Example configuration entry
    azure_iot_hub:
      hub_name: esphome-hub
      device_id: esp32_garden
      device_key: V2VyZSB5b3UgZXhwZWN0aW5nIGEgcmVhbCBzZWNyZXQgaGVyZT8=
      api_version: 2018-06-30
      token_expiration_seconds: 3155760000


Configuration variables:
------------------------

- **hub_name** (string): name of the Azure IoT Hub. Part ofthe hub connection string preceeding .azure-devices.net.
- **device_id** (string): Device ID of the device provisioned in Azure IoT Hub.
- **device_key** (string): Key (can be primary or secondary) assigned to the device in the IoT Hub. If key starts with a zero (0), it needs to be wrapped in quotes.
- **api_version** (*Optional*, string): API version to report to the IoT Hub REST endpoint. Defaults to ``2018-06-30``.
- **token_expiration_seconds** (*Optional*, integer): Limit expiration of the generated SAS token for device. If ``insecure_ssl`` is ``false`` (default), this is reduced to ``hub_name``.azure-devices.net SSL certificate expiration. Defaults to approximately 100 years.


JSON Payload Format
-------------------

``azure_iot_hub`` component will post telemetry data in json format structured as follows:

.. code-block:: javascript

    {
      "deviceId": "device_id",
      "type": "light",
      "sensor_id":
      {
        "name": "Garden Light"
        "state": on,
        "brightness": 255
      }
    }

Each component type supported by :doc:`/components/api` and :doc:`/components/mqtt` will report its type (e.g. ``sensor``, ``switch``, ``light``, etc.). Its values will
be reported as a separate JSON structure keyed by the component id (in the example above *sensor_id*). Inside this structure all the readings will be stored.


See Also
--------

- :doc:`index`
- :apiref:`azure_iot_hub/azure_iot_hub.h`
- :ghedit:`Edit`
