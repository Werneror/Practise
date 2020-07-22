// Package unitconv performs unit conversions.

package unitconv

import "fmt"

type Foot float64
type Metre float64
type Pound float64
type Kilogram float64

func (f Foot) String() string { return fmt.Sprintf("%g ft", f)}
func (m Metre) String() string { return fmt.Sprintf("%g M", m)}

func (p Pound) String() string { return fmt.Sprintf("%g ib", p)}
func (k Kilogram) String() string { return fmt.Sprintf("%g kg", k)}
