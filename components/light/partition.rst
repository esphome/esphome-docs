Light Partition
===============

.. seo::
    :description: Instructions for setting up light partitions.
    :image: color_lens.png

The ``partition`` light platform allows you to combine multiple addressable light segments
(like :doc:`fastled` or :doc:`neopixelbus`) into a single addressable light.
This platform also allows splitting up an addressable lights into multiple segments, so that
segments can be individually controlled.


.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: partition
        name: "Partition Light"
        segments:
          # Use first LED from the light with ID light1
          - id: light1
            from: 0
            to: 0
          # Use 10 leds from light with ID light2 starting 2nd LED
          - id: light2
            from: 1
            to: 10

      # Example for light segment source
      - platform: fastled_clockless
        id: light2
        # Other settings

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **segments** (**Required**, list): The segments this light partition controls

  - **id** (**Required**, :ref:`config-id`): The ID of the light this segment belongs to.
  - **from** (**Required**, int): The first LED to address in the segment. Counting starts with 0,
    so first LED is 0.
  - **to** (**Required**, int): The index of the last LED to address in this segment.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.

- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- If MQTT enabled, all other options from :ref:`MQTT Component <config-mqtt-component>`.

.. note::

    Do *not* use this platform to control each LED on your addressable light - the light
    objects have a moderate overhead and if you try to create many lights you will run out
    of memory quickly.

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/light/fastled`
- :doc:`/components/light/neopixelbus`
- :apiref:`light/addressable_light.h`
- :ghedit:`Edit`

.. disqus::
