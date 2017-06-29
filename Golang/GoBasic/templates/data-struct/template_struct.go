package main

import (
	"os"
	"log"
	"text/template"
)

var tpl *template.Template 

type obj struct {
	Name string
	Last_Name string
}

func init(){
	tpl = template.Must(template.ParseFiles("tpl2.gohtml"))
}

func main(){
	 tetst := obj{
	 	Name: "James",
	 	Last_Name: "Bond",
	 }
	 err := tpl.Execute(os.Stdout, tetst)
	 if err != nil{
	 	log.Fatalln(err)
	 }
}