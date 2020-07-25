package popcount

// pc1[i] is the population count of i.
var pc1[256]byte

func init() {
	for i := range pc1 {
		pc1[i] = pc1[i/2] + byte(i&1)
	}
}

// Popconut1 returns the population count (number of set bits) of x.
func Popcount1(x uint64) int {
	return int(pc1[byte(x>>(0*8))] + 
		pc1[byte(x>>(1*8))] +
		pc1[byte(x>>(2*8))] +
		pc1[byte(x>>(3*8))] +
		pc1[byte(x>>(4*8))] +
		pc1[byte(x>>(5*8))] +
		pc1[byte(x>>(6*8))] +
		pc1[byte(x>>(7*8))])
}

// 练习 2.3： 重写PopCount函数，用一个循环代替单一的表达式。
// Popconut2 returns the population count (number of set bits) of x.
func Popcount2(x uint64) int {
	var count byte = 0
	for i := 0; i < 8; i++ {
		count += pc1[byte(x>>(i*8))]
	}
	return int(count)
}

// 练习 2.4： 用移位算法重写PopCount函数，每次测试最右边的1bit，然后统计总数。
// Popconut3 returns the population count (number of set bits) of x.
func Popcount3(x uint64) int {
	var count byte = 0
	for i := 0; i < 64; i++ {
		count += byte(x>>i & 1)
	}
	return int(count)
}

// 练习 2.5： 表达式x&(x-1)用于将x的最低的一个非零的bit位清零。使用这个算法重写PopCount函数。
// Popconut4 returns the population count (number of set bits) of x.
func Popcount4(x uint64) int {
	count := 0
	for ;x != 0; x = x&(x-1) {
		count ++
	}
	return count
}
