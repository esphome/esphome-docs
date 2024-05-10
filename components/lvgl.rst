.. _lvgl-main:

LVGL Graphics
=============

.. seo::
    :description: LVGL - ESPHome Displays showing contents created with Light and Versatile Graphics Library
    :image: /images/lvgl.png

`LVGL <https://lvgl.io/>`__ (Light and Versatile Graphics Library) is a free and open-source 
embedded graphics library to create beautiful UIs for any MCU, MPU and display type. ESPHome supports `LVGL version 8 <https://docs.lvgl.io/8.4/>`__.

.. figure:: /components/images/lvgl_main_screenshot.png

In order to be able to drive a :ref:`display <display-hw>` with LVGL under ESPHome you need an MCU from the ESP32 family. Although PSRAM is not a strict requirement, it is recommended.

The display itself has to be a graphical binary type, should be configured with ``auto_clear_enabled: false`` and ``update_interval: never``, and should not have any ``lambda`` set. It should have an :ref:`config-id` set, which will be referenced in the main LGVL component configuration.

For interactivity, a :ref:`Touchscreen <touchscreen-main>` (capacitive highly preferred) or a :doc:`/components/sensor/rotary_encoder` can be used.

Check out a few detailed examples :ref:`in the Cookbook <lvgl-cook>` to see a couple ways to integrate LVGL through ESPHome with your environment.

Basics
------

In LVGL, graphical elements like Buttons, Labels, Sliders etc. are called widgets or objects. See :ref:`lvgl-widgets` for a list of the available ones in ESPHome. Not all LVGL widgets are implemented, just the ones having most common use cases in home automation.

Every widget has a parent object where it is created. For example, if a label is created on a button, the button is the parent of label. Some more complex widgets are internally made up from the simpler ones, these are known as parts - which can have separate properties from the main widget.

Pages in ESPHome are implemented as LVGL screens, which are special objects which have no parent. There is always one active page on a display.

Widgets can be assigned with an :ref:`config-id` so that they can be referenced in :ref:`automations <automation>`.

Some widgets integrate also as native ESPHome components:

.. list-table::
    :header-rows: 1
    :widths: 1 1

    * - LVGL Widget
      - ESPHome component

    * - ``btn``
      - :doc:`Binary Sensor </components/binary_sensor/lvgl>`, :doc:`Switch </components/switch/lvgl>`

    * - ``switch``, ``checkbox``
      - :doc:`Switch </components/switch/lvgl>`

    * - ``slider``, ``arc``, ``spinbox``
      - :doc:`Number </components/number/lvgl>`

    * - ``dropdown``,  ``roller``
      - :doc:`Select </components/select/lvgl>`

    * - ``led``
      - :doc:`Light </components/light/lvgl>`

These are useful to make :ref:`automations <automation>` triggered by actions performed at the screen.

Main Configuration
------------------

Although LVGL is a complex matrix of objects-parts-states-styles, in ESPHome this is simplified to a hierarchy.

At the highest level of the LVGL object hierarchy is the display represented the hardware driver. A display can have one or more pages associated with it. Each page contains a hierarchy of objects for graphical widgets representing a layout that covers the entire display.

The following configuration options apply to the main ``lvgl`` component, in order to establish the principal operating conditions. Some :ref:`styling options <lvgl-theme>` can be set at this level too, but only for inheritance purposes.

**Configuration options:**

- **displays** (**Required**, list): A list of displays where to render this entire LVGL configuration:
    - **display_id** (**Required**, :ref:`config-id`): The ID of a display configuration.
- **touchscreens** (*Optional*, list): A list of touchscreens interacting with the LVGL widgets on the display. Can be omitted if there's at least a rotary encoder configured.
    - **touchscreen_id** (**Required**, :ref:`config-id`): ID of a touchscreen configuration related to a display.
    - **long_press_time** (*Optional*, :ref:`Time <config-time>`): For the touchscreen above, delay after which the ``on_long_pressed`` :ref:`event trigger <lvgl-event-trg>` will be called. Defaults to ``400ms``.
    - **long_press_repeat_time** (*Optional*, :ref:`Time <config-time>`): For the touchscreen above, repeated interval after ``long_press_time``, when ``on_long_pressed_repeat`` :ref:`event trigger <lvgl-event-trg>` will be called. Defaults to ``100ms``.
- **rotary_encoders** (*Optional*, list): A list of rotary encoders interacting with the LVGL widgets on the display. Can be omitted if there's at least a touchscreen configured.
    - **sensor:** (**Required**, :ref:`config-id`): The ID of a :doc:`/components/sensor/rotary_encoder` used to interact with the widgets.
    - **binary_sensor** (*Optional*, :ref:`config-id`): The ID of a :doc:`/components/binary_sensor/index`, usually used as a push button within the rotary encoder used to interact with the widgets.
    - **group** (*Optional*, string): A name for a group of widgets which will interact with the the rotary encoder. See the :ref:`common properties <lvgl-widgets>` of the widgets for more information on groups.
    - **long_press_time** (*Optional*, :ref:`Time <config-time>`): For the encoder above, delay after which the ``on_long_pressed`` :ref:`event trigger <lvgl-event-trg>` will be called. Defaults to ``400ms``.
    - **long_press_repeat_time** (*Optional*, :ref:`Time <config-time>`): For the encoder above, repeated interval after ``long_press_time``, when ``on_long_pressed_repeat`` :ref:`event trigger <lvgl-event-trg>` will be called. Defaults to ``100ms``.
- **color_depth** (*Optional*, enum): The color deph at which the contents are generated. Valid values are ``1`` (monochrome), ``8``, ``16`` or ``32``, defaults to ``16``.
- **buffer_size** (*Optional*, percentage): The percentage of screen size to allocate buffer memory. Default is ``100%`` (or ``1.0``). For devices without PSRAM recommended value is ``25%``. 
- **update_interval**: (*Optional*, :ref:`Time <config-time>`): The interval to re-draw the screen if necessary. Defaults to ``1s``.
- **log_level** (*Optional*, enum): Set the logger level specifically for the messages of the LVGL library: ``TRACE``, ``INFO``, ``WARN``, ``ERROR``, ``USER``, ``NONE``. Defaults to ``WARN``.
- **byte_order** (*Optional*, enum): The byte order of the data outputted by lvgl, ``big_endian`` or ``little_endian``. If not specified, defaults to ``big_endian``.
- **disp_bg_color** (*Optional*, :ref:`color <lvgl-color>`): Solid color to fill the background. Can be changed a runtime with ``lvgl.update`` action.
- **disp_bg_image** (*Optional*, :ref:`image <display-image>`):  The ID of an existing image configuration, to be used as background wallpaper. To change the image at runtime use the ``lvgl.update`` action.
- **default_font** (*Optional*, enum): The ID of the :ref:`font <lvgl-fonts>` used by default to render the text or symbols. Defaults to LVGL's internal ``montserrat_14`` if not specified.
- **style_definitions** (*Optional*, list): A batch of style definitions to use in LVGL widgets ``styles`` configuration. See :ref:`below <lvgl-theme>` for more details. 
- **theme** (*Optional*, list): A list of styles to commonly apply to the widgets. See :ref:`below <lvgl-theme>` for more details. 
- **widgets** (*Optional*, list): A list of :ref:`lvgl-widgets` to be drawn on the root display. Not possible if you configure ``pages``.
- **pages** (*Optional*, list): A list of page IDs, where each page acts as a parent for widgets placed on it. Only if no ``widgets`` are configured at this level! Options for each page:
    - **skip** (*Optional*, boolean): Option to skip this page when navigating between them with :ref:`lvgl-pgnx-act`.
    - **layout** (*Optional*, string): ``FLEX``, ``GRID`` or ``NONE``. See :ref:`layouts <lvgl-layouts>`.  If not specified, defaults to ``NONE``, which disables layouts each widget needing manual positioning.
    - **flex_flow** (*Optional*, string): See :ref:`flex layout <lvgl-layouts-flex>` options. 
    - All other options from :ref:`lvgl-styling` to be applied to this page.
    - **widgets** (*Optional*, list): A list of :ref:`lvgl-widgets` to be drawn on the page.
- **page_wrap** (*Optional*, boolean): Wrap pages around when navigating between them with :ref:`lvgl-pgnx-act`. Defaults to ``true`` if not specified.
- **top_layer** (*Optional*, list): A special kind of *Always on Top* page, which acts as a parent for widgets placed on it. It's shown above all the pages - useful for widgets which need to be always visible, regardless of the pages. Only of no ``widgets`` are configured at this level. Options:
    - **layout** (*Optional*, string): ``FLEX``, ``GRID`` or ``NONE``. See :ref:`layouts <lvgl-layouts>`.  If not specified, defaults to ``NONE``, which disables layouts each widget needing manual positioning.
    - **flex_flow** (*Optional*, string): See :ref:`flex layout <lvgl-layouts-flex>` options. 
    - All other options from :ref:`lvgl-styling` to be applied to this page.
    - **widgets** (*Optional*, list): A list of :ref:`lvgl-widgets` to be drawn on the page.
- **layout** (*Optional*, string): ``FLEX``, ``GRID`` or ``NONE``. See :ref:`layouts <lvgl-layouts>`.  If not specified, defaults to ``NONE``, which disables layouts each widget needing manual positioning.
- **flex_flow** (*Optional*, string): See :ref:`flex layout <lvgl-layouts-flex>` options. 

- All other options from :ref:`lvgl-styling` to be commonly apply to the widgets directly.

**Example:**

.. code-block:: yaml

    # Example configuration entry
    lvgl:
      displays:
        - display_id: my_display
      touchscreens:
        - touchscreen_id: my_touch
      pages:
        - id: main_page
          widgets:
            - label:
                align: CENTER
                text: 'Hello World!'

See :ref:`lvgl-cook-navigator` in the Cookbook for an example how to easily implement a page navigation bar at the bottom of the screen.

.. note::

    Currently ``RGB565`` type images are supported, with transparency using the optional parameter ``use_transparency`` set to ``true``. See :ref:`display-image` for how to load an image for rendering in ESPHome.

.. _lvgl-color:

Colors
******

Colors can be specified anywhere in the LVGL configuration either by referencing a preconfigured :ref:`ESPHome color <config-color>` ID, or by representing directly in hexadecimal format. Eg. ``0xFF0000`` for red.

.. _lvgl-opa:

Opacity
*******

Various parts of the widgets (like background, borders etc.) support opacity. It can be overridden with a string: ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or percentage between ``0%`` and ``100%``. Actual default values depend on widget specifics.

.. _lvgl-fonts:

Fonts
*****

There are two font choices for LVGL here: 

**ESPHome fonts**

You can use :ref:`fonts configured normally<display-fonts>`, the glyphs will be rendered while building the binary. This has the advantage that you can define custom sets of glyphs of any size, with icons or diacritic characters of your choice, for any language, from any TrueType/OpenType font, allowing a more optimal flash space usage because you don't need to include all glyphs for all sizes you wish to use.

Check out :ref:`lvgl-cook-icontext`, :ref:`lvgl-cook-iconstat` and :ref:`lvgl-cook-iconbatt` in the Cookbook for examples how to play with texts and icons using various TrueType/OpenType fonts.

**Library fonts**

The LVGL library offers by default prerendered sets with ASCII characters (``0x20-0x7F``) the degree symbol (``0xB0``), the bullet symbol (``0x2022``) from the `Montserrat <https://fonts.google.com/specimen/Montserrat>`__ Medium font, and 60 symbols from the `FontAwesome <https://fontawesome.com/>`__ font (see below). You can use the IDs below when specifying the ``text_font`` parameter:

