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

# In[3]:


BD=pd.read_excel("MATREM_CCC_ENE-AGO2022_V1(SEP_08_EEE3).xlsx",dtype={'CODIGO_CIIU':object, 'MATRICULA': object, 'NIT':object, 'Año de FECHA_RENOVACION':object, 'TELEFONO': object})
BD.info()
BD.head()


# # Medición de calidad de datos por dimensión

# ## Dimensión Exactitud

# In[208]:


## ACTIVOS TOTALES
activos_total=len(BD['TOT_ACTIVOS'].dropna()) #Se borran las entradas que no tienen información
activos_cero=sum(BD['TOT_ACTIVOS']==0) #Se saca aparte un grupo con los Activos que son iguales a cero 
activos_fuera_rango=sum(BD['TOT_ACTIVOS']<0) #Se saca aparte un grupo con los activos negativos

#El objetivo es buscar qué tan bien están las caracterísitcas para el índice
#El cero lo sacamos porque no se está plenamente seguro de donde si se digitó o no la información 

#metrica_activos_rango= 1 - (activos_fuera_rango/(activos_total-activos_cero))
metrica_activos_rango= 1 - ((activos_cero+activos_fuera_rango)/(activos_total))
metrica_activos_rango


# In[10]:


## PASIVOS TOTALES

##Es correcto o incorrecto que los pasivos sean negativos.
pasivos_total=len(BD['TOT_PASIVO'].dropna())
pasivos_cero=sum(BD['TOT_PASIVO']==0) 
pasivos_fuera_rango=sum(BD['TOT_PASIVO']<0)

print(pasivos_total)
print(pasivos_cero)
print(pasivos_fuera_rango)

metrica_pasivos_rango= 1 - (pasivos_fuera_rango/(pasivos_total-pasivos_cero))
#metrica_pasivos_rango= 1 - (pasivos_cero/(pasivos_total))
metrica_pasivos_rango


# In[126]:


## VENTAS
ventas_total=len(BD['VENTAS'].dropna())
ventas_cero=sum(BD['VENTAS']==0)
ventas_fuera_rango=sum(BD['VENTAS']<0)

# print(ventas_total);print(ventas_cero);print(ventas_fuera_rango)
#metrica_ventas_rango= 1 - (ventas_fuera_rango/(ventas_total-ventas_cero))
metrica_ventas_rango= 1 - ((ventas_cero+ventas_fuera_rango)/(ventas_total))
metrica_ventas_rango


# In[127]:


## PATRIMONIO
patrimonio_total=len(BD['PATRIMONIO'].dropna())
patrimonio_cero=sum(BD['PATRIMONIO']==0)
patrimonio_fuera_rango=sum(BD['PATRIMONIO']<0)

print(patrimonio_cero);print(patrimonio_fuera_rango)

#metrica_patrimonio_rango= 1 - (patrimonio_fuera_rango/(patrimonio_total-ventas_cero))
metrica_patrimonio_rango= 1 - ((patrimonio_cero+patrimonio_fuera_rango)/patrimonio_total)
metrica_patrimonio_rango


# In[206]:


## TELEFONO
telefono_total=len(BD['TELEFONO'].dropna())
telefono_cero=sum(BD['TELEFONO']==0)

digitos=np.zeros(len(BD['TELEFONO']))
for i in range(len(BD['TELEFONO'])):
    k=len(str(BD['TELEFONO'][i]))
    digitos[i]=k
#print(digitos)
#digitos
cuenta=np.array(digitos)
cuenta=pd.value_counts(cuenta)
diez=sum(digitos==10)
siete=sum(digitos==7)
telefono_fuera_rango=telefono_total-(diez+siete)

metrica_telefono_rango= 1 - ((telefono_cero+telefono_fuera_rango)/telefono_total)
metrica_telefono_rango


# In[209]:


## COMUNA

BD_cali=BD[BD['CIUDAD']=='Cali']
registros_tot_comunas=len(BD_cali)
comunas=BD_cali['COMUNA'].value_counts()
comunas


# In[132]:


sentence = BD_cali['COMUNA']    
Comuna80 = 0
for i in sentence:
    if i == "Comuna 80":
        Comuna80 = Comuna80 + 1
