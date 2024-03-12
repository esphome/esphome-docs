.. _display-fonts:

Font Renderer Component
=======================

.. seo::
    :description: Instructions for setting up fonts in ESPHome.
    :image: format-font.svg

ESPHome's graphical rendering engine also has a powerful font drawer which integrates seamlessly into the system. You have the option to use **any** OpenType/TrueType (``.ttf``, ``.otf``, ``.woff``) font file at **any** size, as well as fixed-size `PCF <https://en.wikipedia.org/wiki/Portable_Compiled_Format>`_ and `BDF <https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format>`_ bitmap fonts.

These fonts can be used in ESPHome's :ref:`own rendering engine <display-engine>`.

To use fonts you can either
 - Just grab a ``.ttf``, ``.otf``, ``.woff``, ``.pcf``, or ``.bdf`` file from somewhere on the internet and place it, for example, inside a ``fonts`` folder next to your configuration file.
 - Use the ``gfonts://`` short form to use Google Fonts directly.
 - Load a font from a URL directly on build.

Next, create a ``font:`` section in your configuration:

.. code-block:: yaml

    # Various ways to configure fonts
    font:
      - file: "fonts/Comic Sans MS.ttf"
        id: my_font
        size: 20
        bpp: 2

      - file: "fonts/tom-thumb.bdf"
        id: tomthumb

        # gfonts://family[@weight]
      - file: "gfonts://Roboto"
        id: roboto_20
        size: 20

      - file:
          type: gfonts
          family: Roboto
          weight: 900
        id: roboto_16
        size: 16

      - file: "gfonts://Material+Symbols+Outlined"
        id: icons_50
        size: 50
        glyphs: ["\U0000e425"] # mdi-timer

      - file: "fonts/RobotoCondensed-Regular.ttf"
        id: roboto_special_28
        size: 28
        bpp: 4
        glyphs: [
          a,A,á,Á,e,E,é,É,
          (,),+,-,_,.,°,•,µ,
          "\u0020", #space
          "\u0021", #!
          "\u0022", #"
          "\u0027", #'
          ]

      - file: "fonts/RobotoCondensed-Regular.ttf"
        id: my_font_with_icons
        size: 20
        bpp: 4
        extras:
          - file: "fonts/materialdesignicons-webfont.ttf"
            glyphs: [
              "\U000F02D1", # mdi-heart
              "\U000F05D4", # mdi-airplane-landing
              ]

      - file: "https://github.com/IdreesInc/Monocraft/releases/download/v3.0/Monocraft.ttf"
        id: web_font
        size: 20
      - file:
          url: "https://github.com/IdreesInc/Monocraft/releases/download/v3.0/Monocraft.ttf"
          type: web
        id: web_font2
        size: 24

    display:
      # ...

Configuration variables:
------------------------

- **file** (**Required**, string): The path (relative to where the .yaml file is) of the font
  file. You can also use the ``gfonts://`` short form to use Google Fonts, or use the below structure:

  - **type** (**Required**, string): Can be ``local``, ``gfonts`` or ``web``.

  **Local Fonts**:

  - **path** (**Required**, string): The path (relative to where the .yaml file is) of the OpenType/TrueType or bitmap font file.

  **Google Fonts**:

    Each Google Font will be downloaded once and cached for future use. This can also be used to download Material
    Symbols or Icons as in the example above.

  - **family** (**Required**, string): The name of the Google Font family.
  - **italic** (*Optional*, boolean): Whether the font should be italic.
  - **weight** (*Optional*, enum): The weight of the font. Can be either the text name or the integer value:
      - **thin**: 100
      - **extra-light**: 200
      - **light**: 300
      - **regular**: 400 (**default**)
      - **medium**: 500
      - **semi-bold**: 600
      - **bold**: 700
      - **extra-bold**: 800
      - **black**: 900

  **Web Fonts**:

  - **url** (**Required**, string): The URL of the TrueType or bitmap font file.

- **id** (**Required**, :ref:`config-id`): The ID with which you will be able to reference the font later
  in your display code.
- **size** (*Optional*, int): The size of the font in pt (not pixel!).
  If you want to use the same font in different sizes, create two font objects. Note: *size* is ignored
  by bitmap fonts. Defaults to ``20``.
- **bpp** (*Optional*, int): The bit depth of the rendered font from OpenType/TrueType, for anti-aliasing. Can be ``1``, ``2``, ``4``, ``8``. Defaults to ``1``.
- **glyphs** (*Optional*, list): A list of characters you plan to use. Only the characters you specify
  here will be compiled into the binary. Adjust this if you need some special characters or want to
  reduce the size of the binary if you don't plan to use some glyphs. You can also specify glyphs by their codepoint (see below). Defaults to ``!"%()+=,-_.:°/?0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz``.
- **extras** (*Optional*, enum): A list of font glyph configurations you'd like to include within this font, from other OpenType/TrueType files (eg. icons from other font, but at the same size as the main font):

  - **file** (**Required**, string): The path of the font file with the extra glyphs.
  - **glyphs** (**Required**, list): A list of glyphs you want to include. Can't repeat the same glyph codepoint if it was declared in the level above.

.. note::

    OpenType/TrueType font files offer icons at codepoints far from what's reachable on a standard keyboard, for these it's needed
    to specify the unicode codepoint of the glyph as a hex address escaped with ``\u`` or ``\U``.

    - Code points up to ``0xFFFF`` are encoded like ``\uE6E8``. Lowercase ``\u`` and exactly 4 hexadecimal digits.
    - Code points above ``0xFFFF`` are encoded like ``\U0001F5E9``. Capital ``\U`` and exactly 8 hexadecimal digits.

    The ``extras`` section only supports OpenType/TrueType files, ``size`` and ``bpp`` will be the same as the above level. This will allow printing icons alongside the characters in the same string, like ``I \uF004 You \uF001``.

    Many font sizes with multiple glyphs at high bit depths will increase the binary size considerably. Make your choices carefully.


.. note::

    To use fonts you will need to have the python ``pillow`` package installed, as ESPHome uses that package
    to translate the OpenType/TrueType and bitmap font files into an internal format. If you're running this as a Home Assistant add-on or with the official ESPHome docker image, it should already be installed. Otherwise you need
    to install it using ``pip install "pillow==10.2.0"``.

See Also
--------

- :apiref:`display/display_buffer.h`
- :ref:`display-engine`
- `MDI cheatsheet <https://pictogrammers.com/library/mdi/>`_
- `MDI font repository <https://github.com/Pictogrammers/pictogrammers.github.io/tree/main/%40mdi/font/>`_
- :ghedit:`Edit`
