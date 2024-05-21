Light Component
===============

.. seo::
    :description: Instructions for setting up lights and light effects in ESPHome.
    :image: folder-open.svg

The ``light`` domain in ESPHome lets you create lights that will
automatically be shown in Home Assistant’s frontend and have many
features such as RGB colors, transitions, flashing and effects.

This component restores its state on reboot/reset.

.. _config-light:

Base Light Configuration
------------------------

All light configuration schemas inherit these options.

.. code-block:: yaml

    light:
      - platform: ...


Configuration variables:

- **name** (**Required**, string): The name of the light.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the light to use that name, you can set ``name: None``.

- **icon** (*Optional*, icon): Manually set the icon to use for the light in the frontend.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **gamma_correct** (*Optional*, float): Apply a `gamma correction
  factor <https://en.wikipedia.org/wiki/Gamma_correction>`__ to the light channels.
  Defaults to ``2.8``.
- **default_transition_length** (*Optional*, :ref:`config-time`): The default transition length
  to use when no transition length is set in the light call. Defaults to ``1s``.
- **flash_transition_length** (*Optional*, :ref:`config-time`): The transition length to use when flash
  is called. Defaults to ``0s``.
- **restore_mode** (*Optional*): Control how the light attempts to restore state on bootup.
  For restoring on ESP8266s, also see ``esp8266_restore_from_flash`` in the
  :doc:`esphome section </components/esphome>`.

    - ``RESTORE_DEFAULT_OFF`` - Attempt to restore state and default to OFF if not possible to restore.
    - ``RESTORE_DEFAULT_ON`` - Attempt to restore state and default to ON.
    - ``RESTORE_INVERTED_DEFAULT_OFF`` - Attempt to restore state inverted from the previous state and default to OFF.
    - ``RESTORE_INVERTED_DEFAULT_ON`` - Attempt to restore state inverted from the previous state and default to ON.
    - ``RESTORE_AND_OFF`` - Attempt to restore state but initialize the light as OFF.
    - ``RESTORE_AND_ON`` - Attempt to restore state but initialize the light as ON.
    - ``ALWAYS_OFF`` (Default) - Always initialize the light as OFF on bootup.
    - ``ALWAYS_ON`` - Always initialize the light as ON on bootup.

- **on_turn_on** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the light is turned on. See :ref:`light-on_turn_on_off_trigger`.
- **on_turn_off** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the light is turned off. See :ref:`light-on_turn_on_off_trigger`.
- **on_state** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the light's set state is changed. See :ref:`light-on_state_trigger`.

Additional configuration variables for addressable lights:

- **color_correct** (*Optional*, list of float): Apply a color correction to each color channel.
  This defines the maximum brightness of each channel. For example ``[100%, 50%, 100%]`` would set the
  green channel to be at most at 50% brightness.
- **power_supply** (*Optional*, :ref:`config-id`): The :doc:`/components/power_supply` to connect to
  this light. When the light is turned on, the power supply will automatically be switched on too.

Advanced options:

- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options.
  Set to ``""`` to remove the default entity category.
- If MQTT enabled, all other options from :ref:`MQTT Component <config-mqtt-component>`.

.. _light-toggle_action:

``light.toggle`` Action
***********************

This action toggles a light with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - light.toggle:
            id: light_1
        # Shorthand:
        - light.toggle: light_1

Configuration variables:

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
************************

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
            brightness: !lambda |-
              // output value must be in range 0 - 1.0
              return id(some_sensor).state / 100.0;

        # Shorthand
        - light.turn_on: light_1

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition
  if the light supports it.
- **color_mode** (*Optional*, :ref:`templatable <config-templatable>`): For lights that support more than one color mode, the color
  mode that will be activated. The color mode determines which outputs of the light are active, and which parameters can be used.
  This can for example be used to switch between colored and white light. Must be a color mode that is supported by the light.
  Valid color modes are:

    - ``ON_OFF``: Only on/off control.
    - ``BRIGHTNESS``: Only brightness control. Accepts *brightness* parameter.
    - ``WHITE``: Single white channel only. Accepts *brightness* and *white* parameters.
    - ``COLOR_TEMPERATURE``: Color-temperature controlled white channel. Accepts *brightness* and *color_temperature*
      parameters.
    - ``COLD_WARM_WHITE``: Cold and warm white channels. Accepts *brightness*, *color_temperature*, *cold_white* and
      *warm_white* parameters.
    - ``RGB``: RGB color channels. Accepts *brightness*, *color_brightness*, *red*, *green* and *blue* parameters.
    - ``RGB_WHITE``: RGB color channels and a separate white channel. Accepts parameters from ``RGB`` and ``WHITE``
      color modes.
    - ``RGB_COLOR_TEMPERATURE``: RGB color channels and a separate color-temperature controlled white channel. Accepts
      parameters from ``RGB`` and ``COLOR_TEMPERATURE`` color modes.
    - ``RGB_COLD_WARM_WHITE``: RGB color channels and two separate cold and warm white channels. Accepts parameters
      from ``RGB`` and ``COLD_WARM_WHITE`` color modes.

