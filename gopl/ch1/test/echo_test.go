// Echo6 prints its command-line arguments.
// For practice 1.3
// go test -bench=.

package main

import (
	// "fmt"
	"os"
	"strings"
	"testing"
)

func echo1() {
	var s, sep string
	for i := 1; i < len(os.Args); i++ {
		s += sep + os.Args[i]
		sep = " "
	}
	// fmt.Println(sep)
}

func echo2() {
	strings.Join(os.Args[1:], " ")
    // fmt.Println(strings.Join(os.Args[1:], " "))
}

func BenchmarkEcho1(b * testing.B) {
	for i := 0; i < b.N; i++ {
		echo1()
	}
}

func BenchmarkEcho2(b * testing.B) {
	for i := 0; i < b.N; i++ {
		echo2()
	}
}