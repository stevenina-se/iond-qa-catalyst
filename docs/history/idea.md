# Idea: Deseo realizar un sistema para el equipo de QA de mi proyecto que este potenciado netamente por IA

## Contexto del proyecto (Donde se esta haciendo QA)

### Que es el proyecto?
El proyecto es denominado Ionflow, se trata de un SAS orientado a la automatizacion de procesos mediante la conexion de nodos (Muy similar a plataformas como Make.com, Zapier, n8n, etc)

### Cual es su diferencial?
Su diferencial es que busca ser extremadamente sencillo de usar, eliminando la complejidad de la configuracion de nodos, y permitiendo que cualquier persona pueda automatizar sus procesos sin necesidad de conocimientos tecnicos. Y lo principal es que sera orientado a los flujos mas utilizados en e-commerce

### Cual es el stack Tecnologico?
El proyecto actualmente se encuentra ya maduro, consta de 4 repositorios:
1. flow_binaries: este repositorio se encarga de manejar el core de los nodos y el motor de ejecucion de los mismos, asi como tambien la gestion de los flujos entre otras cosas. Esta desarrollado en GO
2. gateway-ion: este repositorio se encaerga de manejar el frontend de la aplicacion. Esta desarrollado copn el framework Vue 3 con Typescript, este repositorio gestiona las vistas y los CRUDS de la aplicacion, sin embargo no gestiona el manejo de los nodos como tal.
3. webcomponents-flow: este repositorio se encarga de encapsular los componentes de manejo de nodos, flows, drawer, formularios, entre otros componentes para los nodos utiliza la libreria vue flow, y se encarga de exponer los componentes al frontend para que pueda utilizarlos. Estos componentes son compilados y expuestos mediante un cdn. Esta desarrolado en Vue 3 con Typescript
4. gateway: este repositorio se encarga de manejar la autenticacion y gestion de usuarios, ademas de manejar aun cierta logica en la gestion de flows, es como un repo legacy que con el tiempo pensamos migrarlo, esta desarrollado en PHP 8.2

### Propoisto de ionflow
Ionflow busca automatizar los procesos repetitivos que se dan en un entorno de e-commerce, generar logica low code, conectar diferentes plataformas mediante nodos y permitir que cualquier persona pueda automatizar sus procesos sin necesidad de conocimientos tecnicos.

### Cual es el estado actual del proyecto?
Actualmente el proyecto se encuentra en una etapa ya consolidado hasta cierto punto, aun faltan algunos detalles para que el proyecto salga.

### Trabajo de QA en el proyecto de Ionflow
Actualmente el equipo de QA esta conformado por mi persona y un QA Analyst, y el proceso de testing ultimamente se ha estado volviendo muy monotono, lento y manual, haciendo que las nuevas features, fixes, historias, epicas y demas lleve mucho tiempo de testearlos por lo que QA llego un punto donde se esta convirtiendo en un cuello de botella en el desarrollo de ionflow, con la nueva era de la IA los desarrolladores sacan nuevas features a gran velocidad, y con IA las cosas se vuelven mas rapidas y dinamicas, no podemos seguir en un proceso de testing lento, manual y monotono, por lo que llego un momento de replantearnos el proceso de testing y hacer algo nuevo, y que mejor manera de hacerlo que potenciarnos con IA.  

## Objtivo
El objetivo principal de este proyecto es desarrollar una herramienta potenciada con IA que permita automatizar el proceso de testing de Ionflow, eliminando la monotonía y lentitud del proceso actual, y permitiendo que el equipo de QA se enfoque en tareas de mayor valor agregado.

EL equipo de QA debe volverse en enquipo de QA Engineers que revisa el trabajo de la IA y aprueba releases

Pienso en implementar un motor de skills IA que permita automatizar el proceso de testing de Ionflow, este motor de skills estara compuesto por una serie de skills, cada skill sera una funcion que permitira ejecutar una accion en la aplicacion, por ejmeplo poder cumplir con los siguientes flujos:

Sprint Testing:
- plan
- test
- report

Test Docs
- Prioritize
- Document

Automation (Actualmente en proceso en un tepositorio bot-test que se encuentra un nivel encima de este directorio)
- Plan
- Code
- Review

Regression
- Run
- Analize
- Decide

Ademas de que se quiere contar con una capa de conocimoiento compartido
- Bussiness flows
- API docs
- Test priorities
- Per-ticket memory

Dentro del proyecto utilizamos la herramienta de gestion de tickets Clickup esta herramienta cuenta con un mcp que permite interactuar con los tickets, este mcp se puede utilizar para obtener informacion y contexto de los tickets. (Inicialmente no realizar comentarios sin autorizacion)

## Vision General del proyecto QA
Quiero estructurar este proyecto de forma que podamos automatizar el flujo de QA SIN PERDER CALIDAD
Como talvez podriamos hacerlo?
Estruturar el contexto en tres niveles;
- Nivel 1. Project Level: "How does de project works?"; Bussiness rules, API architecture, Test priorities
- Nivel 2. Module level: "How does this feature works?", routes, db tables, shared test data
- Nivel 3. Ticket level: "What i'm testing right now?", Acceptance Criteria, Team Desicions, Evidence, Sessions memory

La regla de todo esto es "LA IA LEE EL NIVEL CORRECTO ANTES DE REALIZAR CADA TAREA"