- **brightness** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The master brightness of the light, that
  applies to all channels (both color and white) of the light.
- **color_brightness** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The brightness of the color lights. Useful
  to control brightness of colored and white lights separately for RGBW lights.
- **red** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The red channel of the light.
- **green** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The green channel of the light.
- **blue** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The blue channel of the light.
- **white** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The brightness of the white channel.
- **color_temperature** (*Optional*, float, :ref:`templatable <config-templatable>`): The color temperature
  (in `mireds <https://en.wikipedia.org/wiki/Mired>`__ or Kelvin) of the white channel.
- **cold_white** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The brightness of the cold white channel.
  Cannot be used at the same time as *color_temperature*.
- **warm_white** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The brightness of the warm white channel.
  Cannot be used at the same time as *color_temperature*.
- **flash_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): If set, will flash the given color
  for this period of time and then go back to the previous state.
- **effect** (*Optional*, string, :ref:`templatable <config-templatable>`): If set, will attempt to
  start an effect with the given name.

All percentage options accept values in the range ``0%`` to ``100%`` or ``0.0`` to ``1.0``, and default to not changing
the current value (which might be the value from before the light was last turned off). To reset values, explicitly set
them to zero.

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        auto call = id(light_1).turn_on();
        // set parameters (optional)
        call.set_transition_length(1000); // in ms
        call.set_brightness(1.0); // 1.0 is full brightness
        call.set_color_mode(ColorMode::RGB_COLD_WARM_WHITE);
        call.set_rgb(0.5, 0.25, 1.0); // color in RGB order, this example is purple
        call.set_cold_white(0.5);
        call.set_warm_white(0.75);
        call.set_effect("The Effect");
        // perform action:
        call.perform();

    Shorter example using auto call , call.set_brightness and call.perform.

    .. code-block:: cpp

        id(light_1).turn_on().set_brightness(1.0).perform();


.. note::

    The ``red``, ``green`` and ``blue`` values only control the color of the light, not its
    brightness! If you assign ``50%`` to all RGB channels it will be interpreted as 100% on.
    Only use ``brightness`` or ``color_brightness`` to control the brightness of the light.

.. note::

    The master brightness (``brightness``) and separate brightness controls for the color and
    white channels (``color_brightness``, ``white``, ``cold_white`` and ``warm_white``) are
    multiplied together. Thus, this will result in color at 40% brightness and white at 60%
    brightness:

    .. code-block:: yaml

        - light.turn_on:
            id: light_1
            brightness: 80%
            color_brightness: 50%
            white: 75%

.. _light-turn_off_action:

``light.turn_off`` Action
*************************

This action turns a light with the given ID off when executed.

.. code-block:: yaml

    on_...:
      then:
        - light.turn_off:
            id: light_1

        # Shorthand
        - light.turn_off: light_1

Configuration variables:

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

.. _light-control_action:

``light.control`` Action
************************

This :ref:`Action <config-action>` is a generic call to change the state of a light - it
is essentially just a combination of the turn_on and turn_off calls.

.. code-block:: yaml

    on_...:
      then:
        - light.control:
            id: light_1
            state: on

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **state** (*Optional*, :ref:`templatable <config-templatable>`, boolean): Change the ON/OFF
  state of the light.
- All other options from :ref:`light.turn_on <light-turn_on_action>`.

.. _light-dim_relative_action:

``light.dim_relative`` Action
*****************************

This :ref:`Action <config-action>` allows you to dim a light that supports brightness
by a relative amount.

.. code-block:: yaml

    on_...:
      then:
        # Increases the brightness by 5%
        - light.dim_relative:
            id: light_1
            relative_brightness: 5%

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **relative_brightness** (**Required**, :ref:`templatable <config-templatable>`, percentage):
  The relative brightness to dim the light by.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition.

