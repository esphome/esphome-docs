.. _lvgl-main:

LVGL
====

.. seo::
    :description: LVGL - ESPHome Displays showing contents created with Light and Versatile Graphics Library


`LVGL <https://lvgl.io/>`__ (Light and Versatile Graphics Library) is a free and open-source 
embedded graphics library to create beautiful UIs for any MCU, MPU and display type. ESPHome supports
`LVGL version 8.3.9 <https://docs.lvgl.io/8.3/>`__.

.. figure:: /images/logo_lvgl.png
    :align: center

In order to be able to drive a display with LVGL under ESPHome you need an MCU from the ESP32 family. Although
PSRAM is not a strict requirement, it is recommended.

For interactivity, a capacitive touchscreen is highly prefered because it is more responsive over resistive touchscreens.

Basics
------

In LVGL, graphical elements like Buttons, Labels, Sliders etc. are called objects or widgets. See :ref:`lvgl-widgets` to see the full
list of available widgets in ESPHome.

Every object has a parent object where it is created. For example, if a label is created on a button, the button is the parent of label.
The child object moves with the parent and if the parent is deleted the children will be deleted too. Children can be visible only within
their parent's bounding area. In other words, the parts of the children outside the parent are clipped. A Screen is the "root" parent.
You can have any number of screens.


Component
---------

.. code-block:: yaml

    # Example configuration entry
    lvgl:
      log_level: WARN
      color_depth: 16
      bg_color: 0x000000
      text_font: unscii_8
      touchscreens: my_toucher
      style_definitions:
        - id: style_line
          line_color: color_blue
          line_width: 8
          line_rounded: true
        - id: date_style
          text_font: unscii_8
          align: center
          text_color: 0xFFFFFF
          bg_opa: cover
          radius: 4
          pad_all: 2
      layout: grid
      width: 100%
      widgets:
        - btn:
            id: lv_button0
            x: 5
            y: 30
            widgets:
              - img:
                  src: my_image0
                  width: 96
                  height: 96


Configuration variables:

- **display_id** (*Optional*, :ref:`config-id`): The ID of a display configuration where to render this entire LVGL configuration. If there's only one display configured, this item can be omitted.
- **touchscreens** (*Optional*, list): IDs of touchscreens interacting with the LVGL widgets on the display.
- **rotary_encoders** (*Optional*, list): IDs of rotary encoders interacting with the LVGL widgets on the display.
- **color_depth** (*Optional*, int8): The color deph at which the contents are generated. Valid values are ``1`` (monochrome), ``8``, ``16`` or ``32``, defaults to ``8``.
- **log_level** (*Optional*): Set the :ref:`logger <logger>` level specifically for the messages of the LVGL component. Defaults to ``WARN``.
- **byte_order**: The byte order of the data outputted by lvgl, ``big_endian`` or ``little_endian``. If not specified, will default to ``big_endian``.
- ... (select the default styles from :ref:`Styling <lvgl-styling>`)
- **style_definitions** (*Optional*, list): A list of style definitions to use with LVGL widgets:
    - **id** (*Optional*, :ref:`config-id`): Set the ID of this style definition.
    - ... (select your styles from :ref:`Styling <lvgl-styling>`)
- **theme** ???
- **widgets** (*Optional*, list): A list of LVGL widgets to be drawn on the screen.
    - :ref:`Widgets <lvgl-widgets>` (**Required**): ``btn``, ``img``, ???
    - ... (select your styles from :ref:`Styling <lvgl-styling>`)
    - **widgets** (*Optional*, list): A list of child LVGL widgets to be drawn as children of this widget. Configuration options are is the same as the parent widgets, and values aren inherited.
        - **id** (*Optional*, :ref:`config-id`): Set the ID of this widget.
        - ... (select your styles from :ref:`Styling <lvgl-styling>`)
- **on_idle**: (*Optional*, :ref:`Action <config-action>`): An automation to perform when the display enters *idle* state.

.. note::

    By default, LVGL draws new widgets on top of old widgets, including their children. If widgets are children of other widgets (they have the parentid property set), property inheritance takes place. Some properties (typically that are related to text and opacity) can be inherited from the parent widgets's styles. Inheritance is applied only at first draw. In this case, if the property is inheritable, the property's value will be searched in the parents too until an object specifies a value for the property. The parents will use their own state to detemine the value. So for example if a button is pressed, and the text color comes from here, the pressed text color will be used. Inheritance takes place at run time too.


