# web scraping.



## Contexto
El objeto de este proyecto es el de obtener de 5 webs detalle de todos los productos que venden.
Al final del proyecto obtendremos 5 ficheros csv donde se muestran los productos que cada retail tiene en ese momento.

## Operativa:  
Basicamente los 5 datasets obtenidos tienen como estructura comun los siguientes campos:  

* Url
* Nombre producto
* Preferencia
* Descipción
* Precio

La forma de recopiar los datasets son muy parecidas y en el siguiente orden:  
1. Obtendo la url raiz de la tienda (contendida en un archivo plano)
2. Subtituyo la url por la palabra tienda  
3. Recorro la raiz inicial en busca de url "hijos"  
4. Recopilo los diferentes URL en una lista que la limpio de datos innecesarios y elementos duplicados  
5. Recorro la lista de hijos en busca de nuevas url
6. Recopilo las nuevas url y hago nuevamente una limpieza de la nueva lista.
7. De esta última lista de url donde se detallan cada uno de los productos, realizo el scraping
8. Genero un diccionario seleccionando los campos que más me interesan.
9. Por último convierto el diccionario en un dataframe y este en un csv.

En todas las transformaciones y con el fin de preservar la url y el nombre comercial de la empresa retail,
aplico el pundo 2


## Operativa.

Para su correcta ejecución recomiendo:
1. Generar una carpeta

        $ mkdir -directorio
    
2. Generar un entorno virtual   
    en linux  
    
        $ python3 -m venv /path/to/new/virtual/environment   
    
    en windows
    
        c:\>c:\Python35\python -m venv c:\path\to\myenv
    
3. Instalar los módulos necesarios detallados en el fichero requirements.txt

        $ pip install requirements.txt
    
4. Ejecutar cada un de los ejecutables según la tienda

        $ python tienda_#.py
    
    donde # es el número de tienda, desde 0 hasta 1.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
