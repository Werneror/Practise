package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

func main() {
    s := "aa bb cc dd aa dd cc aa"
    freq := make(map[string]int)
    input := bufio.NewScanner(strings.NewReader(s))
    input.Split(bufio.ScanWords)
    for input.Scan() {
        word := input.Text()
        freq[word] ++
    }

    if err := input.Err(); err != nil {
        fmt.Fprintf(os.Stderr, "wordfreq: %v\n", err)
        os.Exit(1)
    }
 
    fmt.Printf("rune\tcount\n")
    for word, count := range freq {
        fmt.Printf("%s\t%d\n", word, count)
    }
}