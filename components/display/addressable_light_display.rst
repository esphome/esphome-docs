Addressable Light Display
=========================

.. seo::
    :description: Instructions for setting up addressable light displays and LED matrix
    :image: addressable_light_display.jpg

The ``addressable_light_display`` display platform allows to display text and graphics on an addressable
light that has been arranged in a display matrix.

The display requires that an :apiclass:`AddressableLight <light::AddressableLight>` component, such as
:doc:`/components/light/fastled` or :doc:`/components/light/neopixelbus`, be defined.

.. figure:: images/addressable_light_display.jpg
    :align: center
    :width: 75.0%

    WS2812B Addressable Light Display

.. code-block:: yaml

    light:
      - platform: fastled_clockless
        chipset: WS2812B
        pin: GPIO4
        num_leds: 64
        rgb_order: GRB
        name: "led_matrix"
        id: led_matrix_light
        default_transition_length: 0s
        color_correct: [50%, 50%, 50%]
        restore_mode: ALWAYS_ON

    display:
      - platform: addressable_light_display
        id: led_matrix_display
        addressable_light_id: led_matrix_light
        width: 8
        height: 8
        rotation: 180°
        update_interval: 16ms
        lambda: |-
              // Draw a bulls-eye pattern
              Color red = Color(0xFF0000);
              Color green = Color(0x00FF00);
              Color blue = Color(0x0000FF);
              it.rectangle(0, 0, 8, 8, red);
              it.rectangle(1, 1, 6, 6, green);
              it.rectangle(2, 2, 4, 4, blue);
              it.rectangle(3, 3, 2, 2, red);

Configuration variables:
------------------------

- **addressable_light_id** (**Required**, :ref:`config-id`): The id of the addressable light component to use
  as a display.
- **width** (**Required**, int): The width of the LED matrix in pixels.
- **height** (**Required**, int): The height of the LED matrix in pixels.
- **rotation** (*Optional*): Set the rotation of the display. Everything you draw in ``lambda:`` will be rotated
  by this option. One of ``0°`` (default), ``90°``, ``180°``, ``270°``.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the display.
  See :ref:`display-engine` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to call the lambda to update the display.
  Defaults to ``16ms``.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the display.
  ``it`` will be an instance of :apiclass:`AddressableLightDisplay <addressable_light_display::AddressableLightDisplay>`.
  See :ref:`display-engine` for more information. 
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.


.. note::

    When enabled (the default, but also via ``it.set_enabled(true)``), any effect currently running on the
    addressable light will be disabled. When disabled (``it.set_enabled(false)``), the last configured effect will
    be restored.
    
    While the display is enabled, it is still possible to control the parent addressable light component in some
    limited capacity. Changing the brightness will still work, but changing the color will have no affect. It is not
    adivsable to enable any effects (ex: rainbow, color wipe, etc) while the display is enabled, as this will cause a
    great deal of flickering while the effect competes with the display for rendering.

See Also
--------

- :apiref:`addressable_light_display/addressable_light_display.h`
- :doc:`/components/light/index`
- :doc:`/components/light/fastled`
- :doc:`/components/light/neopixelbus`
- :doc:`/components/light/partition`
- :ghedit:`Edit`
