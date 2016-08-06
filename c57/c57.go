package main

import (
	"fmt"
	"math/big"
	"math/rand"
)

func main() {
	r := rand.New(rand.NewSource(99)) //Want a variable seed

	p,_ := new(big.Int).SetString("7199773997391911030609999317773941274322764333428698921736339643928346453700085358802973900485592910475480089726140708102474957429903531369589969318716771",10)

	g,_ := new(big.Int).SetString("4565356397095740655436854503483826832136106141639563487732438195343690437606117828318042418238184896212352329118608100083187535033402010599512641674644143",10)
	
	q,_ := new(big.Int).SetString("236234353446506858198510045061214171961",10)
	
	j := new(big.Int).Sub(p,big.NewInt(1))
	j.Div(j,q)
	
	//Test my group operations
	fmt.Println("Alice-Bob exchange...")
	aPriv := new(big.Int).Rand(r,p)
	aPub := new(big.Int).Exp(g,aPriv,p)
	
	bPriv := new(big.Int).Rand(r,p)
	bPub := new(big.Int).Exp(g,bPriv,p)
	
	aShared := new(big.Int).Exp(bPub,aPriv,p)
	bShared := new(big.Int).Exp(aPub,bPriv,p)
	
	if (aShared.Cmp(bShared) != 0) {
		fmt.Println("Error: Alice and Bob did not get the same shared key")
	}
	else {
		fmt.Println("Alice and Bob can talk!")
	}
	
	//Get some subgroups
	fmt.Println("Factoring...")
	factors []big.Int
	
	
}