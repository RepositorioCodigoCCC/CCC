#!/usr/bin/env python
# coding: utf-8

# # **ÍNDICE CALIDAD DEL DATO**

# ## **Índice V1.1 (16 variables)**

# In[2]:


# cargue de librerias
import numpy as np
import pandas as pd


# In[3]:


get_ipython().system('pip install openpyxl')
from openpyxl import Workbook
import openpyxl


# Ahora procedemos a realizar el cargue de la base de datos 

# In[4]:


BD=pd.read_excel("1. Consilidado de ventas 2022 (Original).xlsx",dtype={'NOMBRE':object, 'MATRICULA': object, 'NIT':object,'CLUSTER': object,'CIUDAD': object})
BD.info()
BD.head()


# # Medición de calidad de datos por dimensión

# ## Dimensión Exactitud

# In[5]:


## ACTIVOS TOTALES
activos_total=len(BD['ACTIVOS 2021 PRELIMINARES'].dropna()) #Se borran las entradas que no tienen información
activos_cero=sum(BD['ACTIVOS 2021 PRELIMINARES']==0) #Se saca aparte un grupo con los Activos que son iguales a cero 
activos_fuera_rango=sum(BD['ACTIVOS 2021 PRELIMINARES']<0) #Se saca aparte un grupo con los activos negativos

#El objetivo es buscar qué tan bien están las caracterísitcas para el índice
#El cero lo sacamos porque no se está plenamente seguro de donde si se digitó o no la información 

#metrica_activos_rango= 1 - (activos_fuera_rango/(activos_total-activos_cero))
metrica_activos_rango= 1 - ((activos_cero+activos_fuera_rango)/(activos_total))
metrica_activos_rango


# In[6]:


## VENTAS
ventas_total=len(BD['VENTAS FULL 2021 COP PRELIMINARES VALLE'].dropna())
ventas_cero=sum(BD['VENTAS FULL 2021 COP PRELIMINARES VALLE']==0)
ventas_fuera_rango=sum(BD['VENTAS FULL 2021 COP PRELIMINARES VALLE']<0)

# print(ventas_total);print(ventas_cero);print(ventas_fuera_rango)
#metrica_ventas_rango= 1 - (ventas_fuera_rango/(ventas_total-ventas_cero))
metrica_ventas_rango= 1 - ((ventas_cero+ventas_fuera_rango)/(ventas_total))
metrica_ventas_rango


# In[7]:


## NIT
nit_total=len(BD['NIT'].dropna())
nit_cero=sum(BD['NIT']==0)
print(nit_cero)

#metrica_nit_rango= 1 - (nit_fuera_rango/(patrimonio_nit_cero))
metrica_nit_rango= 1 - (nit_cero/nit_total)
metrica_nit_rango


# ### Indicador de calidad - Exactitud

# In[8]:


indicador_exactitud_minimo=min(metrica_activos_rango,metrica_ventas_rango,metrica_nit_rango)
indicador_exactitud_promedio=np.mean([metrica_activos_rango,metrica_ventas_rango,metrica_nit_rango])

print(f'El indicador de la dimensión EXACTITUD por medio del mínimo es: {np.round(indicador_exactitud_minimo,5)}')
print(f'El indicador de la dimensión EXACTITUD por medio del promedio es: {np.round(indicador_exactitud_promedio,5)}')


# ## Dimensión Completitud

# In[9]:


## ACTIVOS COMPLETITUD
registros_totales=len(BD) ## Cantidad de registros de la base de datos 

#Estamos buscando calcular el número de registros que tienen ACTIVOS nulo. 

#A la cantidad de registros totales le restamos el número de registros que no son nulos y 
#le sumamos los que tienen activos iguales a cero que también actuan como nulos

#Básicamente hicimos:
#Registros Nulos = Registros Totales - Registros que no son nulos + Registros que tienen activos iguales a cero

activos_nulos=registros_totales-len(BD['ACTIVOS 2021 PRELIMINARES'].dropna())+activos_cero 

activos_completos= 1- (activos_nulos/registros_totales)
activos_completos