- ``montserrat_8``: 8px font
- ``montserrat_10``: 10px font
- ``montserrat_12``: 12px font
- ``montserrat_14``: 14px font (**default**, included if ``default_font`` option is missing)
- ``montserrat_16``: 16px font
- ``montserrat_18``: 18px font
- ``montserrat_20``: 20px font
- ``montserrat_22``: 22px font
- ``montserrat_24``: 24px font
- ``montserrat_26``: 26px font
- ``montserrat_28``: 28px font
- ``montserrat_30``: 30px font
- ``montserrat_32``: 32px font
- ``montserrat_34``: 34px font
- ``montserrat_36``: 36px font
- ``montserrat_38``: 38px font
- ``montserrat_40``: 40px font
- ``montserrat_42``: 42px font
- ``montserrat_44``: 44px font
- ``montserrat_46``: 46px font
- ``montserrat_48``: 48px font

The binary will only include any of the above if used in the configuration.

You can display the embedded symbols among the text by their codepoint address preceded by ``\u``, eg. ``\uF00C``:

.. figure:: /components/images/lvgl_symbols.png
    :align: center

.. note::

    The ``text_font`` parameter affects the size of symbols, since all the built-in font arrays based on Montserrat include these symbols at the respective sizes. If you set ``text_font`` on a widget to a custom ESPHome font, these symbols will likely not display, unless you include them manually from a FontAwesome OpenType file.
    
    For escape sequences to work, you have to put them in strings enclosed in double quotes.

In addition to the above, the following special fonts are available from LVGL as built-in:

- ``unscii_8``: 8 px pixel perfect font with only ASCII characters.
- ``unscii_16``: 16 px pixel perfect font with only ASCII characters.
- ``simsun_16_cjk``: 16 px font with normal range + 1000 most common `CJK Radicals <https://en.wikipedia.org/wiki/CJK_Radicals_Supplement>`__.
- ``dejavu_16_persian_hebrew``: 16 px font with normal range + Hebrew, Arabic, Persian letters and all their forms.

.. _lvgl-styling:

Style properties
****************

LVGL follows CSS's `border-box model <https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing>`__. A widget's *box* is built from the following parts:

.. figure:: /components/images/lvgl_boxmodel.png
    :align: center

