# Meal Prep Planner <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Problemática](#problemática)
- [Objetivo General](#objetivo-general)
- [Objetivos Particulares](#objetivos-particulares)
- [ETL Pipelines](#etl-pipelines)

## Problemática
Este proyecto surge de uno de los principales problemas que he tenido cómo foráneo, y que he visto que muchas otras personas sufren de ello: No saber qué comer durante su día o semana. Planear qué comidas vas a preparar y hacer te ahorra tanto tiempo como dinero, debido a que compras lo necesario para las preparaciones y solo tienes que bloquear un espacio de tu tiempo para hacer las preparaciones para toda tu semana; aunque existe vídeos en YouTube sobre esta técnica de "Meal Prep" orientada para estudiantes, profesionales u oficinistas, de los pocos vídeos que he visto muchos de ellos no hacen una planeación más allá de una semana o de los días laborales, y casi siempre se enfocan en la comida principal (la del mediodía). Por ello, el usar una IA capaz de planificar tus tres comidas diarias durante una semana completa se vuelve un asistente que pueda facilitar mucho tu estilo de vida y mejorar incluso tu alimentación.

## Objetivo General
Crear un ChatBot a modo de asistente personal capaz de comprender y analizar el perfil físico-salud y rutina diaria de una persona para generar una planificación de sus tres comidas diarias durante una semana completa de forma que sea totalmente customizable y adaptable al usuario basada en las recetas y alimentos de México. 

## Objetivos Particulares
* Crear ETL pipelines para la extracción de recetas (ingredientes, instrucciones y valores nutricionales) y hacer loaded hacia una base de datos SQL
* Crear ETL pipelines para la extracción de textos y documentos sobre nutrición, salud y manejo de alimentos, y hacer loaded hacia una base de datos vectorial
* Seleccionar modelar con capacidades de tooling y reasoning
* Crear conexión del modelo hacia la DB vectorial para obtener los textos y documentos para adecuados según el usuario
* Crear conexión del modelo hacia la SQL DB por medio de MCP para obtener recetas específicas en base a una criteria
* Crear interfaz para el chat para la interacción usuario-IA
* Crear dashboards para hacer el tracking de las comidas y nutrientes consumidos por el usuario (para hacer análisis y recomendaciones más relevantes)

## [ETL Pipelines](./ETL_Pipeline/DOCS.md)