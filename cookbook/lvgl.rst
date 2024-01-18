LVGL: Tips and Tricks
=====================

.. seo::
    :description: Recipes for common use cases of LVGL Displays with ESPHome
    :image: /images/logo_lvgl.png

Here are a couple recipes for various interesting things you can do with :ref:`lvgl-main` in ESPHome.

.. note::

    The examples below assume you've set up LVGL correctly with your display and input device, and you have the knowledge to set up various components in ESPHome.

.. _lvgl-cook-relay:

Toggle local light
------------------

If you have a display with GPIO outputs usable with local relays, you can simply create a wall switch for your light.

.. code-block:: yaml

    light:
      - platform: ...
        id: room_light
        name: 'Room light'
        on_state:
            if:
              condition:
                light.is_on: room_light
              then:
                - lvgl.widget.update:
                    id: light_btn
                    state:
                      checked: true
              else:
                - lvgl.widget.update:
                    id: light_btn
                    state:
                      checked: false

    lvgl:
        ...
        pages:
          - id: main_page
            widgets:
              - btn:
                  id: light_btn
                  align: center
                  width: 100
                  height: 70
                  checkable: true
                  widgets:
                    - label:
                        align: center
                        text: 'Room light'
                  on_click:
                    light.toggle: room_light

.. _lvgl-cook-binent:

Toggle remote light
-------------------

If you'd like to control a remote light, which appears as an entity in Home Assistant, first you need to import the light state into ESPHome, and then control it using a service call:

.. code-block:: yaml

    binary_sensor:
      - platform: homeassistant
        id: remote_light
        entity_id: light.remote_light
        on_state:
          then:
            if:
              condition:
                lambda: return x;
              then:
                - lvgl.widget.update:
                    id: light_switch
                    state:
                      checked: true
              else:
                - lvgl.widget.update:
                    id: light_switch
                    state:
                      checked: false

    lvgl:
        ...
        pages:
          - id: main_page
            widgets:
              - switch:
                  align: center
                  id: light_switch
                  on_click:
                    - homeassistant.service:
                        service: light.toggle
                        data: 
                          entity_id: light.remote_light

.. _lvgl-cook-cover:

Cover status and control
------------------------

To make a nice user interface for controlling covers you could use 3 buttons, which also display the state. 

.. figure:: images/lvgl_cook_cover.jpg
    :align: center

Just as above, we need to get the states of the cover first. With a numeric sensor we retrieve the current position of the cover, and wuth a text sensor we retrive the current movement state of it. We are particularly intersted in the moving (*opening* and *opening*) states, because during these we'd like to change the label on the middle to show *STOP*. Otherwise, this button label will show the percentage of the opening. Additionally, we'll change the opacity of the labels on the *UP* and *DOWN* buttons depending on if the cover is fully open or close.

.. code-block:: yaml

    sensor:
      - platform: homeassistant
        id: cover_myroom_pos
        entity_id: cover.myroom
        attribute: current_position
        on_value:
          - if:
              condition:
                lambda: |-
                  return x == 100;
              then:
                - lvgl.widget.update:
                    id: cov_up_myroom
                    text_opa: 50%
              else:
                - lvgl.widget.update:
                    id: cov_up_myroom
                    text_opa: 100%
          - if:
              condition:
                lambda: |-
                  return x == 0;
              then:
                - lvgl.widget.update:
                    id: cov_down_myroom
                    text_opa: 50%
              else:
                - lvgl.widget.update:
                    id: cov_down_myroom
                    text_opa: 100%

    text_sensor:
      - platform: homeassistant
        id: cover_myroom_state
        entity_id: cover.myroom
        on_value:
          - if:
              condition:
                lambda: |-
                  return ((0 == x.compare(std::string{"opening"})) or (0 == x.compare(std::string{"closing"})));
              then:
                - lvgl.label.update:
                    id: cov_stop_myroom
                    text: "STOP"
              else:
                - lvgl.label.update:
                    id: cov_stop_myroom
                    text: !lambda |-
                      static char buf[10];
                      snprintf(buf, 10, "%.0f%%", id(cover_myroom_pos).get_state());
                      return buf;

    lvgl:
        ...
        pages:
          - id: main_page
            widgets:
              - label:
                  x: 10
                  y: 6
                  width: 70
                  text: "My room"
                  text_align: center
              - btn:
                  x: 10
                  y: 30
                  width: 70
                  height: 68
                  widgets:
                    - label:
                        id: cov_up_myroom
                        align: center
                        symbol: UP
                  on_press:
                    then:
                      - homeassistant.service:
                          service: cover.open
                          data:
                            entity_id: cover.myroom
              - btn:
                  x: 10
                  y: 103
                  width: 70
                  height: 68
                  widgets:
                    - label:
                        id: cov_stop_myroom
                        align: center
                        text: STOP
                  on_press:
                    then:
                      - homeassistant.service:
                          service: cover.stop
                          data:
                            entity_id: cover.myroom
              - btn:
                  x: 10
                  y: 178
                  width: 70
                  height: 68
                  widgets:
                    - label:
                        id: cov_down_myroom
                        align: center
                        symbol: DOWN
                  on_press:
                    then:
                      - homeassistant.service:
                          service: cover.close
                          data:
                            entity_id: cover.myroom