- *bounding box*: the box defined with ``width`` and ``height`` of the widgets (pixels or parent content area percentage; not drawn, just for calculations).
- *border*: the border line, drawn on the inner side of the bounding box (pixels).
- *outline*: the outline, drawn on the outer side of the bounding box (pixels).
- *padding*: space to keep between the border of the widget and its content or children (*I don't want my children too close to my sides, so keep this space*). 
- *content*: the content area which is the size of the bounding box reduced by the border width and padding (it's what's referenced as the ``size_content`` option of certain widgets).

You can adjust the appearance of widgets by changing the foreground, background and/or border color, font of each of them. Some widgets allow for more complex styling, effectively changing the appearance of their parts. 

**Styling options:**

- **bg_color** (*Optional*, :ref:`color <lvgl-color>`): Color for the background of the widget. Defaults to ``0xFFFFFF`` (white).
- **bg_grad_color** (*Optional*, :ref:`color <lvgl-color>`): Color to make the background gradually fade to. Defaults to ``0`` (black).
- **bg_dither_mode** (*Optional*, enum): Set dithering of the background gradient. One of ``NONE``, ``ORDERED``, ``ERR_DIFF``. Defaults to ``NONE``.
- **bg_grad_dir** (*Optional*, enum): Choose the direction of the background gradient: ``NONE``, ``HOR``, ``VER``. Defaults to ``NONE``.
- **bg_main_stop** (*Optional*, 0-255): Specify where the gradient should start: ``0`` = at left/top most position, ``128`` = in the center, ``255`` = at right/bottom most position. Defaults to ``0``.
- **bg_grad_stop** (*Optional*, 0-255): Specify where the gradient should stop: ``0`` = upper left, ``128`` = in the center, ``255`` = lower right. Defaults to ``255``.
- **opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the entire widget. Inherited from parent. Defaults to ``COVER``.
- **bg_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the widget background.
- **opa_layered** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the entire layer the widget is on. Inherited from parent. Defaults to ``COVER``.
- **bg_img_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the background image (if such option is supported) of the widget.
- **bg_img_recolor** (*Optional*, :ref:`color <lvgl-color>`): Color to mix with every pixel of the background image (if such option is supported) of the widget.
- **bg_img_recolor_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the recoloring. 
- **border_width** (*Optional*, int16): Set the width of the border in pixels. Defaults to ``0``.
- **border_color** (*Optional*, :ref:`color <lvgl-color>`): Color to draw borders of the widget. Defaults to ``0`` (black).
- **border_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the borders of the widget.  Defaults to ``COVER``.
- **border_post** (*Optional*, boolean): If ``true`` the border will be drawn after all children of the widget have been drawn. Defaults to ``false``.
- **border_side** (*Optional*, list): Select which borders of the widgets to show (multiple can be specified, defaults to ``NONE``):
    - ``NONE``
    - ``TOP``
    - ``BOTTOM``
    - ``LEFT``
    - ``RIGHT``
    - ``INTERNAL``
- **radius** (*Optional*, uint16): The radius to be used to form the widget's rounded corners. 0 = no radius (square corners); 65535 = pill shaped widget (true circle if it has same width and height).
- **clip_corner** (*Optional*, boolean): If set to ``true``, overflowing content will be clipped off by the widget's rounded corners (``radius`` > ``0``).
- **outline_width** (*Optional*, int16): Set the width of the outline in pixels. Defaults to ``0``.
- **outline_color** (*Optional*, :ref:`color <lvgl-color>`): Color used to draw an outline around the widget. Defaults to ``0`` (black).
- **outline_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the outline of the widget. Defaults to ``COVER``.
- **outline_pad** (*Optional*, int16): Distance between the outline and the widget itself. Defaults to ``0``.
- **pad_all** (*Optional*, int16): Set the padding in all directions, in pixels.
- **pad_top** (*Optional*, int16): Set the padding on the top, in pixels.
- **pad_bottom** (*Optional*, int16): Set the padding on the bottom, in pixels.
- **pad_left** (*Optional*, int16): Set the padding on the left, in pixels.
- **pad_right** (*Optional*, int16): Set the padding on the right, in pixels.
- **pad_row** (*Optional*, int16): Set the padding between the rows of the children elements, in pixels.
- **pad_column** (*Optional*, int16): Set the padding between the columns of the children elements, in pixels.
- **shadow_color** (*Optional*, :ref:`color <lvgl-color>`): Color used to create a drop shadow under the widget. Defaults to ``0`` (black).
- **shadow_ofs_x** (*Optional*, int16): Horizontal offset of the shadow, in pixels. Defaults to ``0``.
- **shadow_ofs_y** (*Optional*, int16): Vertical offset of the shadow, in pixels. Defaults to ``0``.
- **shadow_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the shadow. Defaults to ``COVER``.
- **shadow_spread** (*Optional*, int16): Spread of the shadow, in pixels. Defaults to ``0``.
- **shadow_width** (*Optional*, int16): Width of the shadow, in pixels. Defaults to ``0``.
- **transform_angle** (*Optional*, 0-360): Transformation angle of the widget (eg. rotation)
- **transform_height** (*Optional*, int16 or percentage): Transformation height of the widget (eg. stretching)
- **transform_pivot_x** (*Optional*, int16 or percentage): Horizontal anchor point of the transformation. Relative to the widget's top left corner.
- **transform_pivot_y** (*Optional*, int16 or percentage): Vertical anchor point of the transformation. Relative to the widget's top left corner.
- **transform_zoom** (*Optional*, 0.1-10):  Transformation zoom of the widget (eg. resizing)
- **translate_x** (*Optional*, int16 or percentage): Movement of the widget with this value in horizontal direction.
- **translate_y** (*Optional*, int16 or percentage): Movement of the widget with this value in vertical direction.

.. _lvgl-theme:

Themes
******

The widgets support lots of :ref:`lvgl-styling` to customize their appearance and behavior.

You can configure a global theme for all widgets at the top level with the ``theme`` configuration variable. In the example below, all the ``arc``, ``slider`` and ``btn`` widgets will, by default, use the styles and properties defined here. A combination of styles and :ref:`states <lvgl-wgtprop-state>` can be chosen for every widget.

.. code-block:: yaml

    lvgl:
      theme:
        arc:
          scroll_on_focus: true
          group: general
        slider:
          scroll_on_focus: true
          group: general
        btn:
          scroll_on_focus: true
          group: general
          border_width: 2
          outline_pad: 6
          pressed:
            border_color: 0xFF0000
          checked:
            border_color: 0xFFFF00
          focused:
            border_color: 0x00FF00

Naturally, you can override these at the individual configuration level of each widget. This can be done in batches, using ``style_definitions`` configuration option of the main component.
In the example below, you defined ``date_style``:

.. code-block:: yaml

    lvgl:
      style_definitions:
        - id: date_style      # choose an ID for your definition
          text_font: unscii_8
          align: center
          text_color: 0x000000
          bg_opa: cover
          radius: 4
          pad_all: 2

And then you apply these selected styles to two labels, and only change very specific style ``y`` locally:

.. code-block:: yaml

    widgets:
      - label:
          id: day_label
          styles: date_style # apply the definition here by the ID chosen above
          y: -20
      - label:
          id: date_label
          styles: date_style
          y: +20

Additionally, you can change the styles based on the :ref:`state <lvgl-wgtprop-state>` property of the widgets or their parts. If you want to set a property for all states (e.g. red background color) just set it for the default state at the root of the widget. If the widget can't find a property for its current state it will fall back to this.

In the example below, you have an ``arc`` with some styles set here. Note how you change the ``arc_color`` of the ``indicator`` part, based on state changes:

.. code-block:: yaml

    - arc:
        id: my_arc
        value: 75
        min_value: 1
        max_value: 100
        indicator:
          arc_color: 0xF000FF
          pressed:
            arc_color: 0xFFFF00
          focused:
            arc_color: 0x808080

So the inheritance happens like this: state based styles override the locally specified styles, which override the style definitions, which override the theme, which overrides the top level styles.

The precedence (value) of states is quite intuitive, and it's something the user would expect naturally. E.g. if a widget is focused the user will still want to see if it's pressed, therefore the pressed state has a higher precedence. If the focused state had a higher precedence it would overwrite the pressed color.

Feel free to experiment to discover inheritance of the styles based on states between the nested widgets.

:ref:`lvgl-cook-theme` in the Cookbook shows an example how to easily implement a gradient style for your widgets.

.. _lvgl-layouts:

Layouts
*******

Layouts help positioning the widgets automatically, without the need to manually specify the ``x`` and the ``y`` positional coordinates for each. This is a great way to simplify the configuration, allowing you to even omit alignment options.

The layout configuration options are applied to any parent widget or page, influencing the appearance of the children.

.. _lvgl-layouts-flex:

**Flex**

The Flex layout in LVGL is a subset implementation of `CSS Flexbox <https://css-tricks.com/snippets/css/a-guide-to-flexbox/>`__.

It can arrange items into rows or columns (tracks), handle wrapping, adjust the spacing between the items and tracks, handle grow to make the item(s) fill the remaining space with respect to min/max width and height.

Terms used:

- *tracks*: the rows or columns main direction: row or column, the direction in which the items are placed.
- *cross direction*: perpendicular to the main direction.
- *wrap*: if there is no more space in the track a new track is started.
- *grow*: if set on an item it will grow to fill the remaining space on the track. The available space will be distributed among items respective to their grow value (larger value means more space).
- *gap*: the space between the rows and columns or the items on a track.

In a Flex layout, use the following options in the ``flex_flow`` configuration parameter to select the arrangement of the children widgets:

- ``ROW``: place the children in a row without wrapping.
- ``COLUMN``: place the children in a column without wrapping.
- ``ROW_WRAP``: place the children in a row with wrapping (default).
- ``COLUMN_WRAP``: place the children in a column with wrapping.
- ``ROW_REVERSE``: place the children in a row without wrapping but in reversed order.
- ``COLUMN_REVERSE``: place the children in a column without wrapping but in reversed order.
- ``ROW_WRAP_REVERSE``: place the children in a row with wrapping but in reversed order.
- ``COLUMN_WRAP_REVERSE``: place the children in a column with wrapping but in reversed order.

.. _lvgl-layouts-grid:

**Grid**

The Grid layout in LVGL is a subset implementation of `CSS Flexbox <https://css-tricks.com/snippets/css/a-guide-to-flexbox/>`__.

It can arrange items into a 2D "table" that has rows or columns (tracks). The item can span through multiple columns or rows. The track's size can be set in pixel, to the largest item or in "Free unit" to distribute the free space proportionally.

.. _lvgl-widgets:

Widgets
-------

At the next level of the LVGL object hierarchy are the widgets, which support styling directly. They can have sub-parts, which may be styled separately. Usually styles are inherited, but this depends on widget specifics or functionality. The widget and its parts have states, and the different styling can be set for different states.

Widgets can have children, which can be any other widgets. Think of this as a nested structure. The child widgets move with the parent and if the parent is hidden the children will be hidden too. 

By default, LVGL draws new widgets on top of old widgets, including their children. When widgets have children, property inheritance takes place. Some properties (typically that are related to text and opacity) can be inherited from the parent widgets's styles. When the property is inheritable, the property's value will be searched in the parents too until an object specifies a value for it. The parents will use their own :ref:`state <lvgl-wgtprop-state>` to determine the value. So for example if a button is pressed, and the text color comes from here, the pressed text color will be used. 

Common properties
*****************

The properties below are common to all widgets.

- **x** (*Optional*, int16 or percentage): Horizontal position of the widget (anchored in the top left corner, relative to top left of parent or screen). If layouts are used, or if specifying ``align``, it is used as an offset to the calculated position (can also be negative).
- **y** (*Optional*, int16 or percentage): Vertical position of the widget (anchored in the top left corner, relative to to top left of the parent or screen). If layouts are used, or if specifying ``align``, it is used as an offset to the calculated position (can also be negative).

.. note::

    By default, the ``x`` and ``y`` coordinates are measured from the *top left corner* of the parent's content area. :ref:`Important <lvgl-styling>`: content area starts *after the padding* thus if the parent has a non-zero padding value, position will be shifted with that. Percentage values are calculated from the parent's content area size. 

- **width** (*Optional*): Width of the widget in pixels or a percentage, or ``size_content`` (see note below).
- **height** (*Optional*): Height of the widget in pixels or a percentage, or ``size_content`` (see note below).

.. note::

    The size settings support a special value: ``size_content``. It means the widget's size in the respective direction will be set to the size of its children. Note that only children on the right and bottom sides will be considered and children on the top and left remain cropped. This limitation makes the behavior more predictable. Widgets with ``hidden`` or ``floating`` flags will be ignored by the ``size_content`` calculation.
    
    Similarly to CSS, LVGL also supports ``min_width``, ``max_width``, ``min_height`` and ``max_height``. These are limits preventing a widget's size from becoming smaller/larger than these values. They are especially useful if the size is set by percentage or ``size_content``.

- **min_width**, **max_width**, **min_height**, **max_height** (*Optional*, int16 or percentage): Sets a minimal/maximal width or a minimal/maximal height. Pixel and percentage values can be used. Percentage values are relative to the height of the parent's content area. Defaults to ``0%``.
- **scrollbar_mode** (*Optional*, string): If a child widget is outside its parent content area (the size without padding), the parent can become scrollable (see the ``scrollable`` :ref:`flag <lvgl-objupdflag-act>`). The widget can either be scrolled horizontally or vertically in one stroke. Scroll bars can appear depending on the setting:
    - ``"OFF"``: Never show the scroll bars (use the double quotes!).
    - ``"ON"``: Always show the scroll bars (use the double quotes!).
    - ``"ACTIVE"``: Show scroll bars while a widget is being scrolled.
    - ``"AUTO"``: Show scroll bars when the content is large enough to be scrolled (default).

- **align** (*Optional*, enum): Alignment of the of the widget relative to the parent. A child widget is clipped to its parent boundaries. One of the values *not* starting with ``OUT_`` (see picture below).
- **align_to** (*Optional*, list): Alignment of the of the widget relative to another widget on the same level:
    - **id** (**Required**): The ID of a widget *to* which you want to align.
    - **align** (**Required**, enum): Desired alignment (one of the values starting with ``OUT_``).
    - **x** (*Optional*, int16 or percentage): Horizontal offset position. Default ``0``.
    - **y** (*Optional*, int16 or percentage): Vertical offset position. Default ``0``.

.. figure:: /components/images/lvgl_align.png
    :align: center

- **group** (*Optional*, string): The name of the group of widgets which will interact with a  :doc:`/components/sensor/rotary_encoder`. In every group there is always one focused widget which receives the encoder actions. You need to associate an input device with a group. An input device can send key events to only one group but a group can receive data from more than one input device.
- **styles** (*Optional*, :ref:`config-id`): The ID of a *style definition* from the main component configuration to override the theme styles.
- **theme** (*Optional*, list): A list of styles to apply to the widget and children. Same configuration option as at the main component.
- **layout** (*Optional*, string): ``FLEX``, ``GRID`` or ``NONE``. See :ref:`layouts <lvgl-layouts>`.  If not specified, defaults to ``NONE``, which disables layouts each widget needing manual positioning.
- **flex_flow** (*Optional*, string): See :ref:`flex layout <lvgl-layouts-flex>` options. 
- **widgets** (*Optional*, list): A list of LVGL widgets to be drawn as children of this widget. Same configuration option as at the main component.

.. _lvgl-wgtprop-state:

- **state** (*Optional*, enum): Widgets or their (sub)parts can have have states, which support separate styling. These state styles inherit from theme, but can be locally overridden within style definitions or locally set. Can be one of:
    - **default** (*Optional*, boolean): Normal, released state.
    - **disabled** (*Optional*, boolean): Disabled state (also usable with :ref:`shorthand <lvgl-objupd-shorthands>` actions ``lvgl.widget.enable`` and ``lvgl.widget.disable``).
    - **pressed** (*Optional*, boolean): Being pressed.
    - **checked** (*Optional*, boolean): Toggled or checked state.
    - **scrolled** (*Optional*, boolean): Being scrolled.
    - **focused** (*Optional*, boolean): Focused via keypad or encoder or clicked via touch screen.
    - **focus_key** (*Optional*, boolean): Focused via keypad or encoder but *not* via touch screen.
    - **edited** (*Optional*, boolean): Edit by an encoder.
    - **user_1**, **user_2**, **user_3**, **user_4** (*Optional*, boolean): Custom states.

By default, states are all ``false``, and they are templatable.
To apply styles to the states, you need to specify them one level above, for example:

.. code-block:: yaml

    - btn:
        checkable: true
        state:
          checked: true # here you activate the state to be used at boot
        checked:
          bg_color: 0x00FF00 # here you apply styles to be used when in the respective state

The state itself can be can be changed by interacting with the widget, or through :ref:`actions <lvgl-objupd-act>` with ``lvgl.widget.update``.

See :ref:`lvgl-cook-cover` for a cookbook example how to play with styling and properties to show different states of a Home Assistant entity.

.. _lvgl-objupdflag-act:

In addition to visual styling, each widget supports some boolean **flags** to influence the behavior:

- **hidden** (*Optional*, boolean): make the widget hidden (like it wasn't there at all), also usable with :ref:`shorthand <lvgl-objupd-shorthands>` actions ``lvgl.widget.show`` and ``lvgl.widget.hide``. Defaults to ``false``.
- **checkable** (*Optional*, boolean): toggle checked state when the widget is clicked.
- **clickable** (*Optional*, boolean): make the widget clickable by input devices. Defaults to ``true``. If ``false``, it will pass the click to the widgets behind it (clicking through).
- **scrollable** (*Optional*, boolean): the widget can become scrollable. Defaults to ``true`` (also see the ``scrollbar_mode`` property).
- **scroll_elastic** (*Optional*, boolean): allow scrolling inside but with slower speed.
- **scroll_momentum** (*Optional*, boolean): make the widget scroll further when "thrown".
- **scroll_one** (*Optional*, boolean): allow scrolling only on ``snappable`` children.
- **scroll_chain_hor** (*Optional*, boolean): allow propagating the horizontal scroll to a parent.
- **scroll_chain_ver** (*Optional*, boolean): allow propagating the vertical scroll to a parent.
- **scroll_chain simple** (*Optional*, boolean): packaging for (``scroll_chain_hor | scroll_chain_ver``).
- **scroll_on_focus** (*Optional*, boolean): automatically scroll widget to make it visible when focused.
- **scroll_with_arrow** (*Optional*, boolean): allow scrolling the focused widget with arrow keys.
- **click_focusable** (*Optional*, boolean): add focused state to the widget when clicked.
- **snappable** (*Optional*, boolean): if scroll snap is enabled on the parent it can snap to this widget.
- **press_lock** (*Optional*, boolean): keep the widget pressed even if the press slid from the widget.
- **event_bubble** (*Optional*, boolean): propagate the events to the parent too.
- **gesture_bubble** (*Optional*, boolean): propagate the gestures to the parent.
- **adv_hittest** (*Optional*, boolean): allow performing more accurate hit (click) test. E.g. Accounting for rounded corners.
- **ignore_layout** (*Optional*, boolean): do not make the widget positionable by the layouts.
- **floating** (*Optional*, boolean): do not scroll the widget when the parent scrolls and ignore layout.
- **overflow_visible** (*Optional*, boolean): do not clip the children's content to the parent's boundary.
- **layout_1**, **layout_2** (*Optional*, boolean): custom flags, free to use by layouts.
- **widget_1**, **widget_2** (*Optional*, boolean): custom flags, free to use by widget.
- **user_1**, **user_2**, **user_3**, **user_4** (*Optional*, boolean): custom flags, free to use by user.

.. note::

    LVGL only supports only **integers** for numeric ``value``. Visualizer widgets can't display floats directly, but they allow scaling by 10s. Some examples in the :doc:`Cookbook </cookbook/lvgl>` cover how to do that.

.. _lvgl-wgt-lbl:

``label``
*********

A label is the basic widget type that is used to display text.

.. figure:: /components/images/lvgl_label.png
    :align: center

**Specific options:**

- **text** (**Required**, string): The text (or built-in :ref:`symbol <lvgl-fonts>` codepoint) to display. To display an empty label, specify ``""``.
- **text_align** (*Optional*, enum): Alignment of the text in the widget - it doesn't align the object itself, only the lines inside the object. One of ``LEFT``, ``CENTER``, ``RIGHT``, ``AUTO``. Inherited from parent. Defaults to ``AUTO``, which detects the text base direction and uses left or right alignment accordingly.
- **text_color** (*Optional*, :ref:`color <lvgl-color>`): Color to render the text in. Inherited from parent. Defaults to ``0`` (black). 
- **text_decor** (*Optional*, list): Choose decorations for the text: ``NONE``, ``UNDERLINE``, ``STRIKETHROUGH`` (multiple can be specified). Inherited from parent. Defaults to ``NONE``.
- **text_font**: (*Optional*, :ref:`font <lvgl-fonts>`):  The ID of the font used to render the text or symbol. Inherited from parent.
- **text_letter_space** (*Optional*, int16): Extra character spacing of the text. Inherited from parent. Defaults to ``0``.
- **text_line_space** (*Optional*, int16): Line spacing of the text. Inherited from parent. Defaults to ``0``.
- **text_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the text. Inherited from parent. Defaults to ``COVER``.
- **recolor** (*Optional*, boolean): Enable recoloring of button texts with ``#``. This makes it possible to set the color of characters in the text individually, just prefix the text to be re-colored with a ``#RRGGBB`` hexadecimal color code and a *space*, and close with a single hash ``#`` tag. For example: ``Write a #FF0000 red# word``. 
- **long_mode** (*Optional*, list): By default, the width and height of the label is set to ``size_content``. Therefore, the size of the label is automatically expanded to the text size. Otherwise, if the ``width`` or ``height`` are explicitly set (or by a ``layout``), the lines wider than the label's width can be manipulated according to the long mode policies below. These policies can be applied if the height of the text is greater than the height of the label.
    - ``WRAP``: Wrap too long lines. If the height is ``size_content`` the label's height will be expanded, otherwise the text will be clipped (Default). 
    - ``DOT``: Replaces the last 3 characters from bottom right corner of the label with dots.
    - ``SCROLL``: If the text is wider than the label scroll it horizontally back and forth. If it's higher, scroll vertically. Only one direction is scrolled and horizontal scrolling has higher precedence.
    - ``SCROLL_CIRCULAR``: If the text is wider than the label scroll it horizontally continuously. If it's higher, scroll vertically. Only one direction is scrolled and horizontal scrolling has higher precedence.
    - ``CLIP``: Simply clip the parts of the text outside the label.
- **scrollbar** (*Optional*, list): Settings for the indicator *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. The scroll bar that is shown when the text is larger than the widget's size.
- **selected** (*Optional*, list): Settings for the the style of the selected text. Only ``text_color`` and ``bg_color`` style properties can be used.
- Style options from :ref:`lvgl-styling`. Uses all the typical background properties and the text properties. The padding values can be used to add space between the text and the background.

.. note::

    Newline escape sequences are handled automatically by the label widget. You can use ``\n`` to make a line break. For example: ``"line1\nline2\n\nline4"``. For escape sequences like newline to be translated, *enclose the string in double quotes*.

**Specific actions:**

``lvgl.label.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags. 

- **text** (**Required**, :ref:`templatable <config-templatable>`, string): The ``text`` option in this action can contain static text, a :ref:`lambda <config-lambda>` outputting a string or can be formatted using ``printf``-style formatting (see :ref:`display-printf`).
    -  **format** (*Optional*, string): The format for the message in :ref:`printf-style <display-printf>`.
    -  **args** (*Optional*, list of :ref:`lambda <config-lambda>`): The optional arguments for the
       format message.

**Example:**

.. code-block:: yaml

    # Example widget:
    - label:
        align: CENTER
        id: lbl_id
        recolor: true
        text: "#FF0000 write# #00FF00 colored# #0000FF text#"

    - label:
        align: TOP_MID
        id: lbl_symbol
        text_font: montserrat_28
        text: "\uF013"

    # Example action (update label with a value from a sensor):
    on_...:
      then:
        - lvgl.label.update:
            id: lbl_id
            text:
              format: "%.0fdBm"
              args: [ 'id(wifi_signal_db).get_state()' ]

.. _lvgl-wgt-btn:

``btn``
*******

Simple push or toggle button. 

.. figure:: /components/images/lvgl_button.png
    :align: center

**Specific options:**

- **checkable** (*Optional*, boolean): A significant :ref:`flag <lvgl-objupdflag-act>` to make a toggle button (which remains pressed in ``checked`` state). Defaults to ``false``.
- Style options from :ref:`lvgl-styling` for the background of the button. Uses the typical background style properties.

A notable state is ``checked`` (boolean) which can have different styles applied.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated after clicking. If ``checkable`` is ``true``, the boolean variable ``x``, representing the checked state, may be used by lambdas within this trigger.

**Example:**

.. code-block:: yaml

    # Example widget:
    - btn:
        x: 10
        y: 10
        width: 50
        height: 30
        id: btn_id

To have a button with a text label on it, add a child :ref:`lvgl-wgt-lbl` widget to it:

.. code-block:: yaml

    # Example toggle button with text:
    - btn:
        x: 10
        y: 10
        width: 70
        height: 30
        id: btn_id
        checkable: true
        widgets:
          - label:
              align: center
              text: "Light"

    # Example trigger:
    - btn:
        ...
        on_value:
          then:
            - logger.log:
                format: "Button checked state: %d"
                args: [ x ]

The ``btn`` can be also integrated as a :doc:`/components/binary_sensor/lvgl` or as a :doc:`/components/switch/lvgl`.

See :ref:`lvgl-cook-binent` for an example illustrating how to use a checkable button to act on a Home Assistant service.

.. _lvgl-wgt-bmx:

``btnmatrix``
*************

The Button Matrix widget is a lightweight way to display multiple buttons in rows and columns. Lightweight because the buttons are not actually created but just virtually drawn on the fly. This way, one button use only eight extra bytes of memory instead of the ~100-150 bytes a normal Button widget plus the 100 or so bytes for the Label widget.

.. figure:: /components/images/lvgl_btnmatrix.png
    :align: center

**Specific options:**

- **rows** (**Required**, list): A list for the button rows:
    - **buttons** (**Required**, list): A list of buttons in a row:
        - **id** (*Optional*): An ID for the button in the matrix.
        - **text** (*Optional*): Text (or built-in :ref:`symbol <lvgl-fonts>` codepoint) to display on the button.
        - **key_code** (*Optional*, string): One character be sent as the key code to a :ref:`key_collector` instead of ``text`` when the button is pressed.
        - **width** (*Optional*): Width relative to the other buttons in the same row. A value between ``1`` and ``15`` range, default ``1`` (eg. in a line with two buttons: one ``width: 1`` and another one ``width: 2``, the first will be ``33%`` wide while the second will be ``66%`` wide). 
        - **selected** (*Optional*, boolean): Set the button as the most recently released or focused. Defaults to ``false``.
        - **control** (*Optional*): Binary flags to control behavior of the buttons (all ``false`` by default):
            - **hidden** (*Optional*, boolean): Make a button hidden (hidden buttons still take up space in the layout, they are just not visible or clickable).
            - **no_repeat** (*Optional*, boolean): Disable repeating when the button is long pressed.
            - **disabled** (*Optional*, boolean): Apply ``disabled`` styles to the button.
            - **checkable** (*Optional*, boolean): Enable toggling of a button, ``checked`` state will be added/removed as the button is clicked.
            - **checked** (*Optional*, boolean): Make the button checked. Apply ``checked`` styles to the button.
            - **click_trig** (*Optional*, boolean): Control how to :ref:`trigger <lvgl-event-trg>` ``on_value`` : if ``true`` on *click*, if ``false`` on *press*.
            - **popover** (*Optional*, boolean): Show the button label in a popover when pressing this button.
            - **recolor** (*Optional*, boolean): Enable recoloring of button texts with #. E.g. ``It's #ff0000 red#``
            - **custom_1** and **custom_2** (*Optional*, boolean): Custom, free to use flags.

- **items** (*Optional*, list): Settings for the items *part*, the buttons all use the text and typical background style properties except translations and transformations.
- **one_checked** (*Optional*, boolean): Allow only one button to be checked at a time (aka. radio buttons). Defaults to ``false``.
- Style options from :ref:`lvgl-styling` for the background of the button matrix, uses the typical background style properties. ``pad_row`` and ``pad_column`` set the space between the buttons.

**Specific actions:**

``lvgl.button.update`` :ref:`action <config-action>` updates the button styles and properties specified in the specific ``control``, ``width`` and ``selected`` options.

``lvgl.btnmatrix.update`` :ref:`action <config-action>` updates the items styles and properties specified in the specific ``state``, ``items`` options.

**Example:**

.. code-block:: yaml

    # Example widget:
    - btnmatrix:
        x: 10
        y: 40
        width: 220
        items:
          pressed:
            bg_color: 0xFFFF00
        id: b_matrix
        rows:
          - buttons:
            - id: button_1
              text: "\uF04B"
              control:
                checkable: true
            - id: button_2
              text: "\uF04C"
              control:
                checkable: true
          - buttons:
            - id: button_3
              text: "A"
              control:
                popover: true
            - id: button_4
              text: "B"
              control:
                disabled: true
          - buttons:
            - id: button_5
              text: "It's #ff0000 red#"
              width: 2
              control:
                recolor: true

    # Example action:
    on_...:
      then:
        - lvgl.button.update:
            id: button_1
            width: 1
            selected: true
            control:
              checkable: false
        - lvgl.btnmatrix.update:
            id: b_matrix
            state:
              disabled: true
            items:
              bg_color: 0xf0f0f0

.. tip::

    The Button Matrix widget supports the :ref:`key_collector` to collect the button presses as key press sequences for further automations. Check out  :ref:`lvgl-cook-keypad` for an example.

.. _lvgl-wgt-swi:

``switch``
**********

The Switch looks like a little slider and can be used to turn something on and off.

.. figure:: /components/images/lvgl_switch.png
    :align: center

**Specific options:**

- **knob** (*Optional*, list): Settings for the knob *part* to control the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize.
- **indicator** (*Optional*, list): Settings for the indicator *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize.
- Style options from :ref:`lvgl-styling`.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated when toggling the switch, the variable ``x`` returning a boolean representing the checked state.

**Example:**

.. code-block:: yaml

    # Example widget:
    - switch:
        x: 10
        y: 10
        id: switch_id

    # Example trigger:
    - switch:
        ...
        on_value:
          then:
            - logger.log:
                format: "Switch state: %d"
                args: [ x ]

The ``switch`` can be also integrated as a :doc:`/components/switch/lvgl`.

See :ref:`lvgl-cook-relay` for an example how to use a switch to act on a local component.

.. _lvgl-wgt-chk:

``checkbox``
************

The Checkbox widget is made internally from a *tick box* and a label. When the Checkbox is clicked the tick box's ``checked`` state will be toggled.

.. figure:: /components/images/lvgl_checkbox.png
    :align: center

**Specific options:**

- **indicator** (*Optional*, list): Settings for the indicator *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. The "tick box" is a square that uses all the typical background style properties. By default, its size is equal to the height of the main part's font. Padding properties make the tick box larger in the respective directions.
- Style options from :ref:`lvgl-styling` for the background of the widget and it uses the text and all the typical background style properties. ``pad_column`` adjusts the spacing between the tick box and the label.

**Specific actions:**

``lvgl.checkbox.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

- **text** (**Required**, :ref:`templatable <config-templatable>`, string): The ``text`` option in this action can contain static text, a :ref:`lambda <config-lambda>` outputting a string or can be formatted using ``printf``-style formatting (see :ref:`display-printf`).
    -  **format** (*Optional*, string): The format for the message in :ref:`printf-style <display-printf>`.
    -  **args** (*Optional*, list of :ref:`lambda <config-lambda>`): The optional arguments for the
       format message.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated when toggling the checkbox, the variable ``x`` returning a boolean representing the checked state.

**Example:**

.. code-block:: yaml

    # Example widget:
    - checkbox:
        x: 10
        y: 10
        id: checkbox_id
        text: Checkbox

    # Example action:
    on_...:
      then:
        - lvgl.checkbox.update:
            id: checkbox_id
            state:
              checked: true
            text: Checked

    # Example trigger:
    - checkbox:
        ...
        on_value:
          then:
            - logger.log:
                format: "Checkbox state: %d"
                args: [ x ]

The ``checkbox`` can be also integrated as a :doc:`/components/switch/lvgl`.

.. _lvgl-wgt-drp:

``dropdown``
************

The Dropdown widget allows the user to select one value from a list.

The dropdown list is closed by default and displays a single value. When activated (by clicking on the drop-down list), a list is drawn from which the user may select one option. When the user selects a new value, the list is deleted from the screen.

.. figure:: /components/images/lvgl_dropdown.png
    :align: center

The Dropdown widget is built internally from a *button* part and a *list* part (both not related to the actual widgets with the same name).

**Specific options:**

- **options** (**Required**, list): The list of available options in the drop-down.
- **dir** (*Optional*, enum): Where the list part of the dropdown gets created relative to the button part. ``LEFT``, ``RIGHT``, ``BOTTOM``, ``TOP``, defaults to ``BOTTOM``.
- **selected_index** (*Optional*, int8): The index of the item you wish to be selected. 
- **symbol** (*Optional*, enum): A symbol (typically an chevron) is shown in dropdown list. If ``dir`` of the drop-down list is ``LEFT`` the symbol will be shown on the left, otherwise on the right. Choose a different :ref:`symbol <lvgl-fonts>` from the built-in ones or from your own customized font.
- **indicator** (*Optional*, list): Settings for the the parent of ``symbol``. Supports a list of :ref:`styles <lvgl-styling>` to customize.
- **dropdown_list** (*Optional*, list): Settings for the dropdown_list *part*, the list with items. Supports a list of :ref:`styles <lvgl-styling>` to customize. Notable are ``text_line_space`` and ``pad_all`` for spacing of list items, and ``text_font`` to separately change the font in the list.
- **selected** (*Optional*, list): Settings for the selected item in the list. Supports a list of :ref:`styles <lvgl-styling>` to customize.
- **scrollbar** (*Optional*, list): Settings for the scrollbar *part*. Supports a list of :ref:`styles <lvgl-styling>` to customize. The scrollbar background, border, shadow properties and width (for its own width) and right padding for the spacing on the right.
- Style options from :ref:`lvgl-styling` for the background of the button and the list. Uses the typical background properties and :ref:`lvgl-wgt-lbl` text properties for the text on it. ``max_height`` can be used to limit the height of the list. ``text_font`` to set the font of the button part, including the symbol.

**Specific actions:**

``lvgl.dropdown.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated only when you select an item from the list. The new selected index is returned in the variable ``x``. The :ref:`universal <lvgl-event-trg>` LVGL event triggers also apply, and they also return the selected index in ``x``. 
``on_cancel`` :ref:`trigger <automation>` is also activated when you close the dropdown without selecting an item from the list. The currently selected index is returned in the variable ``x``.

**Example:**

.. code-block:: yaml

    # Example widget:
    - dropdown:
        id: dropdown_id
        width: 90
        align: CENTER
        options:
          - Violin
          - Piano
          - Bassoon
          - Chello
          - Drums
        selected_index: 2

    # Example action:
    on_...:
      then:
        - lvgl.dropdown.update:
            id: dropdown_id
            selected_index: 4

    # Example trigger:
    - dropdown:
        ...
        on_value:
          - logger.log:
              format: "Selected index is: %d"
              args: [ x ]
        on_cancel:
          - logger.log:
              format: "Dropdown closed. Selected index is: %d"
              args: [ x ]

The ``dropdown`` can be also integrated as :doc:`/components/select/lvgl`.

.. _lvgl-wgt-rol:

``roller``
**********

Roller allows you to simply select one option from a list by scrolling.

.. figure:: /components/images/lvgl_roller.png
    :align: center

**Specific options:**

- **options** (**Required**, list): The list of available options in the roller.
- **mode** (*Optional*, enum): Option to make the roller circular. ``NORMAL`` or ``INFINITE``, defaults to ``NORMAL``.
- **visible_row_count** (*Optional*, int8): The number of visible rows.
- **selected** (*Optional*, list): Settings for the selected *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. The selected option in the middle. Besides the typical background properties it uses the :ref:`lvgl-wgt-lbl` text style properties to change the appearance of the text in the selected area.
- **selected_index** (*Optional*, int8): The index of the item you wish to be selected. 
- **anim_time** (*Optional*, :ref:`Time <config-time>`): When the Roller is scrolled and doesn't stop exactly on an option it will scroll to the nearest valid option automatically in this amount of time.
- Style options from :ref:`lvgl-styling`. The background of the roller uses all the typical background properties and :ref:`lvgl-wgt-lbl` style properties. ``text_line_space`` adjusts the space between the options. 

**Specific actions:**

``lvgl.roller.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated when you select an item from the list. The new selected index is returned in the variable ``x``. The :ref:`universal <lvgl-event-trg>` LVGL event triggers also apply, and they also return the selected index in ``x``. 

**Example:**

.. code-block:: yaml

    # Example widget:
    - roller:
        align: CENTER
        id: roller_id
        options:
          - Violin
          - Piano
          - Bassoon
          - Chello
          - Drums

    # Example action:
    on_...:
      then:
        - lvgl.roller.update:
            id: roller_id
            selected_index: 4

    # Example trigger:
    - roller:
        ...
        on_value:
          - logger.log:
              format: "Selected index is: %d"
              args: [ x ]

The ``roller`` can be also integrated as :doc:`/components/select/lvgl`.

.. _lvgl-wgt-bar:

``bar``
*******

The bar widget has a background and an indicator on it. The size of the indicator is set according to the current ``value`` of the bar.

.. figure:: /components/images/lvgl_bar.png
    :align: center

Vertical bars can be created if the width is smaller than the height.

Not only the end, but also the start value of the bar can be set, which changes the start position of the indicator.

**Specific options:**

- **value** (**Required**, int8): Actual value of the indicator at start, in ``0``-``100`` range. Defaults to ``0``.
- **min_value** (*Optional*, int8): Minimum value of the indicator. Defaults to ``0``.
- **max_value** (*Optional*, int8): Maximum value of the indicator. Defaults to ``100``.
- **mode** (*Optional*, string): ``NORMAL``: the indicator is drawn from the minimum value to the current. ``REVERSE``: the indicator is drawn counter-clockwise from the maximum value to the current. ``SYMMETRICAL``: the indicator is drawn from the middle point to the current value. Defaults to ``NORMAL``.
- **indicator** (*Optional*, list): Settings for the indicator *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize, all the typical background properties.
- **animated** (*Optional*, boolean): To animate indicator when bar changes value. Defaults to ``true``.
- **anim_time** (*Optional*, :ref:`Time <config-time>`): Sets the animation time if the value is set with ``animated: true``.
- Style options from :ref:`lvgl-styling`. The background of the bar and it uses the typical background style properties. Adding padding will make the indicator smaller or larger.

**Specific actions:**

``lvgl.bar.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

**Example:**

.. code-block:: yaml

    # Example widget:
    - bar:
        x: 10
        y: 100
        id: bar_id
        value: 75
        min_value: 1
        max_value: 100

    # Example action:
    on_...:
      then:
        - lvgl.bar.update:
            id: bar_id
            value: 55

The ``bar`` can be also integrated as :doc:`/components/number/lvgl` or :doc:`/components/sensor/lvgl`.

.. _lvgl-wgt-sli:

``slider``
**********

The Slider widget looks like a bar supplemented with a knob. The knob can be dragged to set a value. Just like Bar, Slider can be vertical or horizontal.

.. figure:: /components/images/lvgl_slider.png
    :align: center

**Specific options:**

- **value** (**Required**, int8): Actual value of the indicator at start, in ``0``-``100`` range. Defaults to ``0``.
- **min_value** (*Optional*, int8): Minimum value of the indicator. Defaults to ``0``.
- **max_value** (*Optional*, int8): Maximum value of the indicator. Defaults to ``100``.
- **knob** (*Optional*, list): Settings for the knob *part* to control the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. A rectangle (or circle) drawn at the current value. Also uses all the typical background properties to describe the knob. By default, the knob is square (with an optional corner radius) with side length equal to the smaller side of the slider. The knob can be made larger with the padding values. Padding values can be asymmetric too.
- **indicator** (*Optional*, list): Settings for the indicator *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. The indicator that shows the current state of the slider. Also uses all the typical background style properties.
- **animated** (*Optional*, boolean): To animate indicator when bar changes value. Defaults to ``true``.
- **anim_time** (*Optional*, :ref:`Time <config-time>`): Sets the animation time if the value is set with ``animated: true``.
- any :ref:`Styling <lvgl-styling>` and state-based option for the background of the slider. Uses all the typical background style properties. Padding makes the indicator smaller in the respective direction.

Normally, the slider can be adjusted either by dragging the knob, or by clicking on the slider bar. In the latter case the knob moves to the point clicked and slider value changes accordingly. In some cases it is desirable to set the slider to react on dragging the knob only. This feature is enabled by enabling the ``adv_hittest`` flag.

**Specific actions:**

``lvgl.slider.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated when the knob changes the value of the arc. The new value is returned in the variable ``x``. The :ref:`universal <lvgl-event-trg>` LVGL event triggers also apply, and they also return the value in ``x``. 

**Example:**

.. code-block:: yaml

    # Example widget:
    - slider:
        x: 10
        y: 10
        width: 220
        id: slider_id
        value: 75
        min_value: 0
        max_value: 100

    # Example action:
    on_...:
      then:
        - lvgl.slider.update:
            id: slider_id
            knob:
              bg_color: 0x00FF00
            value: 55

    # Example trigger:
    - slider:
        ...
        on_value:
          - logger.log:
              format: "Slider value is: %.0f"
              args: [ 'x' ]

.. note::

    The ``on_value`` trigger is sent while the slider is being dragged or changed with keys. The event is sent *continuously* while the slider is being dragged, this can affect performance and have negative effects on the actions to be performed. In such cases use a :ref:`universal event trigger <lvgl-event-trg>` like ``on_release``, to get the ``x`` variable once after the interaction has completed.

The ``slider`` can be also integrated as :doc:`/components/number/lvgl` or :doc:`/components/sensor/lvgl`.

See :ref:`lvgl-cook-bright` and :ref:`lvgl-cook-volume` for examples how to use a slider to control entities in Home Assistant.

.. _lvgl-wgt-arc:

``arc``
*******

The Arc consists of a background and a foreground arc. The foreground (indicator) can be touch-adjusted with a knob.

.. figure:: /components/images/lvgl_arc.png
    :align: center

**Specific options:**

- **value** (**Required**, int8): Actual value of the indicator at start, in ``0``-``100`` range. Defaults to ``0``.
- **min_value** (*Optional*, int8): Minimum value of the indicator. Defaults to ``0``.
- **max_value** (*Optional*, int8): Maximum value of the indicator. Defaults to ``100``.
- **start_angle** (*Optional*, 0-360): start angle of the arc background (see note). Defaults to ``135``.
- **end_angle** (*Optional*, 0-360): end angle of the arc background (see note). Defaults to ``45``.
- **rotation** (*Optional*, int8): Offset to the 0 degree position. Defaults to ``0.0``.
- **adjustable** (*Optional*, boolean): Add a knob that the user can move to change the value. Defaults to ``false``.
- **mode** (*Optional*, string): ``NORMAL``: the indicator is drawn from the minimum value to the current. ``REVERSE``: the indicator is drawn counter-clockwise from the maximum value to the current. ``SYMMETRICAL``: the indicator is drawn from the middle point to the current value. Defaults to ``NORMAL``.
- **change_rate** (*Optional*, int8): If the arc is pressed the current value will set with a limited speed according to the set change rate. The change rate is defined in degree/second. Defaults to ``720``.
- **arc_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the arc.
- **arc_color** (*Optional*, :ref:`color <lvgl-color>`): Color used to draw the arc.
- **arc_rounded** (*Optional*, boolean): Make the end points of the arcs rounded. ``true`` rounded, ``false`` perpendicular line ending.
- **arc_width** (*Optional*, int16): Set the width of the arcs in pixels.
- **knob** (*Optional*, list): Settings for the knob *part* to control the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. Draws a handle on the end of the indicator using all background properties and padding values. With zero padding the knob size is the same as the indicator's width. Larger padding makes it larger, smaller padding makes it smaller.
- **indicator** (*Optional*, list): Settings for the indicator *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. Draws *another arc using the arc style* properties. Its padding values are interpreted relative to the background arc.
- any :ref:`Styling <lvgl-styling>` and state-based option to override styles inherited from parent. The arc's size and position will respect the padding style properties.

If the ``adv_hittest`` :ref:`flag <lvgl-objupdflag-act>` is enabled the arc can be clicked through in the middle. Clicks are recognized only on the ring of the background arc.

.. note::

    Zero degree is at the middle right (3 o'clock) of the widget and the degrees are increasing in a clockwise direction. The angles should be in the ``0``-``360`` range. 

**Specific actions:**

``lvgl.arc.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated when the knob changes the value of the arc. The new value is returned in the variable ``x``. The :ref:`universal <lvgl-event-trg>` LVGL event triggers also apply, and they also return the value in ``x``. 

**Example:**

.. code-block:: yaml

    # Example widget:
    - arc:
        x: 10
        y: 10
        id: arc_id
        value: 75
        min_value: 0
        max_value: 100
        adjustable: true

    # Example action:
    on_...:
      then:
        - lvgl.arc.update:
            id: arc_id
            knob:
              bg_color: 0x00FF00
            value: 55

    # Example trigger:
    - arc:
        ...
        on_value:
          - logger.log:
              format: "Arc value is: %.0f"
              args: [ 'x' ]

.. note::

    The ``on_value`` trigger is sent while the arc knob is being dragged or changed with keys. The event is sent *continuously* while the knob is being dragged, this can affect performance and have negative effects on the actions to be performed. In such cases use a :ref:`universal event trigger <lvgl-event-trg>` like ``on_release``, to get the ``x`` variable once after the interaction has completed.

The ``arc`` can be also integrated as :doc:`/components/number/lvgl` or :doc:`/components/sensor/lvgl`.

See :ref:`lvgl-cook-bright` and :ref:`lvgl-cook-volume` for examples how to use a slider (or an arc) to control entities in Home Assistant.

.. _lvgl-wgt-spb:

``spinbox``
***********

The Spinbox contains a numeric value (as text) which can be increased or decreased through actions. You can use for example buttons labeled with plus and minus to call them as required.

.. figure:: /components/images/lvgl_spinbox.png
    :align: center

**Specific options:**

- **value** (**Required**, float): Actual value to be shown by the spinbox at start. 
- **range_from** (*Optional*, float): The minimum value allowed to set the spinbox to. Defaults to ``0``.
- **range_to** (*Optional*, float): The maximum value allowed to set the spinbox to. Defaults to ``100``.
- **step** (*Optional*, float): The granularity with which the value can be set. Defaults to ``1.0``.
- **digits** (*Optional*, 1..10): The number of digits (excluding the decimal separator and the sign characters).  Defaults to ``4``.
- **decimal_places** (*Optional*, 0..6): The number of digits after the decimal point. If ``0``, no decimal point is displayed. Defaults to ``0``.
- **rollover** (*Optional*, boolean): While increasing or decreasing the value, if either the minimum or maximum value is reached with this option enabled, the value will change to the other limit. If disabled, the value will remain at the minimum or maximum value. Defaults to ``false``.
- **anim_time** (*Optional*, :ref:`Time <config-time>`): Sets the cursor's blink time.

.. note::

    The sign character will only be shown if the set range contains negatives.

**Specific actions:**

``lvgl.spinbox.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.
``lvgl.spinbox.decrement`` :ref:`action <config-action>` decreases the value by one ``step`` configured above.
``lvgl.spinbox.increment`` :ref:`action <config-action>` increases the value by one ``step`` configured above.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated when the knob changes the value of the arc. The new value is returned in the variable ``x``. The :ref:`universal <lvgl-event-trg>` LVGL event triggers also apply, and they also return the value in ``x``. 

**Example:**

.. code-block:: yaml

    # Example widget:
    - spinbox:
        id: spinbox_id
        text_align: center
        range_from: -10
        range_to: 40
        step: 0.5
        digits: 3
        decimal_places: 1

    # Example actions:
    on_...:
      then:
        - lvgl.spinbox.decrement: spinbox_id
    on_...:
      then:
        - lvgl.spinbox.update:
            id: spinbox_id
            value: 25.5

    # Example trigger:
    - spinbox:
        ...
        on_value:
          then:
            - logger.log:
                format: "Spinbox value is %f"
                args: [ x ]

The ``spinbox`` can be also integrated as :doc:`/components/number/lvgl` or :doc:`/components/sensor/lvgl`.

See :ref:`lvgl-cook-climate` for an example how to implement a thermostat control using the spinbox.

.. _lvgl-wgt-mtr:

``meter``
*********

The Meter widget can visualize data in very flexible ways. In can show arcs, needles, ticks lines and labels.

.. figure:: /components/images/lvgl_meter.png
    :align: center

**Specific options:**

- **scales** (**Required**, list): A list with (any number of) scales to be added to meter.  
    - **range_from** (**Required**): The minimum value of the tick scale. Defaults to ``0``.
    - **range_to** (**Required**): The maximum value of the tick scale. Defaults to ``100``.
    - **angle_range** (**Required**): The angle between start and end of the tick scale. Defaults to ``270``.
    - **rotation** (*Optional*): The rotation angle offset of the tick scale. 
    - **ticks** (**Required**, list): A scale can have minor and major ticks and labels on the major ticks. To add the minor ticks:
        - **count** (**Required**): How many ticks to be on the scale. Defaults to ``12``.
        - **width** (*Optional*): Tick line width in pixels. Required if ``count`` is greater than ``0``. Defaults to ``2``.
        - **length** (*Optional*): Tick line length in pixels. Required if ``count`` is greater than ``0``. Defaults to ``10``.
        - **color** (*Optional*, :ref:`color <lvgl-color>`): Color to draw the ticks. Required if ``count`` is greater than ``0``. Defaults to ``0x808080``.
        - **major** (*Optional*, list): If you want major ticks and value labels displayed:
            - **stride**: How many minor ticks to skip when adding major ticks. Defaults to ``3``.
            - **width**: Tick line width in pixels. Defaults to ``5``.
            - **length**: Tick line length in pixels or percentage. Defaults to ``15%``.
            - **color**: :ref:`Color <lvgl-color>` to draw the major ticks. Defaults to ``0`` (black).
            - **label_gap**: Label distance from the ticks with text proportionally to the values of the tick line. Defaults to ``4``.
        - Style options from :ref:`lvgl-styling` for the tick *lines* and *labels* using the :ref:`lvgl-wgt-lin` and :ref:`lvgl-wgt-lbl` text style properties.
    - **indicators** (**Required**, list): A list with indicators to be added to the scale. Multiple of each can be added. Their values are interpreted in the range of the scale:
        - **arc** (*Optional*): Add a background arc the scale: 
            - **start_value**: The value in the scale range to start drawing the arc from.
            - **end_value**: The value in the scale range to end drawing the arc to.
            - **width**: Arc width in pixels. Defaults to ``4``.
            - **color**: :ref:`Color <lvgl-color>` to draw the arc. Defaults to ``0`` (black).
            - **r_mod**: Adjust the position of the arc from the scale radius with this amount (can be negative). Defaults to ``0``.
            - Style options for the *arc* using the :ref:`lvgl-wgt-arc` style properties.
        - **tick_style** (**Optional**): Add tick style modifications:
            - **start_value**: The value in the scale range to modify the ticks from.
            - **end_value**: The value in the scale range to modify the ticks to.
            - **color_start**: :ref:`Color <lvgl-color>` for the gradient start of the ticks.
            - **color_end**: :ref:`Color <lvgl-color>` for the gradient end of the ticks.
            - **local**: If ``true`` the ticks' color will be faded from ``color_start`` to ``color_end`` in the start and end values specified above. If ``false``, ``color_start`` and ``color_end`` will be mapped to the entire scale range (and only a *slice* of that color gradient will be visible in the indicator's start and end value range). Defaults to ``false``.
            - **width**: Modifies the ``width`` of the tick lines.
        - **line** (*Optional*): Add a needle line to the scale. By default, the length of the line is the same as the scale's radius:
            - **id**: Manually specify the :ref:`config-id` used for updating the indicator value at runtime.
            - **width**: Needle line width in pixels. Defaults to ``4``.
            - **color**: :ref:`Color <lvgl-color>` for the needle line. Defaults to ``0`` (black).
            - **r_mod**: Adjust the length of the needle from the scale radius with this amount (can be negative). Defaults to ``0``.
            - **value**: The value in the scale range to show at start.
            - Style options for the *needle line* using the :ref:`lvgl-wgt-lin` style properties, as well as the background properties from :ref:`lvgl-styling` to draw a square (or circle) on the pivot of the needles. Padding makes the square larger.
        - **img** (*Optional*): Add a rotating needle image to the scale:
            - **id**: Manually specify the :ref:`config-id` used for updating the indicator value at runtime.
            - **src**:  The ID of an existing image configuration, representing a needle pointing to the right like ``-o--->``. 
            - **pivot_x**: Horizontal position of the pivot point of rotation relative to the top left corner of the image. Defaults to ``50%`` (center of image).
            - **pivot_y**: Vertical position of the pivot point of rotation relative to the top left corner of the image.. Defaults to ``50%`` (center of image).
            - **value**: The value in the scale range to show at start.
- Style options from :ref:`lvgl-styling` for the background of the meter, using the typical background properties.

.. note::

    Zero degree is at the middle right (3 o'clock) of the widget and the degrees are increasing in a clockwise direction. The angles should be in the ``0``-``360`` range. 

**Specific actions:**

``lvgl.indicator.update`` :ref:`action <config-action>` updates indicator options, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags. ``src`` cannot be updated at runtime.

**Example:**

.. code-block:: yaml

    # Example widget:
    - meter:
        align: center
        scales:
          range_from: -10
          range_to: 40
          angle_range: 240
          rotation: 150
          ticks:
            count: 51
            length: 3
            major:
              stride: 5
              length: 13
              label_gap: 13
          indicators:
            - line:
                id: temperature_needle
                width: 2
                color: 0xFF0000
                r_mod: -4
            - tick_style:
                start_value: -10
                end_value: 40
                color_start: 0x0000bd #FF0000
                color_end: 0xbd0000 #0000FF

    # Example action:
    on_...:
      then:
        - lvgl.indicator.update:
            id: temperature_needle
            value: 3

See :ref:`lvgl-cook-gauge`, :ref:`lvgl-cook-thermometer` and :ref:`lvgl-cook-clock` in the Cookbook for examples how to effectively use this widget.

.. _lvgl-wgt-img:

``img``
*******

Images are the basic widgets to display images. 

.. figure:: /components/images/lvgl_image.png
    :align: center

**Specific options:**

- **src** (**Required**, :ref:`image <display-image>`):  The ID of an existing image configuration.
- Some style options from :ref:`lvgl-styling` for the background rectangle that uses the typical background style properties and the image itself using the image style properties.

**Specific actions:**

``lvgl.img.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags. Updating the ``src`` option changes the image at runtime.

**Example:**

.. code-block:: yaml

    # Example widget:
    - img:
        align: CENTER
        src: cat_image
        id: img_id
        radius: 11
        clip_corner: true

    # Example action:
    on_...:
      then:
        - lvgl.img.update:
            id: img_id
            src: cat_image_bowtie

.. _lvgl-wgt-aim:

``animimg``
***********

The animation image is similar to the normal ``img`` widget. The main difference is that instead of one source image, you set a list of multiple source images. You can also specify a duration and a repeat count.

.. figure:: /components/images/lvgl_animimg.gif
    :align: center

**Specific options:**

- **src** (**Required**, list of :ref:`images <display-image>`): A list of IDs of existing image configurations to be loaded as frames of the animation.
- **auto_start** (*Optional*, boolean): Start the animation playback automatically at boot and when updating the widget. Defaults to ``true``.
- **duration** (**Required**, :ref:`Time <config-time>`): Total duration of a playback cycle (frames are displayed equally in time).
- **repeat_count** (*Optional*, int16 or *forever*): How many times to repeat the playback. Defaults to ``forever``.
- Some style options from :ref:`lvgl-styling` for the background rectangle that uses the typical background style properties and the image itself using the image style properties.

**Specific actions:**

``lvgl.animimg.start`` :ref:`action <config-action>` starts the animation playback if it was displayed with ``auto_start`` false or after ``repeat_count`` expired.
``lvgl.animimg.stop`` :ref:`action <config-action>` stops the animation playback.
``lvgl.animimg.update`` :ref:`action <config-action>` can be used to change ``repeat_count`` and ``duration``, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags. ``src`` and ``auto_start`` cannot be updated at runtime.

**Example:**

.. code-block:: yaml

    # Example widget:
    - animimg:
        align: CENTER
        id: anim_id
        src: [ cat_image, cat_image_bowtie ]
        duration: 1000ms

    # Example actions:
    on_...:
      then:
        - lvgl.animimg.update:
            id: anim_id
            repeat_count: 100
            duration: 300ms

See :ref:`lvgl-cook-animbatt` in the Cookbook for a more detailed example.

.. _lvgl-wgt-lin:

``line``
********

The Line widget is capable of drawing straight lines between a set of points.

.. figure:: /components/images/lvgl_line.png
    :align: center

**Specific options:**

- **points** (**Required**, list): A list of ``x, y`` integer pairs for point coordinates (origin from top left of parent)
- **line_width** (*Optional*, int16): Set the width of the line in pixels.
- **line_dash_width** (*Optional*, int16): Set the width of the dashes in the line (in pixels).
- **line_dash_gap** (*Optional*, int16): Set the width of the gap between the dashes in the line (in pixels).
- **line_rounded** (*Optional*, boolean): Make the end points of the line rounded. ``true`` rounded, ``false`` perpendicular line ending.
- **line_color** (*Optional*, :ref:`color <lvgl-color>`): Color for the line.
- Style options from :ref:`lvgl-styling`, all the typical background properties and line style properties.

By default, the Line widget width and height dimensions are set to ``size_content``. This means it will automatically set its size to fit all the points. If the size is set explicitly, parts of the line may not be visible.

**Example:**

.. code-block:: yaml

    # Example widget:
    - line:
        points:
          - 5, 5
          - 70, 70
          - 120, 10
          - 180, 60
          - 230, 15
        line_width: 8
        line_color: 0x0000FF
        line_rounded: true

.. _lvgl-wgt-led:

``led``
********

The Led widgets are rectangle-like (or circle) widget whose brightness can be adjusted. With lower brightness the colors become darker.

.. figure:: /components/images/lvgl_led.png
    :align: center

**Specific options:**

- **color** (*Optional*, :ref:`color <lvgl-color>`): Color for the background, border, and shadow of the widget.
- **brightness** (*Optional*, percentage): The brightness of the LED color, where ``0%`` corresponds to black, and ``100%`` corresponds to the full brightness of the color specified above.
- Style options from :ref:`lvgl-styling`, using all the typical background style properties.

**Specific actions:**

``lvgl.led.update`` :ref:`action <config-action>` updates the widget styles and properties from the specific options above, just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

**Example:**

.. code-block:: yaml

    # Example widget:
    - led:
        id: led_id
        align: CENTER
        color: 0xFF0000
        brightness: 70%

    # Example action:
    on_...:
      then:
        - lvgl.led.update:
            id: led_id
            color: 0x00FF00

The ``led`` can be also integrated as :doc:`/components/light/lvgl`.

.. note::

    If configured as a light component, ``color`` and ``brightness`` are overridden by the light at startup, according to its ``restore_mode`` setting.

Check out :ref:`lvgl-cook-keypad` in the Cookbook for an example how to change the led styling properties from an automation.

.. _lvgl-wgt-txt:

``textarea``
************

The Textarea is a widget allowing to input text and displays a cursor. Long lines are wrapped and when the text becomes long enough the Text area can be scrolled. It supports one line mode and password mode, where typed characters are replaced visually with bullets or asterisks.

.. figure:: /components/images/lvgl_textarea.png
    :align: center

**Specific options:**

- **placeholder_text** (*Optional*, string): A placeholder text can be specified, which is displayed when the Text area is empty.
- **accepted_chars** (*Optional*, string): You can set a list of accepted characters, so other characters will be ignored.
- **one_line** (*Optional*, boolean): The Text area can be configured to be on a single line when the height is set automatically to show only one line, line break characters are ignored, and word wrap is disabled.
- **password_mode** (*Optional*, boolean): The text area supports password mode. By default, if the ``•`` (bullet, ``0x2022``) glyph exists in the font, the entered characters are converted to it after some time or when a new character is entered. If ``•`` is missing from the font, ``*`` (asterisk) will be used. 
- **max_length** (*Optional*, int): Limit the maximum number of characters to this value.
- any :ref:`Styling <lvgl-styling>` and state-based option for the background of the textarea. Uses all the typical background style properties and the text/label related style properties for the text.

**Specific actions:**

``lvgl.textarea.update`` :ref:`action <config-action>` updates the widget's ``text`` property, to replace the entire text content.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated on every keystroke, the variable ``text`` containing the entire contents of the textarea.
``on_ready`` :ref:`trigger <automation>` is activated in case of ``one_line`` configured as ``true``, when the New Line character is receicved (Enter key on the keyboard).

**Example:**

.. code-block:: yaml

    # Example widget:
    - textarea:
        id: textarea_id
        one_line: true
        placeholder_text: "Enter text here"

    # Example action:
    on_...:
      then:
        - lvgl.textarea.update:
            id: textarea_id
            text: "Hello World!"

    # Example trigger:
    - textarea:
        ...
        on_value:
          then:
            - logger.log:
                format: "Textarea changed to: %s"
                args: [ text ]
        on_ready:
          then:
            - logger.log:
                format: "Textarea ready: %s"
                args: [ text ]

The ``textarea`` can be also integrated as :doc:`/components/text/lvgl` or :doc:`/components/text_sensor/lvgl`.

.. _lvgl-wgt-spi:

``spinner``
***********

The Spinner widget is a spinning arc over a ring.

.. figure:: /components/images/lvgl_spinner.gif
    :align: center

**Specific options:**

- **spin_time** (**Required**, :ref:`Time <config-time>`): Duration of one cycle of the spin.
- **arc_length** (**Required**, 0-360): Length of the spinning arc in degrees.
- **arc_opa** (*Optional*, :ref:`opacity <lvgl-opa>`): Opacity of the arc.
- **arc_color** (*Optional*, :ref:`color <lvgl-color>`): Color to draw the arcs.
- **arc_rounded** (*Optional*, boolean): Make the end points of the arcs rounded. ``true`` rounded, ``false`` perpendicular line ending.
- **arc_width** (*Optional*, int16): Set the width of the arcs in pixels.
- **indicator** (*Optional*, list): Settings for the indicator *part* to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize. Draws *another arc using the arc style* properties. Its padding values are interpreted relative to the background arc.

**Specific actions:**

``lvgl.spinner.update`` :ref:`action <config-action>` updates the widget styles and properties for the *indicator* part (anything other than the properties that apply commonly to all widgets), just like :ref:`lvgl.widget.update <lvgl-objupd-act>` action is used for the common styles, states or flags.

**Example:**

.. code-block:: yaml

    # Example widget:
    - spinner:
        align: center
        spin_time: 2s
        arc_length: 60deg
        id: spinner_id
        indicator:
          arc_color: 0xd4d4d4

    # Example action:
    on_...:
      then:
        - lvgl.spinner.update:
            id: spinner_id
            arc_color: 0x31de70

.. _lvgl-wgt-obj:

``obj``
*******

The Base Object is just a simple, empty widget. By default, it's nothing more than a rounded rectangle:

.. figure:: /components/images/lvgl_baseobj.png
    :align: center

You can use it as a parent container for other widgets. By default, it catches touches.

**Specific options:**

- Style options from :ref:`lvgl-styling`.

**Example:**

.. code-block:: yaml

    # Example widget:
    - obj:
        x: 10
        y: 10
        width: 220
        height: 300
        widgets:
          - ...

.. _lvgl-wgt-tiv:

``tileview``
************

The tileview is a container object whose elements, called tiles, can be arranged in grid form. A user can navigate between the tiles by dragging or swiping. Any direction can be disabled on the tiles individually to not allow moving from one tile to another.

If the Tile view is screen sized, the user interface resembles what you may have seen on smartwatches.

A typical application would probably use an ``obj`` container widget as a tile, to display multiple child widgets, but any widget can be used directly too.

**Specific options:**

- **tiles** (**Required**, list): A list with (any number of) tiles to be added to meter.  
    - *widget* (**Required**): Any kind of widget to be used as tile container.
        - **tile_id** (**Required**): A tile ID to be used with ``lvgl.tileview.select`` action.
        - **dir** (*Optional*): Enable moving to the adjacent tiles into the given direction by swiping/dragging. One or multiple of ``LEFT``, ``RIGHT``, ``TOP``, ``BOTTOM``, ``HOR``, ``VER``, ``ALL``. Defaults to ``ALL``.
        - **row** (**Required**): Horizontal position of the tile in the tileview grid.
        - **column** (**Required**): Vertical position of the tile in the tileview grid.
        - Style options from the widget used as container.

**Specific actions:**

``lvgl.tileview.select`` :ref:`action <config-action>` jumps the ``tileview`` to the desired tile:
 
- **id** (**Required**): The ID of the ``tileview`` which receives this action
- **tile_id** (*Optional*): The ID of the tile from within it, to which to jump. Required if not specifying ``row`` and ``column``.
- **row** (*Optional*): Horizontal position of the tile to which to jump. Required if not specifying ``tile_id``.
- **column** (*Optional*): Vertical position of the tile to which to jump. Required if not specifying ``tile_id``.
- **animated** (*Optional*, boolean): To animate the movement. Defaults to ``false``.

**Specific triggers:**

``on_value`` :ref:`trigger <automation>` is activated when displayed tile changes. The new value is returned in the variable ``tile``, as the ID of the newly visible tile. 

**Example:**

.. code-block:: yaml

    # Example widget:
    - tileview:
        id: tiv_id
        tiles:
          - obj:
              row: 0
              column: 0
              tile_id: cat_tile
              dir: VER
              widgets:
                - img:
                    src: cat_image
                - ...
          - ...

    # Example action:
    on_...:
      then:
        - lvgl.tileview.select:
            id: tiv_id
            row: 0
            column: 0
            animated: true

    # Example trigger:
    - tileview:
        ...
        on_value:
          - if:
              condition:
                lambda: return tile == id(cat_tile);
              then:
                - logger.log: "Cat tile is now showing"

.. _lvgl-wgt-msg:

``msgboxes``
************

The Message boxes act as pop-ups. They are built from a background container, a title, an optional close button, a text and optional buttons.

.. figure:: /components/images/lvgl_msgbox.png
    :align: center

The text will be broken into multiple lines automatically and the height will be set automatically to include the text and the buttons. The message box is modal (blocks clicks on the rest of the screen until closed).

**Specific options:**

- **msgboxes** (*Optional*, enum): A list of message boxes to use. This option has to be added to the top level of the LVGL component configuration.
    - **close_button** (**Required**, boolean): Controls the appearance of the close button to the top right of the message box. 
    - **title** (**Required**, string): A string to display at the top of the message box.
    - **body** (**Required**, enum): The content of body of the message box:
        - **text** (**Required**, string):  The string to be displayed in the body of the message box. Can be shorthanded if no further options are specified.
        - Style options from :ref:`lvgl-styling`. Uses all the typical background properties and the text properties.
    - **buttons** (**Required**, enum): A list of buttons to show at the bottom of the message box:
        - **text** (**Required**, string):  The text (or built-in :ref:`symbol <lvgl-fonts>` codepoint) to display on the button.

**Specific actions:**

The configured message boxes are hidden by default. One can show them with ``lvgl.widget.show`` and ``lvgl.widget.hide`` :ref:`actions <lvgl-objupd-shorthands>`.

**Example:**

.. code-block:: yaml

    # Example widget:
    lvgl:
      ...
      msgboxes:
        - id: message_box
          close_button: true
          title: Message box
          body:
            text: "This is a sample message box."
            bg_color: 0x808080
          buttons:
            - id: msgbox_apply
              text: "Apply"
            - id: msgbox_close
              text: "\uF00D"
              on_click:
                then:
                  - lvgl.widget.hide: message_box

.. tip::

    You can create your own more complex dialogs with a full-screen sized, half-opaque ``obj`` with any child widgets on it, and the ``hidden`` flag set to ``true`` by default. For non-modal dialogs, simply set the ``clickable`` flag to ``false`` on it.

Actions
-------

Specific actions are available for certain widgets, they are described above in their respective section. Some universal actions are available for all the widgets or for LVGL itself:

.. _lvgl-objupd-act:

``lvgl.widget.update``
**********************

This powerful :ref:`action <config-action>` allows changing on the fly any common :ref:`style property <lvgl-styling>`, state (templatable) or :ref:`flag <lvgl-objupdflag-act>` of any widget.

.. code-block:: yaml

    # Example for updating styles (in states):
    on_...:
      then:
        - lvgl.widget.update:
            id: my_button_id
            bg_color: 0xFF0000
            state:
              disabled: true
 
    # Example for updating flag:
    on_...:
      then:
        - lvgl.widget.update:
            id: my_label_id
            hidden: true

Check out in the Cookbook :ref:`lvgl-cook-binent` for an example how to use a template to update the state.

.. _lvgl-objupd-shorthands:

``lvgl.widget.hide``, ``lvgl.widget.show``
******************************************

These :ref:`actions <config-action>` are shorthands for toggling the ``hidden`` :ref:`flag <lvgl-objupdflag-act>` of any widget:

.. code-block:: yaml

    on_...:
      then:
        - lvgl.widget.hide: my_label_id
        - delay: 0.5s
        - lvgl.widget.show: my_label_id

``lvgl.widget.disable``, ``lvgl.widget.enable``
***********************************************

These :ref:`actions <config-action>` are shorthands for toggling the ``disabled`` state of any widget (which controls the appearance of the corresponding *disabled* style set of the theme):

.. code-block:: yaml

    - on_...:
        then:
          - lvgl.widget.disable: my_button_id
    - on_...:
        then:
          - lvgl.widget.enable: my_button_id

.. _lvgl-rfrsh-act:

``lvgl.widget.redraw``
**********************

This :ref:`action <config-action>` redraws the entire screen, or optionally only a widget on it.

- **id** (*Optional*): The ID of a widget configured in LVGL, which you want to redraw. Entire screen if omitted.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.widget.redraw:

.. _lvgl-pause-act:

``lvgl.pause``
**************

This :ref:`action <config-action>` pauses the activity of LVGL, including rendering.

- **show_snow** (*Optional*, boolean): During paused, display random colored pixels across the entire screen in order to minimize screen burn-in, to relief the tension put on each individual pixel. See :ref:`lvgl-cook-antiburn` for an example how to use this.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.pause:
            show_snow: true

.. _lvgl-resume-act:

``lvgl.resume``
***************

This :ref:`action <config-action>` resumes the activity of LVGL, including rendering.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.resume:

``lvgl.update``
***************

This :ref:`action <config-action>` allows changing on the fly the ``disp_bg_color`` or ``disp_bg_image`` configuration options of the main component, making it possible to use change the background color or wallpaper at any time.

.. code-block:: yaml

    # Examples:
    on_...:
      then:
        - lvgl.update:
            disp_bg_color: 0x0000FF
        - lvgl.update:
            disp_bg_image: cat_image

.. _lvgl-pgnx-act:

``lvgl.page.next``, ``lvgl.page.previous``
******************************************

This :ref:`action <config-action>` changes page to the next following in the configuration (except the ones with ``skip`` option enabled), wraps around at the end.

- **animation** (*Optional*): The page change with one of these animations: ``NONE``, ``OVER_LEFT``, ``OVER_RIGHT``, ``OVER_TOP``, ``OVER_BOTTOM``, ``MOVE_LEFT``, ``MOVE_RIGHT``, ``MOVE_TOP``, ``MOVE_BOTTOM``, ``FADE_IN``, ``FADE_OUT``, ``OUT_LEFT``, ``OUT_RIGHT``, ``OUT_TOP``, ``OUT_BOTTOM``. Defaults to ``NONE`` if not specified.
- **time** (*Optional*, :ref:`Time <config-time>`): Duration of the page change animation. Defaults to ``50ms``.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.page.next:
            animation: OUT_LEFT
            time: 300ms

    on_...:
      then:
        - lvgl.page.previous:
            animation: OUT_RIGHT
            time: 300ms

.. _lvgl-pgsh-act:

``lvgl.page.show``
******************

This :ref:`action <config-action>` shows a specific page (even the ones with ``skip`` option enabled).

- **id** (**Required**): The ID of the page to be shown.
- **animation** (*Optional*): The page change with one of these animations: ``NONE``, ``OVER_LEFT``, ``OVER_RIGHT``, ``OVER_TOP``, ``OVER_BOTTOM``, ``MOVE_LEFT``, ``MOVE_RIGHT``, ``MOVE_TOP``, ``MOVE_BOTTOM``, ``FADE_IN``, ``FADE_OUT``, ``OUT_LEFT``, ``OUT_RIGHT``, ``OUT_TOP``, ``OUT_BOTTOM``. Defaults to ``NONE`` if not specified.
- **time** (*Optional*, :ref:`Time <config-time>`): Duration of the page change animation. Defaults to ``50ms``.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.page.show:
            id: secret_page

    on_...:
      then:
        - lvgl.page.show: secret_page  # shorthand version

Conditions
----------

.. _lvgl-idle-cond:

``lvgl.is_idle``
****************

This :ref:`condition <config-condition>` checks if since the last touch event, the amount of time specified here has passed or not.

- **timeout** (**Required**, :ref:`templatable <config-templatable>`, int): :ref:`Time <config-time>` to check against the time that has elapsed since the last touch event.

.. code-block:: yaml

    # In some trigger:
    on_...:
      then:
        - if:
            condition: lvgl.is_idle
              timeout: 5s
            then:
              - light.turn_off:
                  id: display_backlight
                  transition_length: 3s

.. _lvgl-paused-cond:

``lvgl.is_paused``
******************

This :ref:`condition <config-condition>` checks if LVGL is in paused state or not.

.. code-block:: yaml

    # In some trigger:
    on_...:
      then:
        - if:
            condition: lvgl.is_paused
            then:
              - lvgl.resume:

Triggers
--------

Specific triggers like ``on_value`` are available for certain widgets, they are described above in their respective section. Some universal triggers are available for all the widgets or for LVGL itself:

.. _lvgl-event-trg:

Interaction Events
******************

ESPHome implements as universal triggers the following interaction events generated by LVGL:

- ``on_press``: The widget has been pressed.
- ``on_long_press``: The widget has been pressed for at least the ``long_press_time`` specified in the input device configuration. Not called if scrolled.
- ``on_long_press_repeat``: Called after ``long_press_time`` in every ``long_press_repeat_time`` ms. Not called if scrolled.
- ``on_short_click``: The widget was pressed for a short period of time, then released. Not called if scrolled or long pressed.
- ``on_click``: Called on release if a widget did not scroll (regardless of long press).
- ``on_release``: Called in every case when a widget has been released.
- ``on_scroll_begin``: Scrolling of the widget begins.
- ``on_scroll_end``:  Scrolling of the widget ends.
- ``on_scroll``: The widget was scrolled.
- ``on_focus``:  The widget is focused.
- ``on_defocus``: The widget is unfocused.

These triggers can be applied directly to any widget in the lvgl configuration, given that the widget itself supports generating such events. For the widgets having a value, the triggers return the current value in variable ``x``.

.. code-block:: yaml

    # Example triggers:
    - btn:
        ...
        on_short_click:
          then:
            lvgl.page.show: main_page
        on_long_press:
          then:
            light.toggle: display_backlight

    - slider:
        ...
        on_release:
          then:
            - light.turn_on:
                id: display_backlight
                transition_length: 0ms
                brightness: !lambda return x / 100;

.. _lvgl-onidle-trg:

``lvgl.on_idle``
****************

LVGL has a notion of screen inactivity, i.e. how long did the user not interact with the screen. This can be use to dim the display backlight or turn it off after a moment of inactivity (like a screen saver). Every use of an input device (touchscreen, rotary encoder) counts as an activity and resets the inactivity counter. 

The ``on_idle`` :ref:`triggers <automation>` are activated when inactivity time becomes longer than the specified ``timeout``. You can configure any desired number of timeouts with different actions.

- **timeout** (**Required**, :ref:`templatable <config-templatable>`, int): :ref:`Time <config-time>` that has elapsed since the last touch event, after which you want your actions to be performed.

.. code-block:: yaml

    lvgl:
      ...
      on_idle:
        - timeout: 30s
          then:
            - lvgl.page.show: main_page
        - timeout: 60s
          then:
            - light.turn_off: display_backlight
            - lvgl.pause:

See :ref:`lvgl-cook-idlescreen` example how to implement screen saving with idle settings.

.. _lvgl-seealso:

See Also
--------

- :doc:`Examples in the Cookbook </cookbook/lvgl>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/number/lvgl` or :doc:`/components/sensor/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/display/index`
- :doc:`/components/touchscreen/index`
- :doc:`/components/sensor/rotary_encoder`
- `LVGL docs <https://docs.lvgl.io/>`__
- :ghedit:`Edit`
