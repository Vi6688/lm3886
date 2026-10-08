import math


def amplifier_calculations(
    Pout: float,
    RL: float,
    Vin: float = 1.0,
    Rf: float = 100_000,
    headroom: float = 4.0,
    tolerance: float = 0.15,
    margin: float = 1.1,
    fl_audio: float = 20,
    fh_audio: float = 20_000,
    input_impedance: float = 10_000,
    minimum_gain: float = 10.0,
) -> dict[str, float | bool | list[str]]:
    """Calculate first-pass values for a single-supply LM3886 amplifier.

    Voltages and Vin are RMS unless stated otherwise; resistance is in ohms,
    power in watts, and frequencies in hertz.
    """
    positive_values = {
        "Pout": Pout,
        "RL": RL,
        "Vin": Vin,
        "Rf": Rf,
        "margin": margin,
        "fl_audio": fl_audio,
        "fh_audio": fh_audio,
        "input_impedance": input_impedance,
        "minimum_gain": minimum_gain,
    }
    for name, value in positive_values.items():
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a finite positive number")
    if not math.isfinite(headroom) or headroom < 0:
        raise ValueError("headroom must be a finite non-negative number")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be a finite non-negative number")
    if fh_audio <= fl_audio:
        raise ValueError("fh_audio must be greater than fl_audio")
    if minimum_gain < 10:
        raise ValueError("minimum_gain must be at least 10 for LM3886 stability")

    # Output is centered at half the single supply, so both half-cycles need
    # the same output swing plus headroom to a supply rail.
    Vout_peak = math.sqrt(2 * Pout * RL)
    Iout_peak = math.sqrt(2 * Pout / RL)
    V_supply = 2 * (Vout_peak + headroom) * (1 + tolerance) * margin
    V_bias = V_supply / 2

    required_gain = math.sqrt(Pout * RL) / Vin
    Av = max(required_gain, minimum_gain)
    Ri = Rf / (Av - 1)

    # Five-times bandwidth margin from the specified audio band edges.
    fl = fl_audio / 5
    fh = fh_audio * 5
    GBWP_required = Av * fh

    Ci = 1 / (2 * math.pi * input_impedance * fl)
    Cout = 1 / (2 * math.pi * RL * fl)

    warnings = []
    if not 20 <= V_supply <= 84:
        warnings.append(
            "Calculated supply is outside the LM3886 datasheet's 20-84 V "
            "total-supply operating range."
        )
    if GBWP_required > 2_000_000:
        warnings.append(
            "Required gain-bandwidth product exceeds the LM3886 minimum "
            "specified value of 2 MHz."
        )
    warnings.append(
        "Check the datasheet power-dissipation/thermal curves and heatsink; "
        "the voltage and current estimates do not guarantee the requested "
        "continuous output power."
    )

    results: dict[str, float | bool | list[str]] = {
        "output_power_w": Pout,
        "load_resistance_ohm": RL,
        "output_voltage_peak_v": Vout_peak,
        "output_current_peak_a": Iout_peak,
        "single_supply_voltage_v": V_supply,
        "midpoint_bias_voltage_v": V_bias,
        "voltage_gain_v_per_v": Av,
        "input_sensitivity_v_rms": math.sqrt(Pout * RL) / Av,
        "feedback_resistor_rf_ohm": Rf,
        "gain_resistor_ri_ohm": Ri,
        "input_impedance_ohm": input_impedance,
        "low_cutoff_hz": fl,
        "high_cutoff_hz": fh,
        "minimum_gain_bandwidth_hz": GBWP_required,
        "input_coupling_capacitance_f": Ci,
        "output_coupling_capacitance_f": Cout,
        "output_capacitor_voltage_rating_min_v": V_supply,
        "supply_within_datasheet_range": 20 <= V_supply <= 84,
        "gain_bandwidth_within_lm3886_minimum": GBWP_required <= 2_000_000,
        "warnings": warnings,
    }

    print("\n=== SINGLE-SUPPLY LM3886 CALCULATIONS ===\n")
    print(f"Output power                 : {Pout:.2f} W into {RL:.2f} Ω")
    print(f"Output voltage (peak)        : {Vout_peak:.2f} V")
    print(f"Output current (peak)         : {Iout_peak:.2f} A")
    print(f"Estimated single supply      : {V_supply:.2f} V DC")
    print(f"Signal/reference midpoint    : {V_bias:.2f} V")
    print(f"Voltage gain                 : {Av:.2f} V/V")
    print(f"Gain-setting Rf / Ri         : {Rf / 1000:.2f} kΩ / {Ri / 1000:.2f} kΩ")
    print(f"Input coupling capacitor     : {Ci * 1e6:.2f} µF minimum")
    print(f"Speaker coupling capacitor   : {Cout * 1e6:.2f} µF minimum")
    print(f"Output capacitor rating      : at least {V_supply:.2f} V")
    print(f"Required gain-bandwidth      : {GBWP_required / 1e6:.2f} MHz")
    for warning in warnings:
        print(f"Warning: {warning}")
    print("\n==========================================\n")

    return results


if __name__ == "__main__":
    amplifier_calculations(Pout=30, RL=4)
