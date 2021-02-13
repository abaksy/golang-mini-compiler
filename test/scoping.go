package main

func main() {
    i := 1
    a := 2
    if a > 1 {
        Println(i)
        a := 3
        Println(a)
        if a < 10 {
            b := i + 2
            i := b + 3
            Println(b)
            Println(i)
            Println("Wow, Scoping works!\n")
        }
    }
}