.. note::

    Example: dimming a light with a button press

    .. code-block:: yaml

        binary_sensor:
          - platform: gpio
            # ...
            id: my_binary_sensor
            on_press:
              - while:
                  condition:
                    binary_sensor.is_on: my_binary_sensor
                  then:
                    - light.dim_relative:
                        id: light_1
                        relative_brightness: 5%
                        transition_length: 0.1s
                    - delay: 0.1s

.. _light-addressable_set_action:

``light.addressable_set`` Action
********************************

This :ref:`Action <config-action>` allows you to manually set a range of LEDs on an addressable light
to a specific color.

.. code-block:: yaml

    on_...:
      - light.addressable_set:
          id: my_light
          range_from: 0
          range_to: 50
          red: 100%
          green: 0%
          blue: 0%

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the addressable light to control.
- **range_from** (*Optional*, :ref:`templatable <config-templatable>`, int): The beginning
  of the range of LEDs to control, inclusive, using zero-based indexing. Defaults to 0 (the beginning of the strip).
- **range_to** (*Optional*, :ref:`templatable <config-templatable>`, int): The end of the
  range of LEDs to control, inclusive, using zero-based indexing.
  Defaults to the end of the strip (``num_leds`` - 1).
- **color_brightness** (*Optional*, :ref:`templatable <config-templatable>`, percentage): The brightness to
  set the color channel to.
- **red** (*Optional*, :ref:`templatable <config-templatable>`, percentage): The value to
  set the red channel to.
- **green** (*Optional*, :ref:`templatable <config-templatable>`, percentage): The value to
  set the green channel to.
- **blue** (*Optional*, :ref:`templatable <config-templatable>`, percentage): The value to
  set the blue channel to.
- **white** (*Optional*, :ref:`templatable <config-templatable>`, percentage): The brightness to
  set the white channel to.

.. _light-is_on_condition:
.. _light-is_off_condition:

``light.is_on`` / ``light.is_off`` Condition
********************************************

This :ref:`Condition <config-condition>` checks if the given light is ON or OFF. OFF means
that the light is completely OFF, and ON means that the light is emitting at least a bit of light.

.. code-block:: yaml

    # In some trigger:
    on_...:
      if:
        condition:
          # Same syntax for is_off
          light.is_on: my_light


.. _light-on_turn_on_off_trigger:

``light.on_turn_on`` / ``light.on_turn_off`` Trigger
****************************************************

This trigger is activated each time the light is turned on or off. It is consistent
with the behavior of the ``light.is_on`` and ``light.is_off`` condition above.

.. code-block:: yaml

    light:
      - platform: binary # or any other platform
        # ...
        on_turn_on:
        - logger.log: "Light Turned On!"
        on_turn_off:
        - logger.log: "Light Turned Off!"

.. _light-on_state_trigger:

``light.on_state`` Trigger
**************************

This trigger is activated each time the set light state is changed. It is not triggered
based on current state, but rather, it triggers on the set state which can differ from
the current state due to transitions. For example, the ``light.on_state`` trigger can
be used for immediate action when the light is set to off; while ``light.on_turn_off``
does not trigger until the light actually achieves the off state.

.. code-block:: yaml

    light:
      - platform: binary # or any other platform
        # ...
        on_state:
        - logger.log: "Light State Changed!"

.. _light-effects:

Light Effects
-------------

ESPHome also offers a bunch of light effects you can use for your lights. The defaults for the
effect parameters are made to work well on their own but of course ESPHome gives you the option to manually change
these parameters.

With ESPHome's light effects system you're basically creating a bunch of entries for the effects dropdown in
Home Assistant. If you wish to have several variants of the same effect you can of course also create multiple
entries with each having a unique name like so:

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          # Use default parameters:
          - random:
          # Customize parameters
          - random:
              name: "My Slow Random Effect"
              transition_length: 30s
              update_interval: 30s
          - random:
              name: "My Fast Random Effect"
              transition_length: 4s
              update_interval: 5s

.. note::

    After setting a light effect, it is possible to reset the in-use effect back to a static light by setting the ``effect`` to ``none`` when it is being called through Home Assistant or directly on the device.

Pulse Effect
************

