#include "esphome.h"

using namespace esphome;

class MyCustomSensor : public PollingComponent, public Sensor {
 public:
  MyCustomSensor() : PollingComponent(15000) {}

  void setup() override {
    // This will be called by App.setup()
  }
  void update() override {
    publish_state(42.0);
  }
};
