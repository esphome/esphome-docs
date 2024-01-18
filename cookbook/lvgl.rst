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




See Also
--------

- :ref:`lvgl-main`
- :ref:`config-lambda`
- :ref:`automation`

- :ghedit:`Edit`
