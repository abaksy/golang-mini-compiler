package main

import "fmt"

func main() {
	sum := 243
	for sum < 1000 {
		sum += sum
	}
}
