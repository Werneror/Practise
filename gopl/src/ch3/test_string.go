package main

import (
	"fmt"
	"unicode/utf8"
)

func test2() {
	s := "left foot"
	t := s
	s += ", right foot"
	fmt.Println(t)
	fmt.Println(s)

	s = "Hello, 世界"
	fmt.Println(len(s))                    // 13
	fmt.Println(utf8.RuneCountInString(s)) // 9

	for i := 0; i < len(s); {
		r, size := utf8.DecodeRuneInString(s[i:])
		fmt.Printf("%d\t%c\n", i, r)
		i += size
	}

	for i, r := range "Hello, 世界" {
		fmt.Printf("%d\t%q\t%d\n", i, r, r)
	}

	n := 0
	for  _, _ = range s {
		n++
	}
	fmt.Printf("len of s is %d\n\n", n)

	// "program" in Japanese katakana
	s = "プログラム"
	fmt.Printf("% x\n", s)
	r := []rune(s)
	fmt.Printf("%x\n", r)
	fmt.Println(string(r))
	fmt.Println(string(123456))

	fmt.Println(basename1("a/.ssh"))
}
