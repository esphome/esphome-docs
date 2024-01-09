.. _lvgl-main:

LVGL
====

.. seo::
    :description: LVGL - ESPHome Displays showing contents created with Light and Versatile Graphics Library
    :image: /images/logo_lvgl.png


`LVGL <https://lvgl.io/>`__ (Light and Versatile Graphics Library) is a free and open-source 
embedded graphics library to create beautiful UIs for any MCU, MPU and display type. ESPHome supports
`LVGL version 8.3.9 <https://docs.lvgl.io/8.3/>`__.

.. figure:: /components/images/lvgl_main_screenshot.png
    :align: center

In order to be able to drive a display with LVGL under ESPHome you need an MCU from the ESP32 family. Although
PSRAM is not a strict requirement, it is recommended.

For interactivity, a :ref:`Touchscreen <touchscreen-main>` (capacitive highly prefered) or a :doc:`/components/sensor/rotary_encoder` can be used.

Basics
------

In LVGL, graphical elements like Buttons, Labels, Sliders etc. are called widgets or objects. See :ref:`lvgl-widgets` to see the full
list of available LVGL widgets in ESPHome.

Every widget has a parent object where it is created. For example, if a label is created on a button, the button is the parent of label.
The child object moves with the parent and if the parent is deleted the children will be deleted too. Children can be visible only within
their parent's bounding area. In other words, the parts of the children outside the parent are clipped. A screen is the *root* parent.

TODO - SCREEN/PAGE

Widgets integrate in ESPHome also as components:

+-------------+-------------------------------+ 
| LVGL Widget | ESPHome component type        | 
+=============+===============================+
| Checkbox    | Binary Sensor, Switch         | 
+-------------+-------------------------------+ 
| Button      | Binary Sensor, Button, Switch | 
+-------------+-------------------------------+ 
| Slider      | Sensor, Number                | 
+-------------+-------------------------------+ 
| Arc         | Sensor, Number                | 
+-------------+-------------------------------+ 
| Dropdown    | Select                        | 
+-------------+-------------------------------+ 
| Roller      | Select                        | 
+-------------+-------------------------------+ 

These are useful to perform :ref:`automations <automation>` triggered by actions performed at the screen. Check out the :ref:`<lvgl-seealso>` section at the bottom of this document.


Main Component
--------------

Although LVGL is a complex matrix of objects-parts-states-styles, in ESPHome this is simplified to a hierarchy.

At the highest level of the LVGL object hierarchy is the display which represents the driver for a display device (physical display). A display can have one or more screens associated with it. Each screen contains a hierarchy of objects for graphical widgets representing a layout that covers the entire display.

The widget is at the top level, and it allows main styling. It also has sub-parts, which can be styled separately. 
Usually styles are inherited. The widget and the parts have states, and the different styling can be set for different states.

Configuration variables:

- **display_id** (**Required**, list): A list of displays where to render this entire LVGL configuration:
    - **display_id** (**Required**, :ref:`config-id`): The ID of a display configuration.
- **touchscreens** (*Optional*, list): A list of touchscreens interacting with the LVGL widgets on the display. Can be omitted if there's at least a rotary encoder configured.
    - **touchscreen_id** (*Required*, :ref:`config-id`): ID of a touchscreen configuration-
- **rotary_encoders** (*Optional*, list): A list of rotary encoders interacting with the LVGL widgets on the display. Can be omitted if there's at least a touchscreen configured.
    - **sensor:** (*Required*, :ref:`config-id`): The ID of a :doc:`/components/sensor/rotary_encoder` used to interact with the widgets.
    - **binary_sensor** (*Optional*, :ref:`config-id`): The ID of a :doc:`/components/binary_sensor/index`, usually used as a push button within the rotary encoder used to interact with the widgets.
    - **group** (*Optional*, string): A name for a group of widgets whics will interact with the the rotary encoder. See :ref:`below <lvgl-styling>` for more information on groups.
