// Package tempconv performs Celsius and Fahrenheit temperature computations.

package main


import "fmt"

type Celsius float64    // 摄氏温度
type Fahrenheit float64    // 华氏温度

const (
	AbsolutZeroC Celsius = -273.15 // 绝对零度
	FreezingC Celsius = 0 // 冰点温度
	BoilingC Celsius = 100 // 沸点温度
)

func CToF(c Celsius) Fahrenheit { return Fahrenheit(c*9/5 + 32) }

func FToC(f Fahrenheit) Celsius { return Celsius((f-32) * 5 /9 )}

func (c Celsius) Strings() string { return fmt.Sprintf("%g°C", c)}

func main() {
	fmt.Printf("%g\n", BoilingC-FreezingC)
	boilingF := CToF(BoilingC)
	fmt.Printf("%g\n", boilingF-CToF(FreezingC))
	fmt.Printf(BoilingC.Strings())
}