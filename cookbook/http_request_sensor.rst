Share data directly between ESPHome nodes
=========================================

In certain special cases it might be desired to avoid placing any middleware like an MQTT or a home automation server just to transfer small bits of data from one node to another. Direct data polling is possibvle using HTTP, but beware that the involved components are resource hungry and may be less stable on long term. The webserver embedded in the node is not designed to constantly serve a large amount of requests.

The primary node holding the data we need to retrieve from will be the server, and the others polling for it will be the clients (can be multiple). 

Server part
-----------

Setting up a webserver using the  :doc:`/components/web_server` on the primary node will make available the required sensor data through a :ref:`api-rest` interface.

.. code-block:: yaml

    web_server:
      port: 80
  
Client part
-----------

On the client nodes we need an :doc:`/components/http_request` with an ``id`` set, and a :doc:`/components/sensor/template` to make it accessible locally.

.. code-block:: yaml

    http_request:
      useragent: esphome/device
      id: http_request_id

    sensor:
      - platform: template
        name: "Template sensor on client"
        id: template_sensor_id


Pulling the data
****************

To automate the request for data, we use an :ref:`interval` requesting the URL pointing to the sensor id for which the state is needed. See :ref:`api-rest` on how to build up the URL for your sensors.

In the example below we request the value of a sensor from the server node, and after parsing the resulted JSON string we publish it to the local template sensor:

.. code-block:: yaml

    interval:
      - interval: 60s
        then:
          - http_request.get: 
              url: http://address.of.server.node/sensor/ID.of.the.sensor
              on_response:
                then:
                  - lambda: |-
                      json::parse_json(id(http_request_id).get_string(), [](JsonObject root) {
                          id(template_sensor_id).publish_state(root["value"]);
                      });

                 
Result
------

.. figure:: images/server.png
    :align: center
    :width: 95.0%

    Server side real sensor


.. figure:: images/clients.png
    :align: center
    :width: 95.0%

    Client side template sensor


See Also
--------

- :doc:`/components/web_server`
- :doc:`/components/http_request`
- :doc:`/components/sensor/template`
- :ref:`interval`
- :ref:`api-rest`
- :ghedit:`Edit`
