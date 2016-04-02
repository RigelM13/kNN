//k-NN [k] [Distancia]

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define ERR_MSG printf("./k-NN k Distancia [test/cpr]\nk: (1, 3, 5)\nDistancia: e = Euclidea, a = Absoluta\nTest: t\nCPR: c\n");
#define EOL '\n'

//Variables globales
static int c = 0;	//c: Nº de elementos en el structArray
//Clase y distancia al numero de test
struct nClass{
	float d;	
	int c;
};

//Declaracion funciones
void checkArgs(int arg, char *argv[], int *k, int *m, int *opt, FILE **tra_file, FILE **test_file, FILE **cpr_file);
float dEuclidea(int *tra_data, int *data_in);
float dAbsoluta(int *tra_data, int *data_in);
void insertClass(struct nClass class_val, struct nClass *minD_class, int k);
int resultClass(struct nClass *minD_class, int k);
int read_vector(int *vector, FILE *file);
void init_confMat(int mat[10][10]);
void printConfMat(int mat[10][10]);
void writeVectorCPR(FILE *file, int data_in[41]);


//MAIN
int main(int argc, char *argv[]){
	FILE *tra_file, *test_file, *cpr_file, *photo_file;			//Ficheros base de datos
	int i, k, m, opt;								//Variables, k:Parametro, c: Nº de elementos en el struct, modo: 
	int ac, er;										//Aciertos, errores
	int conf_mat[10][10];							//Matriz de confusion
	int tra_data[41], test_data[41], cpr_data[41];	//Vector de datos de entrada y un valor de la B.D.

	//Prueba
	int data_in[40] = {100, 100, 0, 100, 100, 66, 100, 93, 83, 85, 95, 94, 76, 90, 58, 100, 46, 0, 32, 79, 81, 26, 85, 76, 74, 46, 73, 82, 99, 25, 100, 79, 96, 47, 0, 0, 50, 8, 0, 0, 0};

	checkArgs(argc, argv, &k, &m, &opt, &tra_file, &test_file, &cpr_file, &photo_file);

	//Reservar espacio para el array de structs
	struct nClass class_val;		//Estructura que almacena distancia y clase
	struct nClass minD_class[k];	//Array de struct que almacena los 5 elementos mas cercanos

	ac = 0;
	er = 0; 

	//Ejecucion modo foto
	if(m == 0){
		read_vector(data_in, tra_file)
		c = 0;
		while(read_vector(tra_data, tra_file) == 0){
			if(opt == 0){
				class_val.d = dEuclidea(tra_data, data_in);
			}
			else{
				class_val.d = dAbsoluta(tra_data, data_in);
			}
			class_val.c = tra_data[40];

			insertClass(class_val, minD_class, k);
		}
		
		//Resultados
		for(i = 1; i <= k; i++){
			printf("%d: Distancia: %f  Clase: %d\n", i, minD_class[i-1].d, minD_class[i-1].c);
		}
		printf("\nEs un: %d\n", resultClass(minD_class, k));
	}
	//Ejecucion modo Test
	else if(m == 1){
		init_confMat(conf_mat);
		while(read_vector(test_data, test_file) == 0){
			c = 0;
			fseek(tra_file, 0, SEEK_SET);
			while(read_vector(tra_data, tra_file) == 0){
				if(opt == 0){
					class_val.d = dEuclidea(tra_data, test_data);
				}
				else{
					class_val.d = dAbsoluta(tra_data, test_data);
				}
				class_val.c = tra_data[40];

				insertClass(class_val, minD_class, k);
			}
			if(resultClass(minD_class, k) == test_data[40]){
				ac++;
			}
			else{
				er++;
			}
			conf_mat[test_data[40]][resultClass(minD_class, k)]++;
		}
		printConfMat(conf_mat);
		printf("\nAciertos: %d\nErrores:  %d\n", ac, er);
		fclose(test_file);
	}
	//Ejecucion modo CPR
	else if(m == 2){
		for(i = 0; i < 10; i ++){
			ac = 0;
			fseek(tra_file, 0, SEEK_SET);
			while(read_vector(tra_data, tra_file) == 0){
				c = 0;
				fseek(cpr_file, 0, SEEK_SET);
				while(read_vector(cpr_data, cpr_file) == 0){
					if(opt == 0){
						class_val.d = dEuclidea(tra_data, cpr_data);
					}
					else{
						class_val.d = dAbsoluta(tra_data, cpr_data);
					}
					class_val.c = cpr_data[40];

					insertClass(class_val, minD_class, k);
				}
				if(resultClass(minD_class, c) == tra_data[40]){
					ac++;
				}
				else{
					er++;
					writeVectorCPR(cpr_file, tra_data);
				}
			}
		}
		printf("Datos añadidos al CPR: %d de %d\n", er, ac);
		fclose(cpr_file);
	}

	fclose(tra_file);
	return 0;
}