This effect makes a pulsating light. The period can be defined by ``update_interval``, the transition length with ``transition_length``. ``transition_length`` should be set to less than ``update_interval``, setting ``transition_length`` to ``1s`` and ``update_interval`` to ``2s`` will result in a transition from 0% to 100% lasting 1 second, 1 second full light, a transition from 100% to 0% for 1 second and off for 1 second.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - pulse:
          - pulse:
              name: "Fast Pulse"
              transition_length: 0.5s
              update_interval: 0.5s
              min_brightness: 0%
              max_brightness: 100%
          - pulse:
              name: "Slow Pulse"
              # transition_length: 1s      # defaults to 1s
              update_interval: 2s
          - pulse:
              name: "Asymmetrical Pulse"
              transition_length:
                on_length: 1s
                off_length: 500ms
              update_interval: 1.5s

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Pulse``.
- **transition_length** (*Optional*, :ref:`config-time`): The duration of each transition.
  Defaults to ``1s``. Can be a single time or split for on and off using these nested options.

  - **on_length** (*Optional*, :ref:`config-time`): The duration of the transition when the light is turned on.
  - **off_length** (*Optional*, :ref:`config-time`): The duration of the transition when the light is turned off.
- **update_interval** (*Optional*, :ref:`config-time`): The interval when the new transition is started. Defaults to ``1s``.
- **min_brightness** (*Optional*, percentage): The minimum brightness value. Defaults to ``0%``
- **max_brightness** (*Optional*, percentage): The maximum brightness value. Defaults to ``100%``


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
                - state: true
                  brightness: 100%
                  red: 100%
                  green: 90%
                  blue: 0%
                  duration: 500ms
                - state: false
                  duration: 250ms
                - state: true
                  brightness: 100%
                  red: 0%
                  green: 100%
                  blue: 0%
                  duration: 500ms

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Strobe``.
- **colors** (*Optional*, list): A list of colors to cycle through. Defaults to a quick cycle between ON and OFF.

  - **state** (*Optional*, boolean): The on/off state to show. Defaults to ``true``.
  - **color_mode** (*Optional*, string): The color mode of the light. Defaults to the current color mode.
  - **brightness** (*Optional*, percentage): The brightness of the light. Defaults to ``100%``.
  - **color_brightness** (*Optional*, percentage): The brightness of the RGB lights, if applicable. Defaults to ``100%``.
  - **red** (*Optional*, percentage): The red channel of the light, if applicable. Defaults to ``100%``.
  - **green** (*Optional*, percentage): The green channel of the light, if applicable. Defaults to ``100%``.
  - **blue** (*Optional*, percentage): The blue channel of the light, if applicable. Defaults to ``100%``.
  - **white** (*Optional*, percentage): The white channel of the light, if applicable. Defaults to ``100%``.
  - **color_temperature** (*Optional*, float): The color temperature (in `mireds <https://en.wikipedia.org/wiki/Mired>`__ or Kelvin) of the light, if applicable.
  - **cold_white** (*Optional*, percentage): The cold white channel of the light, if applicable. Defaults to ``100%``.
  - **warm_white** (*Optional*, percentage): The warm white channel of the light, if applicable. Defaults to ``100%``.
  - **duration** (**Required**, :ref:`config-time`): The duration this color should be active.
  - **transition_length** (*Optional*, :ref:`config-time`): The duration of each transition. Defaults to ``0s``.

See `light.turn_on <light-turn_on_action>` for more information on the various color fields.

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

Available variable in the lambda:

- **initial_run** - A bool which is true on the first execution of the lambda. Useful to reset static variables when restarting an effect.

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
                auto call = id(my_light).turn_on();
                // Transition of 1000ms = 1s
                call.set_transition_length(1000);
                if (state == 0) {
                  call.set_rgb(1.0, 1.0, 1.0);
                } else if (state == 1) {
                  call.set_rgb(1.0, 0.0, 1.0);
                } else if (state == 2) {
                  call.set_rgb(0.0, 0.0, 1.0);
                } else {
                  call.set_rgb(1.0, 0.0, 0.0);
                }
                call.perform();
                state += 1;
                if (state == 4)
                  state = 0;

Configuration variables:

- **name** (**Required**, string): The name of the custom effect.
- **update_interval** (*Optional*, :ref:`config-time`): The interval with which the lambda code is executed.
  A value of ``0ms`` means that the lambda is always executed, without a cool-down. Defaults to ``0ms``.
- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The code to execute. ``static`` variables are
  especially useful.


Addressable Rainbow Effect
**************************

A light effect for individually-addressable LEDs that creates a moving rainbow over the whole LED strip using
the HSV color wheel.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - addressable_rainbow:
          - addressable_rainbow:
              name: Rainbow Effect With Custom Values
              speed: 10
              width: 50

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Rainbow``.
- **speed** (*Optional*, int): The speed of the effect, unitless. Defaults to ``10``.
- **width** (*Optional*, int): The "width" of a full-scale rainbow, unitless. Defaults to ``50``.


Addressable Color Wipe Effect
*****************************

A light effect for individually-addressable LEDs that continuously introduces new colors at the beginning of
the strip and shifts them forward every ``add_led_interval``.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - addressable_color_wipe:
          - addressable_color_wipe:
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
              reverse: false
              gradient: false

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Color Wipe``.
- **colors** (*Optional*, list): The colors to shift in at the beginning of the strip. Defaults to shifting in random
  colors.

  - **red** (*Optional*, percentage): The percentage the red color channel should be on. Defaults to ``100%``.
  - **green** (*Optional*, percentage): The percentage the green color channel should be on. Defaults to ``100%``.
  - **blue** (*Optional*, percentage): The percentage the blue color channel should be on. Defaults to ``100%``.
  - **random** (*Optional*, boolean): If set to ``true``, will overwrite the RGB colors by a new, randomly-chosen
    color each time. Defaults to ``false``.
  - **num_leds** (**Required**, positive int): The number of LEDs of this type to have before transitioning to the next color. If ``gradient`` is true, this will be the number of LEDs over which the color transition will occur.
  - **gradient** (*Optional*, boolean): If ``true`` the current color will transition with a gradient over ``num_leds`` to the next color. Defaults to ``false``.

- **add_led_interval** (*Optional*, :ref:`config-time`): The interval with which to shift in new leds at the
  beginning of the strip. Defaults to ``100ms``.
- **reverse** (*Optional*, boolean): Whether to reverse the direction of the color wipe. Defaults to ``false``.

Addressable Scan Effect
***********************

Create a single, fast-moving dot moving back and forth an individually-addressable LED strip. The color is chosen by the
currently active light color.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - addressable_scan:
          - addressable_scan:
              name: Scan Effect With Custom Values
              move_interval: 100ms
              scan_width: 1

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Scan``.
- **move_interval** (*Optional*, :ref:`config-time`): The interval with which to move the dot/line one LED forward.
  Defaults to ``100ms``.
- **scan_width** (*Optional*, int): The number of LEDs to use.
  Defaults to ``1``.

Addressable Twinkle Effect
**************************

A light effect for individually-addressable LED strips that randomly chooses some LEDs and let's them bright
up for a moment, like a stars twinkling in the night's sky. The color of the pixels will be chosen by the
currently active light color.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - addressable_twinkle:
          - addressable_twinkle:
              name: Twinkle Effect With Custom Values
              twinkle_probability: 5%
              progress_interval: 4ms

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Twinkle``.
- **twinkle_probability** (*Optional*, percentage): The percentage with which, at any time step, a randomly-chosen
  LED should start its twinkle animation.
- **progress_interval** (*Optional*, :ref:`config-time`): The interval with which to progress the effect. This
  affects the duration of a twinkle animation. Defaults to ``4ms``.

Addressable Random Twinkle Effect
*********************************

A light effect similar to ``addressable_twinkle``, but using random colors for each twinkle animation.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - addressable_random_twinkle:
          - addressable_random_twinkle:
              name: Random Twinkle Effect With Custom Values
              twinkle_probability: 5%
              progress_interval: 32ms

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Random Twinkle``.
- **twinkle_probability** (*Optional*, percentage): The percentage with which, at any time step, a randomly-chosen
  LED should start its twinkle animation.
- **progress_interval** (*Optional*, :ref:`config-time`): The interval with which to progress the effect. This
  affects the duration of a twinkle animation. Defaults to ``4ms``.


Addressable Fireworks Effect
****************************

A light effect for individually-addressable LED strips that randomly sparks some fireworks at random positions
and lets the sparkles cascade over the LED strip.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - addressable_fireworks:
          - addressable_fireworks:
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
- **fade_out_rate** (*Optional*, int): The rate with which to fade out the LED strip, unitless. Needs to be carefully
  chosen so that the whole strip doesn't light up forever if the fade out rate is too low or that the firework
  sparks do not propagate for a long time. Defaults to ``120``.