# In[10]:


## VENTAS (INGRESOS_ACT_ORDINARIA)
ventas_nulos=registros_totales - len(BD['VENTAS FULL 2021 COP PRELIMINARES VALLE'].dropna()) + ventas_cero

ventas_completos= 1- (ventas_nulos/registros_totales)
ventas_completos


# In[11]:


## NIT
nit_nulos=registros_totales - len(BD['NIT'].dropna()) + sum(BD['NIT']==0)

nit_completos=1-(nit_nulos/registros_totales)
nit_completos


# In[12]:


## CIUDAD
ciudad_nulos=registros_totales - len(BD['CIUDAD'].dropna())

ciudad_completos=1 - (ciudad_nulos/registros_totales)
ciudad_completos


# In[13]:


## NOMBRE
nombre_nulos= registros_totales - len(BD['NOMBRE'].dropna())

nombre_completos= 1- (nombre_nulos/registros_totales)
nombre_completos


# In[14]:


## CLUSTER
cluster_nulos= registros_totales - len(BD['CLUSTER'].dropna())

cluster_completos= 1- (cluster_nulos/registros_totales)
cluster_completos


# In[15]:


#FECHA RENOVACIÓN 2021
fecha_ren_nulos= registros_totales - len(BD['FECHA RENOVACIÓN 2021'].dropna())

fecha_ren_completos= 1- (fecha_ren_nulos/registros_totales)
fecha_ren_completos


# ### Indicador de Calidad - Completitud 

# In[16]:


indicador_completitud_minimo=min(activos_completos,ventas_completos,nit_completos,ciudad_completos,
                                cluster_completos,nombre_completos,fecha_ren_completos)
indicador_completitud_promedio= np.mean([activos_completos,ventas_completos,nit_completos,ciudad_completos,
                                cluster_completos,nombre_completos,fecha_ren_completos])

print(f'El indicador de la dimensión COMPLETITUD por medio del mínimo es: {np.round(indicador_completitud_minimo,5)}')
print(f'El indicador de la dimensión COMPLETITUD por medio del promedio es: {np.round(indicador_completitud_promedio,5)}')


# ## Dimensión Consistencia

# In[20]:


## Nombre
#Se evalúa una subbase con los registros que pertenecen a Cali
BD_rm=pd.read_excel("MATREM_CCC_ENE-AGO2022_V1(SEP_08_EEE3).xlsx",dtype={'MATRICULA': object, 'NIT':object, 'Año de FECHA_RENOVACION':object, 'TELEFONO': object, 'RAZON_SOCIAL': object})
BD_rm.head()


# In[76]:


BD_rm_nombre=BD_rm.iloc[:, 7] # octava columna
BD_nombre=BD.iloc[:, 1] # segunda columna

BD["exists"] = BD_nombre.isin(BD_rm_nombre.explode()).astype(int)

sum(BD["exists"]==1)


# In[81]:


## Relación nombre-nombre
#Cumplimiento de relaciones dentro de la Base de Datos. Por ejemplo, las comunas de Cali no pueden tomar el valor de Comuna 80.
#Las relaciones inter-relación es entre bases de datos
nombre_error1=len(BD)-sum(BD["exists"]==1)

nombre_consistencia=1-(nombre_error1/len(BD))
nombre_consistencia


# In[82]:


#NIT
BD_rm_nit=BD_rm.iloc[:, 1] # segunda columna
BD_nit=BD.iloc[:, 0] # segunda columna

BD["exists"] = BD_nit.isin(BD_rm_nit.explode()).astype(int)

sum(BD["exists"]==1)


# In[83]:


## Relación nombre-nombre
#Cumplimiento de relaciones dentro de la Base de Datos. Por ejemplo, las comunas de Cali no pueden tomar el valor de Comuna 80.
#Las relaciones inter-relación es entre bases de datos
nit_error1=len(BD)-sum(BD["exists"]==1)

nit_consistencia=1-(nit_error1/len(BD))
nit_consistencia


# ### Indicador de calidad - Consistencia

# In[84]:


indicador_consistencia_minimo=min(nombre_consistencia,nit_consistencia)
indicador_consistencia_promedio= np.mean([nombre_consistencia,nit_consistencia])

print(f'El indicador de la dimensión CONSISTENCIA por medio del mínimo es: {np.round(indicador_consistencia_minimo,5)}')
print(f'El indicador de la dimensión CONSISTENCIA por medio del promedio es: {np.round(indicador_consistencia_promedio,5)}')


# ## Dimensión Unicidad

# In[85]:


import pandas as pd 
#BD.duplicate()
duplicate = BD[BD.duplicated()] 
  
duplicate 


# ### Indicador de calidad - Unicidad

# In[86]:


## Calculo indicador duplicado

porcentaje_no_duplicados= 1-(len(duplicate)/len(BD))
porcentaje_no_duplicados


# # Cálculo de indicador de calidad agregado

# In[87]:


IQA_min=(0.05*indicador_exactitud_minimo) + (0.3*indicador_completitud_minimo) + (0.05*indicador_consistencia_minimo) + (0.6*porcentaje_no_duplicados)
IQA_promedio=(0.05*indicador_exactitud_promedio) + (0.3*indicador_completitud_promedio) + (0.05*indicador_consistencia_promedio) + (0.6*porcentaje_no_duplicados)

##Minimo
print(f'Valor del IQA tomando como agregación el mínimo: \n')
print(f'Dimensión exactitud: {np.round(indicador_exactitud_minimo,5)}')
print(f'Dimensión completitud: {np.round(indicador_completitud_minimo,5)}')
print(f'Dimensión consistencia: {np.round(indicador_consistencia_minimo,5)}')
print(f'Dimensión unicidad: {np.round(porcentaje_no_duplicados,5)} \n')

print(f'El IQA obtenido por medio del método del mínimo es : {np.round(IQA_min,5)} \n')

##Promedio
print(f'Valor del IQA tomando como agregación el promedio: \n')
print(f'Dimensión exactitud: {np.round(indicador_exactitud_promedio,5)}')
print(f'Dimensión completitud: {np.round(indicador_completitud_promedio,5)}')
print(f'Dimensión consistencia: {np.round(indicador_consistencia_promedio,5)}')
print(f'Dimensión unicidad: {np.round(porcentaje_no_duplicados,5)} \n')

print(f'El IQA obtenido por medio del método del promedio es: {np.round(IQA_promedio,5)}')


# # Cálculo con pesos proporcionales 

# In[88]:


IQA_min=(0.25*indicador_exactitud_minimo) + (0.25*indicador_completitud_minimo) + (0.25*indicador_consistencia_minimo) + (0.25*porcentaje_no_duplicados)
IQA_promedio=(0.25*indicador_exactitud_promedio) + (0.25*indicador_completitud_promedio) + (0.25*indicador_consistencia_promedio) + (0.25*porcentaje_no_duplicados)

##Minimo
print(f'Valor del IQA tomando como agregación el mínimo: \n')
print(f'Dimensión exactitud: {np.round(indicador_exactitud_minimo,5)}')
print(f'Dimensión completitud: {np.round(indicador_completitud_minimo,5)}')
print(f'Dimensión consistencia: {np.round(indicador_consistencia_minimo,5)}')
print(f'Dimensión unicidad: {np.round(porcentaje_no_duplicados,5)} \n')

print(f'El IQA obtenido por medio del método del mínimo es : {np.round(IQA_min,5)} \n')

##Promedio
print(f'Valor del IQA tomando como agregación el promedio: \n')
print(f'Dimensión exactitud: {np.round(indicador_exactitud_promedio,5)}')
print(f'Dimensión completitud: {np.round(indicador_completitud_promedio,5)}')
print(f'Dimensión consistencia: {np.round(indicador_consistencia_promedio,5)}')
print(f'Dimensión unicidad: {np.round(porcentaje_no_duplicados,5)} \n')

print(f'El IQA obtenido por medio del método del promedio es: {np.round(IQA_promedio,5)}')


# In[ ]:




