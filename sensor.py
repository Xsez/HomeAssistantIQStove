"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntries
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, SCAN_INTERVAL
from .coordinator import IQStoveCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensors from a config entry created in the integrations UI."""
    print("Sensor Async Setup")
    coordinator: IQStoveCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = [temperatureSensor(coordinator)]
    async_add_entities(sensors, update_before_add=True)


class temperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator: IQStoveCoordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        print("Temperaturesensor init")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        print("Sensor Handle Coordinator Update", self.coordinator.data)
        self._attr_native_value = self.coordinator.data["appT"]
        self.async_write_ha_state()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{DOMAIN}-temperature"

    @property
    def native_value(self) -> int | float:
        """Return the state of the entity."""
        # Using native value and native unit of measurement, allows you to change units
        # in Lovelace and HA will automatically calculate the correct value.
        # await self.coordinator.async_request_refresh()
        print("Sensor Native Value", self.coordinator.data["appT"])
        # return float(self.coordinator.getValue("appT"))
        return float(self.coordinator.data["appT"])

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return unit of temperature."""
        return UnitOfTemperature.CELSIUS

    @property
    def state_class(self) -> str | None:
        """Return state class."""
        # https://developers.home-assistant.io/docs/core/entity/sensor/#available-state-classes
        return SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-temperature"

    # @property
    # def device_info(self):
    #     """Return device information about this entity."""
    #     return {
    #         "identifiers": {
    #             # Unique identifiers within a specific domain
    #             (DOMAIN, 1234)
    #         },
    #         "manufacturer": "Hase",
    #         "model": 123,
    #         "name": "Stove 123",
    #     }


# # class phaseSensor(SensorEntity):
# #     """Phase Sensor."""

# #     _attr_name = "IQStove Phase"
# #     _attr_device_class = SensorDeviceClass.ENUM
# #     _attr_options = ["idle", "heating up", "burning", "add wood", "don't add wood"]
# #     _attr_unique_id = f"stove{stove.serial}+{_attr_name}"

# #     def update(self) -> None:
# #         """Fetch new state data for the sensor.

# #         This is the only method that should fetch new data for Home Assistant.
# #         """
# #         # phase = stove.phase
# #         # self._attr_native_value = self._attr_options[int(phase)]
# #         # if (int(phase) == 0):
# #         #     self._attr_icon = "mdi:fireplace-off"
# #         # else:
# #         #     self._attr_icon = "mdi:fireplace"

# #     @property
# #     def device_info(self):
# #         """Return device information about this entity."""
# #         return {
# #             "identifiers": {
# #                 # Unique identifiers within a specific domain
# #                 (DOMAIN, stove.serial)
# #             }
# #         }


# # class performanceSensor(SensorEntity):
# #     """Performance Sensor."""

# #     _attr_name = "IQStove Performance"
# #     _attr_native_unit_of_measurement = PERCENTAGE
# #     _attr_state_class = SensorStateClass.MEASUREMENT
# #     _attr_unique_id = f"stove{stove.serial}+{_attr_name}"
# #     _attr_icon = "mdi:gauge"

# #     def update(self) -> None:
# #         """Fetch new state data for the sensor.

# #         This is the only method that should fetch new data for Home Assistant.
# #         """

# #         # self._attr_native_value = stove.performance

# #     @property
# #     def device_info(self):
# #         """Return device information about this entity."""
# #         return {
# #             "identifiers": {
# #                 # Unique identifiers within a specific domain
# #                 (DOMAIN, stove.serial)
# #             }
# #         }


# # class heatingUpSensor(SensorEntity):
# #     """Performance Sensor."""

# #     _attr_name = "IQStove Heating Up"
# #     _attr_native_unit_of_measurement = PERCENTAGE
# #     _attr_state_class = SensorStateClass.MEASUREMENT
# #     _attr_unique_id = f"stove{stove.serial}+{_attr_name}"
# #     _attr_icon = "mdi:elevation-rise"

# #     def update(self) -> None:
# #         """Fetch new state data for the sensor.

# #         This is the only method that should fetch new data for Home Assistant.
# #         """

# #         # self._attr_native_value = stove.heatingPercentage

# #     @property
# #     def device_info(self):
# #         """Return device information about this entity."""
# #         return {
# #             "identifiers": {
# #                 # Unique identifiers within a specific domain
# #                 (DOMAIN, stove.serial)
# #             }
# #         }
