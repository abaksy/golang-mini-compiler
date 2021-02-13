package main

func main() {
    i := 0
    a := 0
    if i <= 3 {
        a = 1
        i += 10
    }
    if i >= 2 {
        a = 2
    } else {
        a = 3
    }
    Println(a)
    Println(i)
}
