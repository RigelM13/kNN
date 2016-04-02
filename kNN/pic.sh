#!/bin/bash 

cd Datos/
python ToPBM.py

./ProCar photo.pbm p basura giro ajustar c zoning_8x5
rm photo.pbm
