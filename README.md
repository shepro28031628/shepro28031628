# 👋 Hola, soy **Edinsson Gonzalez**

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,35:161b22,70:00f2fe,100:4facfe&height=150&section=header&text=Edinsson%20Gonzalez&fontSize=42&fontColor=ffffff&animation=twinkling&fontAlignY=36"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=19&duration=2500&pause=800&color=00F2FE&center=true&vCenter=true&width=750&lines=Data+Analytics+%7C+Big+Data+%7C+Automation;Data+Engineering+%7C+ETL+%2F+ELT+Pipelines;Construyendo+soluciones+escalables+impulsadas+por+datos;Transformando+datos+complejos+en+decisiones+estrat%C3%A9gicas" alt="Typing SVG" />
</p>

<!-- Navegación Rápida -->
<p align="center">
  <a href="#-terminal--resumen-ejecutivo"><b>💻 Resumen</b></a> •
  <a href="#-sobre-m%C3%AD--enfoque-principal"><b>📊 Sobre Mí</b></a> •
  <a href="#-stack-tecnol%C3%B3gico--herramientas"><b>⚙️ Stack</b></a> •
  <a href="#-arquitectura--flujo-de-trabajo-pipeline-de-datos"><b>🚀 Arquitectura</b></a> •
  <a href="#-vitrina-de-proyectos-destacados-project-showcase"><b>📂 Proyectos</b></a> •
  <a href="#-conectemos--colaboraciones"><b>🤝 Contacto</b></a>
</p>

<p align="center">
  <a href="https://github.com/shepro28031628">
    <img src="https://komarev.com/ghpvc/?username=shepro28031628&label=Profile%20Views&color=00f2fe&style=for-the-badge" alt="Profile Views"/>
  </a>
  <a href="https://github.com/shepro28031628?tab=followers">
    <img src="https://img.shields.io/github/followers/shepro28031628?label=Followers&style=for-the-badge&color=4facfe&logo=github" alt="Followers"/>
  </a>
  <img src="https://img.shields.io/badge/Status-🟢%20Disponible%20para%20Proyectos-success?style=for-the-badge&color=00c6ff" alt="Status" />
</p>

<!-- Galería visual compacta a 2 columnas con GIFs animados -->
<table width="100%" align="center">
  <tr>
    <td width="50%" align="center" valign="top">
      <img src="./assets/data_developer_workspace.gif" width="100%" style="border-radius: 8px;" />
      <br/><sub><b>💻 Entorno & Terminal de Datos (Animado)</b></sub>
    </td>
    <td width="50%" align="center" valign="top">
      <img src="./assets/data_analytics_pipeline.gif" width="100%" style="border-radius: 8px;" />
      <br/><sub><b>🔄 Visualización de Pipelines & Data Analytics (Animado)</b></sub>
    </td>
  </tr>
</table>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 💻 Terminal & Resumen Ejecutivo

```bash
edinsson@data-terminal:~$ init_profile.sh --user="Edinsson Gonzalez"

[INFO] Cargando especialidades...
🔹 Especialidad: Data Analytics | Data Engineering | Automation | Systems Integration
🔹 Filosofía: "Transformar datos sin procesar en decisiones estratégicas automatizadas."
🔹 Estado Actual: Construyendo soluciones de datos de alto impacto & optimizando pipelines ETL.

[STATUS] Todos los sistemas operando al 100% 🚀
```

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 📊 Sobre mí & Enfoque Principal

Soy profesional especializado en **Analítica de Datos, Big Data, Automatización de Procesos e Integración de Sistemas**.

Mi objetivo es transformar datos complejos en soluciones **automatizadas, escalables y orientadas a valor**, conectando la infraestructura tecnológica con la visión estratégica de negocio.

Actualmente fortalezco mi perfil hacia **Data Engineering, Analytics Engineering y Automatización Empresarial**.

<table width="100%" align="center">
<tr>
<td width="33%" align="center" valign="top">
  <h4>📊 Data Analytics</h4>
  <sub>Análisis exploratorio, modelos estadísticos, BI y cuadros de mando interactivos.</sub>
</td>
<td width="33%" align="center" valign="top">
  <h4>🔄 Data Engineering</h4>
  <sub>Pipelines ETL/ELT automatizados, arquitectura de datos y optimización SQL/NoSQL.</sub>
</td>
<td width="33%" align="center" valign="top">
  <h4>⚙️ Process Automation</h4>
  <sub>Automatización de flujos operativos, integración de APIs y herramientas de IA.</sub>
</td>
</tr>
</table>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## ⚡ Muestra de Código (Data Pipeline Sample)

```python
# pipeline_example.py - Proceso ETL Automatizado de Ejemplo
import pandas as pd
from datetime import datetime

class DataPipeline:
    def __init__(self, source_url: str):
        self.source = source_url
        
    def extract_and_transform(self) -> pd.DataFrame:
        """Extrae, limpia y enriquece los datos de entrada."""
        raw_data = pd.read_csv(self.source)
        clean_df = raw_data.dropna().drop_duplicates()
        clean_df['processed_at'] = datetime.utcnow()
        return clean_df

    def load_to_warehouse(self, df: pd.DataFrame, target_table: str):
        """Carga los datos procesados a la base de datos empresarial."""
        print(f"🚀 [ETL] Cargando {len(df)} registros limpios en {target_table}...")

if __name__ == "__main__":
    pipeline = DataPipeline(source_url="s3://data-warehouse/raw/daily_sales.csv")
    data = pipeline.extract_and_transform()
    pipeline.load_to_warehouse(data, target_table="analytics.fact_sales")
```

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 🧠 Demostración & Multimedia

<table width="100%" align="center">
  <tr>
    <td width="50%" align="center" valign="top">
      <h4>🧠 Inteligencia Artificial & Automatización</h4>
      <video src="./inteligencia%20artificial.mp4" width="100%" controls autoplay loop muted style="border-radius: 8px;"></video>
    </td>
    <td width="50%" align="center" valign="top">
      <h4>🎨 Diseño UI/UX & Experiencia de Usuario</h4>
      <video src="./Dise%C3%B1o%20de%20interfaz%20de%20usuario%20y%20experiencia%20de%20usuario.mp4" width="100%" controls autoplay loop muted style="border-radius: 8px;"></video>
    </td>
  </tr>
</table>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 🏆 Hitos & Especializaciones

<p align="center">
  <img src="https://img.shields.io/badge/Data%20Engineering-Specialist-00f2fe?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Big%20Data-Analytics-4facfe?style=for-the-badge&logo=apache&logoColor=white" />
  <img src="https://img.shields.io/badge/Automation-Workflows-00c6ff?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-Active%20Developer-181717?style=for-the-badge&logo=github&logoColor=white" />
</p>

<blockquote align="center">
  💡 <i>"Sin datos, solo eres otra persona con una opinión."</i> — <b>W. Edwards Deming</b>
</blockquote>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## ⚙️ Stack Tecnológico & Herramientas

<div align="center">
  <h3>💻 Lenguajes & Scripting</h3>
  <img src="https://skillicons.dev/icons?i=python,java,js,html,css,bash" />

  <br/><br/>

  <h3>📊 Data Analytics, BI & Engineering</h3>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" />
    <img src="https://img.shields.io/badge/Alteryx-0078C8?style=for-the-badge&logo=alteryx&logoColor=white" />
    <img src="https://img.shields.io/badge/KNIME-F5C400?style=for-the-badge&logo=knime&logoColor=black" />
    <img src="https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" />
  </p>

  <h3>🗄️ Bases de Datos & Almacenamiento</h3>
  <img src="https://skillicons.dev/icons?i=mysql,postgres,mongodb" />
  <img src="https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white"/>

  <br/><br/>

  <h3>☁️ Cloud, DevOps & Automatización</h3>
  <img src="https://skillicons.dev/icons?i=azure,docker,jenkins,git,github,githubactions,linux,vscode" />
</div>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 🛡️ Metodologías & Prácticas de Ingeniería

<table width="100%" align="center">
<tr>
<td width="25%" align="center" valign="top">
  <b>🔄 DataOps & CI/CD</b>
  <br/><sub>Automatización de pipelines y pruebas continuas.</sub>
</td>
<td width="25%" align="center" valign="top">
  <b>📐 Clean Code</b>
  <br/><sub>Código modular, mantenible y documentado.</sub>
</td>
<td width="25%" align="center" valign="top">
  <b>🔒 Data Governance</b>
  <br/><sub>Seguridad, privacidad y calidad de datos.</sub>
</td>
<td width="25%" align="center" valign="top">
  <b>🚀 Agile / Scrum</b>
  <br/><sub>Desarrollo iterativo centrado en valor rápido.</sub>
