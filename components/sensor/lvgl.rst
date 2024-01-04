LVGL Sensor
===========

.. seo::
    :description: Instructions for setting up a LVGL widget sensor.
    :image: ../images/logo_lvgl.png

The ``lvgl`` sensor platform creates a sensor from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are ``arc`` and ``slider``. A single sensor supports
a single widget, thus you need to choose among which one's state you want to use.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **arc_id** (*Optional*): The ID of an arc widget configured in LVGL.
- **slider_id** (*Optional*): The ID of a slider widget configured in LVGL.
- All other options from :ref:`Sensor <config-sensor>`.


Example:

.. code-block:: yaml

    sensor:
      - platform: lvgl
        arc_id: arc_value
        id: lvgl_arc_sensor
        name: LVGL Arc



See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/number/lvgl`
- :ghedit:`Edit`
