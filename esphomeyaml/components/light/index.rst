Light Component
===============

.. seo::
    :description: Instructions for setting up lights and light effects in esphomelib.
    :image: folder-open.png

The ``light`` domain in esphomeyaml lets you create lights that will
automatically be shown in Home Assistant’s frontend and have many
features such as RGB colors, transitions, flashing and effects.

.. _light-toggle_action:

``light.toggle`` Action
-----------------------

This action toggles a light with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - light.toggle:
            id: light_1
        # Shorthand:
        - light.toggle: light_1

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition
  if the light supports it.

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(light_1).toggle();
        // perform action:
        call.perform();

.. _light-turn_on_action:

``light.turn_on`` Action
------------------------

This action turns a light with the given ID on when executed.

.. code-block:: yaml

    on_...:
      then:
        - light.turn_on:
            id: light_1
            brightness: 100%
            red: 100%
            green: 100%
            blue: 1.0

        # Templated
        - light.turn_on:
            id: light_1
            brightness: !lambda >-
              // output value must be in range 0 - 1.0
              return id(some_sensor).state / 100.0;

        # Shorthand
        - light.turn_on: light_1

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition
  if the light supports it.
- **brightness** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The brightness of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing brightness.
- **red** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The red channel of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing red.
- **green** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The green channel of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing green channel.
- **blue** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The blue channel of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing blue channel.
- **white** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The white channel value of RGBW lights. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing white value.
- **flash_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): If set, will flash the given color
  for this period of time and then go back to the previous state.
- **effect** (*Optional*, string, :ref:`templatable <config-templatable>`): If set, will attempt to
  start an effect with the given name.

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(light_1).turn_on();
        // set parameters (optional)
        call.set_transition_length(1000); // in ms
        call.set_brightness(1.0); // 1.0 is full brightness
        call.set_rgb(1.0, 1.0, 1.0); // color, 1.0 is fully lit
        call.set_effect("The Effect");
        // perform action:
        call.perform();

.. _light-turn_off_action:

``light.turn_off`` Action
-------------------------

This action turns a light with the given ID off when executed.

.. code-block:: yaml

    on_...:
      then:
        - light.turn_off:
            id: light_1

        # Shorthand
        - light.turn_off: light_1

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition
  if the light supports it.

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(light_1).turn_off();
        // set parameters (optional)
        call.set_transition_length(1000); // in ms
        // perform action:
        call.perform();

.. _light-effects:

Light Effects
-------------

esphomelib also offers a bunch of light effects you can use for your lights. The defaults for the
effect parameters are made to work well on their own but of course esphomelib gives you the option to manually change
these parameters.

With esphomelib's light effects system you're basically creating a bunch of entries for the effects dropdown in
Home Assistant. If you wish to have several variants of the same effect you can of course also create multiple
entries with each having a unique name like so:

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - random:
              name: "My Slow Random Effect"
              transition_length: 30s
              update_interval: 30s
          - random:
              name: "My Fast Random Effect"
              transition_length: 4s
              update_interval: 5s

Random Effect
*************

This effect makes a transition (of length ``transition_length``) to a randomly-chosen color every ``update_interval``.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - random:
          - random:
              name: Random Effect With Custom Values
              transition_length: 5s
              update_interval: 7s

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Random``.
- **transition_length** (*Optional*, :ref:`config-time`): The duration of each transition to start. Defaults to ``5s``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval with which a new color is selected and transitioned
  to.

Strobe Effect
*************

This effect cycles through a list of colors with specific durations.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - strobe:
          - strobe:
              name: Strobe Effect With Custom Values
              colors:
                - state: True
                  brightness: 100%
                  red: 100%
                  green: 90%
                  blue: 0%
                  duration: 500ms
                - state: False
                  duration: 250ms
                - state: True
                  brightness: 100%
                  red: 0%
                  green: 100%
                  blue: 0%
                  duration: 500ms

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Strobe``.
- **colors** (*Optional*, list): A list of colors to cycle through. Defaults to a quick cycle between ON and OFF.

  - **state** (*Optional*, boolean): The ON/OFF state to show. Defaults to ``True``.
  - **brightness** (*Optional*, percentage): The brightness of the light. Defaults to ``100%``.
  - **red** (*Optional*, percentage): The percentage that the red color should be on for RGB lights. Defaults to ``100%``.
  - **green** (*Optional*, percentage): The percentage that the green color should be on for RGB lights. Defaults to ``100%``.
  - **blue** (*Optional*, percentage): The percentage that the blue color should be on for RGB lights. Defaults to ``100%``.
  - **white** (*Optional*, percentage): The percentage that the white color should be on for RGBW lights. Defaults to ``100%``.
  - **duration** (**Required**, :ref:`config-time`): The duration this color should be active.

