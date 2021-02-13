package main

func fibo(z int)

func fibo(z int) int {
    if z == 0 {
        return 0
    } else if z == 1 {
        return 1
    } else {
        return fibo(z-1) + fibo(z-2)
    }
}

func main() {
    e := fibo(15)
    Println(e)
}
