package main

import (
	"os"
	"log"
	"text/template"
)

var tpl *template.Template

func init() {
	tpl = template.Must(template.ParseFiles("tpl1.gohtml"))

}
func main(){
	obj := map[string]string{
		"Something":	"Some",
		"Not Something": "But Some",
		"Maybe Something": "Maybe Some",
	}
	err := tpl.Execute(os.Stdout,obj)
	if err != nil{
		log.Fatalln(err)
	}
}