package main

func main() {
    i := 5
    switch i {
        case 1:
            i+=1
        case 1+1:
            i+=11
        case 2+1:
            i+=111
        case 3+1:
            i+=1111
        case 4+1:
            i+=11111
        case 5+1:
            i+=111111
        case 6+1:
            i+=1111111
    }
    Println(i)
}
