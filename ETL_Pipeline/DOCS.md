# ETL Pipelines <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Data Sources](#data-sources)
  - [Datos para SQL Database e Image Database](#datos-para-sql-database-e-image-database)
  - [Documentos para (Graph)RAG y Vectorial Database](#documentos-para-graphrag-y-vectorial-database)
- [Metadatos y Esquemas](#metadatos-y-esquemas)
  - [Recetas](#recetas)
  - [Imágenes](#imágenes)
  - [Textos Médicos y Nutricionales](#textos-médicos-y-nutricionales)
- [Almacenamiento y Organización de los Datos](#almacenamiento-y-organización-de-los-datos)
  - [Almacenamiento](#almacenamiento)
  - [Organización](#organización)
- [Pipelines](#pipelines)

## Data Sources
Fuentes de datos para cada tipo de base de datos que se van a poblar a lo largo del proyecto. Se tiene contemplado lo siguiente:
* Una base de datos SQL para almacenar las diferentes recetas y sus datos relacionados (instrucciones, ingredientes, valores nutricionales) con el fin de que sea consultada por medio de la IA usando MCP. Por los objetivos adicionales del proyecto, es necesario consolidar entidades al momento de relacionar los ingredientes de las recetas con sus valores nutricionales.
* Una base de datos vectorial para almacenar los documentos e imágenes de las recetas con el fin de que la IA pueda entender y comprender el perfil de usuario al quien le está haciendo su meal prep. Las imágenes servirán para ilustrar al usuario como las comidas se ven

### Datos para SQL Database e Image Database
De las siguientes fuentes se van a extraer: Datos estadísticos (valores nutricionales), Textos (instrucciones de preparación e ingredientes), Imágenes (cómo se ven las comidas)
* [allrecipes: Mexican Cuisine](https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/)
    - Recetas con inspiración y "toques" mexicanos
    - Extraer todos las recetas y su información relevante de ingredientes, instrucciones, tiempo de preparación y sus aportes nutricionales
* [kiwilimon: Recetas](https://www.kiwilimon.com/recetas)
    - Recetas tradicionales y de inspiración regionales
    - Extraer recetas de ciertas categorías y su información relevante de ingredientes, instrucciones y tiempo de preparación
    - No cuentan con aportes nutricionales, por lo que es necesario generar sus aportes nutricionales
* [EatRight: Recipes](https://www.eatright.org/recipes)
    - Recetas internacionales con orientación nutricional y realizadas por expertos
    - Extraer todas las recetas y su información relevantes de ingredientes, para hacerlas y sus aportes nutricionales

### Documentos para (Graph)RAG y Vectorial Database
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
* [Larousse Cocina: Técnicas](https://laroussecocina.mx/tecnicas/)
    - Extraer información sobre algunas técnicas y formas de preparación

## Metadatos y Esquemas
Para cada objeto abstracto/relevante para las bases de datos, se definen sus esquemas de metadatos:

### Recetas
* Formato de Archivo:
    - `.sql` (Debido a que estos valores están en una base de datos SQL)
* Atributos:
    - Total Tiempo de Preparación
      - Valores enteros positivos 
      - Tiempo requerido para elaborar el platillo, este tiempo incluye los tiempos como de cocción o de horneado
    - Ingredientes
      - Dos listas de valores que representan los nombres y cantidades de ingredientes
      - Nombre de Ingredientes
        - Lista de *strings* 
        - Lista que contiene los nombres de cada ingrediente necesario para preparar la receta
      - Cantidad de Ingredientes
        - Lista de números flotantes
        - Lista que contiene la cantidad de cada ingrediente para preparar la receta
    - Instrucciones
      - Lista de *strings*
      - Pasos detallados para elaborar la receta 
    - Aportes Nutricionales
      - Dos listas de valores que representan los nombres de los macronutrientes y micronutrientes de una receta, y otra lista que contienen los valores de cada nutriente
      - Nombre de Nutrientes
        - Lista de *String*
        - Nombre representativo de los macronutrientes y micronutrientes presentes en una receta
      - Cantidad de Nutrientes
        - Lista de números flotantes
        - Cantidad en cada de uno de los nutrientes presente en la receta
    - Origen
      - *String*
      - Fuente URL de la que proviene la receta
    - Imágenes Ilustrativas
      - *String*
      - Referencia URI a la ubicación en la Image DB de la imagen de cómo se ve la receta servida o terminada de preparar
* Número de Recetas:
    - Número de recetas presente en la DB
* Fecha de Extracción:
    - Fecha en la que se recuperó la receta
* Versión:
    - Número/representación de la versión de la DB

### Imágenes
* Formato de Imagen:
    - Formato `.jpg`
* Atributos:
    - Identificador de Receta
      - *String*
      - ID de la receta en la SQL DB que se ilustra en la imagen
    - Contenido
      - Mapa de bits (colores)
      - Representación de la imagen en sí como bits
    - Origen
      - *String*
      - Fuente URL de la que proviene la imagen
* Número de Imágenes:
    - Número de imágenes en la DB
* Fecha de Extracción:
    - Fecha en la que se descargó la imagen
* Versión:
    - Número/representación de la versión de la DB

### Textos Médicos y Nutricionales
* Formato de Archivo:
    - `embeddings` (vector de texto embebido, debido a que estos documentos están en una base de datos vectorial)
* Atributos:
    - Titulo del Texto
      - *String*
      - Título, nombre o siglas que representan el documento o texto
    - Contenido
      - *String*
      - Contenido en texto plano (`.txt` o `.pdf`) o estructurado (`.md`) sobre la información del documento o texto
      - Este atributo solo está presente durante la Extracción, luego se va a embeber en un vector para el RAG
    - Fecha de Publicación
      - *String*
      - Fecha en formato *YYYY/MM/DD* en la que se publicó el texto
    - Origen
      - *String*
      - Fuente URL de la que proviene el texto
    - Autor/Origen/Institución Emisora:
      - Ente encargo de la publicación o emisión del documento en internet
* Número de Documentos:
    - Número de documentos presente en la DB
* Fecha de Extracción:
    - Fecha en la que se obtuvo el documento
* Versión:
    - Número/representación de la versión de la DB

## Almacenamiento y Organización de los Datos
De los objetos relevantes, cada uno pertenece a un tipo de database diferente, esto debido a la naturaleza de cómo se tienen que almacenar para mejorar su disposición para el sistema de IA. La mayoría de los datos y objetos extraídos no son visibles al usuario final, es decir, el usuario solo podrá ver ciertas recetas (las propuestas por la IA y modificadas por el mismo) y el registro de su ingesta de macronutrientes y micronutrientes a lo largo del tiempo.

### Almacenamiento
Los datos que son extraídos y transformados serán almacenados en tres tipos de de bases de datos, y adicionalmente una base de datos para hacer el registro de los nutrientes consumidos por los usuarios:
* SQL DB en Postgres para almacenar los datos de las recetas. Tanto en development y production se emplea la ejecución local de PostgresSQL
* Almacenamiento basado en Objetos (Object-based Storage) para almacenar las imágenes de las recetas. En development se emplea el almacenamiento local y en production S3 de AWS
* Vector DB para almacenar los embeddings de los documentos y textos extraídos. Tanto en development y production se emplea la ejecución local de Qdrant (se considera usar S3 de AWS para almacenar los embeddings en production)
* SQL DB en Postgres para almacenar los datos generados por los usuarios (preferencia de recetas, nutrientes consumidos) incluyendo la información de su perfile (nombre de usuario, contraseña, nacionalidad, datos como peso, estatura, edad y genero)

### Organización
Para la interfaz del usuario se planea hacer dos paneles, uno con el pueda chatear con la IA para la planificación de sus recetas y otro para visualizar los nutrientes que ha consumido, y que estos paneles se encuentren en tabs en un menú lateral ocultable:
* Para la interacción con la IA y la captura de los primeros datos fisiológicos-médicos de un paciente, se tiene contemplado el crear un chat estilo Gemini, ChatGPT o DeepSeek para permitir una transición suave para el uso de nuestra herramienta 
* Para presentarle al usuario las propuestas de recetas, se tiene planeado hacer un mini calendario donde cada entrada sea una receta correspondiente a un día y hora. Con esta disposición podrá ver qué comidas prefiere comer o no, para así mismo solicitar a la IA por medio de un chat su respectiva modificación o cambio. Además, al momento de que el usuario le hace click a una de las recetas pueda ver su información nutricional, ingredientes y una imagen ilustrativa de la receta
* Para que el usuario pueda visualizar el registro de nutrientes que ha consumido a lo largo del tiempo y tener una visión general de su salud nutricional, se plantea hacer un dashboard interactivo con plots intuitivos

## Pipelines
* [*E*] De la página [allrecipes](www.allrecipes.com), extraje las recetas de las diferentes cocinas con las que contaba
* [*T*] De cada receta, solo obtuve y formatee los valores y atributos de interés para el proyecto (ingredientes, pasos de elaboración, información nutricional)
* [*L*] De los atributos extraídos y transformados de cada receta, son vaciados hacia una base de datos SQL con fields basados en texto
* Para la construcción de la pipeline (principalmente la parte de la extraction y parte de la transformation) usé [Crawl4ai](https://docs.crawl4ai.com/), una herramienta que facilita el web scrapping usando una sintaxis más ligera y un procedimiento más corto para formatear el output 