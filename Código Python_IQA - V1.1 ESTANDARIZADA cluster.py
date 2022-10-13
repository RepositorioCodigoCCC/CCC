#!/usr/bin/env python
# coding: utf-8

# # **ÍNDICE CALIDAD DEL DATO**

# ## **Índice V1.1 (16 variables)**

# In[1]:


# cargue de librerias
import numpy as np
import pandas as pd


# In[2]:


get_ipython().system('pip install openpyxl')
from openpyxl import Workbook
import openpyxl


# Ahora procedemos a realizar el cargue de la base de datos del registro mercantil

# In[6]:


BD=pd.read_excel("2. UEC_INICIATIVAS_CLUSTER (Estandarización).xlsx",dtype={'EMPRESA':object, 'SEGMENTO': object, 'NIT':object, 'CLUSTER':object, 'TELÉFONO1': object,'CELULAR': object})
BD.info()
BD.head()


# # Medición de calidad de datos por dimensión

# ## Dimensión Exactitud

# In[7]:


## TELEFONO
telefono_total=len(BD['TELÉFONO1'].dropna())
telefono_cero=sum(BD['TELÉFONO1']==0)

digitos=np.zeros(len(BD['TELÉFONO1']))
for i in range(len(BD['TELÉFONO1'])):
    k=len(str(BD['TELÉFONO1'][i]))
    digitos[i]=k
#print(digitos)
#digitos
cuenta=np.array(digitos)
cuenta=pd.value_counts(cuenta)
siete=sum(digitos==7)
telefono_fuera_rango=telefono_total-(siete)

metrica_telefono_rango= 1 - ((telefono_cero+telefono_fuera_rango)/telefono_total)
metrica_telefono_rango


# In[8]:


## CELULAR
celular_total=len(BD['CELULAR'].dropna())
celular_cero=sum(BD['CELULAR']==0)

digitos=np.zeros(len(BD['CELULAR']))
for i in range(len(BD['CELULAR'])):
    k=len(str(BD['CELULAR'][i]))
    digitos[i]=k
#print(digitos)
#digitos
cuenta=np.array(digitos)
cuenta=pd.value_counts(cuenta)
diez=sum(digitos==10)
celular_fuera_rango=celular_total-(diez)

metrica_celular_rango= 1 - ((celular_cero+celular_fuera_rango)/celular_total)
metrica_celular_rango


# In[9]:


## NIT
nit_total=len(BD['NIT'].dropna())
nit_cero=sum(BD['NIT']==0)
print(nit_cero)

#metrica_nit_rango= 1 - (nit_fuera_rango/(patrimonio_nit_cero))
metrica_nit_rango= 1 - (nit_cero/nit_total)
metrica_nit_rango


# ### Indicador de calidad - Exactitud

# In[10]:


indicador_exactitud_minimo=min(metrica_celular_rango,metrica_nit_rango,metrica_telefono_rango)
indicador_exactitud_promedio=np.mean([metrica_celular_rango,metrica_nit_rango,metrica_telefono_rango])

print(f'El indicador de la dimensión EXACTITUD por medio del mínimo es: {np.round(indicador_exactitud_minimo,5)}')
print(f'El indicador de la dimensión EXACTITUD por medio del promedio es: {np.round(indicador_exactitud_promedio,5)}')


# ## Dimensión Completitud

# In[11]:


registros_totales=len(BD) ## Cantidad de registros de la base de datos 


# In[12]:


## NIT
nit_nulos=registros_totales - len(BD['NIT'].dropna()) + sum(BD['NIT']==0)

nit_completos=1-(nit_nulos/registros_totales)
nit_completos


# In[13]:


## SEGMENTO
segmento_nulos=registros_totales - len(BD['SEGMENTO'].dropna()) + sum(BD['SEGMENTO']==0)

segmento_completos= 1- (segmento_nulos/registros_totales)
segmento_completos


# In[14]:


## CIUDAD
ciudad_nulos=registros_totales - len(BD['CIUDAD'].dropna())

ciudad_completos=1 - (ciudad_nulos/registros_totales)
ciudad_completos


# In[15]:


## CORREO
email_nulos= registros_totales - len(BD['CORREO1'].dropna())

email_completos= 1- (email_nulos/registros_totales)
email_completos


# In[16]:


## CELULAR
celular_nulos= registros_totales - len(BD['CELULAR'].dropna())

celular_completos= 1- (celular_nulos/registros_totales)
celular_completos


# In[17]:


## TELEFONO
telefono_nulos= registros_totales - len(BD['TELÉFONO1'].dropna())

telefono_completos= 1- (telefono_nulos/registros_totales)
telefono_completos


# In[18]:


## DIRECCIÓN COMERCIAL
direccion_nulos= registros_totales - len(BD['DIRECCIÓN'].dropna())

direccion_completos= 1- (direccion_nulos/registros_totales)
direccion_completos


# In[19]:


## CLUSTER
cluster_nulos= registros_totales - len(BD['CLUSTER'].dropna())

cluster_completos= 1- (cluster_nulos/registros_totales)
cluster_completos


# In[20]:


## EMPRESA
empresa_nulos= registros_totales - len(BD['EMPRESA'].dropna())

empresa_completos= 1- (empresa_nulos/registros_totales)
empresa_completos


# In[21]:


## CEDULA
cedula_nulos= registros_totales - len(BD['CEDULA'].dropna())

cedula_completos= 1- (cedula_nulos/registros_totales)
cedula_completos


# ### Indicador de Calidad - Completitud 

# In[22]:


indicador_completitud_minimo=min(nit_completos,segmento_completos,ciudad_completos,email_completos,telefono_completos,
                                 direccion_completos,celular_completos,cedula_completos,empresa_completos,cluster_completos)
                                
indicador_completitud_promedio= np.mean([nit_completos,segmento_completos,ciudad_completos,email_completos,telefono_completos,
                                 direccion_completos,celular_completos,cedula_completos,empresa_completos,cluster_completos])

print(f'El indicador de la dimensión COMPLETITUD por medio del mínimo es: {np.round(indicador_completitud_minimo,5)}')
print(f'El indicador de la dimensión COMPLETITUD por medio del promedio es: {np.round(indicador_completitud_promedio,5)}')


# ## Dimensión Consistencia

# In[23]:


## Nombre
#Se evalúa una subbase con los registros que pertenecen a Cali
BD_rm=pd.read_excel("MATREM_CCC_ENE-AGO2022_V1(SEP_08_EEE3).xlsx",dtype={'MATRICULA': object, 'NIT':object, 'Año de FECHA_RENOVACION':object, 'TELEFONO': object, 'RAZON_SOCIAL': object})
BD_rm.head()


# In[24]:


BD_rm_nombre=BD_rm.iloc[:, 7] # octava columna
BD_nombre=BD.iloc[:, 1] # segunda columna

BD["exists"] = BD_nombre.isin(BD_rm_nombre.explode()).astype(int)

sum(BD["exists"]==1)


# In[25]:


## Relación nombre-nombre
#Cumplimiento de relaciones dentro de la Base de Datos. Por ejemplo, las comunas de Cali no pueden tomar el valor de Comuna 80.
#Las relaciones inter-relación es entre bases de datos
nombre_error1=len(BD)-sum(BD["exists"]==1)

nombre_consistencia= 1 - (nombre_error1/len(BD))
nombre_consistencia


# In[26]:


#NIT
BD_rm_nit=BD_rm.iloc[:, 1] # segunda columna
BD_nit=BD.iloc[:, 0] # segunda columna

BD["exists"] = BD_nit.isin(BD_rm_nit.explode()).astype(int)

sum(BD["exists"]==1)


# In[27]:


## Relación nombre-nombre
#Cumplimiento de relaciones dentro de la Base de Datos. Por ejemplo, las comunas de Cali no pueden tomar el valor de Comuna 80.
#Las relaciones inter-relación es entre bases de datos
nit_error1=len(BD)-sum(BD["exists"]==1)

nit_consistencia= 1 - (nit_error1/len(BD))
nit_consistencia


# ### Indicador de calidad - Consistencia

# In[28]:


indicador_consistencia_minimo=min(nombre_consistencia,nit_consistencia)
indicador_consistencia_promedio= np.mean([nombre_consistencia,nit_consistencia])

print(f'El indicador de la dimensión CONSISTENCIA por medio del mínimo es: {np.round(indicador_consistencia_minimo,5)}')
print(f'El indicador de la dimensión CONSISTENCIA por medio del promedio es: {np.round(indicador_consistencia_promedio,5)}')


# ## Dimensión Unicidad

# In[29]:


#Copia de la BD inicial
df=BD.copy()


# In[30]:


# Para obtener los duplicados EXCEPTO la primera observación revisando todas las columnas 
duplicados = df[df.duplicated()]
print('El número de registros duplicados con todas las columnas iguales son:')
print (duplicados.count())


# In[31]:


# Antes de partir la base de datos. Se hace un conteo para saber cuantas Matriculas y Renovaciones se tienen en la base sin eliminar duplicados
len(duplicados)


# ### Indicador de calidad - Unicidad

# In[32]:


## Calculo indicador duplicado

porcentaje_no_duplicados= 1-(len(duplicados)/len(df))
porcentaje_no_duplicados

#


# # Cálculo de indicador de calidad agregado

# In[33]:


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

# In[34]:


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

