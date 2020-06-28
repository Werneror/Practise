// Echo5 prints its command-line arguments.
// For practice 1.2

package main

import (
	"fmt"
	"os"
)

func main() {
	for index, arg := range os.Args[1:] {
        fmt.Println(index, arg)
	}
}
