
// PREPROCESOS.C

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define TAMANIO 100

//variables im caracter
unsigned char im[TAMANIO][TAMANIO];
int filas,cols,clase,bytesxfil;
long id;


// FILTRO BASURA
void Limpiar (int ini_fil,int fin_fil,int ini_col,int fin_col)
{
	int i,j;

	for (i=ini_fil;i<fin_fil;i++)
		for (j=ini_col;j<fin_col;j++) im[i][j]=0;
}

void EliminarBasura ()
{
	int i,j,col_25,fil_25;

	col_25 = (int)((float)cols*0.25+0.5);
	fil_25 = (int)((float)filas*0.15+0.5);
	
	//Limpiar Izquierda
	for (j=col_25;j>=0;j--)
	{	
		for (i=0;i<filas;i++) if (im[i][j]==1) break;
		if (i==filas) break;
	}
	if (j>=0) Limpiar(0,filas,0,j);

	//Limpiar Derecha
	for (j=cols-col_25;j<cols;j++)
	{	
		for (i=0;i<filas;i++) if (im[i][j]==1) break;
		if (i==filas) break;
	}
	if (j<cols) Limpiar(0,filas,j,cols);
	
	//Limpiar Superior
	for (i=fil_25;i>=0;i--)
	{	
		for (j=0;j<cols;j++) if (im[i][j]==1) break;
		if (j==cols) break;
	}
	if (i>=0) Limpiar(0,i,0,cols);	
	
	//Limpiar Inferior
	for (i=filas-fil_25;i<filas;i++)
	{	
		for (j=0;j<cols;j++) if (im[i][j]==1) break;
		if (j==cols) break;
	}
	if (i<filas) Limpiar(i,filas,0,cols);
}


//FILTRO GIRAR
void Girar()
{
  int i,j,valor;
  float xi,yi,xiyi,xi2,nn,mediax,mediay,pendiente,h,difer; //parametros Giro
  unsigned char wim[TAMANIO][TAMANIO]; //auxiliar
  
  memset(wim,0,TAMANIO*TAMANIO*sizeof(unsigned char)); 
  xi=yi=xiyi=xi2=nn=(float)0.0;//parametros de la recta de regresion

  // Calculo de parametros de giro (para el calculo de la recta de regresion) 
  for(i=0;i<filas;i++)
    for(j=0;j<cols;j++)
    {	
        if (im[i][j]==1)
		{        
			xi+=(i+1);
			yi+=(j+1);
			xiyi+=(i+1)*(j+1);
			xi2+=(i+1)*(i+1);
			nn++;
		}
    }
  mediax=xi/nn;
  mediay=yi/nn;
  pendiente=((xiyi/nn)-(mediax*mediay))/((xi2/nn)-(mediax*mediax));
  for(i=0;i<filas;i++)
  {
	//valor previsto de la funcion
    h=mediay+pendiente*((float)(i+1)-mediax);
    // girar en funcion del valor previsto 
    difer=h-mediay;
    for (j=0;j<cols;j++)
    {
      if(im[i][j]==1)
      {  
        valor=(int)((float)j-difer);
        if(valor<0) valor=0;
        else
          if(valor>=TAMANIO) valor=TAMANIO-1;
        wim[i][valor]=1;
      }
    }
  }
  //copiar a im
  for (i=0;i<filas;i++)
	  for (j=0;j<cols;j++) im[i][j]=wim[i][j];
}

// AJUSTAR IM DEL DIGITO
void AjustarIM()
{
	int fili,filf,coli,colf;
	int i,j,fin;
	unsigned char wim[TAMANIO][TAMANIO]; //auxiliar
	
	//establecer los límites de la imagen
	fin=0;
	for (i=0;i<filas;i++)
	{
		for (j=0;j<cols;j++) if (im[i][j]==1) {fin=1; break;}
		if (fin) {fili=i; break;}
	}
	fin=0;
	for (i=filas-1;i>=0;i--)
	{
		for (j=0;j<cols;j++) if (im[i][j]==1) {fin=1; break;}
		if (fin) {filf=i; break;}
	}
	fin=0;
	for (i=0;i<cols;i++)
	{
		for (j=0;j<filas;j++) if (im[j][i]==1) {fin=1; break;}
		if (fin) {coli=i; break;}
	}
	fin=0;
	for (i=cols-1;i>=0;i--)
	{
		for (j=0;j<filas;j++) if (im[j][i]==1) {fin=1; break;}
		if (fin) {colf=i; break;}
	}

	//copiar la imagen ajustada
	memset(wim,0,TAMANIO*TAMANIO*sizeof(unsigned char));
	for (i=fili;i<=filf;i++)
		for (j=coli;j<=colf;j++) wim[i-fili][j-coli]=im[i][j];
	memcpy(im,wim,TAMANIO*TAMANIO*sizeof(unsigned char));
	filas=filf-fili+1;
	cols=colf-coli+1;
}

/* ANADIR LAS NUEVAS FUNCIONES DE PREPROCESO */


///////////////////////////////////////////////////////////////////
// LECTURA DEL IM
void LeerIM(FILE *fdent) 
{
  int i,j;
  char aux[50];

  fscanf (fdent,"%s %d %d %d %d",aux,&clase,&bytesxfil,&cols,&filas);
  id=atol(&(aux[1]));
  for(i=0;i<filas;i++)
    for(j=0;j<cols;j++) fscanf(fdent,"%d",&(im[i][j]));
}

// ESCRITURA DEL PBM MODIFICADO
void EscribirIMp(FILE *fdsal)
{
	int i,j;

	fprintf(fdsal,"#%05ld %d %d\n%d %d\n",id,clase,bytesxfil,cols,filas);
	for(i=0;i<filas;i++)
	{
		for(j=0;j<cols;j++) fprintf(fdsal,"%d ",im[i][j]);
		fprintf(fdsal,"\n");
	}
	fprintf(fdsal,"\n");
}