.. _lvgl-fonts:

Fonts
-----

LVGL internally uses fonts in a C array. The library offers by default the following ones preconverted:

- ``montserrat_12_subpx``
- ``montserrat_28_compressed``
- ``dejavu_16_persian_hebrew``
- ``simsun_16_cjk16``
- ``unscii_8``
- ``unscii_16``

These may not contain all the glyphs corresponding to certain diacritic characters. You can generate your own set of glyphs in a C array using LVGL's `Online Font Converter <https://lvgl.io/tools/fontconverter/>`__ or use the tool `Offline <https://github.com/lvgl/lv_font_conv>`__.

In ESPHome you can also use a :ref:`font configured in the normal way<display-fonts>`, conversion will be done while building the binary.

.. _lvgl-styling:

Styling
-------

You can adjust the appearance of objects by changing the foreground, background and/or border color, font of each object. Some objects allow for more complex styling, effectively changing the appearance of their sub-components. 

- **x** (*Optional*, int16 or percentage): Horizontal position of the widget (anchored in the top left corner, relative to the parent or screen).
- **y** (*Optional*, int16 or percentage): Vertical position of the widget (anchored in the top left corner, relative to the parent or screen).
- **width** (*Optional*): Width of the widget - one of ``size_content``, a number (pixels) or a percentage.
- **height** (*Optional*): Height of the widget - one of ``size_content``, a number (pixels) or a percentage.
- **opa** (*Optional*, string or percentage): Opacity of the entire widget. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **opa_layered** (*Optional*, string or percentage): Opacity of the entire layer the widget is on. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **align** (*Optional*, string): Alignment of the contents of the widget. One of the values below:
    - ``TOP_LEFT``
    - ``TOP_MID``
    - ``TOP_RIGHT``
    - ``LEFT_MID``
    - ``CENTER``
    - ``RIGHT_MID``
    - ``BOTTOM_LEFT``
    - ``BOTTOM_MID``
    - ``BOTTOM_RIGHT``
    - ``OUT_LEFT_TOP``
    - ``OUT_TOP_LEFT``
    - ``OUT_TOP_MID``
    - ``OUT_TOP_RIGHT``
    - ``OUT_RIGHT_TOP``
    - ``OUT_LEFT_MID``
    - ``OUT_CENTER``
    - ``OUT_RIGHT_MID``
    - ``OUT_LEFT_BOTTOM``
    - ``OUT_BOTTOM_LEFT``
    - ``OUT_BOTTOM_MID``
    - ``OUT_BOTTOM_RIGHT``
    - ``OUT_RIGHT_BOTTOM``
- **bg_color** (*Optional*, :ref:`color <config-color>`): The ID of a color for the background of the widget.
- **bg_grad_color** (*Optional*, :ref:`color <config-color>`): The ID of a color to make the background gradually fade to.
- **bg_dither_mode** (*Optional*, string): Set ditherhing of the background gradient. One of ``NONE``, ``ORDERED``, ``ERR_DIFF``.
- **bg_grad_dir** (*Optional*, string): Choose the direction of the background gradient: ``NONE``, ``HOR``, ``VER``.
- **bg_main_stop** (*Optional*, 0-255): Specify where the gradient should start: ``0`` = at left/top most position, ``128`` = in the center, ``255`` = at right/bottom most position. Defaults to ``0``.
- **bg_grad_stop** (*Optional*, 0-255): Specify where the gradient should stop: ``0`` = at left/top most position, ``128`` = in the center, ``255`` = at right/bottom most position. Defaults to ``255``.
- **bg_img_opa** (*Optional*, string or percentage): Opacity of the background image of the widget. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **bg_img_recolor** (*Optional*, :ref:`color <config-color>`): The ID of a color to mix with every pixel of the image. 
- **bg_img_recolor_opa** (*Optional*, string or percentage): Opacity of the recoloring. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **bg_opa** (*Optional*, string or percentage): Opacity of the background. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **border_color** (*Optional*, :ref:`color <config-color>`): The ID of a color to draw borders of the widget.
- **border_opa** (*Optional*, string or percentage): Opacity of the borders of the widget. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **border_post** (*Optional*, boolean): If ``true`` the border will be drawn after all children of the widget have been drawn.
- **border_side** (*Optional*, list): Select which borders of the widgets to show (multiple can be chosen):
    - ``NONE``
    - ``TOP``
    - ``BOTTOM``
    - ``LEFT``
    - ``RIGHT``
    - ``INTERNAL``
- **border_width** (*Optional*, int16): Set the width of the border in pixels.
- **radius** (*Optional*, uint16): The radius of the rounded corners of the object. 0 = no radius i.e. square corners; 65535 = pill shaped object (true circle if object has same width and height).
- **clip_corner** (*Optional*, boolean): Enable to clip off the overflowed content on the rounded (``radius`` > ``0``) corners of a widget.
- **text_align** (*Optional*, string): Alignment of the text in the widget. One of ``LEFT``, ``CENTER``, ``RIGHT``, ``AUTO``
- **text_color** (*Optional*, :ref:`color <config-color>`): The ID of a color to render the text in.
- **text_decor** (*Optional*, list): Choose decorations for the text: ``NONE``, ``UNDERLINE``, ``STRIKETHROUGH`` (multiple can be chosen)
- **text_font``: (*Optional*, :ref:`font <lvgl-fonts>`):  The ID or the C array file of the font used to render the text.
- **text_letter_space** (*Optional*, int16): Characher spacing of the text.
- **text_line_space** (*Optional*, int16): Line spacing of the text.
- **text_opa** (*Optional*, string or percentage): Opacity of the text. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **line_width** (*Optional*, int16): Set the width of the line in pixels.
- **line_dash_width** (*Optional*, int16): Set the width of the dashes in the line (in pixels).
- **line_dash_gap** (*Optional*, int16): Set the width of the gap between the dashes in the line (in pixels).
- **line_rounded** (*Optional*, boolean): Make the end points of the line rounded. ``true`` rounded, ``false`` perpendicular line ending.
- **line_color** (*Optional*, :ref:`color <config-color>`): The ID of a color for the line.
- **outline_color** (*Optional*, :ref:`color <config-color>`): The ID of a color to draw an outline around the widget.
- **outline_opa** (*Optional*, string or percentage): Opacity of the outline. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **outline_pad** (*Optional*, int16): Distance between the outline and the widget itself.
- **outline_width** (*Optional*, int16): Set the width of the outline in pixels.
- **pad_all** (*Optional*, int16): Set the padding in all directions, in pixels.
- **pad_top** (*Optional*, int16): Set the padding on the top, in pixels.
- **pad_bottom** (*Optional*, int16): Set the padding on the bottom, in pixels.
- **pad_left** (*Optional*, int16): Set the padding on the left, in pixels.
- **pad_right** (*Optional*, int16): Set the padding on the right, in pixels.
- **pad_row** (*Optional*, int16): Set the padding between the rows of the children elements, in pixels.
- **pad_column** (*Optional*, int16): Set the padding between the columns of the children elements, in pixels.
- **shadow_color** (*Optional*, :ref:`color <config-color>`): The ID of a color to create a drop shadow under the widget.
- **shadow_ofs_x** (*Optional*, int16): Horrizontal offset of the shadow, in pixels
- **shadow_ofs_y** (*Optional*, int16): Vertical offset of the shadow, in pixels
- **shadow_opa** (*Optional*, string or percentage): Opacity of the shadow. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **shadow_spread** (*Optional*, int16): Spread of the shadow, in pixels.
- **shadow_width** (*Optional*, int16): Width of the shadow, in pixels.
- **transform_angle** (*Optional*, 0-360): Trannsformation angle of the widget (eg. rotation)
- **transform_height** (*Optional*, int16 or percentage): Trannsformation height of the widget (eg. stretching)
- **transform_pivot_x** (*Optional*, int16 or percentage): Horizontal anchor point of the transformation. Relative to the widget's top left corner.
- **transform_pivot_y** (*Optional*, int16 or percentage): Vertical anchor point of the transformation. Relative to the widget's top left corner.
- **transform_zoom** (*Optional*, 0.1-10):  Trannsformation zoom of the widget (eg. resizing)
- **translate_x** (*Optional*, int16 or percentage): Move of the object with this value in horizontal direction.
- **translate_y** (*Optional*, int16 or percentage): Move of the object with this value in vertical direction.
- **max_height** (*Optional*, int16 or percentage): Sets a maximal height. Pixel and percentage values can be used. Percentage values are relative to the height of the parent's content area. Defaults to ``0``.
- **min_height** (*Optional*, int16 or percentage): Sets a minimal height. Pixel and percentage values can be used. Percentage values are relative to the width of the parent's content area. Defaults to ``0``. 
- **max_width** (*Optional*, int16 or percentage): Sets a maximal width. Pixel and percentage values can be used. Percentage values are relative to the height of the parent's content area. Defaults to ``0``.
- **min_width** (*Optional*, int16 or percentage): Sets a minimal width. Pixel and percentage values can be used. Percentage values are relative to the height of the parent's content area. Defaults to ``0``.
- **arc_opa** (*Optional*, string or percentage): Opacity of the arcs. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **arc_color** (*Optional*, :ref:`color <config-color>`): The ID of a color to use to draw the arcs.
- **arc_rounded** (*Optional*, boolean): Make the end points of the arcs rounded. ``true`` rounded, ``false`` perpendicular line ending.
- **arc_width** (*Optional*, int16): Set the width of the arcs in pixels.




