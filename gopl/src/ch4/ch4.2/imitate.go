package main

import "fmt"

func main() {
	months := [...]string{
		1:  "January",
		2:  "February",
		3:  "March",
		4:  "April",
		5:  "May",
		6:  "June",
		7:  "July",
		8:  "August",
		9:  "September",
		10: "October",
		11: "November",
		12: "December"}
	Q2 := months[4:7]
	summer := months[6:9]

	fmt.Println(months)
	fmt.Println(Q2)
	fmt.Println(summer)

	for _, s := range summer {
		for _, q := range Q2 {
			if s == q {
				fmt.Printf("%s appears in both\n", s)
			}
		}
	}

	fmt.Println(len(summer))
	fmt.Println(cap(summer))

	fmt.Println([]int(nil))

	var runes []rune
	for _, r := range "Hello, 世界" {
		runes = append(runes, r)
	}
	fmt.Printf("%U\n", runes) // "['H' 'e' 'l' 'l' 'o' ',' ' ' '世' '界']"

	var x, y []int
    for i := 0; i < 10; i++ {
        y = append(x, i)
        fmt.Printf("%d cap=%d\tlen=%d\t%v\n", i, cap(y), len(y), y)
        x = y
	}
}
