.. _lvgl-main:

LVGL
====

.. seo::
    :description: LVGL - ESPHome Displays showing contents created with Light and Versatile Graphics Library


`LVGL <https://lvgl.io/>`__ (Light and Versatile Graphics Library) is a most free and open-source 
embedded graphics library to create beautiful UIs for any MCU, MPU and display type. ESPHome supports
`LVGL version 8.3.9 <https://docs.lvgl.io/8.3/>`__.

.. figure:: /images/logo_lvgl.png
    :align: center



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

- **log_level** (*Optional*): Set the logger level specifically for the messages of the lvgl component.
- **color_depth** (**Required**, int8): The color deph at which the contents are generated. Valid values are 1 (monochrome), 8, 16 or 32.
- **bg_color** (*Optional*, :ref:`color <config-color>`): A basic background color, to draw contents on.
- **text_font** (**Required**, :ref:`font <display-fonts>`): The ID of the font used to render textual contents by default on all *lvgl* widget.
- **touchscreens** (*Optional*, list): IDs of touchscreens interacting with the *lvgl* widget on the screen.
- **style_definitions** (*Optional*, list): A list of style definitions to use with *lvgl* widget:
    - **id** (*Optional*, :ref:`config-id`): Set the ID of this style definition.
    - **line_color** (*Optional*, :ref:`color <config-color>`): The ID of a color you want to use for lines. If not specified, defaults to ???
    - **line_width** (*Optional*, int16): The desired width of the line, in pixels. Defaults to ???
    - **line_rounded** (*Optional*, boolean): Draw the end of the lines rounded. Defaults to ???
    - **text_font** (*Optional*, :ref:`font <display-fonts>`):  The ID of the font used to override the render of textual contents on *lvgl* widget using this style. 
    - **align** (*Optional*): The alignment of the text within the object. Possible values: ``left``, ``center``, ``right``. Defaults to ``center``.
    - **text_color** (*Optional*, :ref:`color <config-color>`): The ID of a color for text rendering.
    - **bg_opa**(*Optional*): The opacity of the background of the widget. ???
    - **radius** (*Optional*, uint16): The radius of the rounded corners of the object. 0 = no radius i.e. square corners; 65535 = pill shaped object (true circle if object has same width and height)
    - **pad_all** (*Optional*, int16): Paddigng of all the edges of the widget. Default based on widget type.
- **layout** (*Optional*): ???
- **width** (*Optional*, percentage): Percentage of the screen width used by *lvgl*.
- **height** (*Optional*, percentage): Percentage of the screen height used by *lvgl*.
- **widgets** (*Optional*, list): A list of *lvgl* widgets to be drawn on the screen.
    - :ref:`Widgets <lvgl-widgets>` (**Required**): ``btn``, ``img``, ???
    - **widgets** (*Optional*, list): A list of *lvgl* widgets to be drawn as children of this widget. Configuration options are is the same as the parent widgets, and values aren inherited.
    - **id** (*Optional*, :ref:`config-id`): Set the ID of this widget.
    - **x** (**Required**, int16): Horizontal position of the widget (anchored in the top left corner). Can be a negative value, and it's relative to the screen.
    - **y** (**Required**, int16): Vertical position of the widget (anchored in the top left corner). Can be a negative value, and it's relative to the screen.
    - **w** (**Required**, int16): Width of the widget (anchored in the top left corner). 
    - **h** (**Required**, int16): Height of the widget (anchored in the top left corner). 
    - **enabled** (*Optional*, boolean): Widget is touchable, if ``false``, a _disabled_ style is applied. Defaults to ``true``.
    - **hidden** (*Optional*, boolean): Widget is hidden. Defaults to ``false``.
    - **opacity** (*Optional*, uint8): How much the the widget is opaque (0-255).
    - **click** (*Optional*, boolean): Widget is touch/clickable (also see ``enabled``). Defaults to ``true``.
    - **ext_click_h** (*Optional*, uint8): Extended horizontal clickable area on the left and right. Defaults to ``0``.
    - **ext_click_v** (*Optional*, uint8): Extended vertical clickable area on the top and bottom. Defaults to ``0``.


.. note::

    By default, LVGL draws new widgets on top of old widgets, including their children. 



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

  - **bg_color10** (*Optional*, :ref:`color <config-color>`): The ID of a color for indicator
  - **bg_color20** (*Optional*, :ref:`color <config-color>`): The ID of a color for knob
  - **radius20** (*Optional*, int16): Knob corner radius


**Checkbox**: ``checkbox``

  - **text** (*Optional*, string): The label of the checkbox. Defaults to "Checkbox"