- **color_depth** (*Optional*, enum): The color deph at which the contents are generated. Valid values are ``1`` (monochrome), ``8``, ``16`` or ``32``, defaults to ``16``.
- **buffer_size** (*Optional*, percentage): The percentage of scren size to allocate buffer memory. Default is ``100%`` (or ``1.0``). For devices without PSRAM recommended value is ``25%``. 
- **log_level** (*Optional*, enum): Set the logger level specifically for the messages of the LVGL library: ``TRACE``, ``INFO``, ``WARN``, ``ERROR``, ``USER``, ``NONE"``. Defaults to ``WARN``.
- **byte_order** (*Optional*, enum): The byte order of the data outputted by lvgl, ``big_endian`` or ``little_endian``. If not specified, will default to ``big_endian``.
- **style_definitions** (*Optional*, list): A batch of style definitions to use with selected LVGL widgets. See :ref:`below <lvgl-theme>` for more details. 
- **theme** (*Optional*, list): A list of styles to commonly apply to the widgets. See :ref:`below <lvgl-theme>` for more details. 
- **layout** (*Optional*, string): ``FLEX``, ``GRID`` or ``NONE``. LVGL supports two styles of layouts, ``FLEX`` and ``GRID``. ``FLEX`` can arrange items into rows or columns (tracks), handle wrapping, adjust the spacing between the items and tracks, handle grow to make the item fill the remaining space with respect to min/max width and height. ``GRID`` can arrange items into a 2D "table" that has rows or columns (tracks). The item can span through multiple columns or rows. With these layouts the widgets can be placed automatically, and there's no need to specify the ``x`` and the ``y`` positional coordinates for each. If not specified, defaults to ``NONE``, which disables layouts each widget needing manual positioning.
- **flex_flow** (*Optional*, string): In case of ``FLEX`` layout, choose one of the following options. Defaults to ``ROW_WRAP``:
    - ``ROW`` to place the children in a row without wrapping
    - ``COLUMN`` to place the children in a column without wrapping
    - ``ROW_WRAP`` to place the children in a row with wrapping
    - ``COLUMN_WRAP`` to place the children in a column with wrapping
    - ``ROW_REVERSE`` to place the children in a row without wrapping but in reversed order
    - ``COLUMN_REVERSE`` to place the children in a column without wrapping but in reversed order
    - ``ROW_WRAP_REVERSE`` to place the children in a row with wrapping but in reversed order
    - ``COLUMN_WRAP_REVERSE`` to place the children in a column with wrapping but in reversed order
- **widgets** (*Optional*, list): A list of LVGL widgets to be drawn on the screen.
- **update_interval**: (*Optional*, :ref:`Time <config-time>`): The interval to re-draw the screen. Defaults to 1s.
- All other options from :ref:`lvgl-styling`.


Example:

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
      layout: grid
      width: 100%
      widgets:
        - btn:
            id: lv_button0
            x: 5
            y: 30


.. note::

    By default, LVGL draws new widgets on top of old widgets, including their children. If widgets are children of other widgets (they have the parentid property set), property inheritance takes place. Some properties (typically that are related to text and opacity) can be inherited from the parent widgets's styles. Inheritance is applied only at first draw. In this case, if the property is inheritable, the property's value will be searched in the parents too until an object specifies a value for the property. The parents will use their own state to detemine the value. So for example if a button is pressed, and the text color comes from here, the pressed text color will be used. Inheritance takes place at run time too.



.. _lvgl-theme:

Theming and Styling
-------------------

The widgets support lots of :ref:`lvgl-styling` to customize their appearance and behavior.

You can configure a global theme for all the widgets at the top level with the ``theme`` configuration option. In the example below, all the ``arc``, ``slider`` and ``btn`` widgets will use the styles and properties predefined by default here. A combination of styles and states can be chosen for every widget.

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

Naturally, you can override these at the indivdual configuration level of each widget. This can be done in batches, using ``style_definitions`` configuration option of the main component.
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


And then you apply these selected styles to two labels, and only change very specific stlye ``y`` locally:

.. code-block:: yaml

    widgets:
      - label:
          id: day_label
          styles: date_style # apply the definiton here by the ID chosen above
          y: -20
      - label:
          id: date_label
          styles: date_style
          y: +20

Additionally, you can change the styles based on the state of the widgets or their parts. 

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


.. _lvgl-styling:

Style properties
----------------

You can adjust the appearance of widgets by changing the foreground, background and/or border color, font of each object. Some widgets allow for more complex styling, effectively changing the appearance of their parts. 

