# Meal Prep Planner <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Problemática](#problemática)
- [Objetivo General](#objetivo-general)
- [Objetivos Particulares](#objetivos-particulares)
- [ETL Pipelines](#etl-pipelines)
- [Regulaciones (Legal)](#regulaciones-legal)
- [Referencias](#referencias)

## Problemática
En las escuela de tiempo (jornada) completa o, en general, en cualquier institución educativa se tiende a tener una estigma negativa hacia los alimentos que ofrecen, tachándolos de alimentos de baja calidad o con poco valor nutricional; y además, los menús ofertados pueden son poco variados a lo largo de las semanas haciendo que los niños y jóvenes pierdan el interés de comer de forma saludable o, incluso, de probar otras opciones de alimentos. Por ello, pueden existir una aparente desnutrición entre los estudiantes por falta de más opciones y variedad, situación que se puede resolver a través de una planificación cuidadosa de los menús semanales.

## Objetivo General
Crear un repositorio digital de recetas saludables y variadas basadas en la cocina regional mexicana, que sean fáciles de consultar usando criterios como: aportes nutricionales, precio por porción y tiempo de preparación. 

## Objetivos Particulares
* Desarrollar e implementar *ETL Pipelines* para:
    - Extraer aportes nutricionales y precio estimado de ingredientes de la cocina mexicana. Cargar los datos hacia una base de datos SQL en Postgres
    - Extraer tiempo total de preparación, porciones por preparación, ingredientes, instrucciones de elaboración y aportes nutricionales de recetas. Añadir estimación de precio por porción y valores de aportes nutricionales faltantes. Cargar los datos hacia una base de datos SQL en Postgres
    - Extraer y descargar imágenes representativas y/o ilustrativas de las recetas extraídas. Cargar las imágenes hacia un almacenamiento basado en objetos
    - Extraer textos, documentos y artículos sobre nutrición, salud, manejo de alimentos, técnicas de preparación y políticas públicas de alimentación saludable en las escuelas e instituciones educativas. Generar los embeddings de los textos y cargarlos hacia una base de datos vectorial en Qdrant

* Seleccionar modelar con capacidades de tooling y reasoning
* Crear conexión del modelo hacia la DB vectorial para obtener los textos y documentos para adecuados según el usuario
* Crear conexión del modelo hacia la SQL DB por medio de MCP para obtener recetas específicas en base a una criteria
* Crear interfaz para el chat para la interacción usuario-IA
* Crear dashboards para hacer el tracking de las comidas y nutrientes consumidos por el usuario (para hacer análisis y recomendaciones más relevantes)
* Crear un buscador de recetas (recetarios) con las recetas extraídas 

## [ETL Pipelines](./ETL_Pipeline/DOCS.md)

## Regulaciones (Legal)
* Sellos alimenticios
  
## Referencias