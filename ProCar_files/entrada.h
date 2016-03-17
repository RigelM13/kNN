
// ENTRADA.H

//vector de preprocesos a realizar: MAXIMO 10
#define NP 10
extern int preprocesos[NP]; // varias posibles: BASURA,GIRO

//caracteristicas a aplicar
extern int caracteristica; // 1 solo posible: ZONING_8x5,ZONING_13x8,ZONING_4x3

//funciones auxiliares
extern int num_preprocesos(),caracteristicas();

