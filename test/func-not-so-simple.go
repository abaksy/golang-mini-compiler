package main

func bar(x int) int {
    return 11*11
}

func foo(x int) int {
    i := 1
    Println(x)
    y := bar(i+x)
    return i+y
}

func main() {
    a := foo(10)
    Println(a)
}
