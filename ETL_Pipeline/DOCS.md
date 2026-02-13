# ETL Pipelines <!-- omit in toc -->

- [Data Sources](#data-sources)
  - [Datos para SQL Database](#datos-para-sql-database)
  - [Documentos para (Graph)RAG](#documentos-para-graphrag)
- [Metadatos y Esquemas](#metadatos-y-esquemas)
  - [Recetas](#recetas)
  - [Textos Médicos](#textos-médicos)
- [Pipelines](#pipelines)

## Data Sources
Fuentes de datos para cada tipo de base de datos que se van a poblar a lo largo del proyecto. Se tiene contemplado lo siguiente:
* Una base de datos SQL para almacenar las diferentes recetas y sus datos relacionados (instrucciones, ingredientes, valores nutricionales) con el fin de que sea consultada por medio de la IA usando MCP
* Una base de datos vectorial para almacenar los documentos e imágenes de las recetas con el fin de que la IA pueda entender y comprender el perfil de usuario al quien le está haciendo su meal prep. Las imágenes servirán para ilustrar al usuario como las comidas se ven

### Datos para SQL Database
De las siguientes fuentes se van a extraer: Datos estadísticos (valores nutricionales), Textos (instrucciones de preparación e ingredientes), Imágenes (cómo se ven las comidas)
* [allrecipes](https://www.allrecipes.com/)
    - Recetas de diferentes cocinas y estilos que no cuentan con un respaldo de expertos para ser consumidas o preparadas
    - Extraer todos las recetas y su información relevante de ingredientes, para hacerlas y sus aportes nutricionales
* [EatRight: Recipes](https://www.eatright.org/recipes)
    - Recetas con orientación nutricional y realizadas por expertos
    - Extraer todas las recetas y su información relevantes de ingredientes, para hacerlas y sus aportes nutricionales

### Documentos para (Graph)RAG
De las siguientes fuentes se van a extraer: Textos y Documentos (relacionados sobre salud, nutrición, dietas y wellness)
* [WHO Fact Sheet](https://www.who.int/news-room/fact-sheets)
    - Extraer textos relevantes sobre alimentación, dietas, salud alimentaria y manejo de alimentos
    * [Healthy diet](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)
    * [Food safety](https://www.who.int/news-room/fact-sheets/detail/food-safety)
    * [Malnutrition](https://www.who.int/news-room/fact-sheets/detail/malnutrition)
    * [Obesity and overweight](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight)
* [INSP (Instituto Nacional de Salud Pública, México)](https://insp.mx/) y Gobierno de México:
    - Extraer texto de las guías de alimentación para la población mexicana
    * [Guías Alimentarias y de Actividad Física](https://www.insp.mx/images/stories/2015/Noticias/Nutricion_y_Salud/Docs/151118_guias_alimentarias.pdf)
    * [Guías Alimentarias Saludables y Sostenibles para la Población Mexicana](https://www.gob.mx/cms/uploads/attachment/file/1029510/Guias_Alimentarias_Mexico_2025.pdf)
* [EatRight: Health](https://www.eatright.org/health)
    - Extraer textos relacionados al cuidado personal (wellness) y sobre nutrición en las condiciones de salud

## Metadatos y Esquemas
Para cada objeto abstracto/relevante para las bases de datos, se definen sus metadatos:

### Recetas
### Textos Médicos

## Pipelines
* [*E*] De la página [allrecipes](www.allrecipes.com), extraje las recetas de las diferentes cocinas con las que contaba
* [*T*] De cada receta, solo obtuve y formatee los valores y atributos de interés para el proyecto (ingredientes, pasos de elaboración, información nutricional)
* [*L*] De los atributos extraídos y transformados de cada receta, son vaciados hacia una base de datos SQL con fields basados en texto
* Para la construcción de la pipeline (principalmente la parte de la extraction y parte de la transformation) usé [Crawl4ai](https://docs.crawl4ai.com/), una herramienta que facilita el web scrapping usando una sintaxis más ligera y un procedimiento más corto para formatear el output 