.. _lvgl-cook-gradient:

Gradient styles for widgets
---------------------------

Since LVGL uses inheritance to apply styles across the widgets, it's possible to apply them at the top level, and only make modifications on demand, if necessarry. 

.. figure:: images/lvgl_cook_gradient_styles.jpg
    :align: center

In this example we prepare a set of gradient styles in the *theme*, and make some modifications in a *style_definition* which can be applied in a batch to the desired widgets. Theme is applied automatically, the style definition is applied manually.

.. code-block:: yaml

    lvgl:
      ...
      theme:
        btn:
          bg_color: 0x2F8CD8
          bg_grad_color: 0x005782 #0x006699
          bg_grad_dir: VER
          bg_opa: cover
          border_color: 0x0077b3
          border_width: 1
          text_color: 0xFFFFFF
          pressed:
            bg_color: 0x006699
            bg_grad_color: 0x00334d
          checked:
            bg_color: 0x1d5f96
            bg_grad_color: 0x03324A
            text_color: 0x005580
      style_definitions:
        - id: header_footer
          bg_color: 0x2F8CD8
          bg_grad_color: 0x005782 #0x004466
          bg_grad_dir: VER
          bg_opa: cover
          border_width: 0
          radius: 0
          pad_all: 0
          pad_row: 0
          pad_column: 0
          border_color: 0x0077b3
          text_color: 0xFFFFFF

.. _lvgl-cook-navigator:

Page navigation footer
----------------------

If using multiple pages, a navigation bar can be useful at the bottom of the screen:

.. figure:: images/lvgl_cook_pagenav.jpg
    :align: center

To save from repeating the same widgets on each page, there's the *top_layer* which is the *Always on Top* transparent page above all the pages. Everything you put on this page will be on top of all the others. 

For the navigation bar we use a button matrix. Note how the *header_footer* style definition is being applied to the widget and its children objects, and how a few more styles are configured to the main widget:

.. code-block:: yaml

    lvgl:
      ...
      top_layer:
        widgets:
          - btnmatrix:
              width: 100%
              height: 30px
              align: bottom_mid
              styles: header_footer
              pad_all: 0
              outline_width: 0
              id: top_layer
              items:
                styles: header_footer
              rows:
                - buttons:
                  - id: top_prev
                    symbol: left
                    on_press:
                      then:
                        lvgl.page.previous:
                  - id: top_home
                    symbol: home
                    on_press:
                      then:
                        lvgl.page.show: main_page
                  - id: top_next
                    symbol: right
                    on_press:
                      then:
                        lvgl.page.next:


.. _lvgl-cook-statico:

HA connection status icon
-------------------------

The top layer is useful to show status icons visible on all pages:

.. figure:: images/lvgl_cook_statico.jpg
    :align: center

In the example below we only show the icon when connection with Home Assistant is established:

.. code-block:: yaml

    api:
      on_client_connected:
        - if:
            condition:
              lambda: 'return (0 == client_address.compare(std::string{"your.ha.static.ip"}));'
            then:
              - lvgl.widget.show: lbl_hastatus
      on_client_disconnected:
        - if:
            condition:
              lambda: 'return (0 == client_address.compare(std::string{"your.ha.static.ip"}));'
            then:
              - lvgl.widget.hide: lbl_hastatus

    lvgl:
      ...
      top_layer:
        widgets:
          - label:
              symbol: WIFI
              id: lbl_hastatus
              hidden: true
              align: top_right
              x: -2
              y: 7
              text_align: right
              text_color: 0xFFFFFF

Two notable things here, the widget starts *hidden* at boot, and it's only shown when triggered by connection with the API, and alignment of the widget: since the *align* option is given, the *x* and *y* options are used to position the widget relative to the calculated position.

.. _lvgl-cook-titlebar:

Title bar for each page
-----------------------

Each page can have its own title bar

.. figure:: images/lvgl_cook_titlebar.jpg
    :align: center

To put a titlebar under the status icon, we need to add it to each page, also containing the label with a unique title:

.. code-block:: yaml

    lvgl:
      ...
      pages:
        - id: main_page
          widgets:
            - obj:
                align: TOP_MID
                width: 240
                height: 30
                styles: header_footer
                widgets:
                  - label:
                      text: "ESPHome LVGL Display"
                      align: center
                      text_align: center
                      text_color: 0xFFFFFF
            ...
        - id: second_page
          widgets:
            - obj:
                align: TOP_MID
                width: 240
                height: 30
                styles: header_footer
                widgets:
                  - label:
                      text: "A second page"
                      align: center
                      text_align: center
                      text_color: 0xFFFFFF
            ...


See Also
--------

- :ref:`lvgl-main`
- :ref:`config-lambda`
- :ref:`automation`

- :ghedit:`Edit`
