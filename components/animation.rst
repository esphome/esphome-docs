.. _display-animation:

Animation
=========

Allows to use animated images on displays. Animation inherits all options from the image component.
It adds additional lambda methods: ``next_frame()``, ``prev_frame()`` and ``set_frame()`` to change the shown picture of a gif.

.. code-block:: yaml

    animation:
      - file: "animation.gif"
        id: my_animation
        resize: 100x100

The animation can be rendered just like the image component with the ``image()`` function of the display component.

To show the next frame of the animation call ``id(my_animation).next_frame()``, to show the previous picture use ``id(my_animation).prev_frame()``. To show a specific picture use ``id(my_animation).set_frame(int frame)``.
This can be combined with all Lambdas:

.. code-block:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          //Ingress shown animation Frame.
          id(my_animation).next_frame();
          // Draw the animation my_animation at position [x=0,y=0]
          it.image(0, 0, id(my_animation), COLOR_ON, COLOR_OFF);

Additionally, you can use the ``animation.next_frame``, ``animation.prev_frame`` or ``animation.set_frame`` actions.

.. note::

    To draw the next animation independent of Display draw cycle use an interval:

    .. code-block:: yaml

        interval:
          - interval: 5s
              then:
                animation.next_frame: my_animation

Configuration variables:
------------------------

- **file** (**Required**, string): The path (relative to where the .yaml file is) of the gif file.
- **id** (**Required**, :ref:`config-id`): The ID with which you will be able to reference the animation later
  in your display code.
- **resize** (*Optional*, string): If set, this will resize all the frames to fit inside the given dimensions ``WIDTHxHEIGHT``
  and preserve the aspect ratio.
- **type** (*Optional*): Specifies how to encode each frame internally. Defaults to ``BINARY``.

  - ``BINARY``: Two colors, suitable for 1 color displays or 2 color image in color displays. Uses 1 bit
    per pixel, 8 pixels per byte.
  - ``TRANSPARENT_BINARY``: One color, any pixel that is fully transparent will not be drawn, and any other pixel
    will be the on color. Uses 1 bit per pixel, 8 pixels per byte.
  - ``GRAYSCALE``: Full scale grey. Uses 8 bits per pixel, 1 pixel per byte.
  - ``RGB565``: Lossy RGB color stored. Uses 2 bytes per pixel.
  - ``RGB24``: Full RGB color stored. Uses 3 bytes per pixel.
  - ``RGBA``: Full RGB color stored. Uses 4 bytes per pixel. Any pixel with an alpha value < 127 will not be drawn.

- **use_transparency** (*Optional*): If set the alpha channel of the input image will be taken into account, and pixels with alpha < 127 will not be drawn. For image types without explicit alpha channel, the color (0, 0, 1) (very dark blue) will be mapped to black, to be able to store transparency information within the image. Explicitly transparent types (``TRANSPARENT_BINARY`` and ``RGBA``) default to ``True`` and cannot be set to ``False``; other types default to ``False``.
- **loop** (*Optional*): If you want to loop over a subset of your animation (e.g. a fire animation where the fire "starts", then "burns" and "dies") you can specify some frames to loop over.

  - **start_frame** (*Optional*, int): The frame to loop back to when ``end_frame`` is reached. Defaults to the first frame in the animation.
  - **end_frame** (*Optional*, int): The last frame to show in the loop; when this frame is reached it will loop back to ``start_frame``. Defaults to the last frame in the animation.
  - **repeat** (*Optional*, int): Specifies how many times the loop will run. When the count is reached, the animation will continue with the next frame after ``end_frame``, or restart from the beginning if ``end_frame`` was the last frame. Defaults to "loop forever".

Actions:
--------

- **animation.next_frame**: Moves the animation to the next frame. This is equivalent to the ``id(my_animation).next_frame();`` lambda call.

  - **id** (**Required**, :ref:`config-id`): The ID of the animation to animate.

- **animation.prev_frame**: Moves the animation to the previous frame. This is equivalent to the ``id(my_animation).prev_frame();`` lambda call.

  - **id** (**Required**, :ref:`config-id`): The ID of the animation to animate.

- **animation.set_frame**: Moves the animation to a specific frame. This is equivalent to the ``id(my_animation).set_frame(frame);`` lambda call.

  - **id** (**Required**, :ref:`config-id`): The ID of the animation to animate.
  - **frame** (**Required**, int): The frame index to show next.

