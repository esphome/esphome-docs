LVGL Binary Sensor
==================

.. seo::
    :description: Instructions for setting up a LVGL widget binary sensor.
    :image: ../images/logo_lvgl.png

The ``lvgl`` binary sensor platform creates a binary sensor from LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **checkbox** (*Optional*): The ID of a checkbox widget configured in LVGL.
- **btn** (*Optional*): The ID of a button widget configured in LVGL.

  .. note::

      Choose only one of ``checkbox`` or ``btn`` for a single binary sensor.


Example

.. code-block:: yaml

    binary_sensor:
      - platform: lvgl
        name: LVGL checkbox
        checkbox: lv_checkbox

See Also
--------
- :ref:`LVGL <lvgl-main>`
- :ghedit:`Edit`
