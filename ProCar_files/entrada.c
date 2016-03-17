
// ENTRADA.C

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "defines.h"

//vector de preprocesos a realizar y numero de preprocesos
#define NP 10
int preprocesos[NP]; // varias posible: BASURA,GIRO
int np=0;

//caracteristica a aplicar
int caracteristica=0; // 1 solo posible: ZONING_4x3,ZONING_8x5,ZONING_13x8

char * mayusculas(char *s)
{
	int i;

	for (i=0;i<strlen(s);i++) s[i]=toupper(s[i]);
	return (s);
}

int procesar_entrada(int argc, char*argv[])
{
	int i,car;
	char fsal[50];

	for (i=0;i<NP;i++) preprocesos[i]=0;

	strcpy(fsal,argv[1]); // comprobar que existe fichero
	if (strcmp(&(fsal[strlen(fsal)-3]),"pbm")!=0) return(1);

	car=2; //posición por defecto (sin preprocesos)
	if ((strcmp(argv[2],"P")==0) || (strcmp(argv[2],"p")==0)) // hay preprocesos
	{
		for (i=3;i<argc;i++,np++) if ((strcmp(argv[i],"C")==0)||(strcmp(argv[i],"c")==0)) {car=i; break;}
		if (np==0) return(2); // preprocesos sin completar
		for (i=0;i<np;i++)
		{
			/* AQUI HAY QUE ANADIR LA GESTION DEL TOKEN DEL NUEVO PREPROCESO*/
			if (strcmp(mayusculas(argv[i+3]),"BASURA")==0) preprocesos[i]=BASURA;
			else if (strcmp(mayusculas(argv[i+3]),"GIRO")==0) preprocesos[i]=GIRO;
			else if (strcmp(mayusculas(argv[i+3]),"AJUSTAR")==0) preprocesos[i]=AJUSTAR;
			else return(2);
		}
	}
	if ((np+3)==argc) return (0); // no hay caracteristicas
	if (car==(argc-1)) return(3); // caracteristica sin completar
	
	// caracteristica a aplicar
	/* AQUI HAY QUE ANADIR LA GESTION DEL TOKEN DE LA NUEVA CARACTERISTICA*/
	if (strcmp(mayusculas(argv[argc-1]),"ZONING_4X3")==0) caracteristica=ZONING_4x3;
	else if (strcmp(mayusculas(argv[argc-1]),"ZONING_8X5")==0) caracteristica=ZONING_8x5;
	else if (strcmp(mayusculas(argv[argc-1]),"ZONING_13X8")==0) caracteristica=ZONING_13x8;
	else return(3);
	
	return(0);
}

int num_preprocesos()
{
	return(np);
}

int caracteristicas()
{
	return(caracteristica);
}