print(Comuna80)


# In[210]:


comuna_fuera_rango=Comuna80
metrica_comuna_rango= 1 - ((comuna_fuera_rango)/registros_tot_comunas)
metrica_comuna_rango


# In[211]:


## NIT
nit_total=len(BD['NIT'].dropna())
nit_cero=sum(BD['NIT']==0)
print(nit_cero)

#metrica_nit_rango= 1 - (nit_fuera_rango/(patrimonio_nit_cero))
metrica_nit_rango= 1 - (nit_cero/nit_total)
metrica_nit_rango


# ### Indicador de calidad - Exactitud

# In[212]:


indicador_exactitud_minimo=min(metrica_activos_rango,metrica_pasivos_rango,metrica_ventas_rango,metrica_patrimonio_rango,metrica_comuna_rango,metrica_nit_rango,metrica_telefono_rango)
indicador_exactitud_promedio=np.mean([metrica_activos_rango,metrica_pasivos_rango,metrica_ventas_rango,metrica_patrimonio_rango,metrica_comuna_rango,metrica_nit_rango,metrica_telefono_rango])

print(f'El indicador de la dimensión EXACTITUD por medio del mínimo es: {np.round(indicador_exactitud_minimo,5)}')
print(f'El indicador de la dimensión EXACTITUD por medio del promedio es: {np.round(indicador_exactitud_promedio,5)}')


# ## Dimensión Completitud

# In[149]:


## ACTIVOS COMPLETITUD
registros_totales=len(BD) ## Cantidad de registros de la base de datos 

#Estamos buscando calcular el número de registros que tienen ACTIVOS nulo. 

#A la cantidad de registros totales le restamos el número de registros que no son nulos y 
#le sumamos los que tienen activos iguales a cero que también actuan como nulos

#Básicamente hicimos:
#Registros Nulos = Registros Totales - Registros que no son nulos + Registros que tienen activos iguales a cero

activos_nulos=registros_totales-len(BD['TOT_ACTIVOS'].dropna())+activos_cero 

activos_completos= 1- (activos_nulos/registros_totales)
activos_completos


# In[150]:


## PASIVOS COMPLETITUD 
pasivos_nulos=registros_totales-len(BD['TOT_PASIVO'].dropna())

pasivos_completos= 1-(pasivos_nulos/registros_totales)
pasivos_completos


# In[151]:


## VENTAS (INGRESOS_ACT_ORDINARIA)
ventas_nulos=registros_totales - len(BD['VENTAS'].dropna()) + ventas_cero

ventas_completos= 1- (ventas_nulos/registros_totales)
ventas_completos


# In[152]:


## PATRIMONIO
patrimonio_nulos=registros_totales - len(BD['PATRIMONIO'].dropna())

patrimonio_completos= 1-(patrimonio_nulos/registros_totales)
patrimonio_completos


# In[153]:


## NIT
nit_nulos=registros_totales - len(BD['NIT'].dropna()) + sum(BD['NIT']==0)

nit_completos=1-(nit_nulos/registros_totales)
nit_completos


# In[154]:


## SECTOR
sector_nulos=registros_totales - len(BD['SECTOR'].dropna()) + sum(BD['SECTOR']==0)

sector_completos= 1- (sector_nulos/registros_totales)
sector_completos


# In[155]:


## CIUDAD
ciudad_nulos=registros_totales - len(BD['CIUDAD'].dropna())

ciudad_completos=1 - (ciudad_nulos/registros_totales)
ciudad_completos


# In[156]:


## COMUNA
#Se evalúa una subbase con los registros que pertenecen a Cali
BD_cali=BD[BD['CIUDAD']=='Cali']
registros_tot_comunas=len(BD_cali)

comuna_nulos= registros_tot_comunas - len(BD_cali['COMUNA'].dropna())

comuna_completos= 1- (comuna_nulos/registros_tot_comunas)
comuna_completos


# In[157]:


#UTILIDAD PERDIDA (UTILIDAD OPERACIONAL)
#Cómo manejar el hecho que la variable tenga tantos registros iguales a cero, los manejamos como nulos?
utilidad_perdida_nulos=registros_totales - len(BD['UTILILIDAD_PERDIDA'].dropna())