- **align** (*Optional*, enum): Alignment of the of the widget `relative to the parent <https://docs.lvgl.io/8.3/widgets/obj.html?#alignment>`__. One of:
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
- **bg_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color for the background of the widget.
- **bg_grad_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color to make the background gradually fade to.
- **bg_dither_mode** (*Optional*, enum): Set ditherhing of the background gradient. One of ``NONE``, ``ORDERED``, ``ERR_DIFF``.
- **bg_grad_dir** (*Optional*, enum): Choose the direction of the background gradient: ``NONE``, ``HOR``, ``VER``.
- **bg_main_stop** (*Optional*, 0-255): Specify where the gradient should start: ``0`` = at left/top most position, ``128`` = in the center, ``255`` = at right/bottom most position. Defaults to ``0``.
- **bg_grad_stop** (*Optional*, 0-255): Specify where the gradient should stop: ``0`` = at left/top most position, ``128`` = in the center, ``255`` = at right/bottom most position. Defaults to ``255``.
- **bg_img_opa** (*Optional*, enum or percentage): Opacity of the background image of the widget. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **bg_img_recolor** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color to mix with every pixel of the image. 
- **bg_img_recolor_opa** (*Optional*, enum or percentage): Opacity of the recoloring. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **bg_opa** (*Optional*, enum or percentage): Opacity of the background. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **opa** (*Optional*, enum or percentage): Opacity of the entire widget. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **opa_layered** (*Optional*, enum or percentage): Opacity of the entire layer the widget is on. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **border_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color to draw borders of the widget.
- **border_opa** (*Optional*, enum or percentage): Opacity of the borders of the widget. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
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
- **line_width** (*Optional*, int16): Set the width of the line in pixels.
- **line_dash_width** (*Optional*, int16): Set the width of the dashes in the line (in pixels).
- **line_dash_gap** (*Optional*, int16): Set the width of the gap between the dashes in the line (in pixels).
- **line_rounded** (*Optional*, boolean): Make the end points of the line rounded. ``true`` rounded, ``false`` perpendicular line ending.
- **line_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color for the line.
- **outline_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color to draw an outline around the widget.
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
- **shadow_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color to create a drop shadow under the widget.
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
- **translate_x** (*Optional*, int16 or percentage): Move of the widget with this value in horizontal direction.
- **translate_y** (*Optional*, int16 or percentage): Move of the widget with this value in vertical direction.
- **max_height** (*Optional*, int16 or percentage): Sets a maximal height. Pixel and percentage values can be used. Percentage values are relative to the height of the parent's content area. Defaults to ``0``.
- **min_height** (*Optional*, int16 or percentage): Sets a minimal height. Pixel and percentage values can be used. Percentage values are relative to the width of the parent's content area. Defaults to ``0``. 
- **max_width** (*Optional*, int16 or percentage): Sets a maximal width. Pixel and percentage values can be used. Percentage values are relative to the height of the parent's content area. Defaults to ``0``.
- **min_width** (*Optional*, int16 or percentage): Sets a minimal width. Pixel and percentage values can be used. Percentage values are relative to the height of the parent's content area. Defaults to ``0``.
- **text_align** (*Optional*, enum): Alignment of the text in the widget. One of ``LEFT``, ``CENTER``, ``RIGHT``, ``AUTO``
- **text_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color to render the text in.
- **text_decor** (*Optional*, list): Choose decorations for the text: ``NONE``, ``UNDERLINE``, ``STRIKETHROUGH`` (multiple can be chosen)
- **text_font**: (*Optional*, :ref:`font <lvgl-fonts>`):  The ID or the C array file of the font used to render the text.
- **text_letter_space** (*Optional*, int16): Characher spacing of the text.
- **text_line_space** (*Optional*, int16): Line spacing of the text.
- **text_opa** (*Optional*, string or percentage): Opacity of the text. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.


.. _lvgl-widgets:

Widgets
-------

Common properties
*****************

The properties below are common to all widgets.

