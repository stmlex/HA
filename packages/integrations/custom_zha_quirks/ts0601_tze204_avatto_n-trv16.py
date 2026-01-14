from zigpy.quirks.v2 import EntityType, EntityPlatform
from zigpy.quirks.v2.homeassistant import UnitOfTemperature
from zigpy.quirks.v2.homeassistant.binary_sensor import BinarySensorDeviceClass
from zigpy.zcl.clusters.hvac import RunningState, Thermostat
from zhaquirks.tuya import (
    PowerConfiguration,
    TuyaLocalCluster,
    TuyaPowerConfigurationCluster3AA
)
from zhaquirks.tuya.mcu import TuyaAttributesCluster
import zigpy.types as t

class PresetMode(t.enum8):
    """PresetMode Enum."""

    Manual = 0x00
    Schedule = 0x01
    Eco = 0x02
    Comfort = 0x03
    FrostProtection = 0x04
    Holiday = 0x05
    Off = 0x06

class TuyaThermostat(Thermostat, TuyaAttributesCluster):
    """Tuya local thermostat cluster."""

    _CONSTANT_ATTRIBUTES = {
        Thermostat.AttributeDefs.ctrl_sequence_of_oper.id: Thermostat.ControlSequenceOfOperation.Heating_Only
    }

    def __init__(self, *args, **kwargs):
        """Init a TuyaThermostat cluster."""
        super().__init__(*args, **kwargs)
        self.add_unsupported_attribute(
            Thermostat.AttributeDefs.setpoint_change_source.id
        )
        self.add_unsupported_attribute(
            Thermostat.AttributeDefs.setpoint_change_source_timestamp.id
        )
        self.add_unsupported_attribute(Thermostat.AttributeDefs.pi_heating_demand.id)

from zhaquirks.tuya.builder import TuyaQuirkBuilder
(
    TuyaQuirkBuilder("_TZE204_vjpaih9f", "TS0601")
    .tuya_enum(
        dp_id=2,
        attribute_name="preset_mode",
        enum_class=PresetMode,
        translation_key="preset_mode",
        fallback_name="Preset mode",
    )
    .tuya_dp(
        dp_id=3,
        ep_attribute=TuyaThermostat.ep_attribute,
        attribute_name=TuyaThermostat.AttributeDefs.running_state.name,
        converter=lambda x: RunningState.Heat_State_On if x else RunningState.Idle,
    )
    .tuya_dp(
        dp_id=4,
        ep_attribute=TuyaThermostat.ep_attribute,
        attribute_name=TuyaThermostat.AttributeDefs.occupied_heating_setpoint.name,
        converter=lambda x: x * 10,
        dp_converter=lambda x: x // 10,
    )
    .tuya_dp(
        dp_id=5,
        ep_attribute=TuyaThermostat.ep_attribute,
        attribute_name=TuyaThermostat.AttributeDefs.local_temperature.name,
        converter=lambda x: x * 10,
    )
    .tuya_battery(dp_id=6, power_cfg=TuyaPowerConfigurationCluster3AA)
    .tuya_switch(
        dp_id=7,
        attribute_name="child_lock",
        translation_key="child_lock",
        fallback_name="Child lock",
    )
    .tuya_switch(
        dp_id=14,
        attribute_name="window_detection",
        translation_key="window_detection",
        fallback_name="Window Detection",
    )
    .tuya_binary_sensor(
        dp_id=15, 
        attribute_name="window_open", 
        translation_key="window_open", 
        fallback_name="Window Open",
        entity_type=EntityType.STANDARD,
        device_class=BinarySensorDeviceClass.WINDOW,
    )
    .tuya_number(
        dp_id=21,
        attribute_name="holiday_temperature",
        type=t.int32s,
        min_value=5,
        max_value=35,
        unit=UnitOfTemperature.CELSIUS,
        step=0.5,
        multiplier=0.1,
        translation_key="holiday_temperature",
        fallback_name="Holiday Temperature",
    )
    .tuya_binary_sensor(
        dp_id=35, 
        attribute_name="battery_low", 
        translation_key="battery_low", 
        fallback_name="Battery Low",
        entity_type=EntityType.DIAGNOSTIC,
        device_class=BinarySensorDeviceClass.BATTERY,
    )
    .tuya_switch(
        dp_id=36,
        attribute_name="frost_protection",
        translation_key="frost_protection",
        fallback_name="Frost protection",
    )
    .tuya_number(
        dp_id=47,
        attribute_name=TuyaThermostat.AttributeDefs.local_temperature_calibration.name,
        type=t.int32s,
        min_value=-9.5,
        max_value=9.5,
        unit=UnitOfTemperature.CELSIUS,
        step=0.5,
        multiplier=0.1,
        translation_key="local_temperature_calibration",
        fallback_name="Local temperature calibration",
    )
    .tuya_number(
        dp_id=103,
        attribute_name="eco_temperature",
        type=t.int32s,
        min_value=5,
        max_value=35,
        unit=UnitOfTemperature.CELSIUS,
        step=0.5,
        multiplier=0.1,
        translation_key="eco_temperature",
        fallback_name="Eco Temperature",
    )
    .tuya_number(
        dp_id=104,
        attribute_name="comfort_temperature",
        type=t.int32s,
        min_value=5,
        max_value=35,
        unit=UnitOfTemperature.CELSIUS,
        step=0.5,
        multiplier=0.1,
        translation_key="comfort_temperature",
        fallback_name="Comfort Temperature",
    )
    .tuya_number(
        dp_id=105,
        attribute_name="frost_protection_temperature",
        type=t.int32s,
        min_value=5,
        max_value=35,
        unit=UnitOfTemperature.CELSIUS,
        step=0.5,
        multiplier=0.1,
        translation_key="frost_protection_temperature",
        fallback_name="Frost Protection Temperature",
    )
    .adds(TuyaThermostat)
    .skip_configuration()
    .add_to_registry()
)
