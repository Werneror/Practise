package main

import (
	"fmt"
	"strings"
)


// basename removes directory components and a .suffix.
// e.g., a => a, a.go => a, a/b/c.go =>c, a/b.c.go => b.c
func basename1(s string) string {
	// Discard last '/' and everything before.
	for i := len(s) - 1; i >=0; i-- {
		if s[i] == '/' {
			s = s[i+1:]
			break
		}
	}

	// Preserve everything before last '.'.
	for i := len(s) -1; i >=0; i-- {
		if s[i] == '.' {
			s = s[:i]
			break
		}
	}
	return s
 }

 func basename2(s string) string {
	 slash := strings.LastIndex(s, "/")  // -1 if "/" not found
	 s = s[slash+1:]
	 if dot := strings.LastIndex(s, "."); dot >=0 {
		 s = s[:dot]
	 }
	 return s
 }

 // comma insert commas in a non-negative decimal interger string.
 func comma(s string) string {
	 n := len(s)
	 if n <= 3 {
		 return s
	 }
	 return comma(s[:n-3]) + "," + s[n-3:]
 }

func main() {
	path := "a/b.ssh"
	number := "1234567"
	fmt.Println(basename1(path))
	fmt.Println(basename2(path))
	fmt.Println(comma(number))

	s := "abc"
	b := []byte(s)
	s2 := string(b)
	fmt.Println(s2)
}
