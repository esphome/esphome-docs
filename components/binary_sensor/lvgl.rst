.. _lvgl-bse:

LVGL Binary Sensor
==================

.. seo::
    :description: Instructions for setting up a LVGL widget binary sensor.
    :image: ../images/logo_lvgl.png

The ``lvgl`` binary sensor platform creates a binary sensor from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are ``btn`` and ``checkbox``. A single binary sensor supports
a single widget, thus you need to choose among which one's state you want to use.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the binary sensor.
- **obj** (*Optional*): The ID of a button widget configured in LVGL.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.


Example:

.. code-block:: yaml

    binary_sensor:
      - platform: lvgl
        obj: checkbox_id
        name: LVGL checkbox

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/switch/lvgl`
- :ghedit:`Edit`
