
// PROCAR.C

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "defines.h"
#include "entrada.h"
#include "preprocesos.h"
#include "caracteristicas.h"

main (int argc, char *argv[]) // argv[1]: fent
{

	FILE *fdent,*fdsal,*fdcar;
	int i,error;
	char fsal[80],fcar[80],aux[10];

	if (argc<4)
	{
		printf ("\nUSO: %s fent.pbm P preprocesos C caracter�stica\n",argv[0]);
		exit(-1);
	}
	
	error=procesar_entrada(argc,argv);
	switch (error)
	{
		case 1:	printf("ERROR FICHERO DE ENTRADA\n");
				break;
		case 2:	printf("ERROR EN PREPROCESOS\n");
				break;
		case 3:	printf("ERROR EN CARACTERISTICAS\n");
	}
	if (error!=0) exit(-1);

	if ((fdent=fopen(argv[1],"r"))==NULL)
	{
		printf("\nError al abrir el fichero: %s\n",argv[1]);
		exit(-1);
	}

	if (num_preprocesos()!=0) // si hay preprocesos, abrir fichero salida (pbm procesado)
	{
                strcpy(fsal,argv[1]);
		strcpy(&(fsal[strlen(fsal)-4]),"_p.pbm");
		fdsal=fopen(fsal,"w");
		fprintf(fdsal,"P1\n");
                printf("Generado fichero imagenes procesadas: %s\n",fsal);
	}

	if (caracteristicas()!=0) // si hay caracteristicas, abrir fichero salida (caracteristicas)
	{
		strcpy(fcar,argv[1]);
		strcpy(&(fcar[strlen(fcar)-3]),"car");
		fdcar=fopen(fcar,"w");
                printf("Generado fichero de caracteristicas: %s\n",fcar);
	}

	fscanf(fdent,"%s",aux); // leer tipo pbm: P1 en nuestro caso
	LeerIM(fdent);
	while(!feof(fdent))
	{
		/* ANADIR LA GESTION DE NUEVOS PREPROCESOS */
		for (i=0;i<num_preprocesos();i++)
			switch (preprocesos[i])
			{
				case BASURA: EliminarBasura(); break;
				case GIRO: Girar(); break;	
				case AJUSTAR: AjustarIM(); break;
			}
		if (num_preprocesos()!=0) EscribirIMp(fdsal); // tras aplicar los filtros, sacar el nuevo pbm a un fichero

		/* ANADIR LA GESTION DE NUEVAS CARACTERISTICAS */
		switch(caracteristica)
		{
			case ZONING_4x3: Zoning(4,3,fdcar); break;
			case ZONING_8x5: Zoning(8,5,fdcar); break;
			case ZONING_13x8:Zoning(13,8,fdcar);break;
		}

		LeerIM(fdent);
	}
	fclose(fdent);
	if (num_preprocesos()!=0) fclose(fdsal);
	if (caracteristicas()!=0) fclose(fdcar);
}