.. _lvgl-widgets:

LVGL Widgets
------------

**Base Object**: ``obj``

The Base Object can be directly used as a simple, empty widget. It is nothing more then a (rounded) rectangle. You can use it as a background shape for other objects by putting its jsonl line before the object. It catches touches!

**Text Label**: ``label``

  - **text** (*Optional*, string): The text of the label. Use``\n`` for line break. Defaults to "Text".
  - **mode** (*Optional*, string): The wrapping mode of long text labels: ``expand`` expands the object size to the text size; ``break`` keeps the object width, breaks the too long lines and expands the object height; ``dots`` keeps the size and writes dots at the end if the text is too long; ``scroll`` keeps the size and rolls the text back and forth; ``loop`` keeps the size and rolls the text circularly; ``crop`` keeps the size and crops the text out of it. Defaults to ``crop``.
  - **align** (*Optional*, string): Text alignment: ``left``, ``center``, ``right``. Defaults to ``left``.


**Button**: ``btn``

  - **toggle** (*Optional*, boolean): When enabled, creates a toggle-on/toggle-off button. If false, creates a normal button. Defaults to ``false``.
  - **text** (*Optional*, string): The text of the label. Defaults to "" (empty string).
  - **mode** (*Optional*, string): The wrapping mode of long text button texts: ``expand`` expands the object size to the text size; ``break`` keeps the object width, breaks the too long lines and expands the object height; ``dots`` keeps the size and writes dots at the end if the text is too long; ``scroll`` keeps the size and rolls the text back and forth; ``loop`` keeps the size and rolls the text circularly; ``crop`` keeps the size and crops the text out of it. Defaults to ``expand``.
  - **align** (*Optional*, string): Text alignment: ``left``, ``center``, ``right``. Defaults to ``left``.

**Switch**: ``switch``

  - **bg_color10** (*Optional*, :ref:`color <config-color>`): The ID of a color for indicator.
  - **bg_color20** (*Optional*, :ref:`color <config-color>`): The ID of a color for knob.
  - **radius20** (*Optional*, int16): Knob corner radius.


**Checkbox**: ``checkbox``

  - **text** (*Optional*, string): The label of the checkbox. Defaults to "Checkbox".


**Progress Bar**: ``bar``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``.
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``.
  - **start_value** (*Optional*, int16): Minimal allowed value of the indicator. Defaults to ``0``.

**Slider**: ``slider``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``.
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``.
  - **start_value** (*Optional*, int16): Minimal allowed value of the indicator. Defaults to ``0``.