</td>
</tr>
</table>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 🚀 Arquitectura & Flujo de Trabajo (Pipeline de Datos)

```mermaid
flowchart LR
    classDef source fill:#0d1117,stroke:#00f2fe,stroke-width:2px,color:#fff;
    classDef etl fill:#0d1117,stroke:#4facfe,stroke-width:2px,color:#fff;
    classDef process fill:#0d1117,stroke:#00c6ff,stroke-width:2px,color:#fff;
    classDef analytics fill:#0d1117,stroke:#0072ff,stroke-width:2px,color:#fff;
    classDef action fill:#0d1117,stroke:#00f2fe,stroke-width:2px,color:#fff;

    A[📥 Fuentes de Datos]:::source --> B[🔄 ETL / ELT Pipelines]:::etl
    B --> C[🗄️ Procesamiento & Modelado]:::process
    C --> D[📊 Analítica & BI]:::analytics
    D --> E[💡 Decisiones Estratégicas]:::action

    B --> F[⚙️ Automatización de Procesos]:::process
    F --> G[🚀 Integración CI / CD]:::etl
    G --> H[☁️ Despliegue en la Nube]:::action
```

<p align="center">
  <b><code>Datos ➔ Procesos ➔ Automatización ➔ Información ➔ Impacto Organizacional</code></b>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## ✨ Dashboard de Métricas & Actividad GitHub

<table width="100%" align="center">
  <tr>
    <td width="50%" align="center" valign="top">
      <img width="100%" src="https://github-readme-stats.vercel.app/api?username=shepro28031628&show_icons=true&theme=tokyonight&hide_border=true&include_all_commits=true&count_private=true&border_radius=8" />
    </td>
    <td width="50%" align="center" valign="top">
      <img width="100%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=shepro28031628&layout=compact&theme=tokyonight&hide_border=true&langs_count=8&border_radius=8" />
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center" valign="top">
      <img width="100%" src="https://github-readme-streak-stats.herokuapp.com/?user=shepro28031628&theme=tokyonight&hide_border=true&border_radius=8" />
    </td>
  </tr>
</table>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=shepro28031628&theme=tokyonight&hide_border=true&area=true" width="100%" />
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 🐍 Gráfico de Contribuciones Animado (Snake Animation)

<p align="center">
  <img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake-dark.svg" alt="GitHub Contribution Snake Animation" width="100%"/>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 📂 Vitrina de Proyectos Destacados (Project Showcase)

<table width="100%" align="center">
<tr>
<td width="50%" valign="top">

### 📊 Pipelines & Data Analytics
- 🔄 **ETL Automated Engine**: Procesamiento masivo de fuentes de datos con Python y SQL.
- 📈 **BI Executive Dashboard**: Visualizaciones interactivas de métricas clave de negocio.
- 🗄️ **Modelado Multidimensional**: Diseño de esquemas en estrella y copo de nieve.

</td>
<td width="50%" valign="top">

### ⚙️ Automatización & Cloud
- 🤖 **Intelligent Workflow Automation**: Integración de APIs e IA para automatizar flujos complejos.
- 🐳 **Dockerized Services**: Microservicios de datos aislados y desplegados mediante CI/CD.
- ☁️ **Cloud Data Operations**: Integración de pipelines en entornos Azure.

</td>
</tr>
</table>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## ❓ Preguntas Frecuentes & Metodología de Trabajo

<details>
  <summary><b>🛠️ ¿Cuál es mi enfoque de trabajo principal?</b></summary>
  <br/>
  Combino las mejores prácticas de <b>Clean Architecture</b>, desarrollo guiado por datos (Data-Driven) y automatización orientada a resultados empresariales escalables.
</details>

<details>
  <summary><b>💬 ¿En qué tipo de proyectos suelo participar?</b></summary>
  <br/>
  Proyectos de arquitectura e ingeniería de datos, optimización de consultas SQL/NoSQL, construcción de dashboards ejecutivos e integración de APIs con modelos de Inteligencia Artificial.
</details>

<p align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" />
</p>

## 🤝 Conectemos & Colaboraciones

<p align="center">
  <a href="https://github.com/shepro28031628">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
  <a href="https://www.linkedin.com/in/edinsson-gonzalez">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00f2fe,50:4facfe,100:0d1117&height=100&section=footer"/>
</p>

<p align="center">
  <b>⚡ Transformando datos en soluciones. Automatizando procesos. Construyendo el futuro.</b>
</p>