//FUNCIONES
void checkArgs(int argc, char *argv[], int *k, int *m, int *opt, FILE **tra_file, FILE **test_file, FILE **cpr_file, **photo_file){
	//Comprobar argumentos
	if(argc < 3 || argc > 5){
		ERR_MSG
		exit(-1);
	}

	//Comprpbar 1er argumento
	*k = atoi(argv[1]);
	if(*k != 1 && *k != 3 && *k != 5){
		ERR_MSG
		exit(-1);
	}

	//Comprpbar 2do argumento
	if(!strcmp(argv[2], "e")){
		*opt = 0;
	}
	else if(!strcmp(argv[2], "a")){
		*opt = 1;
	}
	else{
		ERR_MSG
		exit(-1);
	}

	//Abrir ficheros de training
	if((*tra_file = fopen("Datos/tra.car", "r")) < 0){
		printf("Error al abrir fichero de training.\n");
		exit(-1);
	}
	
	*m = 0;
	//Modo test/cpr
	if(argc == 4){
		if((!strcmp(argv[3],"t"))){
			*m = 1;
			//Abrir fichero test
			if((*test_file = fopen("Datos/test1.car", "r")) < 0){
				printf("Error al abrir fichero de test.\nNombre: test1.car\nFormato: Leer manual.txt\n");
				exit(-1);
			}
		}
		//Abrir fichero CPR
		else if((!strcmp(argv[3],"c"))){
			*m = 2;
			if((*cpr_file = fopen("Datos/cpr.car", "w+")) < 0){
				printf("Error al crear fichero CPR.\nNombre: cpr.car\nFormato: Leer manual.txt\n");
				exit(-1);
			}
			int cpr_data[41];
			read_vector(cpr_data, *tra_file);
			writeVectorCPR(*cpr_file, cpr_data);

		}
		else{
			ERR_MSG
			exit(-1);
		}
	}
	else{
		if((*photo_file = fopen("Datos/photo.car", "r")) < 0){
				printf("Error al abrir foto.\nNombre: photo.car\nFormato: Leer manual.txt\n");
				exit(-1);
			}
	}
}

float dEuclidea(int *tra_data, int *data_in){
	int i = 0;
	float d = 0;

	for(i = 0; i < 40; i++){
		d += (tra_data[i] - data_in[i])*(tra_data[i] - data_in[i]);
	}
	d = sqrt(d);

	return d;
}

float dAbsoluta(int *tra_data, int *data_in){
	int i;
	int d = 0;
	int tr, dt;
	
	for(i = 0; i < 40; i++){
		tr = tra_data[i];
		dt = data_in[i];
		d += abs(tr - dt);
	}

	return d;
}

void insertClass(struct nClass class_val, struct nClass *minD_class, int k){
	int i, j;
	int r = 0;
	
	if(c == 0){
		minD_class[0] = class_val;
		c++;
	}
	else{
		for(i = 0; (i < c) && (r == 0); i++){
			//Comprobar si la distancia es menor que el valor[i] del array
			if(class_val.d < minD_class[i].d){
				//Desplazar los correspondientes struct para mantener orden ascendente
				for(j = c; j > i; j--){
					minD_class[j] = minD_class[j-1];
				}
				minD_class[i] = class_val;
				r = 1;
				if(c < 5){
					c++;
				}
			}
		}
	}
}

int resultClass(struct nClass *minD_class, int k){
	int class[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
	int i, pos, max;

	for(i = 0; i < k; i++){
		class[minD_class[i].c]++;
	}

	max = -1;
	for(i = 0; i < 10; i++){
		if(class[i] > max){
			max = class[i];
			pos = i;
		}
	}
	return pos;
}

int read_vector(int *vector, FILE *file){
	int i, r, digit, currentNum;
	
	i = 0;
	r = 0;
	
	digit = getc(file);
	if(digit == EOF){
		return -1;
	}
	
	while(digit != EOL){
		currentNum = 0;
		while(digit != ' '){
			currentNum = (currentNum*10) + (digit - '0');
			digit = getc(file);
		}
		vector[i] = currentNum;
		i++;
		digit = getc(file);
	}
	
	return 0;
}

void init_confMat(int mat[10][10]){
	int i, j;

	for(i = 0; i < 10; i++){
		for(j = 0; j < 10; j++){
			mat[i][j] = 0;
		}
	}
}

void printConfMat(int mat[10][10]){
	int i, j;
	printf("\n0\t1\t2\t3\t4\t5\t6\t7\t8\t9\tR/P\n\n");
	for(i = 0; i < 10; i++){
		for(j = 0; j < 10; j++){
			printf("%d\t", mat[i][j]);
		}
		printf(":%d\n", i);
	}
}

void writeVectorCPR(FILE *file, int data_in[41]){
	int i;

	for(i = 0; i < 41; i++){
		fprintf(file, "%d ", data_in[i]);
	}
	fprintf(file, "\n");
	fflush(file);
}

