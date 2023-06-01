Share data directly between ESPHome nodes
=========================================

In certain special cases you might want to avoid placing any middleware like an MQTT or a home automation server just to transfer small bits of data from one node to another. Direct data polling is possibvle using HTTP, but beware that the involved components are resource hungry and may be less stable on long term than the usual methods. The webserver embedded in the node is not designed to constantly serve a large amount of requests.

The node holding the data we need to retrieve will be the server, and the others polling for it will be the clients (can be multiple). 

Server part
-----------

You must set up a webserver on your primary node to make available the required sensor data using the  :doc:`/components/web_server`.

.. code-block:: yaml

    web_server:
      port: 80
  
Client part
-----------

On the client nodes we need a :doc:`/components/http_request` with an ``id`` set, and a :doc:`/components/sensor/template` to make it accessible locally.

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

To automate the request for data, we use an :ref:`interval` component requesting the URL pointing to the sensor id for which the state is needed. See :ref:`api-rest` on how to build up the URL for your sensors.

.. note::

    The domain is the type of the component, for example ``sensor`` or ``light``. ``id`` refers to the internal ID of the component - which is created from the name of the component, stripping out all non-alphanumeric characters, making everything lowercase and replacing all spaces by underscores. To confirm the corrrct ID to use, you can set the log level to VERY_VERBOSE on your server node and look for ``object_id:`` in the logs.

In the example below we pull the value of a sensor, and after parsing the resulted JSON string we publish it to the template sensor:

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

    Server side real sensor.


.. figure:: images/clients.png
    :align: center
    :width: 95.0%

    Client side template sensor.


See Also
--------

- :doc:`/components/web_server`
- :doc:`/components/http_request`
- :doc:`/components/sensor/template`
- :ref:`interval`
- :ref:`api-rest`
- :ghedit:`Edit`
