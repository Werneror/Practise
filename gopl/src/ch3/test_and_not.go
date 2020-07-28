// 测试 x&^y 和 x&(^)y 是否相同
package main

import "fmt"

func main() {
	var x uint8 = 2<<1 | 2<<5
	var y uint8 = 1<<3 | 4<<2
	fmt.Printf("%08b\n", x&^y)
	fmt.Printf("%08b\n", x&(^y))
}
