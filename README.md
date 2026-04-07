# Meal Prep Planner for Schools<!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Context and Problem](#context-and-problem)
  - [Key Operational Requirements](#key-operational-requirements)
- [Value Proposition](#value-proposition)
- [Objective](#objective)
- [Key Features](#key-features)
- [ETL Pipelines](#etl-pipelines)
- [Author, Affiliation and Contact](#author-affiliation-and-contact)
- [Referencias](#referencias)

## Context and Problem
Between 2020 and 2024, the combined prevalence of **overweight and obesity in Mexico** reached **36.6% in school-age children** and **40.1% in adolescents**. These figures indicate a significant **deterioration in the health and nutritional** status of minors, driven largely by the recurrent consumption of ultra-processed products and sugary drinks, particularly in urban environments (Gaona-Pineda et al., 2025). 

Data shows that the **caloric contribution of ultra-processed products** in daily diets ranges from **16.8% in adults to 26.4% in school-aged children**, making this a **critical public health priority** (Gaona-Pineda et al., 2025).

In response, the Mexican government has implemented public policies such as the **"Sistema de Etiquetado Frontal de Advertencia Mexicano" (NOM-051)** to increase consumer awareness regarding high-calorie density and harmful additives (Secretaría de Economía, Secretaría de Salud, 2020).

### Key Operational Requirements
Following the **guidelines of "La Escuela es Nuestra"** (Programas para el Bienestar, 2026), this system is designed to meet the following standards:
* **Balanced Nutrition**: Providing food and beverages that foster a varied and healthy diet.
* **Economic Accessibility**: Maintaining a suggested cost of up to $15.00 MXN per student.
* **Cyclic Menu Planning**: Designing monthly menu cycles that satisfy specific nutritional requirements through recipe diversity.
* **Strategic Logistics**: Planning ingredient acquisition and storage management to guarantee safety and optimal usage conditions.

## Value Proposition
While commercial platforms exist, they often **lack full nutritional metadata** or **hide planning tools** behind **premium paywalls**. This project **bridges that gap** by providing:
* **Data-Driven Menu Planning**: Consolidating structured and unstructured data (instructions, nutritional facts, and costs) to design menus based on specific nutritional targets.
* **Inventory Generation**: Automatically calculating required supplies based on student enrollment.
* **Nutritional Analytics**: Processing structured and unstructured data to provide insights into caloric and bromatological contributions.

## Objective
Develop a **digital repository of nutritionally balanced recipes that streamlines weekly menu planning** in compliance with the operational guidelines of the "La Escuela es Nuestra" food service program (Programas para el Bienestar, 2026).

## Key Features
* **Implement Robust ETL Pipelines**: Design and deploy automated data flows for the extraction, transformation, and loading (ETL) of nutritional metadata and market costs from heterogeneous web sources.
* **Engineered Knowledge Ingestion**: Build a specialized pipeline for the ingestion and processing of technical literature and regulatory standards regarding food safety and nutritional requirements.
* **Develop Multi-Objective Optimization Models**: Deploy an AI-driven algorithm designed to balance high nutritional density with cost-efficiency, providing intelligent meal recommendations.
* **Design Real-Time UI/UX Interfaces**: Develop an intuitive and accessible dashboard that provides synchronous feedback on nutritional goal attainment and per-student budget constraints.
* **Automate Supply Chain Management**: Integrate a logistics module for the automated generation of ingredient lists and inventory requirements based on planned menu cycles.
* **Establish Foundation for Autonomous Agents**: Integrate technical documentation and embeddings to facilitate future development of a RAG-based autonomous assistant for intelligent menu generation.

## [ETL Pipelines](./ETL_Pipeline/DOCS.md)

## Author, Affiliation and Contact
Alexis Aguilar [Student of Bachelor's Degree in "Tecnologías para la Información en Ciencias" at Universidad Nacional Autónoma de México [UNAM](https://www.unam.mx/)]: alexis.uaguilaru@gmail.com

Project developed for the subject "Digital Repositories" taught in semestre 2026-2 and it is not affiliated to a political party.

## Referencias
* Gaona-Pineda, E. B., Arango-Angarita, A., Valenzuela-Bravo, D. G., Medina-Zacarías, M. C., Martinez-Tapia, B., Rodríguez-Ramírez, S., & Hernández-Carapia, N. (2025). Contribución energética de alimentos mínimamente procesados, ultraprocesados y factores sociodemográficos asociados. Salud Pública de México, 67 (6 (nov-dic)), 587-597. https://doi.org/10.21149/16998
* Secretaría de Economía, Secretaría de Salud. (2020, 24 de enero). NOM-051-SCFI/SSA1-2010, Especificaciones generales de etiquetado para alimentos y bebidas no alcohólicas preenvasados. https://www.dof.gob.mx/normasOficiales/8150/seeco11_C/seeco11_C.html
* Programas para el Bienestar. (2026, ene.). Guías LEEN 2026. https://laescuelaesnuestra.sep.gob.mx/