Addressable Flicker Effect
**************************

An effect similar to the ``flicker`` effect, but for individually-addressable LED strips. This effect flickers
each LED by its own random amount around the currently active light color.

.. code-block:: yaml

    light:
      - platform: ...
        # ...
        effects:
          - addressable_flicker:
          - addressable_flicker:
              name: Flicker Effect With Custom Values
              update_interval: 16ms
              intensity: 5%

Configuration variables:

- **name** (*Optional*, string): The name of the effect. Defaults to ``Addressable Flicker``.
- **update_interval** (*Optional*, :ref:`config-time`): The time interval for updating the random offsets.
  Defaults to ``16ms``.
- **intensity** (*Optional*, percentage): The intensity of the effect, basically how much the random values can offset
  the currently active light color. Defaults to ``5%``.

Addressable Lambda Effect
*************************

This effect allows you to access each LED individually in a custom light effect.

Available variables in the lambda:

- **it** - :apiclass:`AddressableLight <light::AddressableLight>` instance (see API reference for more info).
- **current_color**  - :apistruct:`ESPColor <light::ESPColor>` instance (see API reference for more info).
- **initial_run** - A bool which is true on the first execution of the lambda. Useful to reset static variables when restarting an effect.

  .. note::

      ESPColor has been migrated to Color. See :apistruct:`Color <Color>` for more information.

.. code-block:: yaml

    light:
    - platform: ...
      effects:
        - addressable_lambda:
            name: "My Custom Effect"
            update_interval: 16ms
            lambda: |-
              // it.size() - Number of LEDs
              // it[num] - Access the LED at index num.
              // Set the LED at num to the given r, g, b values
              // it[num] = Color(r, g, b);
              // Get the color at index num (Color instance)
              // it[num].get();

              // Example: Simple color wipe
              for (int i = it.size() - 1; i > 0; i--) {
                it[i] = it[i - 1].get();
              }
              it[0] = Color::random_color();

              // Bonus: use .range() and .all() to set many LEDs without having to write a loop.
              it.range(0, 50) = Color::BLACK;
              it.all().fade_to_black(10);

.. code-block:: yaml

    light:
    - platform: ...
      effects:
        - addressable_lambda:
            name: "My Custom Effect"
            update_interval: 16ms
            lambda: |-
              // Static variables keep their value even when
              // stopping and starting the effect again
              static uint16_t progress = 0;

              // normal variables lose their value after each
              // execution - basically after each update_interval
              uint16_t changes = 0;

              // To reset static when stopping and starting the effect
              // again you can use the initial_run variables
              if (initial_run) {
                progress = 0;
                it.all() = Color::BLACK;
                // optionally do a return so nothing happens until the next update_interval
                return;
              }


Examples of this API can be found here:
https://github.com/esphome/esphome/blob/dev/esphome/components/light/addressable_light_effect.h
(the built-in addressable light effects).

Automation Light Effect
***********************

Additionally to the ``lambda`` and ``addressable_lambda`` light effects, effects can also
be written through ESPHome's :ref:`Automation <automation>` system with the ``automation``
effect type.

The automation given in the ``sequence`` block will be repeatedly executed until the effect
is stopped by the user.

.. code-block:: yaml

    light:
    - platform: ...
      id: my_light
      effects:
        - automation:
            name: Custom Automation Effect
            sequence:
              - light.addressable_set:
                  id: my_light
                  red: 100%
                  green: 100%
                  blue: 100%
              - delay: 100ms
              - light.addressable_set:
                  id: my_light
                  range_from: 0
                  range_to: 20
                  red: 100%
                  green: 0%
                  blue: 0%

Configuration variables:

- **name** (*Optional*, string): The name of the effect.
- **sequence** (*Optional*, :ref:`Action <config-action>`): The actions to perform in sequence
  until the effect is stopped.

.. _e131-light-effect:

E1.31 Effect
************

This effect enables controlling addressable lights using UDP-based
E1.31_ protocol.

For Example JINX_ or Hyperion.NG_ could be used to control E1.31_ enabled ESPHome.

.. code-block:: yaml

    e131:
      method: multicast # default: register E1.31 to Multicast group

    light:
      - platform: neopixelbus
        num_leds: 189
        effects:
          - e131:
              universe: 1
              channels: RGB

Configuration variables:

