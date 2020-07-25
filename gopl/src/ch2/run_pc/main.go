package main

import (
	"fmt"
	"ch2/popcount"
)

func main() {
	var x uint64 = 0b1101111111101011
	fmt.Printf("%d 的二进制有 %d 个 1。", x, popcount.Popcount4(x))
}
