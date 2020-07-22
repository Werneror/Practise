package unitconv

// FtoM converts a Foot to Metre.
func FToM(f Foot) Metre { return Metre(0.3048*f) }

// MtoF converts a Metre to Foot.
func MToF(m Metre) Foot { return Foot(3.28084*m) }

// PtoK converts a Pound to Kilogram.
func PToK(p Pound) Kilogram { return Kilogram(0.4535923*p) }

// KtoP converts a Kilogram to Pound.
func KToP(k Kilogram) Pound { return Pound(2.204623*k) }