- **universe** (**Required**, int): The value of universe, between 1 to 512.
- **channels** (*Optional*): The type of data. This is used to specify if it is a ``MONO``,
  ``RGB`` or ``RGBW`` light and in which order the colors are. Defaults to ``RGB``.

There are three modes of operation:

- ``MONO``: this supports 1 channel per LED (luminance), up-to 512 LEDs per universe
- ``RGB``: this supports 3 channels per LED (RGB), up-to 170 LEDs (3*170 = 510 bytes) per universe
- ``RGBW``: this supports 4 channels per LED (RGBW), up-to 128 LEDs (4*128 = 512 bytes) per universe

If there's more LEDs than allowed per-universe, additional universe will be used.
In the above example of 189 LEDs, first 170 LEDs will be assigned to 1 universe,
the rest of 19 LEDs will be automatically assigned to 2 universe.

It is possible to enable multiple light platforms to listen to the same universe concurrently,
allowing to replicate the behaviour on multiple strips.

E1.31 Component
^^^^^^^^^^^^^^^

The :ref:`e131-light-effect` requires a component hub for the ``e131`` light effect.

Configuration variables:

- **method** (*Optional*): Listening method, one of ``multicast`` or ``unicast``. Defaults to ``multicast``.

The udp port esphome is listening on is 5568.

.. _E1.31: https://www.doityourselfchristmas.com/wiki/index.php?title=E1.31_(Streaming-ACN)_Protocol
.. _JINX: http://www.live-leds.de/jinx-v1-3-with-resizable-mainwindow-real-dmx-and-sacne1-31/
.. _Hyperion.NG: https://github.com/hyperion-project/hyperion.ng

Adalight Effect
***************

This effect enables controlling addressable lights using UART-based
Adalight_ protocol, allowing to create realtime ambient lighting effects.

Prismatik_ can be used to control addressable lights via Adalight_ protocol
on ESPHome.

.. code-block:: yaml

    # Example configuration entry
    # Disable logging over USB
    logger:
      baud_rate: 0

    # Adalight requires higher RX buffer size
    # to operate without flickering
    uart:
      rx_buffer_size: 1024

    adalight:

    light:
      - platform: neopixelbus
        ...
        effects:
          - adalight:
              # uart_id: additional_uart

Configuration variables:

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want
  to use multiple UART buses.

.. _Adalight: https://learn.adafruit.com/adalight-diy-ambient-tv-lighting
.. _Prismatik: https://github.com/psieg/Lightpack

WLED Effect
***********

This effect enables controlling addressable lights using UDP-based
`UDP Realtime Control`_ protocol used by WLED_, allowing to create realtime ambient
lighting effects.

Prismatik_ can be used to control addressable lights over network on ESPHome.
It is also possible to use LedFx_ to control the lights. Please use the connection type ``udp`` on the default port and add the Data Prefix ``0201``.

.. code-block:: yaml

    wled:

    light:
      - platform: neopixelbus
        ...
        effects:
          - wled:
              # port: 21324
              # blank_on_start: True
              # sync_group_mask: 0

Configuration variables:

- **port** (*Optional*, int): The port to run the UDP server on. Defaults to ``21324``.
- **blank_on_start** (*Optional*, boolean): Whether or not to blank all LEDs when effect starts. Deaults to ``True``.
- **sync_group_mask** (*Optional*, int): Used with WLED Notifier. The Sync Group mask value that specifies which WLED Sync Groups to listen to. Defaults to ``0`` (All Sync Groups). Sync Groups 1, 2, 3, 4, 5, 6, 7, 8 use masks 1, 2, 4, 8, 16, 32, 64, 128. Combine mask values to listen to multiple Sync Groups.

.. note::

    You can also set the ``port`` to ``19446`` for compatibility with Hyperion Classic using a
    UDP device with protocol 0.

Currently the following realtime protocols are supported:
WARLS, DRGB, DRGBW, DNRGB and WLED Notifier.

.. _UDP Realtime Control: https://github.com/Aircoookie/WLED/wiki/UDP-Realtime-Control
.. _WLED: https://github.com/Aircoookie/WLED/wiki/UDP-Realtime-Control
.. _Prismatik: https://github.com/psieg/Lightpack
.. _LedFx: https://github.com/LedFx/LedFx

See Also
--------

- :apiref:`light/light_state.h`
- `WS2812FX library <https://github.com/kitesurfer1404/WS2812FX>`__ by `@kitesurfer1404 <https://github.com/kitesurfer1404>`__
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
