import math

def amplifier_calculations(Pout, RL, Vin=1.0, Rf=100_000,
                           headroom=4.0, tolerance=0.15, margin=1.1,
                           fl_audio=20, fh_audio=20_000):

    print("\n=== AUDIO POWER AMPLIFIER CALCULATIONS ===\n")

    # Peak output voltage & current
    Vout_peak = math.sqrt(2 * Pout * RL)
    Iout_peak = math.sqrt(2 * Pout / RL)

    # Max supply voltage
    V_supply = (Vout_peak + headroom) * (1 + tolerance) * margin

    # Voltage gain
    Av = math.sqrt(Pout * RL) / Vin

    # Input resistance (non-inverting)
    Rin = Rf / (Av - 1)

    # Bandwidth design (5× rule)
    fl = fl_audio / 5
    fh = fh_audio * 5

    # Gain Bandwidth Product
    GBWP_required = Av * fh

    # Input coupling capacitor
    Ci = 1 / (2 * math.pi * Rin * fl)

    # Print results neatly
    print(f"Output Power               : {Pout:.2f} W")
    print(f"Load Resistance            : {RL:.2f} Ω\n")

    print(f"Output Voltage (Peak)      : {Vout_peak:.2f} V")
    print(f"Output Current (Peak)      : {Iout_peak:.2f} A\n")

    print(f"Required Supply Voltage    : ±{V_supply:.2f} V\n")

    print(f"Required Voltage Gain      : {Av:.2f} V/V (~{math.ceil(Av)})")
    print(f"Feedback Resistor (Rf)     : {Rf/1000:.1f} kΩ")
    print(f"Input Resistance (Rin)     : {Rin/1000:.2f} kΩ\n")

    print("Bandwidth Requirements:")
    print(f"  Low cutoff frequency     : {fl:.2f} Hz")
    print(f"  High cutoff frequency    : {fh/1000:.2f} kHz\n")

    print(f"Minimum GBWP Required      : {GBWP_required/1e6:.2f} MHz")
    print("LM3886 GBWP (min)          : 2.00 MHz\n")

    print(f"Input Coupling Capacitor   : {Ci*1e6:.2f} µF (~4.7 µF standard)")

    print("\n========================================\n")


# Example usage
amplifier_calculations(Pout=68, RL=4)