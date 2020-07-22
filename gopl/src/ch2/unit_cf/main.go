package main

import (
	"fmt"
	"ch2/unitconv"
	"os"
	"strconv"
)

func main() {
	for _, arg := range os.Args[1:] {
		t, err := strconv.ParseFloat(arg, 64)
		if err != nil {
			fmt.Fprintf(os.Stderr, "cf: %v\n", err)
			os.Exit(1)
		}
		f := unitconv.Foot(t)
		m := unitconv.Metre(t)
		fmt.Printf("%s = %s, %s = %s\n",
		    f, unitconv.FToM(f), m, unitconv.MToF(m))
		p := unitconv.Pound(t)
		k := unitconv.Kilogram(t)
		fmt.Printf("%s = %s, %s = %s\n",
		    p, unitconv.PToK(p), k, unitconv.KToP(k))
	}
}