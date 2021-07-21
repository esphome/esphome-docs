Light Partition
===============

.. seo::
    :description: Instructions for setting up light partitions.
    :image: color_lens.png

The ``partition`` light platform allows you to combine multiple addressable light segments
(like :doc:`fastled` or :doc:`neopixelbus`) into a single addressable light.
This platform also allows splitting up an addressable lights into multiple segments, so that
segments can be individually controlled.

Splitting a single LED strip
----------------------------

If you want to split a strip, you may run into strange behavior like that the original light entity (e.g., ``fastled_clockless``)
may be conflicting with the partition. For better control over which segments of the strip will overlap each other,
mark the original ``light`` as ``internal: true``.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: partition
        name: "Partition Light 1"
        segments:
          # Use first 10 LEDs from the light with ID light1
          - id: light1
            from: 0
            to: 9

      - platform: partition
        name: "Partition Light 2"
        segments:
          # Use LEDs 11-20 from the light with ID light1
          - id: light1
            from: 10
            to: 19

      # Example for light segment source
      - platform: fastled_clockless
        id: light1
        # You may want (but don't need) this
        internal: true
        # Other settings

Joining multiple LED strips into one
------------------------------------

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: partition
        name: "Partition Light"
        segments:
          # Use first 10 LEDs from the light with ID light1
          - id: light1
            from: 0
            to: 9
          # Use first 10 LEDs from light with ID light2
          # they become LEDs 11-20 in the joined partition
          - id: light2
            from: 0
            to: 9

      # Example for light segment source
      - platform: fastled_clockless
        id: light1
        # You may want (but don't need) this
        internal: true
        # Other settings

      # Example for light segment source
      - platform: fastled_clockless
        id: light2
        # You may want (but don't need) this
        internal: true
        # Other settings

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **segments** (**Required**, list): The segments this light partition controls

  - **id** (**Required**, :ref:`config-id`): The ID of the light this segment belongs to.
  - **from** (**Required**, int): The first LED to address in the segment. Counting starts with 0,
    so first LED is 0.
  - **to** (**Required**, int): The index of the last LED to address in this segment.
  - **reversed** (**Required**, int): Whether to reverse the LEDs in this segment.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.

- All other options from :ref:`Light <config-light>`.

.. note::

    Do *not* use this platform to control each LED on your addressable light - the light
    objects have a moderate overhead and if you try to create many lights you will run out
    of memory quickly.

    See :ref:`light-addressable_set_action` for that.

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/light/fastled`
- :doc:`/components/light/neopixelbus`
- :apiref:`partition/light_partition.h`
- :ghedit:`Edit`
