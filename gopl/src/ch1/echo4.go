// Echo4 prints its command-line arguments.
// For practice 1.1

package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Println(strings.Join(os.Args, " "))
}