Flicker Effect
**************

This effect "hovers" around the active color of the light and flickers each color channel a bit.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - flicker:
          - flicker:
              name: Flicker Effect With Custom Values
              alpha: 95%
              intensity: 1.5%

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Flicker``.
- **alpha** (*Optional*, percentage): The percentage that the last color value should affect the light. More
  or less the "forget-factor" of an exponential moving average. Defaults to ``95%``.
- **intensity** (*Optional*, percentage): The intensity of the flickering, basically the maximum amplitude of the
  random offsets. Defaults to ``1.5%``.

Lambda Effect
*************

This effect allows you to write completely custom light effects yourself using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - lambda:
              name: My Custom Effect
              update_interval: 1s
              lambda: |-
                static int state = 0;
                if (state == 0) {
                  id(my_light).start_transition(light::LightColorValues::from_rgb(1.0, 1.0, 1.0)));
                } else if (state == 1) {
                  id(my_light).start_transition(light::LightColorValues::from_rgb(1.0, 0.0, 1.0)));
                } else if (state == 2) {
                  id(my_light).start_transition(light::LightColorValues::from_rgb(0.0, 0.0, 1.0)));
                } else {
                  id(my_light).start_transition(light::LightColorValues::from_rgb(0.0, 0.0, 0.0)));
                }
                state += 1;
                if (state == 4)
                  state = 0;

Configuration variables:

- **name** (**Required**, string): The name of the custom effect.
- **update_interval** (*Optional*, :ref:`config-time`): The interval with which the lambda code is executed.
  A value of ``0ms`` means that the lambda is always executed, without a cool-down. Defaults to ``0ms``.
- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The code to execute. ``static`` variables are
  especially useful.

FastLED Rainbow Effect
**********************

A light effect for individually-addressable LEDs that creates a moving rainbow over the whole LED strip using
the HSV color wheel.

.. code-block:: yaml

    light:
      - platform: fastled_...
        # ...
        effects:
          - fastled_rainbow:
          - fastled_rainbow:
              name: Rainbow Effect With Custom Values
              speed: 10
              width: 50

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Rainbow``.
- **speed** (*Optional*, int): The speed of the effect, unitless. Defaults to ``10``.
- **width** (*Optional*, int): The "width" of a full-scale rainbow, unitless. Defaults to ``50``.


FastLED Color Wipe Effect
*************************

A light effect for individually-addressable LEDs that continuously introduces new colors at the beginning of
the strip and shifts them forward every ``add_led_interval``.

.. code-block:: yaml

    light:
      - platform: fastled_...
        # ...
        effects:
          - fastled_color_wipe:
          - fastled_color_wipe:
              name: Color Wipe Effect With Custom Values
              colors:
                - red: 100%
                  green: 100%
                  blue: 100%
                  num_leds: 1
                - red: 0%
                  green: 0%
                  blue: 0%
                  num_leds: 1
              add_led_interval: 100ms
              reverse: False

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Color Wipe``.
- **colors** (*Optional*, list): The colors to shift in at the beginning of the strip. Defaults to shifting in random
  colors.

  - **red** (*Optional*, percentage): The percentage the red color channel should be on. Defaults to ``100%``.
  - **green** (*Optional*, percentage): The percentage the green color channel should be on. Defaults to ``100%``.
  - **blue** (*Optional*, percentage): The percentage the blue color channel should be on. Defaults to ``100%``.
  - **random** (*Optional*, boolean): If set to ``True``, will overwrite the RGB colors by a new, randomly-chosen
    color each time. Defaults to ``False``.
  - **num_leds** (*Optional*, int): The number of leds of this type to have before moving on to the next color.

- **add_led_interval** (*Optional*, :ref:`config-time`): The interval with which to shift in new leds at the
  beginning of the strip. Defaults to ``100ms``.
- **reverse** (*Optional*, boolean): Whether to reverse the direction of the color wipe. Defaults to ``False``.

