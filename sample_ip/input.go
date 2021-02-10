// Golang Program to create Pyramid
package main

import "fmt"

func main() {
	var rows int
	var k int = 0
	fmt.Print("Enter number of rows :")
	fmt.Scan(&rows)
	for i := 1; i <= rows; i++ {
		k = 0
		for space := 1; space <= rows-i; space++ {
			fmt.Print("  ")
		}
		for {
			fmt.Print("* ")
			k++
			if k == 2*i-1 {
				break
			}
			/*
				This is a multiline comment
				This is a multiline commment
			*/
		}
		fmt.Println("")
	}
	//This is a single line comment
}
