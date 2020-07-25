package popcount

/*
D:\code\Practise\gopl\src\ch2\popcount>go test -bench=.
goos: windows
goarch: amd64
pkg: ch2/popcount
BenchmarkPopcount1-8    1000000000               0.257 ns/op
BenchmarkPopcount2-8    70653901                14.5 ns/op
BenchmarkPopcount3-8    26625072                43.0 ns/op
BenchmarkPopcount4-8    175432261                6.81 ns/op
PASS
ok      ch2/popcount    4.598s
*/

import (
	"testing"
)


func BenchmarkPopcount1(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Popcount1(54326543)
	}
}

func BenchmarkPopcount2(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Popcount2(54326543)
	}
}

func BenchmarkPopcount3(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Popcount3(54326543)
	}
}

func BenchmarkPopcount4(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Popcount4(54326543)
	}
}
