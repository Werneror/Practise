package main

import (
	"fmt"
	"crypto/sha256"
)

func zero(ptr [4]int) {
	ptr[0] = 0
	ptr[1] = 0
	ptr[2] = 0
	ptr[3] = 0
}

func diffBitCount(c1 [32]uint8, c2 [32]uint8) int {
	count := 0
	for i, v := range c1 {
		if v != c2[i] {
			count += 1
		}
	}
	return count
}

func main() {
	var a [3]int
	fmt.Println(a[0])            // 第一个元素
	fmt.Println(a[len(a)-1]) // 最后一个元素

	// 打印索引和元素
	for i , v := range a{
		fmt.Printf("%d %d\n", i, v)
	}

	// 只打印元素
	for _, v := range a {
		fmt.Printf("%d\n", v)
	}

	var q [3]int = [3]int{1, 2, 3}
	var r [3]int = [3]int{1, 2}
	fmt.Println(q)
	fmt.Println(r[2])  // 0

	p := [...]int{1, 2, 3}
	fmt.Printf("%T\n", p)  // [3]int

	type Currency int
	const (
		USB Currency = iota // 美元
		EUR                            // 欧元
		GBP                            // 英镑
		RMB                           // 人民币
	)

	symbol := [...]string{USB: "$", EUR: "€", GBP: "￡", RMB: "￥"}
	fmt.Println(RMB, symbol[RMB])

	t := [...]int{1, 2, 3, 4}
	zero(t)
	fmt.Println(t)


	c1 := sha256.Sum256([]byte("x"))
	c2 := sha256.Sum256([]byte("Z"))
	fmt.Println(c1)
	fmt.Println(c2)
	fmt.Println(diffBitCount(c1, c2))
}