#Formas de revisar la cantidad de ceros que tiene esta variable 
#sum(BD['UTILILIDAD_PERDIDA'] == 0)
#print((BD['UTILILIDAD_PERDIDA']==0).value_counts())


utilidad_perdida_completos = 1 - (utilidad_perdida_nulos/registros_totales)
utilidad_perdida_completos


# In[158]:


## UTILIDAD BRUTA (RESULTADO_PERIODO)
utilidad_bruta_nulos= registros_totales - len(BD['UTILILIDAD_BRUTA'].dropna())

#Siempres es 1 menos el complemento (lo que está mal). El resultado nos da la proporción de la variable que está bien

utilidad_bruta_completos= 1- (utilidad_bruta_nulos/registros_totales)
utilidad_bruta_completos


# In[159]:


## EMAIL
email_nulos= registros_totales - len(BD['EMAIL'].dropna())

email_completos= 1- (email_nulos/registros_totales)
email_completos


# In[160]:


## TELEFONO
telefono_nulos= registros_totales - len(BD['TELEFONO'].dropna())

telefono_completos= 1- (telefono_nulos/registros_totales)
telefono_completos


# In[161]:


## BARRIO
barrio_nulos= registros_totales - len(BD['BARRIO'].dropna())

barrio_completos= 1- (barrio_nulos/registros_totales)
barrio_completos


# In[162]:


## DIRECCIÓN COMERCIAL
direccion_nulos= registros_totales - len(BD['DIRECCION_COMERCIAL'].dropna())

direccion_completos= 1- (direccion_nulos/registros_totales)
direccion_completos


# In[163]:


## PERSONAL OCUPADO
personal_ocupado_nulos= registros_totales - len(BD['PERSONAL_OCUPADO'].dropna())

personal_ocupado_completos= 1- (personal_ocupado_nulos/registros_totales)
personal_ocupado_completos


# In[164]:


## REPRESENTANTE LEGAL
rep_legal_nulos= registros_totales - len(BD['REP_LEGAL'].dropna())

rep_legal_completos= 1- (rep_legal_nulos/registros_totales)
rep_legal_completos


# In[165]:


## ESTABLECIMIENTOS
establecimientos_nulos= registros_totales - len(BD['ESTABLECIMIENTOS'].dropna())

establecimientos_completos= 1- (establecimientos_nulos/registros_totales)
establecimientos_completos


# ### Indicador de Calidad - Completitud 

# In[166]:


indicador_completitud_minimo=min(activos_completos,pasivos_completos,patrimonio_completos,ventas_completos,
                                nit_completos,sector_completos,ciudad_completos,comuna_completos, utilidad_perdida_completos,
                                utilidad_bruta_completos,email_completos,telefono_completos,barrio_completos,direccion_completos,
                                personal_ocupado_completos,rep_legal_completos,establecimientos_completos)
indicador_completitud_promedio= np.mean([activos_completos,pasivos_completos,patrimonio_completos,ventas_completos,
                                nit_completos,sector_completos,ciudad_completos,comuna_completos, utilidad_perdida_completos,
                                utilidad_bruta_completos,email_completos,telefono_completos,barrio_completos,direccion_completos,
                                        personal_ocupado_completos,rep_legal_completos,establecimientos_completos])

print(f'El indicador de la dimensión COMPLETITUD por medio del mínimo es: {np.round(indicador_completitud_minimo,5)}')
print(f'El indicador de la dimensión COMPLETITUD por medio del promedio es: {np.round(indicador_completitud_promedio,5)}')


# ## Dimensión Consistencia

# In[167]:


## Relación CIUDAD-COMUNA
#Cumplimiento de relaciones dentro de la Base de Datos. Por ejemplo, las comunas de Cali no pueden tomar el valor de Comuna 80.
#Las relaciones inter-relación es entre bases de datos
ciudad_comuna_error1=sum(BD_cali['COMUNA']=='Comuna 80')

ciudad_comuna_consistencia= 1 - (ciudad_comuna_error1/len(BD_cali))
ciudad_comuna_consistencia


# In[168]:


## Relación PATRIMONIO = ACTIVO - PASIVO

