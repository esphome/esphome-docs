.. _lvgl-bse:

LVGL Binary Sensor
==================

.. seo::
    :description: Instructions for setting up a LVGL widget binary sensor.
    :image: ../images/logo_lvgl.png

The ``lvgl`` binary sensor platform creates a binary sensor from a LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widget is :ref:`lvgl-wgt-btn`. A single binary sensor supports
a single widget, thus you need to choose among which one's state you want to use.

Configuration options:
----------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the binary sensor.
- **widget** (**Required**): The ID of a ``btn`` widget configured in LVGL.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

.. note::

    ``publish_initial_state`` ??

Example:

.. code-block:: yaml

    binary_sensor:
      - platform: lvgl
        widget: btn_id
        name: LVGL push button

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Button widget <lvgl-wgt-btn>`
- :doc:`/components/number/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/light/lvgl`
- :ghedit:`Edit`
