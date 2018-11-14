Template Cover
==============

.. seo::
    :description: Instructions for setting up template covers in esphomelib.
    :image: description.svg

The ``template`` cover platform allows you to create simple covers out of just a few
actions and a value lambda. Once defined, it will automatically appear in Home Assistant
as a cover and can be controlled through the frontend.

.. figure:: images/cover-ui.png
    :align: center
    :width: 75.0%

.. code:: yaml

    # Example configuration entry
    cover:
      - platform: template
        name: "Template Cover"
        lambda: >-
          if (id(top_end_stop).state) {
            return cover::COVER_OPEN;
          } else {
            return cover::COVER_CLOSED;
          }
        open_action:
          - switch.turn_on: open_cover_switch
        close_action:
          - switch.turn_on: close_cover_switch
        stop_action:
          - switch.turn_on: stop_cover_switch
        optimistic: true


Possible return values for the optional lambda:

 - ``return cover::COVER_OPEN;`` if the cover should be reported as OPEN.
 - ``return cover::COVER_CLOSED;`` if the cover should be reported as CLOSED.
 - ``return {};`` if the last state should be repeated.

Configuration variables:
------------------------

-  **name** (**Required**, string): The name of the cover.
-  **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
   Lambda to be evaluated repeatedly to get the current state of the cover.
   Only state *changes* will be published to MQTT.
-  **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
   any command sent to the template cover will immediately update the reported state and no lambda
   needs to be used. Defaults to ``false``.
-  **open_action** (*Optional*, :ref:`Action <config-action>`): The action that should
   be performed when the remote (like Home Assistant's frontend) requests the cover to be opened.
-  **close_action** (*Optional*, :ref:`Action <config-action>`): The action that should
   be performed when the remote requests the cover to be closed.
-  **stop_action** (*Optional*, :ref:`Action <config-action>`): The action that should
   be performed when the remote requests the cover to stopped.
-  **id** (*Optional*,
   :ref:`config-id`): Manually specify
   the ID used for code generation.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`
   and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`/esphomeyaml/components/cover/index`
- :ref:`automation`
- :doc:`/esphomeyaml/cookbook/garage-door`
- :doc:`API Reference </api/cover/template>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/cover/template.rst>`__

.. disqus::
