package main

import (
	"fmt"
)

func noAdjoinRepeat(strings []string) []string {
	previous := ""
	i  := 0
	for _, s := range(strings) {
		if previous != s{
			strings[i] = s
			i += 1
			previous = s
		}
	}
	return strings[:i]
}

func main() {
	data := []string{"aaa", "bbb", "bbb", "cc", "cc", "cc", "aaa"}
	fmt.Println("练习 4.5： 写一个函数在原地完成消除[]string中相邻重复的字符串的操作。")
	fmt.Println("input is", data)
	fmt.Println("output is", noAdjoinRepeat(data))
}