**Arc**: ``arc``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``.
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``.
  - **rotation** (*Optional*, int16): Offset to the 0 degree position. Defaults to ``0``.
  - **type** (*Optional*, 0-2): ``0`` = normal, ``1`` = symmetrical, ``2`` = reverse. Defaults to ``0``.
  - **adjustable** (*Optional*, boolean): Add a knob that the user can move to change the value. Defaults to ``false``.
  - **start_angle** (*Optional*, 0-360): start angle of the arc background (see note).
  - **end_angle** (*Optional*, 0-360): end angle of the arc background (see note).
  - **start_angle10** (*Optional*, 0-360): start angle of the arc indicator (see note).
  - **end_angle10** (*Optional*, 0-360): end angle of the arc indicator (see note).

  .. note::

      Zero degree is at the middle right (3 o'clock) of the object and the degrees are increasing in a clockwise direction. The angles should be in the [0-360] range. 


**Dropdown List**: ``dropdown``

  - **options** (*Optional*, string): List of items separated by ``\n``. Defaults to "" (empty).
  - **text** (*Optional*, string): *Read-only* The text of the selected item. Defaults to "" (empty).
  - **direction** (*Optional*, 0-3): Direction where the dropdown expands: ``0`` = down, ``1`` = up, ``2`` = left, ``3`` = right. *Note:* up and down are superseeded by the screen size.
  - **show_selected** (*Optional*, boolean): Show the selected option or a static text. Defaults to ``true``.
  - **max_height** (*Optional*, int16): The maximum height of the open drop-down list. Defaults to 3/4 of screen height.


**Roller**: ``roller``

  - **options** (*Optional*, string): List of items separated by ``\n``. Defaults to "" (empty).
  - **text** (*Optional*, string): *Read-only* The text of the selected item. Defaults to "" (empty).
  - **rows** (*Optional*, int8): The number of rows that are visible. Use this property instead of ``h`` to set object height! Defaults to ``3``.
  - **mode** (*Optional*, 0-1): Roller mode: ``0`` = normal (finite), ``1`` = infinite. Defaults to ``0``.
  - **align** (*Optional*, string): Text alignment: ``left``, ``center``, ``right``. Defaults to ``center``.


**Line Meter**: ``linemeter``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``.
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``.
  - **angle** (*Optional*, 0-360): Angle between start and end of the scale. Defaults to ``240``.
  - **line_count** (*Optional*, uint16): Tick count of the scale. Defaults to ``31``.
  - **rotation** (*Optional*, 0-360): Offset for the scale angles to rotate it. Defaults to ``0``.
  - **type** (*Optional*, 0-1): ``0`` = indicator lines are activated clock-wise, ``1`` = indicator lines are activated counter-clock-wise. Defaults to ``0``.

**Gauge**: ``gauge``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``.
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``.
  - **critical_value** (*Optional*, int16): Scale color will be changed to ``scale_end_color`` after this value. Defaults to ``80``.
  - **scale_end_color**: (*Optional*, :ref:`color <config-color>`): The ID of a color for values above critical.
  - **label_count** (*Optional*, uint8): Number of labels (and major ticks) of the scale. Defaults to ``0``.
  - **line_count** (*Optional*, uint16): Number of minor ticks of the entire scale. Defaults to ``31``.
  - **angle** (*Optional*, 0-360): Angle between start and end of the scale. Defaults to ``240``.
  - **rotation** (*Optional*, 0-360): Offset for the gauge's angles to rotate it. Defaults to ``0``.
  - **scale** ???
  - **format** (*Optional*, uint16): Divider for major tick values. Defaults to ``0``.

  .. note::

      To strip trailing zero's of major tick labels the ``format`` divider can be used to scale the values before printing:
      
        - ``0``: print the major tick value as is.
        - ``1``: strip 1 zero, i.e. divide tick value by 10 before printing the major tick label.
        - ``2``: strip 2 zeros, i.e. divide tick value by 100 before printing the major tick label.
        - ``3``: strip 3 zeros, i.e. divide tick value by 1000 before printing the major tick label.
        - ``4``: strip 4 zeros, i.e. divide tick value by 10000 before printing the major tick label.

      Only these values are allowed, arbitrary numbers are not supported.




Data types
----------

LVLG supports numeric properties only as integer values with variable minimums and maximums. Certain object properties also support negative values.

- ``int8`` (signed) supports values ranging from -128 to 127.
- ``uint8`` (unsigned) supports values ranging from 0 to 255.
- ``int16`` (signed) supports values ranging from -32768 to 32767.   
- ``uint16`` (unsigned) supports values ranging from 0 to 65535.


See Also
--------

- `LVGL 8.3 docs <https://docs.lvgl.io/8.3/>`__
- `LVGL Online Font Converter <https://lvgl.io/tools/fontconverter/>`__
- :ghedit:`Edit`
