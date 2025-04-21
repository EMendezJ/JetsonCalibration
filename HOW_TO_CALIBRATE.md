# COMO CALIBRAR LA CAMARA (PARA DUMMIES)

### Mini tuto para calibrar cualquier camara con los archivos que se encuentran en esta branch.
😁👍
## REQUERIMIENTOS:

### Correr
```bash
pip uninstall opencv-contrib-python
pip install opencv-python
```

## PASO 1

### - Imprimir un [tablero de ajedrez](https://github.com/opencv/opencv/blob/master/doc/pattern.png) (puede ser alguno real si es que se tiene a la mano).

#### (En mi caso utilicé uno pequeño de madera)
![WIN_20250129_15_32_13_Pro](https://github.com/user-attachments/assets/9ef98e8c-c6ac-4983-84ff-df95eea8723b)
  

### Una vez que se tiene el tablero se deberá 
- Medir el largo de uno de los lados de los cuadrados de este. (en metros)
- Contar los recuadros en **X** y **Y** del tablero seleccionado.

#### Tablero oficial de la documentación de OpenCV https://github.com/opencv/opencv/blob/master/doc/pattern.png

## PASO 2 

### - Tomar de 10 a 30 fotos con la camara que se desea calibrar. Desde diferentes distancias y rotaciones (siempre y cuando el tablero sea visible). 

![fotos ejemplos](https://github.com/user-attachments/assets/cd952cef-f67f-411f-a434-d168c9bb0451)

## PASO 3 

### - Descargar el archivo para calibración de la camara ["camera_calibration.py"](https://github.com/vanttec/TMR2025/blob/pose_estimator/camera_calibration.py). 
- Dentro del archivo sustituir con los valores obtenidos del Paso 1. 
![dimensiones](https://github.com/user-attachments/assets/2f07b641-2359-46e3-8e21-64ae409d10bc)

## PASO 4 

### - Guardar el archivo ["camera_calibration.py"](https://github.com/vanttec/TMR2025/blob/pose_estimator/camera_calibration.py) y las fotos que fueron tomadas en la misma carpeta.

![FolderExample](https://github.com/user-attachments/assets/dcea9c5b-099b-48e8-b577-db4b5f5ecd46)


## PASO 5 

### - ¡CORRER EL PROGRAMA!

- Al correr el programa se analizaran las fotos y se mostrara el proceso de esta manera:
![camera calibration](https://github.com/user-attachments/assets/e5506e28-4482-4d23-8e89-e48780dcd64e)

- Al finalizar se generará un archivo .yaml de nombre "calibration_chessboard". Archivo que contendrá los parametros obtenidos de la calibración de la camara.

#### [Mi archivo](https://github.com/vanttec/TMR2025/blob/pose_estimator/calibration_chessboard.yaml) se ve de esta manera:
![yamlexmpl](https://github.com/user-attachments/assets/4ea71ca0-10e5-4ddc-b2c5-2858739407b9)


## 🎉🎉!LISTO!🎉🎉
### ¡La camara ya esta calibrada y lista para usarse! 😎


## EXTRA

### - Para estimación de pose se deberá descargar el archivo ["aruco_marker_pose_estimator.py"](https://github.com/vanttec/TMR2025/blob/pose_estimator/aruco_marker_pose_estimator.py) (que se puede encontrar en esta branch) y correr dentro del mismo folder en donde tenemos el archivo con los valores de calibración.
- Y despues corremos el codigo y empezamos a estimar 😁
![arucoestimation](https://github.com/user-attachments/assets/6ce9c419-d721-4454-bbbf-df6a2d1d019e)
![pouses](https://github.com/user-attachments/assets/a975383e-addb-4e25-ac5f-abccb70e704c)