**Progress Bar**: ``bar``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``
  - **start_value** (*Optional*, int16): Minimal allowed value of the indicator. Defaults to ``0``

**Slider**: ``slider``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``
  - **start_value** (*Optional*, int16): Minimal allowed value of the indicator. Defaults to ``0``

**Arc**: ``arc``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``
  - **rotation** (*Optional*, int16): Offset to the 0 degree position. Defaults to ``0``
  - **type** (*Optional*, 0-2): ``0`` = normal, ``1`` = symmetrical, ``2`` = reverse. Defaults to ``0``
  - **adjustable** (*Optional*, boolean): Add a knob that the user can move to change the value. Defaults to ``false``
  - **start_angle** (*Optional*, 0-360): start angle of the arc background (see note)
  - **end_angle** (*Optional*, 0-360): end angle of the arc background (see note)
  - **start_angle10** (*Optional*, 0-360): start angle of the arc indicator (see note)
  - **end_angle10** (*Optional*, 0-360): end angle of the arc indicator (see note)

  .. note::

      Zero degree is at the middle right (3 o'clock) of the object and the degrees are increasing in a clockwise direction. The angles should be in the [0-360] range. 


**Dropdown List**: ``dropdown``

  - **options** (*Optional*, string): List of items separated by ``\n``. Defaults to "" (empty).
  - **text** (*Optional*, string): *Read-only* The text of the selected item. Defaults to "" (empty).
  - **direction** (*Optional*, 0-3): Direction where the dropdown expands: ``0`` = down, ``1`` = up, ``2`` = left, ``3`` = right. *Note:* up and down are superseeded by the screen size.
  - **show_selected** (*Optional*, boolean): Show the selected option or a static text. Defaults to ``true``
  - **max_height** (*Optional*, int16): The maximum height of the open drop-down list. Defaults to 3/4 of screen height


**Roller**: ``roller``

  - **options** (*Optional*, string): List of items separated by ``\n``. Defaults to "" (empty).
  - **text** (*Optional*, string): *Read-only* The text of the selected item. Defaults to "" (empty).
  - **rows** (*Optional*, int8): The number of rows that are visible. Use this property instead of ``h`` to set object height! Defaults to ``3``.
  - **mode** (*Optional*, 0-1): Roller mode: ``0`` = normal (finite), ``1`` = infinite. Defaults to ``0``.
  - **align** (*Optional*, string): Text alignment: ``left``, ``center``, ``right``. Defaults to ``center``


**Line Meter**: ``linemeter``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``.
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``.
  - **angle** (*Optional*, 0-360): Angle between start and end of the scale. Defaults to ``240``.
  - **line_count** (*Optional*, uint16): Rick count of the scale. Defaults to ``31``.
  - **rotation** (*Optional*, 0-360): Offset for the scale angles to rotate it. Defaults to ``0``.
  - **type** (*Optional*, 0-1): ``0`` = indicator lines are activated clock-wise, ``1`` = indicator lines are activated counter-clock-wise. Defaults to ``0``.

**Gauge**: ``gauge``

  - **min** (*Optional*, int16): Minimum value of the indicator. Defaults to ``0``.
  - **max** (*Optional*, int16): Maximum value of the indicator. Defaults to ``100``.
  - **critical_value** (*Optional*, int16): Scale color will be changed to scale_end_color after this value. Defaults to ``80``.
  - **scale_end_color**: (*Optional*, :ref:`color <config-color>`): The ID of a color for values above critical.
  - **label_count** (*Optional*, uint8): Number of labels (and major ticks) of the scale. Defaults to ``0``.
  - **line_count** (*Optional*, uint16): Number of minor ticks of the entire scale. Defaults to ``31``.
  - **angle** (*Optional*, 0-360): Angle between start and end of the scale. Defaults to ``240``.
  - **rotation** (*Optional*, 0-360): Offset for the gauge's angles to rotate it. Defaults to ``0``.
  - **scale** ???
  - **format** (*Optional*, uint16): Divider for major tick values. Defaults to ``0``.

  .. note::

      To strip trailing zero's of major tick labels the ``format`` divider can be used to scale the values before printing:
      
        - ``0`` : print the major tick value as is
        - ``1`` : strip 1 zero, i.e. divide tick value by 10 before printing the major tick label
        - ``2`` : strip 2 zeros, i.e. divide tick value by 100 before printing the major tick label
        - ``3`` : strip 3 zeros, i.e. divide tick value by 1000 before printing the major tick label
        - ``4`` : strip 4 zeros, i.e. divide tick value by 10000 before printing the major tick label

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
- :ghedit:`Edit`
