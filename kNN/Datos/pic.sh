#!/bin/bash 

cd Datos/
python cam.py
python ToPBM.py

./ProCar photo.pbm p basura giro ajustar c zoning_8x5
rm photo.pbm