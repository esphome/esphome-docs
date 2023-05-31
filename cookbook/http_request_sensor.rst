Share data directly between ESPHome nodes
=========================================
You need two ESPHome nodes. One will be the server, and the others will be the clients (can be multiple). You must set up a webserver on your primary esphome to make available the required sensor data using the  :doc:`/components/web_server`.

Server part
-----------

.. code-block:: yaml

    # Webserver configration
    web_server:
      port: 80
  
Client part
-----------

On the client nodes we need a :doc:`/components/http_request` with an ``http_request_data`` id set, and a :doc:`/components/sensor/template` to make it accessible locally.

.. code-block:: yaml

    http_request:
      useragent: esphome/device
      timeout: 10s
      id: http_request_data

    sensor:
      - platform: template
        name: "Name of the template sensor"
        id: id_of_the_template_sensor


Pulling the data
****************

To automate the request for data, we will add an interval component requesting the URL pointing to the sensor id for which the state is needed. See :ref:`api-rest` on how to build up the URL for your sensors.

.. note::

    The domain is the type of the component, for example ``sensor`` or ``light``. ``id`` refers to the ID of the component - which is created from the name of the component, stripping out all non-alphanumeric characters, making everything lowercase and replacing all spaces by underscores. To confirm the corrrct ID to use, you can set the log level to VERY_VERBOSE on your server node and look for ``object_id:`` in the logs.

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
                  json::parse_json(id(http_request_data).get_string(), [](JsonObject root) {
                      id(id_of_the_template_sensor).publish_state(root["value"]);
                  });

                 
Result
------

.. figure:: images/server.png
    :align: center
    :width: 90.0%

Server side real sensor.


.. figure:: images/clients.png
    :align: center
    :width: 90.0%

Client side template sensor.


See Also
--------

- :doc:`/components/web_server`
- :doc:`/components/http_request`
- :ref:`api-rest`
- :doc:`/components/sensor/template`
- :ghedit:`Edit`
