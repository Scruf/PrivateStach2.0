package main
import "fmt"

type person struct {
	fname string
	lname string
}
type secretAgent struct {
	person
	license bool
}
func (p person) speak(){
	fmt.Println(p.fname)
	fmt.Println(p.lname)
}
func main() {
	xi := [] int {2,4,57}
	m := map[string]int{
		"Todd":45,
		"Joe":42,
	}
	per := person {
		"Miss",
		"Lol",
	}

	fmt.Println(xi)
	fmt.Println(m)
	fmt.Println(per)
	per.speak()
	sec := secretAgent{
			person{
				"Some",
				"Random",
			},
		true,
	}
	fmt.Println(sec)
}