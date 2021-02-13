package main

func main() {
    a := 4
    if a <= 10 {
        if a <= 5 {
            Println("A is <= 5\n")
        } else {
            Println("A is >= 5\n")
        }
    } else {
        Println("A is non <= 10\n")
    }
    i := 1
    for i < 10 {
        if i%2 == 0 {
            Println("Even\n")
        } else {
            Println("Odd\n")
        }
        i = i + 1
    }
}