FastLED Scan Effect
*******************

Create a single, fast-moving dot moving back and forth an individually-addressable LED strip. The color is chosen by the
currently active light color.

.. code-block:: yaml

    light:
      - platform: fastled_...
        # ...
        effects:
          - fastled_scan:
          - fastled_scan:
              name: Scan Effect With Custom Values
              move_interval: 100ms

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Scan``.
- **move_interval** (*Optional*, :ref:`config-time`): The interval with which to move the dot one LED forward.
  Defaults to ``100ms``.

FastLED Twinkle Effect
**********************

A light effect for individually-addressable LED strips that randomly chooses some LEDs and let's them bright
up for a moment, like a stars twinkling in the night's sky. The color of the pixels will be chosen by the
currently active light color.

.. code-block:: yaml

    light:
      - platform: fastled_...
        # ...
        effects:
          - fastled_twinkle:
          - fastled_twinkle:
              name: Twinkle Effect With Custom Values
              twinkle_probability: 5%
              progress_interval: 4ms

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Twinkle``.
- **twinkle_probability** (*Optional*, percentage): The percentage with which, at any time step, a randomly-chosen
  LED should start its twinkle animation.
- **progress_interval** (*Optional*, :ref:`config-time`): The interval with which to progress the effect. This
  affects the duration of a twinkle animation. Defaults to ``4ms``.

FastLED Random Twinkle Effect
*****************************

A light effect similar to ``fastled_twinkle``, but using random colors for each twinkle animation.

.. code-block:: yaml

    light:
      - platform: fastled_...
        # ...
        effects:
          - fastled_random_twinkle:
          - fastled_random_twinkle:
              name: Random Twinkle Effect With Custom Values
              twinkle_probability: 5%
              progress_interval: 32ms

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Random Twinkle``.
- **twinkle_probability** (*Optional*, percentage): The percentage with which, at any time step, a randomly-chosen
  LED should start its twinkle animation.
- **progress_interval** (*Optional*, :ref:`config-time`): The interval with which to progress the effect. This
  affects the duration of a twinkle animation. Defaults to ``4ms``.


FastLED Fireworks Effect
************************

A light effect for individually-addressable LED strips that randomly sparks some fireworks at random positions
and lets the sparkles cascade over the LED strip.

.. code-block:: yaml

    light:
      - platform: fastled_...
        # ...
        effects:
          - fastled_fireworks:
          - fastled_fireworks:
              name: Fireworks Effect With Custom Values
              update_interval: 32ms
              spark_probability: 10%
              use_random_color: false
              fade_out_rate: 120

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Fireworks``.
- **update_interval** (*Optional*, :ref:`config-time`): The interval with which to progress the effect.
  Defaults to ``32ms``.
- **spark_probability** (*Optional*, percentage): The probability to start a new firework spark at a randomly-chosen
  LED at any given time step. Defaults to ``10%``.
- **use_random_color** (*Optional*, boolean): Whether to use random colors for new firework sparks. Defaults to
  using the currently active light color.
- **fade_out_rate** (*Optional*, integer): The rate with which to fade out the LED strip, unitless. Needs to be carefully
  chosen so that the whole strip doesn't light up forever if the fade out rate is too low or that the firework
  sparks do not propagate for a long time. Defaults to ``120``.

FastLED Flicker Effect
**********************

An effect similar to the ``flicker`` effect, but for individually-addressable LED strips. This effect flickers
each LED by its own random amount around the currently active light color.

.. code-block:: yaml

    light:
      - platform: fastled_...
        # ...
        effects:
          - fastled_flicker:
          - fastled_flicker:
              name: Flicker Effect With Custom Values
              update_interval: 16ms
              intensity: 5%

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``FastLED Flicker``.
- **update_interval** (*Optional*, :ref:`config-time`): The time interval for updating the random offsets.
  Defaults to ``16ms``.
- **intensity** (*Optional*, percentage): The intensity of the effect, basically how much the random values can offset
  the currently active light color. Defaults to ``5%``.

See Also
--------

- :doc:`API Reference </api/light/index>`
- `WS2812FX library <https://github.com/kitesurfer1404/WS2812FX>`__ by `@kitesurfer1404 <https://github.com/kitesurfer1404>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/light/index.rst>`__

.. toctree::
    :maxdepth: 1
    :glob:

    *

.. disqus::
