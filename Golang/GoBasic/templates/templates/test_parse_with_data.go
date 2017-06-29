package main


import (
	"log"
	"os"
	"text/template"
)
var tpl *template.Template

func init(){
	tpl = template.Must(template.ParseFiles("tpl_2.gohtml"))
}


func main(){
	err := tpl.ExecuteTemplate(os.Stdout, "tpl_2.gohtml", `Some random String `)
	if err != nil {
		log.Fatalln(err)
	}
}