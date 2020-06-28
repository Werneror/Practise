// For practice 1.4

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	counts := make(map[string]int)
	files := os.Args[1:]
	if len(files) == 0 {
		countLines(os.Stdin, "", counts)
	} else {
		for _, arg := range files {
			f, err := os.Open(arg)
			if err != nil {
				fmt.Fprintf(os.Stderr, "dup2: %v\n", err)
				continue
			}
			countLines(f, arg, counts)
			f.Close()
		}
	}
	for line, n := range counts {
		if n > 1 {
			temp := strings.Split(line, "$")
			fmt.Printf("%d\t%s\t%s\n", n, temp[0], temp[1])
		}
	}
}

func countLines(f * os.File, filename string, counts map[string]int) {
	 input := bufio.NewScanner(f)
	 for input.Scan() {
	 	counts[filename+"$"+input.Text()]++
	 }
	 // NOTE: ignoring potential errors from input.Err()
}