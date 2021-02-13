package main

func fact(z int)

func fact(z int) int {
    if z == 0 {
        return 1
    } else {
        return fact(z-1) * z
    }
}

func main() {
    f := fact(10)
    Println(f)
}
