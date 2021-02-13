package main

func main() {
    a := 1
    b := 1
    a, b = a+b, a-b
    Println("This works flawlessly!\n")
    Println(a)
    Println(b)
}