- **x** (*Optional*, int16 or percentage): Horizontal position of the widget (anchored in the top left corner, relative to top left of parent or screen). If layouts are used, or if specfiyng ``align``, can be omitted for automatic placement.
- **y** (*Optional*, int16 or percentage): Vertical position of the widget (anchored in the top left corner, relative to to top left of the parent or screen). If layouts are used, or if specfiyng ``align``, can be omitted for automatic placement.
- **width** (*Optional*): Width of the widget in pixels or a percentage, or ``size_content`` (see below).
- **height** (*Optional*): Height of the widget in pixels or a percentage, or ``size_content``. Use ``size_content`` to automatically size the widget based on its contents (children objects, or eg. image size in case of ``img``.
- **group** (*Optional*, string): Widgets can be grouped together for interaction with a :doc:`/components/sensor/rotary_encoder`. In every group there is always one focused object which receives the encoder actions. You need to associate an input device with a group. An input device can send key events to only one group but a group can receive data from more than one input device.
- **styles** (*Optional*, :ref:`config-id`): The ID of a *style definition* from the main component configuration to override the theme styles.
- **theme** (*Optional*, list): A list of styles to apply to the widget and children. Same configuration option as at the main component.
- **layout** (*Optional*, string): ``FLEX``, ``GRID`` or ``NONE``. Same configuration option as at the main component.
- **flex_flow** (*Optional*, string): Option for ``FLEX`` layout, similar configuration as at the main component.
- **widgets** (*Optional*, list): A list of LVGL widgets to be drawn as children of this widget. Same configuration option as at the main component.
- **state** (*Optional*, string): Widgets or their (sub)parts can have have states, which support separate styling. These state styles inherit from theme, but can be locally overriden withing style definitions or locally set. The state itself can be can be changed by interacting with the widget itself, or :ref:`programatically <lvgl-objupd-act>` with ``lvgl.obj.update`` action. Can be one of:
    - ``default``: Normal, released state
    - ``disabled``: Disabled state (also usable with :ref:`shorthand <lvgl-objupd-shorthands>` actions ``lvgl.obj.enable`` and ``lvgl.obj.disable``)
    - ``pressed``: Being pressed
    - ``checked``: Toggled or checked state
    - ``scrolled``: Being scrolled
    - ``focused``: Focused via keypad or encoder or clicked via touchpad/mouse
    - ``focus_key``: Focused via keypad or encoder but not via touchpad/mouse
    - ``edited``: Edit by an encoder
    - ``user_1``: Custom state
    - ``user_2``: Custom state
    - ``user_3``: Custom state
    - ``user_4``: Custom state

In addition to visual stilyng, each widget supports :ref:`dynamically settable flags <lvgl-objupdflag-act>` to influence the behavior at runtime.


``arc``
*******

The Arc consists of a background and a foreground arc. The foreground (indicator) can be touch-adjusted with a knob.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **min_value** (*Optional*, int8): Minimum value of the indicator. Defaults to ``0``.
- **max_value** (*Optional*, int8): Maximum value of the indicator. Defaults to ``100``.
- **start_angle** (*Optional*, 0-360): start angle of the arc background (see note). Defaults to ``135``.
- **end_angle** (*Optional*, 0-360): end angle of the arc background (see note). Defaults to ``45``.
- **rotation** (*Optional*, int8): Offset to the 0 degree position. Defaults to ``0.0``.
- **adjustable** (*Optional*, boolean): Add a knob that the user can move to change the value. Defaults to ``false``.
- **mode** (*Optional*, string): ``NORMAL``: the indicator is drawn from the minimum value to the current. ``REVERSE``: the indicator is drawn counter-clockwise from the maximum value to the current. ``SYMMETRICAL``: the indicator is drawn from the middle point to the current value. Defaults to ``NORMAL``.
- **change_rate** (*Optional*, int8): If the arc is pressed the current value will set with a limited speed according to the set change rate. The change rate is defined in degree/second. Defaults to ``720``.
- **arc_opa** (*Optional*, enum or percentage): Opacity of the arcs. ``TRANSP`` for fully transparent, ``COVER`` for fully opaque, or an integer between ``0`` and ``100`` for percentage.
- **arc_color** (*Optional*, :ref:`color <config-color>`): The ID of a configured color, or a hexadecimal representation of a RGB color to use to draw the arcs.
- **arc_rounded** (*Optional*, boolean): Make the end points of the arcs rounded. ``true`` rounded, ``false`` perpendicular line ending.
- **arc_width** (*Optional*, int16): Set the width of the arcs in pixels.
- **knob** (*Optional*, list): Settings for the knob **part** to control the value. Supports a list of styles and state-based styles to customize.
- **indicator** (*Optional*, list): Settings for the indicator **part** to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize.
- any :ref:`Styling <lvgl-styling>` and state-based option to override styles inherited from parent.

.. note::

    Zero degree is at the middle right (3 o'clock) of the object and the degrees are increasing in a clockwise direction. The angles should be in the ``0``-``360`` range. 

Example:

.. code-block:: yaml

    # Example widget:
    - arc:
        group: general
        scroll_on_focus: true
        id: arc_value
        value: 75
        min_value: 1
        max_value: 100
        arc_color: 0xFF0000
        indicator:
          arc_color: 0xF000FF
          pressed:
            arc_color: 0xFFFF00
          focused:
            arc_color: 0x808080
        knob:
          focused:
            bg_color: 0x808080


The ``arc`` can be also integrated as :doc:`/components/sensor/lvgl` and :doc:`/components/number/lvgl`.


``bar``
*******

The bar object has a background and an indicator on it. The width of the indicator is set according to the current value of the bar.

Vertical bars can be created if the width of the object is smaller than its height.

Not only the end, but also the start value of the bar can be set, which changes the start position of the indicator.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **indicator** (*Optional*, list): Settings for the indicator **part**
- **min_value** (*Optional*, int8): Minimum value of the indicator. Defaults to ``0``.
- **max_value** (*Optional*, int8): Maximum value of the indicator. Defaults to ``100``.
- **mode** (*Optional*, string): ``NORMAL``: the indicator is drawn from the minimum value to the current. ``REVERSE``: the indicator is drawn counter-clockwise from the maximum value to the current. ``SYMMETRICAL``: the indicator is drawn from the middle point to the current value. Defaults to ``NORMAL``.
- **animated** (*Optional*, boolean): ``true`` , ``false`` . TODO
- **indicator** (*Optional*, list): Settings for the indicator **part** to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize.

Example:

.. code-block:: yaml

    # Example widget:
    - 


``btn``
*******

Simple push or toggle button.

.. figure:: /components/images/lvgl_button.png
    :align: center

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.


Example:

.. code-block:: yaml

    # Example widget:
    - 

The ``btn`` can be also integrated as :doc:`/components/binary_sensor/lvgl` or as a :doc:`/components/switch/lvgl`.


``btnmatrix``
*************

The Button Matrix object is a lightweight way to display multiple buttons in rows and columns. Lightweight because the buttons are not actually created but just virtually drawn on the fly. This way, one button use only eight extra bytes of memory instead of the ~100-150 bytes a normal Button object plus the 100 or so bytes for the Label object.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **items** (*Optional*, list): Settings for the items **part**


Example:

.. code-block:: yaml

    # Example widget:
    - 



``canvas``
**********

A Canvas inherits from Image where the user can draw anything. Rectangles, texts, images, lines, arcs can be drawn here using lvgl's drawing engine. Additionally "effects" can be applied, such as rotation, zoom and blur.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.


Example:

.. code-block:: yaml

    # Example widget:
    - 



``checkbox``
************

The Checkbox object is made from a "tick box" and a label. When the Checkbox is clicked the tick box is toggled.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **indicator** (*Optional*, list): Settings for the indicator **part**


Example:

.. code-block:: yaml

    # Example widget:
    - 

The ``checkbox`` can be also integrated as :doc:`/components/binary_sensor/lvgl` or as a :doc:`/components/switch/lvgl`.


``dropdown``
************

The drop-down list allows the user to select one value from a list.

The drop-down list is closed by default and displays a single value or a predefined text. When activated (by click on the drop-down list), a list is drawn from which the user may select one option. When the user selects a new value, the list is deleted from the screen.

.. figure:: /components/images/lvgl_dropdown.png
    :align: center

Specific configuration options:

- **selected** (*Optional*): 
- **scrollbar**
- **selected_index**
- **dir** ``LEFT``, ``RIGHT``, ``BOTTOM``, ``TOP``, defaults to ``BOTTOM``.
- **dropdown_list**
- **symbol** (*Optional*, enum): A symbol (typically an arrow) can be added to the dropdown list. If ``dir`` of the drop-down list is ``LEFT`` the symbol will be shown on the left, otherwise on the right. One of: ``AUDIO``, ``VIDEO``, ``LIST``, ``OK``, ``CLOSE``, ``POWER``, ``SETTINGS``, ``HOME``, ``DOWNLOAD``, ``DRIVE``, ``REFRESH``, ``MUTE``, ``VOLUME_MID``, ``VOLUME_MAX``, ``IMAGE``, ``TINT``, ``PREV``, ``PLAY``, ``PAUSE``, ``STOP``, ``NEXT``, ``EJECT``, ``LEFT``, ``RIGHT``, ``PLUS``, ``MINUS``, ``EYE_OPEN``, ``EYE_CLOSE``, ``WARNING``, ``SHUFFLE``, ``UP``, ``DOWN``, ``LOOP``, ``DIRECTORY``, ``UPLOAD``, ``CALL``, ``CUT``, ``COPY``, ``SAVE``, ``BARS``, ``ENVELOPE``, ``CHARGE``, ``PASTE``, ``BELL``, ``KEYBOARD``, ``GPS``, ``FILE``, ``WIFI``, ``BATTERY_FULL``, ``BATTERY_3``, ``BATTERY_2``, ``BATTERY_1``, ``BATTERY_EMPTY``, ``USB``, ``BLUETOOTH``, ``TRASH``, ``EDIT``, ``BACKSPACE``, ``SD_CARD``, ``NEW_LINE``


Example:

.. code-block:: yaml

    # Example widget:
    - 

The ``dropdown`` can be also integrated as :doc:`/components/select/lvgl`.


``img``
*******

Images are the basic widgets to display images.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.


Example:

.. code-block:: yaml

    # Example widget:
    - 



``label``
*********

A label is the basic object type that is used to display text.

.. figure:: /components/images/lvgl_label.png
    :align: center

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **scrollbar** (*Optional*, list): Settings for the scrollbar **part**
- **selected** (*Optional*, list): Settings for the selected **part**


Example:

.. code-block:: yaml

    # Example widget:
    - 




``line``
********

The Line object is capable of drawing straight lines between a set of points.

Specific configuration options:

  - **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.


Example:

.. code-block:: yaml

    # Example widget:
    - 



``meter``
*********

The Meter widget can visualize data in very flexible ways. In can show arcs, needles, ticks lines and labels.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **indicator** (*Optional*, list): Settings for the indicator **part** to show the value. Supports a list of :ref:`styles <lvgl-styling>` and state-based styles to customize, and additionally:
    - **r_mod** (*Optional*): TODO in pixels or a percentage, or ``size_content``. Use ``size_content`` to automatically size the object based on its contents.

Example:

.. code-block:: yaml

    # Example widget:
    - 


``obj``
*******

The Base Object can be directly used as a simple, empty widget. It is nothing more than a (rounded) rectangle.

You can use it as a parent background shape for other objects. It catches touches!

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.


Example:

.. code-block:: yaml

    # Example widget:
    - 




``roller``
**********

Roller allows you to simply select one option from a list by scrolling.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **selected** (*Optional*, list): Settings for the selected **part**


Example:

.. code-block:: yaml

    # Example widget:
    - 

The ``roller`` can be also integrated as :doc:`/components/select/lvgl`.


``slider``
**********

The Slider object looks like a Bar supplemented with a knob. The knob can be dragged to set a value. Just like Bar, Slider can be vertical or horizontal.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **indicator** (*Optional*, list): Settings for the indicator **part**
- **knob** (*Optional*, list): Settings for the knob **part**


Example:

.. code-block:: yaml

    # Example widget:
    - 

The ``slider`` can be also integrated as :doc:`/components/sensor/lvgl` and :doc:`/components/number/lvgl`.


``switch``
**********

The Switch looks like a little slider and can be used to turn something on and off.

.. figure:: /components/images/lvgl_switch.png
    :align: center

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **indicator** (*Optional*, list): Settings for the indicator **part**
- **knob** (*Optional*, list): Settings for the knob **part**

The ``switch`` can be also integrated as :doc:`/components/binary_sensor/lvgl` or as a :doc:`/components/switch/lvgl`.

Example:

.. code-block:: yaml

    # Example widget:
    - 



``table``
*********

Tables, as usual, are built from rows, columns, and cells containing texts.

The Table object is very lightweight because only the texts are stored. No real objects are created for cells but they are just drawn on the fly.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **items** (*Optional*, list): Settings for the items **part**


Example:

.. code-block:: yaml

    # Example widget:
    - 



``textarea``
************

The Text Area is a Base object with a Label and a cursor on it. Texts or characters can be added to it. Long lines are wrapped and when the text becomes long enough the Text area can be scrolled.

One line mode and password modes are supported.

Specific configuration options:

- **value** (*Required*, int8): Actual value of the indicator, in ``0``-``100`` range. Defaults to ``0``.
- **scrollbar** (*Optional*, list): Settings for the scrollbar **part**
- **selected** (*Optional*, list): Settings for the selected **part**
- **cursor** (*Optional*, list): Settings for the cursor **part**
- **textarea_placeholder** (*Optional*, list): Settings for the textarea_placeholder **part**

Example:

.. code-block:: yaml

    # Example widget:
    - 




.. _lvgl-fonts:

Fonts
-----

TODO

LVGL internally uses fonts in a C array. The library offers by default the following ones preconverted:

- ``montserrat_12_subpx``
- ``montserrat_28_compressed``
- ``dejavu_16_persian_hebrew``
- ``simsun_16_cjk16``
- ``unscii_8``
- ``unscii_16``

These may not contain all the glyphs corresponding to certain diacritic characters. You can generate your own set of glyphs in a C array using LVGL's `Online Font Converter <https://lvgl.io/tools/fontconverter/>`__ or use the tool `Offline <https://github.com/lvgl/lv_font_conv>`__.

In ESPHome you can also use a :ref:`font configured in the normal way<display-fonts>`, conversion will be done while building the binary.





.. _lvgl-objupd-act:

``lvgl.obj.update`` Action
--------------------------

This powerful :ref:`action <config-action>` allows changing on the fly any :ref:`style property <lvgl-styling>` or :ref:`flag <lvgl-objupdflag-act>` of any widget.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.obj.update:
            id: my_button_id
            bg_color: 0xFF0000
            state:
              disabled: true
 

.. _lvgl-objupdflag-act:

In addition to visual stilyng, each widget supports some boolean flags to influence the behavior:

.. code-block:: yaml

    on_...:
      then:
        - lvgl.obj.update:
            id: my_label_id
            hidden: true


- **hidden** (*Optional*, boolean): make the object hidden (like it wasn't there at all), also usable with :ref:`shorthand <lvgl-objupd-shorthands>` actions ``lvgl.obj.show`` and ``lvgl.obj.hide``
- **clickable** (*Optional*, boolean): make the object clickable by input devices
- **click_focusable** (*Optional*, boolean): add focused state to the object when clicked
- **checkable** (*Optional*, boolean): toggle checked state when the object is clicked
- **scrollable** (*Optional*, boolean): make the object scrollable
- **scroll_elastic** (*Optional*, boolean): allow scrolling inside but with slower speed
- **scroll_momentum** (*Optional*, boolean): make the object scroll further when "thrown"
- **scroll_one** (*Optional*, boolean): allow scrolling only one snappable children
- **scroll_chain_hor** (*Optional*, boolean): allow propagating the horizontal scroll to a parent
- **scroll_chain_ver** (*Optional*, boolean): allow propagating the vertical scroll to a parent
- **scroll_chain simple** (*Optional*, boolean): packaging for (``scroll_chain_hor** or ``scroll_chain_ver``)
- **scroll_on_focus** (*Optional*, boolean): automatically scroll object to make it visible when focused
- **scroll_with_arrow** (*Optional*, boolean): allow scrolling the focused object with arrow keys
- **snappable** (*Optional*, boolean): if scroll snap is enabled on the parent it can snap to this object
- **press_lock** (*Optional*, boolean): keep the object pressed even if the press slid from the object
- **event_bubble** (*Optional*, boolean): propagate the events to the parent too
- **gesture_bubble** (*Optional*, boolean): propagate the gestures to the parent
- **adv_hittest** (*Optional*, boolean): allow performing more accurate hit (click) test. E.g. Accounting for rounded corners
- **ignore_layout** (*Optional*, boolean): make the object positionable by the layouts
- **floating** (*Optional*, boolean): do not scroll the object when the parent scrolls and ignore layout
- **overflow_visible** (*Optional*, boolean): do not clip the children's content to the parent's boundary
- **layout_1** (*Optional*, boolean): custom flag, free to use by layouts
- **layout_2** (*Optional*, boolean): custom flag, free to use by layouts
- **widget_1** (*Optional*, boolean): custom flag, free to use by widget
- **widget_2** (*Optional*, boolean): custom flag, free to use by widget
- **user_1** (*Optional*, boolean): custom flag, free to use by user
- **user_2** (*Optional*, boolean): custom flag, free to use by user
- **user_3** (*Optional*, boolean): custom flag, free to use by user
- **user_4** (*Optional*, boolean): custom flag, free to use by user



.. _lvgl-objupd-shorthands:

``lvgl.obj.hide`` and ``lvgl.obj.show`` Actions
-----------------------------------------------

These :ref:`actions <config-action>` are shorthands for toggling the ``hidden`` flag of any widget:

.. code-block:: yaml

    on_...:
      then:
        - lvgl.obj.hide: my_label_id
        - delay: 0.5s
        - lvgl.obj.show: my_label_id


``lvgl.obj.disable`` and ``lvgl.obj.enable`` Actions
----------------------------------------------------

These :ref:`actions <config-action>` are shorthands for toggling the ``disabled`` state of any widget (which controls the appearance of the corresponding *disabled* style set of the theme):

.. code-block:: yaml

    - on_...:
        then:
          - lvgl.obj.disable: my_button_id
    - on_...:
        then:
          - lvgl.obj.enable: my_button_id



.. _lvgl-rfrsh-act:

``lvgl.obj.invalidate`` Action
------------------------------

This :ref:`action <config-action>` redraws the entire screen, or optionally only a widget on it.

- **obj_id** (*Optional*): The ID of a widget configured in LVGL, which you want to redraw.

obj_id

.. code-block:: yaml

    on_...:
      then:
        - lvgl.obj.invalidate:




.. _lvgl-pause-act:

``lvgl.pause`` Action
---------------------

This :ref:`action <config-action>` pauses the activity of LVGL, including rendering.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.pause


.. _lvgl-resume-act:

``lvgl.resume`` Action
----------------------

This :ref:`action <config-action>` resumes the activity of LVGL, including rendering.

.. code-block:: yaml

    on_...:
      then:
        - lvgl.resume






.. _lvgl-idle-cond:

``lvgl.is_idle`` Condition
--------------------------

This :ref:`condition <config-condition>` checks if LVGL is in idle state or not.

.. code-block:: yaml

    # In some trigger:
    on_...:
      then:
        - if:
            condition: lvgl.is_idle
            then:
              - light.turn_off:
                  id: display_backlight
                  transition_length: 3s


.. _lvgl-paused-cond:

``lvgl.is_paused`` Condition
----------------------------

This :ref:`condition <config-condition>` checks if LVGL is in paused state or not.

.. code-block:: yaml

    # In some trigger:
    on_...:
      then:
        - if:
            condition: lvgl.is_paused
            then:
              - lvgl.resume:
              - light.turn_on:
                  id: display_backlight
                  transition_length: 150ms


.. _lvgl-onidle-act:

``lvgl.on_idle`` Trigger
------------------------

LVGL has a notion of screen inactivity, i.e. how long did the user not interact with the screen. This can be use to dim the display backlight or turn it off after a moment of inactivity (like a screen saver). Every use of an input device (touchscreen, rotary encoder) counts as an activity and resets the inactivity counter. 

The ``on_idle`` :ref:`trigger <automation>` is activated when inactivity time becomes longer than the specified ``timeout``. 

- **timeout** (**Required**, :ref:`templatable <config-templatable>`, int): :ref:`Time <config-time>` value after which LVGL should enter idle state. 

.. code-block:: yaml

    lvgl:
        on_idle:
          timeout: 30s
          then:
            - logger.log: "LVGL is idle"
            - lvgl.pause:
            - light.turn_off:
                id: display_backlight



Data types
----------

LVLG supports numeric properties only as integer values with variable minimums and maximums. Certain object properties also support negative values.

- ``int8`` (signed) supports values ranging from -128 to 127.
- ``uint8`` (unsigned) supports values ranging from 0 to 255.
- ``int16`` (signed) supports values ranging from -32768 to 32767.   
- ``uint16`` (unsigned) supports values ranging from 0 to 65535.


.. _lvgl-seealso:

See Also
--------

- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/touchscreen/index`
- :doc:`/components/sensor/rotary_encoder`
- `LVGL 8.3 docs <https://docs.lvgl.io/8.3/>`__
- `LVGL Online Font Converter <https://lvgl.io/tools/fontconverter/>`__
- :ghedit:`Edit`
