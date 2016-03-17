
// CARACTERISTICAS.C

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "preprocesos.h"

//caracterstica zonning
int Saca_Vec (int *v_menor,int *v_mayor,int *v_cuanto,int menor,int mayor)
{
  int ind_menor,ind_mayor;
  int llevo_menor,llevo_mayor;
  int queda_menor,queda_mayor;
  int consumo_total,i;
 
  ind_menor=ind_mayor=v_menor[0]=v_mayor[0]=0;
  v_cuanto[0]=llevo_menor=llevo_mayor=menor;
  consumo_total=menor*mayor-menor;
 
  for (i=1;consumo_total!=0;i++)
  {
    if (llevo_menor==mayor)
    {
      ind_menor++;
      llevo_menor=0;
    }
    if (llevo_mayor==menor)
    {
      ind_mayor++;
      llevo_mayor=0;
    }
    v_menor[i]=ind_menor;
    v_mayor[i]=ind_mayor;
    queda_menor=mayor-llevo_menor;
    queda_mayor=menor-llevo_mayor;
    if (queda_menor>queda_mayor) v_cuanto[i]=queda_mayor;
    else v_cuanto[i]=queda_menor;
    llevo_menor+=v_cuanto[i];
    llevo_mayor+=v_cuanto[i];
    consumo_total-=v_cuanto[i];
  }
  return (i);
}

void Zoning (int fil,int col,FILE *fdcar)
{
  int v_menor1[120],v_mayor1[120], v_cuanto1[120];
  int v_menor2[120],v_mayor2[120], v_cuanto2[120];
  long **peque1,*vcarac; 
  int i,dim1,dim2,j;

  vcarac=(long*)malloc(fil*col*sizeof(long));
  peque1=(long**)malloc(fil*sizeof(long*));
  for (i=0;i<fil;i++) peque1[i]=(long*)malloc(col*sizeof(long));
  for (i=0;i<fil;i++)
	  for (j=0;j<col;j++) peque1[i][j]=0;

  if (filas<fil)
    dim1=Saca_Vec(v_menor1,v_mayor1,v_cuanto1,filas,fil);
  else  
    dim1=Saca_Vec(v_menor1,v_mayor1,v_cuanto1,fil,filas);

  if (cols<col)
    dim2=Saca_Vec(v_menor2,v_mayor2,v_cuanto2,cols,col);
  else  
    dim2=Saca_Vec(v_menor2,v_mayor2,v_cuanto2,col,cols);

  if((filas>=fil)&&(cols>=col))
  {
    for (i=0;i<dim1;i++)
      for (j=0;j<dim2;j++)
	if (im[v_mayor1[i]][v_mayor2[j]]==1)
		peque1[v_menor1[i]][v_menor2[j]]+=(long)((long)(v_cuanto1[i])*v_cuanto2[j]);
  }              
  else
    if((filas>=fil)&&(cols<col))
    {
      for (i=0;i<dim1;i++)
        for (j=0;j<dim2;j++)
	 if (im[v_mayor1[i]][v_menor2[j]]==1)
		peque1[v_menor1[i]][v_mayor2[j]]+=(long)((long)(v_cuanto1[i])*v_cuanto2[j]);
	}              
    else
      if((filas<fil)&&(cols>=col))
      {
        for (i=0;i<dim1;i++)
          for (j=0;j<dim2;j++)
	   if (im[v_menor1[i]][v_mayor2[j]]==1)
		peque1[v_mayor1[i]][v_menor2[j]]+=(long)((long)(v_cuanto1[i])*v_cuanto2[j]);
	  }              
      else
        for (i=0;i<dim1;i++)
          for (j=0;j<dim2;j++)
	   if (im[v_menor1[i]][v_menor2[j]]==1)
		peque1[v_mayor1[i]][v_mayor2[j]]+=(long)((long)(v_cuanto1[i])*v_cuanto2[j]);

  int cf,cc;
  if(filas>fil) cf=filas;
  else cf=fil;
  if(cols>col) cc=cols;
  else cc=col;

  for (i=0;i<fil;i++) 
    for (j=0;j<col;j++)
	  vcarac[i*col+j]=100*peque1[i][j]/(cf*cc);

  // volcar el zoning al fichero fdcar
  for (i=0;i<fil*col;i++) fprintf(fdcar,"%d ",vcarac[i]);
  fprintf(fdcar,"%d ",clase);
  fprintf(fdcar,"\n");

  for (i=0;i<fil;i++) free(peque1[i]);
  free(peque1);
  free(vcarac);
}  

/* ANADIR LAS NUEVAS FUNCIONES DE CARACTERISTICAS */


