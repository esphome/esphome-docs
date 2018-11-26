#include "esphomelib.h"

using namespace esphomelib;

class MyCustomSensor : public PollingComponent, public sensor::Sensor {
 public:
  MyCustomSensor() : PollingComponent(15000) {}

  void setup() override {
    // This will be called by App.setup()
  }
  void update() override {
    publish_state(42.0);
  }
};
