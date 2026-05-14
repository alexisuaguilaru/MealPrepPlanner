# Meal Prep Planner for Schools<!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Context and Problem](#context-and-problem)
  - [Key Operational Requirements](#key-operational-requirements)
- [Value Proposition](#value-proposition)
- [Objective](#objective)
- [Key Features](#key-features)
- [ETL Pipeline](#etl-pipeline)
  - [Usage](#usage)
  - [Datasets](#datasets)
  - [Frontend and Dashboard](#frontend-and-dashboard)
- [Future Roadmap \& Expansion](#future-roadmap--expansion)
- [Author, Affiliation and Contact](#author-affiliation-and-contact)
- [References](#references)

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

## ETL Pipeline
For a **detailed technical overview** of the recipe, ingredient and technical documents **data ingestion flows**, please refer to the [ETL Pipeline](./ETL_Pipeline/README.md) documentation.

### Usage
Follow these steps to properly use the pipeline:
1. **Configure Credentials**: Create a *Kiwilimón account*. Copy the example credential file and update it with your *username* and *password*:
```bash
cp ./ETL_Pipeline/CREDENTIAL_EXAMPLE.json ./ETL_Pipeline/CREDENTIAL.json
```
2. **Install Dependencies**: It is recommended to use a Python virtual environment. Install the required libraries with:
```bash
pip install -r ./ETL_Pipeline/requirements.txt
```
3. **Environment Variables**: For production or custom deployments, configure your environment variables by copying the example file:
```bash
cp .env.example .env
```
4. **Start Services**: Launch the Docker services for the database:
```bash
docker compose up -d
```
5. **Run the Pipeline**: Execute the ETL process with the following command:
```bash
python -m ETL_Pipeline
```
6. **Run the Frontend**: Execute the Streamlit script to show  the planner:
```bash
streamlit run Frontend
```

*Note: Ensure the environment variables are exported to your system so the ETL script can access them during execution.*

### Datasets
Upon successful execution of the pipeline, all **processed data** (available in CSV, JSON, PDF, and Markdown formats) is **organized and stored** in the [Datasets](./Datasets/) folder. Additionally, this directory includes **specific CSV files** designed for **database reconstruction**, facilitating seamless migrations to other systems or a complete database reset if required.

### Frontend and Dashboard
For a **detailed technical overview** of the **frontend and dashboard**, please refer to the [Frontend](./Frontend/README.md) documentation.

## Future Roadmap & Expansion
This project is designed for **continuous evolution**, with several key expansion axes to enhance systemic quality:
* **Database Scaling**: Increasing the repository's volume and quality by integrating diverse international recipes and real-time data sources for market costs and nutritional metrics.
* **End-to-End Automation**: Transitioning into a comprehensive service model to simplify planning through intelligent processes. This reduces operational overhead by automating supplier prospecting and recipe selection.
* **Agentic AI Integration**: Implementing autonomous agents to manage the entire planning lifecycle-optimizing for nutritional requirements, remaining inventory, and automated procurement without human intervention.

## Author, Affiliation and Contact
Alexis Aguilar [Student of Bachelor's Degree in "Tecnologías para la Información en Ciencias" at Universidad Nacional Autónoma de México [UNAM](https://www.unam.mx/)]: alexis.uaguilaru@gmail.com

Project developed for the subject "Digital Repositories" taught in semestre 2026-2 and it is not affiliated to a political party.

## References
* Gaona-Pineda, E. B., Arango-Angarita, A., Valenzuela-Bravo, D. G., Medina-Zacarías, M. C., Martinez-Tapia, B., Rodríguez-Ramírez, S., & Hernández-Carapia, N. (2025). Contribución energética de alimentos mínimamente procesados, ultraprocesados y factores sociodemográficos asociados. Salud Pública de México, 67 (6 (nov-dic)), 587-597. https://doi.org/10.21149/16998
* Secretaría de Economía, Secretaría de Salud. (2020, 24 de enero). NOM-051-SCFI/SSA1-2010, Especificaciones generales de etiquetado para alimentos y bebidas no alcohólicas preenvasados. https://www.dof.gob.mx/normasOficiales/8150/seeco11_C/seeco11_C.html
* Programas para el Bienestar. (2026, ene.). Guías LEEN 2026. https://laescuelaesnuestra.sep.gob.mx/