#Sacamos los registros donde hay información para las tres variables al tiempo
BD_patrimonio=BD[BD['PATRIMONIO'].notna() & BD['TOT_ACTIVOS'].notna() & BD['TOT_PASIVO'].notna()] ##Registros donde hay información para evaluar la ecuación contable

patrimonio_calc= BD_patrimonio['TOT_ACTIVOS'] - BD_patrimonio['TOT_PASIVO'] 

#Revisar si la forma en que calculamos la ecuación contable corresponde al dato que hay en la base

compara_patrimonio= BD_patrimonio['PATRIMONIO'] == patrimonio_calc

##Formas de revisar cuántos cumplen la condición de la ecuación contable
print(compara_patrimonio.value_counts())

print((BD['UTILILIDAD_PERDIDA']==0).value_counts())

patrimonio_consistencia = sum(compara_patrimonio)/len(patrimonio_calc)
patrimonio_consistencia


# ### Indicador de calidad - Consistencia

# In[169]:


indicador_consistencia_minimo=min(ciudad_comuna_consistencia,patrimonio_consistencia)
indicador_consistencia_promedio= np.mean([ciudad_comuna_consistencia,patrimonio_consistencia])

print(f'El indicador de la dimensión CONSISTENCIA por medio del mínimo es: {np.round(indicador_consistencia_minimo,5)}')
print(f'El indicador de la dimensión CONSISTENCIA por medio del promedio es: {np.round(indicador_consistencia_promedio,5)}')


# ## Dimensión Unicidad

# In[170]:


#Copia de la BD inicial
df=BD.copy()
df.rename(columns={'Año de FECHA_RENOVACION':'ULTIMO_ANO_RENOVADO',
                          'FECHA_MAT_REN':'FECHA_MATRICULA_RENOVACION_HORA',
                          'TOT_ACTIVOS':'ACTIVO_TOTAL',
                          'UTILILIDAD_PERDIDA': 'UTILILIDAD_OPERACIONAL',
                          'VENTAS' : 'INGRESOS_ACTIVIDAD_ORDINARIA',
                          'TOT_PASIVO': 'PASIVO_TOTAL',
                          'UTILILIDAD_BRUTA': 'RESULTADO_PERIODO',
                          'MAT_REN' : 'MATRICULA_RENOVACION'}, 
                 inplace=True)


# In[171]:


# Se separa la fecha para facilitar el análisis
df[['FECHA_MATRICULA_RENOVACION','HORA_FECHA_MAT_REN']] =  df.FECHA_MATRICULA_RENOVACION_HORA.str.split(' ', n=1, expand=True)


# In[172]:


# Se separa día, mes y año para facilitar el análisis
df[['DIA','MES', 'ANO']] =  df.FECHA_MATRICULA_RENOVACION.str.split('/', n=3, expand=True)
#Se convierte la variable FECHA_MATRICULA_RENOVACION_HORA en datetime para facilitar manupulación de los datos
df.FECHA_MATRICULA_RENOVACION_HORA = pd.to_datetime(df.FECHA_MATRICULA_RENOVACION_HORA)


# In[173]:


#Se convierte la variable FECHA_MATRICULA en datetime para facilitar manupulación de los datos
df.FECHA_MATRICULA = pd.to_datetime(df.FECHA_MATRICULA)


# In[174]:


#Se organiza el DataFrame según la fecha del movimiento registrado. Esto facilitará las particiones que se harán de la base de datos
df=df.sort_values('FECHA_MATRICULA_RENOVACION_HORA')
print(df.info())
df.head(2)


# In[175]:


df.groupby('ESTADO_MAT_REN').nunique()


# In[176]:


# Para obtener los duplicados EXCEPTO la primera observación revisando todas las columnas 
duplicados = df[df.duplicated()]
print('El número de registros duplicados con todas las columnas iguales son:')
print (duplicados.MATRICULA.count())


# In[177]:


# Antes de partir la base de datos. Se hace un conteo para saber cuantas Matriculas y Renovaciones se tienen en la base sin eliminar duplicados
df.MATRICULA_RENOVACION.value_counts()


# In[178]:


# Ahora es necesario partir la base de datos en dos para hacer la correspondiente limpieza. Se requieren tratar las empresas Matriculadas y Renovadas diferenciadas por su fecha de registro
df_matricula = df.loc[df['MATRICULA_RENOVACION'].isin(['Matricula'])]
df_renovacion = df.loc[df['MATRICULA_RENOVACION'].isin(['Renovacion'])]
print('El número de registros en la BD para Matriculas es:', df_matricula.MATRICULA_RENOVACION.value_counts(), sep='\n')
print('El número de registros en la BD para Renovaciones:', df_renovacion.MATRICULA_RENOVACION.value_counts(), sep='\n')


# In[179]:


# Aqui DEBE IR EL CODIGO DESPUES DE LIMPIAR EL TEMA DE RENOVACIONES MAS VIEJAS QUE LAS MATRICULAS. SE DEBEN ELIMINAR LAS RENOVACIONES CON FECHAS ANTERIORES A LAS DE LAS MATRICULAS porque esto es un indicador que la empresa hizo un translado de domicilio y se trajo todo su historial a la CCC
# Se convierte la variable FECHA_MATRICULA_RENOVACION_HORA en datetime para facilitar manupulación de los datos
df_renovacion.FECHA_MATRICULA_RENOVACION = pd.to_datetime(df_renovacion.FECHA_MATRICULA_RENOVACION)
df_renovacion = df_renovacion.loc[df_renovacion['FECHA_MATRICULA']<=df_renovacion['FECHA_MATRICULA_RENOVACION']]


# In[180]:


# Se organizan las bases según la fecha en la cual se hizo el movimiento corresspondiente a Matricual o Renovación para posterior limpieza. Vale aclarar que esta el ordenamiento es descendente, es decir, se comienza desde YYYY/01/01 00:00 hasta YYYY/12/31 23:59 (de enero a diciembre)
df_matricula=df_matricula.sort_values('FECHA_MATRICULA_RENOVACION_HORA')
df_renovacion=df_renovacion.sort_values('FECHA_MATRICULA_RENOVACION_HORA')
df_renovacion.head(2)


# In[183]:


# Se procede a eliminar los duplicados en las dos bases y la idea es dejar el último movimiento registrado. Esto se debe gracias a que se identificó que algunas empresas registran algun movimiento y por algun motivo este es devuelto, en la mayoría de los casos la corrección sugerida es hecha en el plazo para mantener la fecha inicial del movimiento, sin embargo, cuando la empresa deja pasar este plazo máximo se debe generar un nuevo movimiento lo cual genera duplicados en la información
df2_matricula=df_matricula.sort_values('FECHA_MATRICULA_RENOVACION_HORA').drop_duplicates('MATRICULA', keep='last')
df2_renovacion=df_renovacion.sort_values('FECHA_MATRICULA_RENOVACION_HORA').drop_duplicates('MATRICULA', keep='last')


# In[184]:


# Una vez eliminados lo duplicados se cuenta el número de resgitros 
print('El número de registros en la BD para Matriculas después de eliminar duplicados es:', df2_matricula.MATRICULA_RENOVACION.value_counts(), sep='\n')
print('El número de registros en la BD para Renovaciones después de eliminar duplicados es:', df2_renovacion.MATRICULA_RENOVACION.value_counts(), sep='\n')


# In[185]:


# Se procede a unir las bases de datos para la posterior limpieza en conjunto
df2 = pd.concat([df2_matricula, df2_renovacion])
df2 = df2.sort_values('MATRICULA_RENOVACION', ascending=True)
print('El número de registros en la BD unida es:', df2.MATRICULA_RENOVACION.value_counts(), sep='\n')


# In[186]:


# Para eliminar duplicados se debe tener en cuenta que en Matricula nos interesa dejar el primer registro que tengamos en la base pues por cada matricula se genera una renovación
df3 = df2.sort_values('MATRICULA_RENOVACION', ascending=True).drop_duplicates('MATRICULA', keep='first')
print('El número de registros en la BD unida sin duplicados es:', df3.MATRICULA_RENOVACION.value_counts(), sep='\n')


# ### Indicador de calidad - Unicidad

# In[213]:


## Calculo indicador duplicado

porcentaje_no_duplicados= (len(df3)/len(df))
porcentaje_no_duplicados

#


# # Cálculo de indicador de calidad agregado

# In[214]:


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

# In[189]:


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




