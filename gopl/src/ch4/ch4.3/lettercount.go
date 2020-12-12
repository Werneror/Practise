package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
    "unicode"
)

func main() {
    letter := 0
    digit := 0
    other := 0
    invalid := 0

    in := bufio.NewReader(os.Stdin)
    for {
        r, n, err := in.ReadRune() // returns rune, nbytes, error
        if err == io.EOF {
            break
        }
        if err != nil {
            fmt.Fprintf(os.Stderr, "charcount: %v\n", err)
            os.Exit(1)
        }
        if r == unicode.ReplacementChar && n == 1 {
            invalid++
            continue
        }
        if unicode.IsLetter(r) {
            letter++
        } else if unicode.IsDigit(r) {
            digit++
        } else {
            other++
        }
    }
    fmt.Printf("rune\tcount\n")
    fmt.Printf("letter\t%d\n", letter)
    fmt.Printf("digit\t%d\n", digit)
    fmt.Printf("other\t%d\n", other)
    if invalid > 0 {
        fmt.Printf("\n%d invalid UTF-8 characters\n", invalid)
    }
}