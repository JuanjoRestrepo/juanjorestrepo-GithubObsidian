---
title: "Desarrollo integral de solución desde ingeniería y datos"
date: 2026-04-23T06:21:34.443673Z
tags: [ai_memory, claude_context]
summary: "**Conversation Overview**  The person initiated a technical project engagement focused on precision agriculture UAV operations in Colombia, sharing a document (PDF) that outlined a data and software engineering problem. The document described a "cold start problem" in UAV agricultural missions: each flight begins without access to historical mission data because proprietary platforms (DJI SmartFarm, PIX4D, DJI Terra) operate as closed silos with no integration toward a centralized data ecosystem. The absence of historical data lineage combining UAV telemetry, IDEAM climate data, and soil/edaphology information makes it mathematically impossible to train supervised ML models for NDVI anomaly detection or flight parameter optimization.  The person asked Claude to read the document and begin architecting a solution from scratch, applying full software engineering methodology including Scrum, Design Thinking, data engineering, MLOps, and DevOps practices. Claude synthesized the problem into three dimensions (core problem, technical root cause, scientific consequence), proposed a hybrid methodology (Design Thinking for weeks 1–2 followed by 2-week Scrum sprints), designed a five-layer data architecture (Sources → Ingestion → Data Lake medallion → ML Platform → Serving), and created an interactive sprint roadmap covering 8 sprints across 16 weeks. The architecture features Apache Kafka and Airflow for ingestion, S3/GCS with Delta Lake/Iceberg for storage using Raw/Silver/Gold zones, Feast Feature Store and MLflow for ML, and FastAPI plus React/Deck.gl for serving. The conversation used domain terminology including Data Lineage, cold start problem, medallion architecture, feature engineering, NDVI, IDEAM, edafología, and MLOps. Both outputs were delivered as interactive SVG and HTML widgets with clickable components linking to deeper exploration prompts."
---

### Human
Lee el contexto y el pdf que te di, para que empecemos a abarcar esta problematica, empezando desde cero, desde las ideas, diagramas, aplicando toda la ingenieria y metodologias de desarrollo, scrum, design thinking o lo que mejor se adapte a este contexto. Recuerda emplear tus skills para este contexto de data, software development, devops y relacionados

### Assistant
 The user wants me to read the PDF file about drones in Colombia and start working on addressing the problem from scratch, applying engineering methodologies. Let me first read the PDF and relevant skills.
```
This block is not supported on your current device yet.
```

Now let me read the PDF file.
```
This block is not supported on your current device yet.
```

The PDF may be a non-standard or corrupted PDF. Let me try with pypdf or rasterize it.
```
This block is not supported on your current device yet.
```

The file seems to be a ZIP file (PK header). Let me check.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now I have a complete picture of the problem. Let me view the page images as well, but actually the text is sufficient to understand the context. Let me now analyze this deeply and create a comprehensive response.

The problem is:
1. **Domain**: AgriTech + UAV/Drones for precision agriculture in Colombia
2. **Core Problem**: Absence of a centralized, standardized data ecosystem (Data Lineage) that consolidates:
   - Agronomic history of crops
   - UAV operational telemetry
   - Exogenous variables (climate - IDEAM data)
   - Soil science (edaphology)
3. **Consequence**: "Cold start problem" - each mission starts from zero knowledge
4. **Goal**: Transition from reactive to predictive agriculture using ML

Key issues:
- Proprietary software silos (DJI SmartFarm, PIX4D, DJI Terra) - closed ecosystems
- No retrospective digitalization pipelines
- No metadata standards for missions
- No unified data repository correlating terrain history with UAV configurations

Research questions:
1. Architecture: How does the absence of historical data lineage impact operational efficiency, and what information architecture is needed?
2. Analytical: How does a unified data repository that correlates terrain history with past UAV mission configurations optimize decision-making?

Problem tree:
Root Causes:
- Proprietary Software Silos
- Retrospective Digitalization Gap
- Lack of Metadata Standards

Direct Effects:
- Inability to apply Predictive Modeling
- Hardware underutilization
- False positives in spatial analysis (NDVI)

Now I need to create a comprehensive response that:
1. Validates understanding of the problem
2. Proposes a project structure from scratch
3. Applies appropriate methodologies (Design Thinking, Scrum, data engineering)
4. Creates architecture diagrams
5. Defines the roadmap

Let me create a rich visual output with a full project overview including:
- Problem summary
- Proposed architecture
- Development methodology
- Technology stack
- Roadmap/Sprints

I'll use the visualizer to create diagrams and a comprehensive plan. Let me structure my response:

1. Problem validation summary
2. Methodology selection (Design Thinking for discovery + Scrum for execution)
3. System architecture diagram
4. Data pipeline diagram
5. Technology stack
6. Sprint roadmap
7. Next steps

Let me read the frontend design skill too since I'll create visualizations.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now I have a full understanding of the document and the design system. Let me create a comprehensive response. The problem is:

1. **Context**: Precision agriculture in Colombia using UAVs (DJI SmartFarm, PIX4D, DJI Terra)
2. **Core Problem**: No centralized data ecosystem → "cold start problem" every mission
3. **Root Causes**: 
   - Proprietary software silos
   - No retrospective digitalization pipelines (IDEAM climate data)
   - No metadata standards
4. **Effects**:
   - Can't train ML models (no features/labels)
   - Hardware underutilized (empirical config instead of optimized)
   - False positives in NDVI analysis

I'll structure this as:
1. Brief problem synthesis
2. Methodology selection diagram
3. Architecture overview diagram
4. System architecture (data pipeline)
5. Technology stack
6. Sprint roadmap
7. Next steps

Let me plan the diagrams:

**Diagram 1**: Methodology approach - Design Thinking + Scrum hybrid (simple flowchart)

**Diagram 2**: System Architecture - structural diagram showing layers:
- Data Sources (IDEAM, DJI/PIX4D logs, Sensors)
- Ingestion Layer
- Data Lake / Storage
- Processing / ML Layer
- Output / Dashboard

**Diagram 3**: Sprint Roadmap / Timeline

Let me create all of these. I'll start with the overall response text and then the diagrams.

For the methodology:
- **Design Thinking** for the Discovery phase (Empathize, Define, Ideate) - weeks 1-2
- **Scrum** for the Build phase (sprints of 2 weeks)
- **MLOps** for the production phase

For the architecture, I'll propose:
1. **Data Sources Layer**: DJI SmartFarm API, PIX4D logs, DJI Terra logs, IDEAM API (climate), Soil/edaphology databases, Manual farmer data
2. **Ingestion Layer**: Apache Kafka / Airflow DAGs, custom extractors for proprietary formats
3. **Data Lake**: AWS S3 / GCS - raw, processed, curated zones
4. **Processing Layer**: Apache Spark / dbt for transformations, feature engineering
5. **ML Layer**: Feature Store, Model Registry, ML models (anomaly detection, NDVI prediction, flight parameter optimization)
6. **Serving Layer**: FastAPI, dashboard (React/Streamlit)
7. **Orchestration**: Airflow / Prefect
8. **Observability**: Great Expectations, MLflow

For the tech stack:
- **Cloud**: AWS or GCP
- **Data Lake**: S3 + Delta Lake / Iceberg
- **Ingestion**: Apache Kafka, Airflow
- **Processing**: Apache Spark (PySpark), dbt
- **Feature Store**: Feast
- **ML Framework**: scikit-learn, PyTorch, MLflow
- **API**: FastAPI
- **Dashboard**: React + Plotly/Deck.gl (for geospatial)
- **CI/CD**: GitHub Actions, Docker, Kubernetes
- **Monitoring**: Prometheus, Grafana, Great Expectations

For Scrum sprints:
- Sprint 0 (2 weeks): Design Thinking, requirements, architecture finalization
- Sprint 1 (2 weeks): Data source exploration & connectors (DJI, PIX4D log parsers, IDEAM API)
- Sprint 2 (2 weeks): Data Lake setup, ingestion pipelines
- Sprint 3 (2 weeks): Data modeling, feature engineering, metadata standards
- Sprint 4 (2 weeks): First ML models (anomaly detection)
- Sprint 5 (2 weeks): API + Dashboard MVP
- Sprint 6 (2 weeks): ML optimization (flight params), testing
- Sprint 7 (2 weeks): Production deployment, monitoring

Let me create a rich response now.

Let me plan the SVG diagrams carefully:

**Diagram 1 - System Architecture (Structural)**:
- Layers from bottom to top:
  - Data Sources (left side, external)
  - Ingestion Layer
  - Data Lake (3 zones: Raw, Processed, Curated)
  - ML/Processing Layer
  - API/Dashboard Layer
  
  Width: 680px
  
  Let me think of a good layout. I'll do a horizontal layered approach:
  
  Row 1 (y=40): Title area
  Row 2 (y=80): Data Sources (external boxes on left)
  Row 3 (y=180): Ingestion Layer
  Row 4 (y=260): Data Lake (container with 3 zones)
  Row 5 (y=380): ML Layer
  Row 6 (y=460): API/Serving Layer

Actually, let me think about this differently. A structural diagram works best as a top-down flow here. Let me do:

Top: External Data Sources
↓ Arrows
Ingestion Layer (Kafka + Airflow)
↓
Data Lake (S3 - Raw → Processed → Curated zones)
↓
ML/Feature Platform
↓
API + Dashboard

Width 680, let me space things:
- Sources: 4 boxes across: DJI logs, PIX4D, IDEAM, Edaphología
  - Each ~130px wide, spaced evenly
  - y=40-84, gap between each: (680-40*2-4*130)/3 = (600-520)/3 = 80/3 ≈ 26px
  - x positions: 40, 196, 352, 508 (each 130px wide, gaps 26px)
  
- Ingestion (y=120): 1 wide box or 2 boxes
  - Kafka + Airflow: 2 boxes
  - x=100, width=200 | x=380, width=200
  - arrows from sources to ingestion: y=84→y=120
  
- Data Lake container (y=180-320): 1 big container with 3 inner boxes
  - Outer: x=40, width=600, height=140
  - Inner boxes: Raw (x=60,y=200,w=160), Processed (x=250,y=200,w=160), Curated (x=440,y=200,w=160)
  - arrows between: 220→250, 410→440
  
- ML Platform (y=360): Feature Store + Model Training + Model Registry
  - 3 boxes: x=60,y=360,w=160 | x=250,y=360,w=160 | x=440,y=360,w=160
  
- API + Dashboard (y=460): 2 boxes
  - FastAPI: x=140,y=460,w=160
  - Dashboard: x=380,y=460,w=160

Actually this is getting complex. Let me simplify and make a clean structural diagram with fewer elements but make each section clickable.

Let me plan more carefully:

ViewBox: 680 x 640

**Layer 1 - Data Sources** (y=30 to y=90)
4 source boxes across the top, each 120px wide:
- DJI TelemData: x=40, w=120
- PIX4D / Terra: x=190, w=120  
- IDEAM Climate: x=340, w=120
- Edafología: x=490, w=120

**Arrows** y=90 → y=130 (collected into funnel)

**Layer 2 - Ingestion** (y=130 to y=185) 
One wide box: x=40, w=600, h=55
"Ingestion layer · Airflow + Kafka"

**Arrow** y=185 → y=200

**Layer 3 - Data Lake** (y=200 to y=330)
Outer container: x=40, w=600, h=130, c-blue
3 inner boxes (y=225, h=80):
- Raw zone: x=60, w=160
- Processed: x=250, w=160  
- Curated: x=440, w=160
Arrows between inner boxes

**Arrow** y=330 → y=355

**Layer 4 - ML Platform** (y=355 to y=445)
Outer container: x=40, w=600, h=90, c-purple
3 inner boxes (y=380, h=55):
- Feature store: x=60, w=160
- Model training: x=250, w=160
- Model registry: x=440, w=160

**Arrow** y=445 → y=465

**Layer 5 - Serving** (y=465 to y=520)
2 boxes side by side:
- FastAPI: x=100, w=180
- Dashboard: x=400, w=180

Total height: 520 + 40 = 560

Let me check widths:
- 4 source boxes: 4*120 = 480, gaps: (680-80-480)/3 = (120)/3 = 40px between
  - x positions: 40, 200, 360, 520 — right edge: 520+120=640 ✓

Actually let me simplify the source boxes to be a bit narrower:
4 boxes * 110px = 440, plus 3 gaps of 30px = 90, total = 530, plus 2 margins of 75px = 530+150 = 680 ✓
- x=75, x=215, x=355, x=495, w=110

Let me verify: 75+110=185, gap=30, 215+110=325, gap=30, 355+110=465, gap=30, 495+110=605. Right edge 605 < 640 ✓

Now I'll create the SVG. Actually, let me create this as an interactive HTML widget with tabs or sections that the user can click. That would be more engaging.

Actually for this first pass, let me create a clean SVG architectural overview. Then I'll create an HTML interactive sprint roadmap.

Let me code this up properly.

**Diagram 1: System Architecture (SVG structural)**

```svg
<svg width="100%" viewBox="0 0 680 600" role="img">
  <title>AgroUAV Data Platform Architecture</title>
  <desc>Layered system architecture from data sources to serving layer</desc>
  <defs>
    <marker id="arrow" .../>
  </defs>
  
  <!-- Layer labels on left -->
  <!-- Source boxes (row 1) -->
  <!-- Ingestion box (row 2) -->
  <!-- Data Lake container (row 3) -->
  <!-- ML Platform container (row 4) -->
  <!-- Serving layer (row 5) -->
</svg>
```

Let me write the full SVG with precise coordinates.

Layer heights:
- y=20: layer label "Sources"
- y=40-90: source boxes (h=50)
- y=90-130: arrows (40px)
- y=130: layer label "Ingestion"
- y=150-205: ingestion box (h=55)
- y=205-235: arrows (30px)
- y=235: layer label "Data Lake"
- y=255-375: data lake container (h=120)
- y=375-405: arrows (30px)
- y=405: layer label "ML Platform"
- y=425-510: ML container (h=85)
- y=510-535: arrows (25px)
- y=535: layer label "Serving"
- y=555-595: serving boxes (h=40)
- viewBox height = 595+20 = 615

Actually I'm overcomplicating this. Let me look at this differently and make a simpler but cleaner diagram. The key insight is to have 5 horizontal layers.

Let me plan more carefully:

Row 1 - Sources (y=30 to y=80):
- 4 boxes, 110px wide each
- Positions: x=40, x=180, x=320, x=460 (gap=30px)
- Right edge: 460+110 = 570 < 640 ✓
- Center of each: 95, 235, 375, 515

Row 2 - Ingestion (y=115 to y=165):
- 2 boxes: Kafka (x=80, w=200) and Airflow (x=310, w=200)  
- Wait, "Airflow + Kafka" could be one wide box
- 1 box: x=40, w=600, h=50

Row 3 - Data Lake (y=200 to y=320):
- Container: x=40, w=600, h=120
- 3 inner boxes at y=225, h=70:
  - Raw: x=60, w=160
  - Processed: x=250, w=160
  - Curated: x=440, w=160
- Label at top: "Data Lake / Object Storage (S3)"

Row 4 - ML Platform (y=355 to y=460):
- Container: x=40, w=600, h=105  
- 3 inner boxes at y=380, h=65:
  - Feature Store: x=60, w=160
  - ML Training: x=250, w=160
  - Model Registry: x=440, w=160

Row 5 - Serving (y=490 to y=545):
- 2 boxes: FastAPI (x=130, w=180) and Dashboard (x=370, w=180)
  - Center of FastAPI: 220, Center of Dashboard: 460

ViewBox height = 545 + 30 = 575

Now let me also add the layer labels on the left side. Actually that would require negative space. Let me add labels above each section instead. But the section boxes already have titles.

Let me do the annotations differently:
- Each major section has a label at the top of its container
- Add vertical "layer" labels on the left side (x=10-30)? This could get tricky.
- Better: Put descriptive labels inside or at top of each container

Let me just code this properly now:

```svg
<svg width="100%" viewBox="0 0 680 580" role="img">
<title>AgroUAV Platform Architecture</title>
<desc>Five-layer data architecture from UAV/climate sources to dashboard serving</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<!-- LAYER 1: Data Sources -->
<!-- Source box 1: DJI -->
<g class="node c-teal" onclick="sendPrompt('Explain how DJI telemetry data is extracted')">
  <rect x="40" y="30" width="110" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="95" y="50" text-anchor="middle" dominant-baseline="central">DJI logs</text>
  <text class="ts" x="95" y="68" text-anchor="middle" dominant-baseline="central">SmartFarm·Terra</text>
</g>
<!-- Source box 2: PIX4D -->
<g class="node c-teal" onclick="sendPrompt('How is PIX4D data extracted?')">
  <rect x="180" y="30" width="110" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="235" y="50" text-anchor="middle" dominant-baseline="central">PIX4D</text>
  <text class="ts" x="235" y="68" text-anchor="middle" dominant-baseline="central">Multispectral maps</text>
</g>
<!-- Source box 3: IDEAM -->
<g class="node c-teal" onclick="sendPrompt('What IDEAM data APIs are available for Colombia?')">
  <rect x="320" y="30" width="110" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="375" y="50" text-anchor="middle" dominant-baseline="central">IDEAM</text>
  <text class="ts" x="375" y="68" text-anchor="middle" dominant-baseline="central">Climate history</text>
</g>
<!-- Source box 4: Ground truth -->
<g class="node c-teal" onclick="sendPrompt('What ground truth and soil data sources exist for Colombia?')">
  <rect x="460" y="30" width="130" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="525" y="50" text-anchor="middle" dominant-baseline="central">Terreno</text>
  <text class="ts" x="525" y="68" text-anchor="middle" dominant-baseline="central">Suelos·Edafología</text>
</g>
```

Hmm, let me check: 460+130=590 < 640 ✓

Let me simplify. 4 boxes:
- x=40, w=120: DJI
- x=185, w=120: PIX4D  
- x=330, w=120: IDEAM
- x=475, w=120: Terreno
- Right edge: 475+120=595 < 640 ✓
- Centers: 100, 245, 390, 535

Arrows from each to ingestion layer:
- Line from x=100,y=80 to x=100,y=115 (but ingestion box starts at x=40)
- Actually I should fan them to a central point or just draw 4 downward arrows

Let me fan 4 arrows down:
- From (100,80) to (340,115)? No, they go to the ingestion box broadly
- Or just 4 vertical arrows each going to their x, then ingestion box spans full width

Let me just draw 4 short vertical arrows:
- (100,80)→(100,115)
- (245,80)→(245,115)
- (390,80)→(390,115)
- (535,80)→(535,115)

The ingestion box is x=40, w=600, y=115-165

Actually y=80+5=85 for arrow start (5px gap from box edge)
y=115-5=110 for arrow end

Then ingestion box: y=120-175 (h=55)

Inner structure now:
- Row 1 Sources: y=30-80
- Arrows: y=80-120
- Row 2 Ingestion: y=120-175
- Arrow: y=175-205
- Row 3 Data Lake: y=205-330 (container), inner boxes y=230-315 (h=85)
- Arrow: y=330-360
- Row 4 ML Platform: y=360-465 (container), inner boxes y=385-450 (h=65)
- Arrow: y=465-490
- Row 5 Serving: y=490-540
- ViewBox height: 540+20=560

Let me now write the complete SVG. I'll make it clean and professional.

Actually, let me think about what the inner boxes for Row 3 and Row 4 should be:

Row 3 - Data Lake (3 zones):
- Raw Zone (c-blue-200): "Raw / Bronze" - "Logs, rasters, CSVs"
- Processed Zone (c-blue): "Processed / Silver" - "Cleaned, joined"
- Curated Zone (c-purple): "Curated / Gold" - "Features, training sets"

Row 4 - ML Platform (3 components):
- Feature Store (c-purple): "Feature store" - "Feast / Hopsworks"
- ML Training (c-purple): "ML training" - "MLflow + sklearn/torch"
- Model Registry (c-purple): "Model registry" - "MLflow artifacts"

Row 5 - Serving (2 components):
- REST API (c-coral): "FastAPI" - "Endpoints for mission config"
- Dashboard (c-coral): "Dashboard" - "React + Geospatial"

Now let me also add orchestration/monitoring as a vertical band on the right? Or skip that for simplicity.

Let me write the full SVG. I need to be very careful with coordinates.

Source boxes (h=50, y=30):
- Box1: x=40, w=120 → center x=100, edges y:30-80
- Box2: x=185, w=120 → center x=245, edges y:30-80
- Box3: x=330, w=120 → center x=390, edges y:30-80
- Box4: x=475, w=120 → center x=535, edges y:30-80

Arrows y=80 → y=115 (35px gap, 4 vertical arrows):
- (100,80)→(100,113)
- (245,80)→(245,113)
- (390,80)→(390,113)
- (535,80)→(535,113)

Ingestion box: x=40, y=115, w=600, h=55 → center: y=142.5
- Title: x=340, y=138 "Capa de ingesta"
- Subtitle: x=340, y=155 "Apache Kafka · Apache Airflow · Custom extractors"

Arrow: (340,170)→(340,200)

Data Lake container: x=40, y=200, w=600, h=130, rx=20, c-blue
- Container title: x=340, y=225 "Data lake · AWS S3 / GCS · Delta Lake"
- Inner Raw: x=60, y=238, w=160, h=78
- Inner Processed: x=250, y=238, w=160, h=78
- Inner Curated: x=440, y=238, w=160, h=78
- Arrows: (220,277)→(248,277), (410,277)→(438,277)

ML Platform container: x=40, y=345, w=600, h=120, rx=20, c-purple
- Container title: x=340, y=368 "Plataforma ML"
- Inner Feature Store: x=60, y=380, w=160, h=70
- Inner ML Training: x=250, y=380, w=160, h=70
- Inner Model Registry: x=440, y=380, w=160, h=70

Wait, outer container ends at y=345+120=465.

Arrow: x=340, y=465→y=490

Serving boxes: y=490, h=50
- FastAPI: x=120, w=170 → center x=205
- Dashboard: x=390, w=170 → center x=475

ViewBox height: 490+50+25 = 565

Let me verify that the inner boxes fit in their containers:
- Data Lake: container x=40-640, inner boxes: Raw x=60-220, Proc x=250-410, Curat x=440-600
  - Container y=200-330, inner boxes y=238-316 → 238>200+20=220? No, 238>220 ✓, 316<330-5=325 ✓
  - But the label at y=225 needs room. Let me push inner boxes to y=238.
  - Actually container title is at y=225 (text), so inner boxes at y=238 would be right below. But the container height needs to accommodate the title (y=225) + inner box height (78px) + padding = 225-200=25 top + 78 body + ~15 bottom = 118px min. Container height=130 ✓

- ML Platform: container x=40-640, inner boxes x=60-220, 250-410, 440-600 (same as above)
  - Container y=345-465, container title at y=368
  - Inner boxes y=380-450 → 380>345+20=365 ✓, 450<465-5=460 ✓

Looks good. Let me write the full SVG now.

Actually, let me reconsider the inner box heights for Row 3:
- Container: y=200, h=130 → bottom at 330
- Label text: y=225 (text center), so text top ~218, text bottom ~232
- Inner boxes: y=238, need gap of 6px above (238-232=6 ✓)
- Inner box height: 330-15(padding)-238 = 77px ≈ 77px
- Inner title text: y=255, inner subtitle: y=272

For Row 4 ML Platform:
- Container: y=345, h=120 → bottom at 465
- Label text: y=368
- Inner boxes: y=380
- Inner box height: 465-15-380 = 70px
- Inner title: y=397, subtitle: y=414

Now for the inner boxes:
Data Lake inner (w=160, h=77):
- Title at y_box+17 = 255 (relative: 17px from top)
- Subtitle at y_box+34 = 272

ML inner (w=160, h=70):
- Title at y_box+16 = 396
- Subtitle at y_box+33 = 413

For color: I want 3 different colors for the 3 zones:
- Raw: c-gray (neutral, raw data)
- Processed: c-blue (processed)
- Curated: c-teal (curated/ready)

For ML:
- Feature Store: c-purple
- ML Training: c-purple (same category)
- Model Registry: c-amber (output/artifact)

For the outer containers, I should use the same color but lighter:
- Data Lake outer: c-blue (lighter background for the container)
- ML Platform outer: c-purple

But the issue is that c-blue is also used for inner boxes. Let me use:
- Data Lake outer: c-blue (50 fill) - using the `c-blue` class on the outer
- Data Lake inner: different colors for each zone

Actually, looking at the structural diagram rules: "Nested regions need distinct ramps — c-{ramp} classes resolve to fixed fill/stroke stops, so the same class on parent and child gives identical fills."

So:
- Data Lake outer: c-blue
- Inside: Raw=c-gray, Processed=c-teal, Curated=c-amber

- ML outer: c-purple
- Inside: Feature Store=c-teal, Training=c-coral, Registry=c-amber

That makes visual sense and differentiates the zones.

Now for the arrows between inner zones (Raw→Processed→Curated):
- (220,277)→(248,277) — 2px gap between box edge and arrow
- (410,277)→(438,277)

Let me check: Raw box right edge = 60+160=220, Processed left edge = 250, gap = 30px. Arrow from 222 to 248.
Processed right edge = 250+160=410, Curated left edge = 440, gap = 30px. Arrow from 412 to 438.

Arrow y positions: center of inner boxes = 238 + 77/2 = 238+38.5 = 276.5 ≈ 277

Also for the arrows from sources: I need to be careful not to cross through boxes. The ingestion box starts at y=115, so arrows from y=80 to y=113 (2px before box edge).

Now let me think about the arrow from ingestion to data lake:
- From (340, 172) to (340, 198) — ingestion box bottom = 170, data lake top = 200, gap 30px

Arrow from data lake to ML:
- From (340, 332) to (340, 343) — data lake bottom = 330, ML top = 345, gap 15px

Arrow from ML to Serving:
- From (340, 467) to (340, 488) — ML bottom = 465, serving top = 490, gap 25px

For the serving layer, I'll do 2 boxes:
- FastAPI REST: x=120, y=490, w=170, h=50
- Dashboard: x=390, y=490, w=170, h=50

Centers: 205, 475

Now the arrow from ML platform to both serving boxes... The ML platform arrow goes to center (340) but the boxes are at 205 and 475. I could do an L-path that forks. Or just have 2 arrows: one from (205,465) down to (205,488), and one from (475,465) down to (475,488). But the ML container ends at 465. Let me draw a horizontal line at y=475 from x=205 to x=475, with downward arrows at each end. No, that would be confusing.

Better: Single arrow from (340,467) to (340,478), then horizontal line from (205,478) to (475,478), then down-arrows at each:
- (205,478)→(205,488) → box starts at 490, so arrow to 488
- (475,478)→(475,488)

Actually that's complex SVG path. Let me simplify: just put the arrow in the center and let both boxes be implicitly "downstream". The connection can be drawn as a fork:
- Vertical line: (340,467)→(340,475)
- Horizontal line: (205,475)→(475,475)
- Vertical lines: (205,475)→(205,488) and (475,475)→(475,488)

Using a single path: M340 467 L340 475 M205 475 L475 475 M205 475 L205 488 M475 475 L475 488

But I need arrows at the bottom. Let me use separate lines with marker-end.

Actually let me just do 2 separate downward arrows from two different points:
One arrow from (220,465)→(220,488) — to FastAPI
One arrow from (460,465)→(460,488) — to Dashboard

These go from ML container bottom to serving boxes without crossing anything.

But then there's nothing connecting these arrows to the ML container clearly. Let me check if 220 and 460 are within the ML container (x=40-640). Yes they are.

Actually the cleanest solution is one arrow going from center to a horizontal bar and then down to each box. Let me write this as paths:

```svg
<path fill="none" stroke="var(--t)" stroke-width="0.5" d="M340 465 L340 475 L205 475 L205 490" marker-end="url(#arrow)"/>
<path fill="none" stroke="var(--t)" stroke-width="0.5" d="M475 475 L475 490" marker-end="url(#arrow)"/>
<line x1="205" y1="475" x2="475" y2="475" stroke="var(--t)" stroke-width="0.5"/>
```

Hmm this is getting complex. Let me just draw simple arrows:

From data lake to ML: arrow from (340,330)→(340,343)
From ML to FastAPI: arrow from (205,465)→(205,488)
From ML to Dashboard: arrow from (475,465)→(475,488)

This implies both serving boxes connect to ML without explicit forks. That's fine.

Actually wait, I realize for the arrows from sources to ingestion, if I draw 4 vertical arrows, they all terminate at different x positions on the ingestion box. That's fine since the ingestion box spans the full width.

But there's another issue: the arrow at x=535 (right source box) goes straight down. The ingestion box right edge is at x=640. So x=535 is within the box. ✓

OK let me also figure out: for the source box centers:
- Box1: x=40+120/2=100
- Box2: x=185+120/2=245  
- Box3: x=330+120/2=390
- Box4: x=475+120/2=535

These are the x positions for the downward arrows.

And for subtitles, "SmartFarm·Terra" is 14 chars at 12px ≈ 98px width. The box is 120px wide, so 120-2*10=100px available. 98 ≤ 100 ✓ (barely fits, let me use ·Terra/PIX4D instead)

Let me simplify subtitles:
- DJI: "SmartFarm · Terra"
- PIX4D: "Imágenes multiespectrales"  -- too long! 25 chars at 12px ≈ 175px >> 100px
  - Use: "NDVI · RGB maps"  9+10=... actually "NDVI · RGB maps" = 15 chars ≈ 105px > 100px
  - Use: "Mapas NDVI" = 10 chars ≈ 70px ✓
- IDEAM: "Datos climáticos" = 16 chars ≈ 112px > 100px
  - Use: "Clima · histórico" -- still long
  - Use: "Clima histórico" = 15 chars ≈ 105px
  - Use: "API clima" = 9 chars ✓
- Terreno: "Suelos · Edaf." = 14 chars ≈ 98px → fits at 12px

And for the ingestion box subtitle (full width, w=600):
"Apache Kafka · Apache Airflow · Extractores custom" = OK, wide box

Let me also think about whether to add a monitoring/orchestration side label. Skip for now to keep it clean.

One more thing: let me add a simple legend or annotation. Actually, let me add clickable functionality to each node so clicking opens a relevant sendPrompt.

Now let me write the complete SVG. I'll be very systematic:

```html
<svg width="100%" viewBox="0 0 680 580" role="img">
<title>Arquitectura AgroUAV Data Platform</title>
<desc>Five-layer data architecture for precision agriculture UAV platform in Colombia</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>

<!-- LAYER 1: DATA SOURCES -->
<!-- DJI: x=40, w=120, y=30, h=50 -->
<g class="node c-teal" onclick="sendPrompt('¿Cómo se extraen los logs de telemetría de DJI SmartFarm y Terra?')">
  <rect x="40" y="30" width="120" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="100" y="49" text-anchor="middle" dominant-baseline="central">DJI logs</text>
  <text class="ts" x="100" y="67" text-anchor="middle" dominant-baseline="central">SmartFarm · Terra</text>
</g>

<!-- PIX4D: x=185, w=120 -->
<g class="node c-teal" onclick="sendPrompt('¿Cómo exportamos datos de misiones de PIX4D hacia el Data Lake?')">
  <rect x="185" y="30" width="120" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="245" y="49" text-anchor="middle" dominant-baseline="central">PIX4D</text>
  <text class="ts" x="245" y="67" text-anchor="middle" dominant-baseline="central">Mapas NDVI · RGB</text>
</g>

<!-- IDEAM: x=330, w=120 -->
<g class="node c-teal" onclick="sendPrompt('¿Qué APIs del IDEAM están disponibles para datos climáticos históricos en Colombia?')">
  <rect x="330" y="30" width="120" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="390" y="49" text-anchor="middle" dominant-baseline="central">IDEAM</text>
  <text class="ts" x="390" y="67" text-anchor="middle" dominant-baseline="central">API clima histórico</text>
</g>

<!-- Terreno: x=475, w=140 -->
<g class="node c-teal" onclick="sendPrompt('¿Qué fuentes de datos de suelos y edafología existen para Colombia?')">
  <rect x="475" y="30" width="140" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="545" y="49" text-anchor="middle" dominant-baseline="central">Terreno</text>
  <text class="ts" x="545" y="67" text-anchor="middle" dominant-baseline="central">Suelos · Edafología</text>
</g>
```

Wait, 475+140=615 < 640 ✓

But now the boxes are not evenly spaced. Let me re-plan:
- 4 boxes with total available width 640-40*2=560
- Box widths: 120, 120, 120, 140 = 500 → gaps = (560-500)/3 = 60/3 = 20px each
- x positions: 40, 180, 320, 460
- Right edge: 460+140=600 < 640 ✓
- Centers: 100, 240, 380, 530

Actually, let me make all 4 boxes the same width (130px) for symmetry:
- 4 * 130 = 520, gaps = (560-520)/3 = 40/3 ≈ 13px (not clean)
- 4 * 130 with gap = 20: total = 4*130 + 3*20 = 520+60=580 > 560 ❌
- 4 * 120 with gap = 20: total = 480+60=540, available=560 → margins: (560-540)/2=10px each
  - x positions: 50, 190, 330, 470, right edge=470+120=590 < 640 ✓
  - Centers: 110, 250, 390, 530

Or use 4 * 130 with gap = 12:
- total = 520+36=556 < 560 ✓
- x positions: 42, 184, 326, 468, right edge=468+130=598 < 640 ✓
- Centers: 107, 249, 391, 533

Let me just go with x=40, gap=30, w=120:
- x: 40, 190, 340, 490, right edge=490+120=610 < 640 ✓
- Centers: 100, 250, 400, 550

And for arrows from these to ingestion:
- 4 vertical arrows from y=80 to y=113:
  - (100,80)→(100,113)
  - (250,80)→(250,113)
  - (400,80)→(400,113)
  - (550,80)→(550,113)

Ingestion box: x=40, y=115, w=600, h=55, center=(340,142)

Arrow from Ingestion to DataLake: (340,170)→(340,198)

DataLake container: x=40, y=200, w=600, h=130
DataLake label: x=340, y=222 (th, center of top 20px)
Inner boxes: y=232, h=80
- Raw: x=60, w=166, center=(143, 272)
- Processed: x=256, w=166, center=(339, 272)
- Curated: x=452, w=166, center=(535, 272) - right edge: 452+166=618 < 640 ✓

Wait, let me check: inner boxes with container x=40, w=600:
- Container right edge: 640
- Inner boxes need to fit within x=60 to x=620 (with 20px padding)
- 3 boxes: total available = 560px, box width + gaps:
  - 3 * 166 + 2 * 20 = 498+40=538 < 560 ✓
  - x: 60, 246, 432, right edge: 432+166=598 < 620 ✓

Adjusted:
- Raw: x=60, w=166, center=143, right=226
- Processed: x=246, w=166, center=329, right=412
- Curated: x=432, w=166, center=515, right=598

Arrows between inner boxes (y at center 272):
- (228,272)→(244,272) — Raw right to Processed left (gap 20px, arrow from 228 to 244)
- (414,272)→(430,272) — Processed right to Curated left

Container height: 200+130=330

Arrow from DataLake to ML: (340,330)→(340,343)

ML Platform container: x=40, y=345, w=600, h=120
ML label: x=340, y=367
Inner boxes: y=378, h=72
- Feature Store: x=60, w=166 → center=(143,414)
- ML Training: x=246, w=166 → center=(329,414)
- Model Registry: x=432, w=166 → center=(515,414)

Container bottom: 345+120=465

Serving layer (y=490, h=50):
- FastAPI: x=100, w=180, center=190
- Dashboard: x=400, w=180, center=490

Arrows from ML to serving:
- (190,465)→(190,488)
- (490,465)→(490,488)

ViewBox height: 490+50+20=560

Now let me also add colors for inner boxes:
- Raw: c-gray
- Processed: c-blue
- Curated: c-amber

- Feature Store: c-teal
- ML Training: c-coral
- Model Registry: c-purple

- FastAPI: c-coral
- Dashboard: c-amber

And for the containers:
- DataLake outer: uses a dashed rect approach? Or c-blue?
  - Actually I should use a light container. Let me use class="c-blue" for DataLake outer
  - And class="c-purple" for ML outer

But the inner boxes of DataLake are c-gray, c-blue, c-amber. And the outer is also c-blue. That's a conflict for Processed (both outer and inner are c-blue). Let me change:
- DataLake outer: use a dashed rect (no c-* class, just box class)
- ML outer: use a dashed rect

Actually looking at the structural diagram examples, they use nested colors. Let me use:
- DataLake outer: c-teal (different from the source boxes? Actually source boxes are c-teal too... let me change source boxes to c-green)

Let me rethink the color scheme:
- Sources: c-green (organic/natural = agriculture/field data)
- Ingestion: c-gray (structural/neutral)
- DataLake outer: c-blue (information/data)
  - Raw inner: c-gray
  - Processed inner: c-teal (different from blue, same cool family)
  - Curated inner: c-amber (warm = ready to use, valuable)
- ML Platform outer: c-purple (AI/ML)
  - Feature Store inner: c-teal
  - Training inner: c-coral
  - Model Registry inner: c-amber
- Serving: c-coral

This color scheme makes semantic sense:
- Green = natural sources
- Gray = neutral infrastructure
- Blue = data storage
- Purple = intelligence/ML
- Coral = output/user-facing

Now, one issue: if the outer DataLake container is c-blue with c-blue's 50 fill, and inner Processed is also c-teal, the contrast may be good. Let me verify by checking the visual:
- c-blue 50 fill: #E6F1FB (very light blue background)
- c-teal 50 fill: #E1F5EE (very light green-ish)
- These will be distinguishable ✓

For the outer container background - actually when using c-* class on a g with a rect inside, the rect gets the 50 fill. So the DataLake container rect (600px wide, 130px tall) would have a light blue background. That could be too heavy. 

Let me instead use a custom approach for the outer containers: dashed border rects with just a slight fill, labeled at the top.

From the structural diagram example, they just use class="c-green" on the outer g and c-teal/c-amber on the inner g. The outer gets a 50-stop fill (very light) and inner gets 50-stop too but in a different ramp. This should work visually.

Let me go ahead and write the full SVG. I've been overthinking this.

For text inside boxes (2-line format):
- Title (th): y = rect_y + rect_h * 0.35
- Subtitle (ts): y = rect_y + rect_h * 0.65

For single-line, center it at rect_y + rect_h/2.

For inner boxes (h=80):
- Title y: rect_y + 27 (about 1/3 from top)
- Subtitle y: rect_y + 52 (about 2/3 from top)

Let me now write the full SVG carefully. I'll do this in one shot.

ViewBox: 680 x 565

Layer headers (on left side, y positions):
- y=55 → "Fuentes" (sources, rotated text? No, let me avoid rotated text)

Actually, let me just put a small "layer label" to the left as a vertical text or just skip it. The containers themselves have titles.

Wait, the spec says "No rotated text". Let me just not add left-side labels. The containers have their own titles.

Actually I can add a thin dashed vertical border on the left side (x=0-30) with horizontal labels... no, let me just skip layer labels entirely. The diagram is self-explanatory with container titles.

Let me write the SVG now. Final coordinate plan:

Sources (y=20-70):
- c-green boxes
- DJI: x=40, w=120, center=(100,45)
- PIX4D: x=190, w=120, center=(250,45)
- IDEAM: x=340, w=120, center=(400,45)
- Terreno: x=490, w=130, center=(555,45)
  (total: 490+130=620 < 640 ✓)

4 source arrows (y=70→y=108):
from (100,70),(250,70),(400,70),(555,70) to same x,y=110

Ingestion box (y=110, h=55):
- c-gray
- x=40, w=600
- Title: x=340, y=132 (center)
- Subtitle: x=340, y=150

Arrow y=165→y=185:
- (340,165)→(340,183)

DataLake container (y=185, h=130):
- c-blue outer
- x=40, w=600
- "Data lake · S3 / GCS · Delta Lake" at y=205 (th)
- Inner boxes at y=217, h=80:
  - Raw: x=60, w=166
  - Processed: x=246, w=166  
  - Curated: x=432, w=166
  Inner titles at y=244, subtitles at y=261
- Container bottom: 185+130=315

Inner arrows (y=257 = center of inner boxes 217+80/2=257):
- Raw right=226, Processed left=246: arrow (228,257)→(244,257)
- Processed right=412, Curated left=432: arrow (414,257)→(430,257)

Arrow y=315→y=333:
- (340,315)→(340,331)

ML Platform container (y=333, h=120):
- c-purple outer
- x=40, w=600
- "Plataforma ML" at y=352 (th)
- Inner boxes at y=363, h=72:
  - Feature Store: x=60, w=166, center=(143,399)
  - ML Training: x=246, w=166, center=(329,399)
  - Model Registry: x=432, w=166, center=(515,399)
  Inner titles at y=390, subtitles at y=407
- Container bottom: 333+120=453

Serving arrows:
- (190,453)→(190,475)
- (490,453)→(490,475) 

Actually the serving boxes need to be centered under the ML boxes. Feature Store is at center x=143, Model Registry at x=515. Let me put:
- FastAPI at x=100, w=180 → center=190 (near Feature Store)
- Dashboard at x=400, w=180 → center=490 (near Model Registry)

Serving boxes (y=477, h=50):
- FastAPI: x=100, y=477, w=180
- Dashboard: x=400, y=477, w=180

ViewBox height: 477+50+20 = 547

Let me now also add a dividing label for each section. I'll add section labels at the left margin.

Actually wait, I realize the box placements for sources don't evenly cover the container space. Let me add:
- Left margin note: Let me add "Fuentes" text at y=45, x=??

Actually x=40 is the leftmost source box. There's no room for a label to the left. Let me skip this or alternatively note the layer using a small tag/badge.

Let me just add small italic text labels:
- "01 · Fuentes" at x=42, y=20 (ts, text-anchor=start)
- "02 · Ingesta" at x=42, y=107 (ts)
- "03 · Data Lake" in the container label (already there)
- "04 · ML Platform" in the container label (already there)
- "05 · Serving" at x=42, y=473 (ts)

That works! Let me make them subtle.

Actually, these small labels might clash with the boxes below them. Let me put them at the appropriate y values:
- "01 Fuentes" at x=42, y=19 (just above the source boxes)
- "02 Ingesta" at x=42, y=109 (just above ingestion box)
- Source boxes start at y=20, so y=19 is 1px above... too tight. Let me shift source boxes to y=28.

OK let me finalize:

Layer label → section:
- y=20: "01 · Fuentes" label (ts, secondary)
- y=30 to y=76: Source boxes (h=46, title+subtitle)
- y=76→y=110: arrows (34px)
- y=112: "02 · Ingesta" label (ts, secondary)
- y=120 to y=170: Ingestion box (h=50)
- y=170→y=188: arrow
- y=190 to y=320: DataLake container (h=130)
- y=320→y=338: arrow
- y=340 to y=460: ML container (h=120)
- y=460→y=475: arrows to serving
- y=477: "05 · Serving" label
- y=488 to y=538: Serving boxes (h=50)

ViewBox height: 538+20=558

Actually, I realize I don't need "02 · Ingesta" label because the ingestion box itself already says its name. And the DataLake and ML containers have their own labels. Let me just add step numbers as small badges in the corner of each section.

I think I'm over-planning this. Let me just write the SVG now with the coordinates I have. I'll write it clean and systematic. Here goes:

Actually let me think about one more thing: the arrows from source boxes to ingestion box. They go straight down from the center of each source box. But the rightmost source box center is at x=555 (or wherever). This arrow at x=555 goes straight down to the ingestion box at y=110. The ingestion box spans x=40 to x=640, so x=555 is within it. ✓

Same for leftmost at x=100. ✓

Now, for the arrows from ML to serving boxes, the arrow from Feature Store center (x=143) would go straight down to FastAPI (center=190). These don't perfectly align. Let me route them properly:

- Arrow from ML container bottom at (190,453) to FastAPI (190,477) -- going straight down ✓
- Arrow from ML container bottom at (490,453) to Dashboard (490,477) -- going straight down ✓

But 190 and 490 are not under any specific ML inner box. That's fine, they represent the aggregate output.

OK. Writing now. Let me also think about text labels carefully to avoid overflow:

Source boxes (w=120 for DJI, PIX4D, IDEAM; w=130 for Terreno):
- "DJI logs" = 8 chars * 8px/char * (500/400 for th) ≈ 67px width, fits in 120px ✓
- "SmartFarm · Terra" = 18 chars * 7px/char (ts 12px) ≈ 126px... might overflow 120px box! 
  Let me shorten to "SmartFarm · Terra" → use "SFarm · Terra" or "SmartFarm · DJI T." 
  Actually: "SmartFarm · Terra" at 12px: 18 chars * ~6.5px = ~117px, fits in 120px with 1.5px margin each side. Tight but should be OK.

Wait, the font calibration table shows: "Authentication Service" (22 chars, 14px, 500wt) = 167px → 7.6px/char
For 12px (ts): scale factor = 12/14 * maybe 0.9 = ~0.77. So 7.6 * 0.77 = 5.85px/char at 12px regular.
"SmartFarm · Terra" = 18 chars * 5.85 = 105px < 120px ✓

"Mapas NDVI · RGB" = 17 * 5.85 = 99px < 120px ✓
"API clima hist." = 15 * 5.85 = 88px < 120px ✓
"Suelos · Edafología" = 20 * 5.85 = 117px < 130px ✓

Good. Now for ingestion box subtitle:
"Apache Kafka · Airflow · Extractores custom" = 44 chars at 12px: 44 * 5.85 = 257px < 600px ✓

DataLake container title (th, 14px):
"Data lake · S3/GCS · Delta Lake" = 31 chars * 7.6px = 236px < 600px ✓

ML container title: "Plataforma ML · Feature Store · MLflow · FastAPI" - let me break this:
"Plataforma ML · MLflow" = 22 chars * 7.6 = 167px ✓

Inner box titles (w=166):
"Feature Store" = 13 * 7.6 = 99px ✓
"ML Training" = 11 * 7.6 = 84px ✓
"Model Registry" = 14 * 7.6 = 106px ✓

Inner box subtitles (w=166):
"Feast / Hopsworks" = 18 * 5.85 = 105px < 166px ✓
"sklearn · PyTorch" = 17 * 5.85 = 99px ✓
"MLflow Artifacts" = 16 * 5.85 = 94px ✓

Raw zone subtitle (ts):
"Logs brutos · CSVs" = 18 * 5.85 = 105px ✓
"Limpieza · Joins" = 16 * 5.85 = 94px ✓
"Features · Labels" = 17 * 5.85 = 99px ✓

Serving boxes (w=180):
"REST API" = 8 * 7.6 = 61px ✓ (title, th)
"FastAPI · Endpoints" = 19 * 5.85 = 111px < 180px ✓

"Dashboard" = 9 * 7.6 = 68px ✓
"React · Geospatial" = 19 * 5.85 = 111px < 180px ✓

All good. Let me write the SVG now. Let me finalize coordinate system:

Source boxes (h=46, y=30-76):
- DJI: x=40, y=30, w=120, h=46 → cx=100, title_y=44, sub_y=60
- PIX4D: x=190, y=30, w=120, h=46 → cx=250, title_y=44, sub_y=60
- IDEAM: x=340, y=30, w=120, h=46 → cx=400, title_y=44, sub_y=60  
- Terreno: x=490, y=30, w=130, h=46 → cx=555, title_y=44, sub_y=60

Hmm, for 2-line text in h=46 box:
- Title at y = box_top + 46*0.38 = 30 + 17.5 ≈ 48
- Subtitle at y = box_top + 46*0.7 = 30 + 32.2 ≈ 62

Actually let me use dominant-baseline="central" approach:
- Title at y = box_top + h/3 (upper third center)
- Subtitle at y = box_top + 2*h/3 (lower third center)

For h=46: 
- Title y = 30 + 15 = 45
- Subtitle y = 30 + 31 = 61

Source arrows from y=76 to y=110:
Actually y=76 is the bottom of source boxes. I want 2px gap: arrow from y=78.
Ingestion box top = y=115. Arrow to y=113.

Ingestion box: x=40, y=115, w=600, h=52 → bottom=167
- Title y = 115 + 52*0.35 = 115+18 = 133
- Subtitle y = 115 + 52*0.68 = 115+35 = 150

Arrow from (340, 169) to (340, 185):

DataLake container: x=40, y=187, w=600, h=133 → bottom=320
- Container label: y=207 (th, 15px below top of container)
- "03" label: y=207
- Inner boxes: x=60/246/432, y=218, w=166, h=80 → bottom of inner=298
  - title_y = 218+28 = 246
  - sub_y = 218+52 = 270

Arrows inside DataLake:
- Raw→Processed: x=(226+2,244-2)=228→244, y=218+40=258
- Proc→Curated: x=(412+2,430-2)=414→430, y=258

Arrow from DataLake bottom (340,322) to (340,338):

ML Platform container: x=40, y=340, w=600, h=120 → bottom=460
- Container label: y=360 (th)
- Inner boxes: y=372, w=166, h=72 → bottom=444
  - title_y = 372+24 = 396
  - sub_y = 372+46 = 418

Arrows from ML bottom to serving:
- (190, 462) → (190, 478)
- (490, 462) → (490, 478)

Serving boxes: y=480, h=50 → bottom=530
- FastAPI: x=100, w=180 → cx=190 → title_y=497, sub_y=513
- Dashboard: x=400, w=180 → cx=490 → title_y=497, sub_y=513

ViewBox height: 530+25=555

Now let me check that inner ML boxes have room:
ML inner boxes: x=60, y=372, w=166, h=72 → right=226 < 620 ✓
x=246, y=372, w=166 → right=412 ✓
x=432, y=372, w=166 → right=598 < 620 ✓

ML container bottom: 340+120=460. Inner boxes bottom: 372+72=444. Padding below: 460-444=16 ✓

Let me also verify DataLake inner:
x=60, y=218, w=166, h=80 → right=226
x=246 → right=412
x=432 → right=598
Container bottom: 187+133=320. Inner bottom: 218+80=298. Padding below: 320-298=22 ✓
Inner title at y=246, subtitle at y=270. Both within inner box (218 to 298) ✓

DataLake inner box arrow y positions: center of boxes = 218+40=258. Arrows at (228,258)→(244,258) and (414,258)→(430,258). These don't cross any other elements ✓.

Also: the section label arrows from source boxes:
Source bottom=76. Arrows from 76+2=78 to 115-2=113. Arrow length=35px. These go from x=100,250,400,555 down 35px. None cross any elements ✓.

Do the arrows from ML to serving cross the serving boxes?
Arrow from (190,462) to (190,480). Serving FastAPI box: x=100, y=480. Arrow goes to y=478, box starts at y=480. Gap: 2px. ✓

Now let me also add `fill="none"` to all connectors/arrows.

Alright, I think I have enough to write this. Let me now write the final SVG.

One last thing: for the raw/processed/curated zones, I want arrows between them inside the DataLake container. The arrows need fill="none".

Line from Raw→Processed: (228,258)→(244,258), marker-end="url(#arrow)"
Line from Proc→Curated: (414,258)→(430,258), marker-end="url(#arrow)"

These are inside the DataLake container (x=40-640, y=187-320). The arrows y=258 is within container (187-320 ✓). The arrows x range: 228-244 is between Raw right (226) and Processed left (246). So the arrows are in the gap between boxes ✓.

One more: I need to add the orchestration and monitoring layer. Let me add it as a side box:

Actually, let me skip the orchestration side box to keep the diagram clean. I'll mention it in text.

Now, for the section number labels above each section, I'll add them as small ts-class text:

"Fuentes de datos" at x=42, y=20 (above source boxes at y=30)
"Ingesta" at x=42, y=105 (above ingestion box at y=115, 10px above)
"Observabilidad" and "Orquestación" could be side labels but let me skip.

Actually since the DataLake and ML containers already have titles, and there's no room for layer labels without rotation, let me just put step numbers as small badges.

Let me add small circle badges with step numbers:
- "1" badge at x=32, y=55 (next to sources)
- "2" badge at x=32, y=141 (next to ingestion)
- "3" badge at x=32, y=253 (next to data lake)
- "4" badge at x=32, y=410 (next to ML)
- "5" badge at x=32, y=505 (next to serving)

These circles at x=32 would be at x=32-10=22 to x=32+10=42. Ingestion box starts at x=40. So badges sit just inside or overlapping the left edge. Let me move them to x=22, so right edge=32, just to the left of the boxes. But viewBox starts at x=0, so there's space.

Actually these badges might clutter. Let me skip them and just go with clean unlabeled sections.

Final decision: No step badges. The diagram is self-explanatory.

Let me now write the complete SVG code. I'll be careful and systematic.

```svg
<svg width="100%" viewBox="0 0 680 560" role="img">
<title>AgroUAV Data Platform — arquitectura de capas</title>
<desc>Arquitectura de 5 capas: fuentes de datos UAV y clima, ingesta, Data Lake con zonas Raw/Procesada/Curada, Plataforma ML y capa de serving.</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<!-- ── LAYER 1: FUENTES ── -->
<g class="node c-green" onclick="sendPrompt('¿Cómo extraemos los logs de telemetría de DJI SmartFarm y DJI Terra?')">
  <rect x="40" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
  <text class="th" x="100" y="45" text-anchor="middle" dominant-baseline="central">DJI logs</text>
  <text class="ts" x="100" y="62" text-anchor="middle" dominant-baseline="central">SmartFarm · Terra</text>
</g>

<g class="node c-green" onclick="sendPrompt('¿Cómo exportamos datos de misiones PIX4D al Data Lake?')">
  <rect x="190" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
  <text class="th" x="250" y="45" text-anchor="middle" dominant-baseline="central">PIX4D</text>
  <text class="ts" x="250" y="62" text-anchor="middle" dominant-baseline="central">Mapas NDVI · RGB</text>
</g>

<g class="node c-green" onclick="sendPrompt('¿Qué APIs del IDEAM existen para datos climáticos históricos en Colombia?')">
  <rect x="340" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
  <text class="th" x="400" y="45" text-anchor="middle" dominant-baseline="central">IDEAM</text>
  <text class="ts" x="400" y="62" text-anchor="middle" dominant-baseline="central">API clima histórico</text>
</g>

<g class="node c-green" onclick="sendPrompt('¿Qué fuentes de datos de suelos y edafología existen para Colombia?')">
  <rect x="490" y="30" width="130" height="46" rx="8" stroke-width="0.5"/>
  <text class="th" x="555" y="45" text-anchor="middle" dominant-baseline="central">Terreno</text>
  <text class="ts" x="555" y="62" text-anchor="middle" dominant-baseline="central">Suelos · Edafología</text>
</g>

<!-- Arrows: sources → ingestion -->
<line x1="100" y1="78" x2="100" y2="113" class="arr" marker-end="url(#arrow)" fill="none"/>
<line x1="250" y1="78" x2="250" y2="113" class="arr" marker-end="url(#arrow)" fill="none"/>
<line x1="400" y1="78" x2="400" y2="113" class="arr" marker-end="url(#arrow)" fill="none"/>
<line x1="555" y1="78" x2="555" y2="113" class="arr" marker-end="url(#arrow)" fill="none"/>

<!-- ── LAYER 2: INGESTA ── -->
<g class="node c-gray" onclick="sendPrompt('¿Cuál es la arquitectura del pipeline de ingesta con Kafka y Airflow para drones agrícolas?')">
  <rect x="40" y="115" width="600" height="52" rx="8" stroke-width="0.5"/>
  <text class="th" x="340" y="133" text-anchor="middle" dominant-baseline="central">Capa de ingesta</text>
  <text class="ts" x="340" y="151" text-anchor="middle" dominant-baseline="central">Apache Kafka · Apache Airflow · Extractores custom (DJI SDK, PIX4D API)</text>
</g>

<!-- Arrow: ingestion → data lake -->
<line x1="340" y1="169" x2="340" y2="185" class="arr" marker-end="url(#arrow)" fill="none"/>

<!-- ── LAYER 3: DATA LAKE ── -->
<g class="c-blue">
  <rect x="40" y="187" width="600" height="133" rx="12" stroke-width="0.5"/>
  <text class="th" x="340" y="207" text-anchor="middle" dominant-baseline="central">Data lake · S3 / GCS · Delta Lake / Iceberg</text>
</g>

<!-- Raw zone -->
<g class="node c-gray" onclick="sendPrompt('¿Qué datos se almacenan en la zona Raw del Data Lake para drones agrícolas?')">
  <rect x="60" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
  <text class="th" x="143" y="246" text-anchor="middle" dominant-baseline="central">Raw · Bronze</text>
  <text class="ts" x="143" y="270" text-anchor="middle" dominant-baseline="central">Logs brutos · Rasters · CSVs</text>
</g>

<!-- Processed zone -->
<g class="node c-teal" onclick="sendPrompt('¿Cómo se transforma la zona Processed/Silver del Data Lake con dbt y Spark?')">
  <rect x="246" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
  <text class="th" x="329" y="246" text-anchor="middle" dominant-baseline="central">Processed · Silver</text>
  <text class="ts" x="329" y="270" text-anchor="middle" dominant-baseline="central">Limpieza · Joins · Metadatos</text>
</g>

<!-- Curated zone -->
<g class="node c-amber" onclick="sendPrompt('¿Qué forma tienen los datos de la zona Curated/Gold y cómo se usan en los modelos ML?')">
  <rect x="432" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
  <text class="th" x="515" y="246" text-anchor="middle" dominant-baseline="central">Curated · Gold</text>
  <text class="ts" x="515" y="270" text-anchor="middle" dominant-baseline="central">Features · Labels · Series temporales</text>
</g>

<!-- Arrows inside Data Lake -->
<line x1="228" y1="258" x2="244" y2="258" class="arr" marker-end="url(#arrow)" fill="none"/>
<line x1="414" y1="258" x2="430" y2="258" class="arr" marker-end="url(#arrow)" fill="none"/>

<!-- Arrow: data lake → ML -->
<line x1="340" y1="322" x2="340" y2="338" class="arr" marker-end="url(#arrow)" fill="none"/>

<!-- ── LAYER 4: ML PLATFORM ── -->
<g class="c-purple">
  <rect x="40" y="340" width="600" height="120" rx="12" stroke-width="0.5"/>
  <text class="th" x="340" y="360" text-anchor="middle" dominant-baseline="central">Plataforma ML · MLflow · Feast</text>
</g>

<!-- Feature Store -->
<g class="node c-teal" onclick="sendPrompt('¿Cómo implementamos un Feature Store con Feast para series temporales de UAVs agrícolas?')">
  <rect x="60" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
  <text class="th" x="143" y="396" text-anchor="middle" dominant-baseline="central">Feature store</text>
  <text class="ts" x="143" y="418" text-anchor="middle" dominant-baseline="central">Feast · time-series features</text>
</g>

<!-- ML Training -->
<g class="node c-coral" onclick="sendPrompt('¿Qué modelos de ML se entrenan para predicción de anomalías NDVI y optimización de vuelo?')">
  <rect x="246" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
  <text class="th" x="329" y="396" text-anchor="middle" dominant-baseline="central">ML training</text>
  <text class="ts" x="329" y="418" text-anchor="middle" dominant-baseline="central">sklearn · PyTorch · Anomalías</text>
</g>

<!-- Model Registry -->
<g class="node c-amber" onclick="sendPrompt('¿Cómo gestionamos el ciclo de vida de modelos ML con MLflow para este sistema?')">
  <rect x="432" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
  <text class="th" x="515" y="396" text-anchor="middle" dominant-baseline="central">Model registry</text>
  <text class="ts" x="515" y="418" text-anchor="middle" dominant-baseline="central">MLflow · Versionado · Deploy</text>
</g>

<!-- Arrows: ML → Serving -->
<line x1="190" y1="462" x2="190" y2="478" class="arr" marker-end="url(#arrow)" fill="none"/>
<line x1="490" y1="462" x2="490" y2="478" class="arr" marker-end="url(#arrow)" fill="none"/>

<!-- ── LAYER 5: SERVING ── -->
<g class="node c-coral" onclick="sendPrompt('¿Cómo diseñamos la API REST con FastAPI para servir configuraciones óptimas de misiones UAV?')">
  <rect x="100" y="480" width="180" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="190" y="499" text-anchor="middle" dominant-baseline="central">REST API</text>
  <text class="ts" x="190" y="517" text-anchor="middle" dominant-baseline="central">FastAPI · Endpoints misiones</text>
</g>

<g class="node c-amber" onclick="sendPrompt('¿Qué features de visualización geoespacial necesita el dashboard para operadores de drones?')">
  <rect x="400" y="480" width="180" height="50" rx="8" stroke-width="0.5"/>
  <text class="th" x="490" y="499" text-anchor="middle" dominant-baseline="central">Dashboard</text>
  <text class="ts" x="490" y="517" text-anchor="middle" dominant-baseline="central">React · Deck.gl · Geospatial</text>
</g>

</svg>
```

Wait, I have some issues:
1. "Logs brutos · Rasters · CSVs" - let me check: 26 chars * 5.85 = 152px < 166px ✓
2. "Limpieza · Joins · Metadatos" - 29 chars * 5.85 = 170px > 166px ❌ → shorten to "Limpieza · Joins · Meta" or "Limpieza · Joins"
3. "Features · Labels · Series temporales" - 37 chars * 5.85 = 216px > 166px ❌ → shorten to "Features · Labels"
4. "Feast · time-series features" - 28 chars * 5.85 = 164px ≈ 166px (very tight) → "Feast · time-series feat." = 25 chars * 5.85 = 146px ✓
5. "sklearn · PyTorch · Anomalías" - 30 chars * 5.85 = 175px > 166px ❌ → "sklearn · PyTorch"
6. "MLflow · Versionado · Deploy" - 28 chars * 5.85 = 164px ≈ 166px (tight) → "MLflow · versioning"
7. "Apache Kafka · Apache Airflow · Extractores custom (DJI SDK, PIX4D API)" - very long but box is 600px wide, so 600/5.85 ≈ 102 chars max. 72 chars ✓

Also check "S3 / GCS · Delta Lake / Iceberg": the title box is 600px wide, title text is about 32 chars * 7.6 = 243px ✓

Let me also check the Curated subtitle "Features · Labels" - 18 chars * 5.85 = 105px ✓

And for the ML subtitles:
- "Feast · time-series" - 19 chars * 5.85 = 111px ✓
- "sklearn · PyTorch" - 17 chars * 5.85 = 99px ✓  
- "MLflow · versioning" - 19 chars * 5.85 = 111px ✓

Dashboard subtitle: "React · Deck.gl · Geo" - 22 chars * 5.85 = 129px < 180px ✓
FastAPI subtitle: "FastAPI · Endpoints" - 19 chars * 5.85 = 111px < 180px ✓

Now let me also verify the ingestion subtitle:
"Apache Kafka · Airflow · Extractores custom" - 44 chars * 5.85 = 257px < 600px ✓

One more: for `class="arr"`, this already has stroke properties. Let me check if I still need `fill="none"`. Actually, `line` elements default to `fill="none"` since SVG `fill` on a line has no visible effect. But for `path` elements used as connectors, I'd need `fill="none"`. For `line` elements, it's not needed. Let me keep it clean and remove the `fill="none"` from lines.

Actually looking at the spec: "**Connector paths need `fill="none"`.** SVG defaults to `fill: black`". This applies to `<path>` elements, not `<line>` elements. Lines are fine without it.

But the `class="arr"` style should already set the stroke. Let me check what arr does: from the spec, "class='arr' = arrow line (1.5px, open chevron head)". So `arr` class has `fill="none"` and stroke settings built in.

I'll remove the explicit `fill="none"` from lines since they don't need it.

Now let me also double check the arrow endpoints vs box edges:
- Source bottom edge: y=76 (30+46=76)
- Arrow start: y=78 (2px gap below source box) ✓
- Arrow end: y=113 (2px above ingestion box top at y=115) ✓

- Ingestion bottom: y=167 (115+52=167)
- Arrow start: y=169 ✓
- DataLake top: y=187
- Arrow end: y=185 (2px gap) ✓

- DataLake bottom: y=320 (187+133=320)
- Arrow start: y=322 ✓
- ML top: y=340
- Arrow end: y=338 ✓

- ML bottom: y=460 (340+120=460)
- Arrow starts: y=462 ✓
- Serving top: y=480
- Arrow ends: y=478 ✓

ViewBox height: serving bottom = 480+50=530, plus 20px padding = 550.
Let me set viewBox height to 555.

One issue: the inner arrows inside DataLake need to not overlap with box edges. Let me check:
- Raw box right edge: 60+166=226. Arrow from x=228. Gap: 2px ✓
- Processed box left edge: 246. Arrow to x=244. Gap: 2px ✓
- Processed box right edge: 246+166=412. Arrow from x=414. Gap: 2px ✓
- Curated box left edge: 432. Arrow to x=430. Gap: 2px ✓

These arrows are in the 20px gaps between boxes (gaps: 226-246=20px, 412-432=20px). Arrow lengths: 16px each ✓.

Now, one more concern: the text in the outer containers (DataLake, ML Platform) - these `text` elements are inside the `c-blue`/`c-purple` groups, so they'll inherit the text color from those ramp classes. Let me check: the spec says for c-{ramp}, "Sets fill+stroke on shapes, auto-adjusts child t/ts/th". So the text color inside c-blue should be auto-adjusted to the 800 stop of blue (dark blue). That's fine for readability.

But wait - I have `<g class="c-blue">` with a rect and text inside, then separately `<g class="node c-gray">` etc. for the inner boxes. The inner boxes are separate `g` elements after the outer `g` closes. So they're siblings, not children of the outer container. This is important: the inner boxes won't inherit the outer container's color ramp.

But visually, the inner boxes need to appear "inside" the outer container. Since SVG renders in document order, elements later in the document are drawn on top. So:
1. Draw outer container (c-blue) with its rect (fills the area)
2. Draw inner boxes (c-gray, c-teal, c-amber) on top

This is correct SVG rendering. The inner boxes will appear inside the outer container because they have smaller coordinates that overlap the outer container's rect area.

The issue is that the outer container's background (light blue from c-blue 50 fill) will show where the inner boxes aren't. That creates the visual effect of a container holding sub-elements. ✓

So the structure should be:
```svg
<!-- Outer container -->
<g class="c-blue">
  <rect x="40" y="187" width="600" height="133" rx="12" stroke-width="0.5"/>
  <text class="th" x="340" y="207"...>Data lake · S3 / GCS · Delta Lake</text>
</g>

<!-- Inner zones (drawn after, so they appear on top) -->
<g class="node c-gray" ...>
  <rect x="60" y="218".../>
  ...
</g>
...
```

This works! The inner rects will cover part of the outer container's background.

But there's a subtle issue: the `c-blue` class sets both fill AND stroke on child rects. The text color is also set. So the outer container text gets blue-family coloring (800 stop text on 50 fill background). ✓

And the inner boxes each have their own color classes that override the parent... wait, actually no. In SVG, CSS classes on child elements override parent if there's specificity, but the `c-*` classes use direct child selectors (`>`). Since the inner boxes are separate `<g>` elements NOT inside the outer container `<g>`, they're siblings in the SVG. The direct child selectors won't affect them at all.

Let me re-read: "c-{ramp} nesting: These classes use direct-child selectors (>). Nest a <g> inside a <g class="c-blue"> and the inner shapes become grandchildren — they lose the fill and render BLACK"

So if I close the outer `g` before the inner boxes, the inner boxes are siblings and get their own c-* class styling independently. This is exactly what I'm doing. ✓

Great, the structure is correct. Let me write the final SVG.

Actually, one more thing: the arrows `class="arr"` - these are sibling elements in the SVG. The `arr` class provides stroke styling. Let me verify these are lines (not paths), which means they don't need fill="none".

For the inner DataLake arrows between zones:
```svg
<line x1="228" y1="258" x2="244" y2="258" class="arr" marker-end="url(#arrow)"/>
```

These will inherit whatever stroke the `arr` class sets. ✓

Now let me also add a note about the Orchestration/Monitoring layer. I'll add a small separate box at the bottom or as a sidebar annotation. Actually, let me add it as a small horizontal bar below the serving layer, annotated as "Observabilidad y orquestación".

Or I can just mention it in text. Let me keep the diagram clean and mention it in text.

OK I think I'm ready to write the complete SVG. Let me also plan the second visual: an interactive sprint roadmap in HTML.

For the sprint roadmap, I'll create an HTML widget showing:
- 8 sprints across time
- Each sprint has a set of tasks
- Color-coded by phase (Discovery, Build, ML, Deploy)
- Interactive: click to see tasks in each sprint

This will be a separate tool call with text in between.

Then I'll write a comprehensive text summary covering:
1. Problem synthesis
2. Methodology (Design Thinking + Scrum)
3. Architecture explanation
4. Technology stack table
5. Sprint roadmap
6. Key decisions and risks
7. Next steps

Let me structure my full response:

---

**RESPONSE STRUCTURE:**

1. Opening paragraph: Problem synthesis in my own words (2-3 sentences)

2. Methodology selection (brief, 1 paragraph)
   - Phase 1: Design Thinking (Weeks 1-2) - Discovery & Definition
   - Phase 2: Scrum (Sprints 1-7) - Build
   - Phase 3: MLOps - Production

3. [SVG Diagram 1: System Architecture]

4. Brief explanation of the architecture layers (1 paragraph per layer)

5. [HTML Widget: Sprint Roadmap - interactive]

6. Technology Stack (brief table or prose)

7. Critical decisions & risks (brief)

8. Immediate next steps (3-4 items)

---

Let me now write this all out. The key is to be comprehensive but not verbose.

Let me also think about what specific sendPrompt() calls make sense for the roadmap widget:
- Click on Sprint → "Detalla las tareas del Sprint X con criterios de aceptación y definición of done"

For the architecture diagram clickable nodes, I already planned the sendPrompt messages.

Now, for the sprint roadmap HTML widget, let me plan:

8 sprints * 2 weeks = 16 weeks total

Sprint 0 (Semanas 1-2): Design Thinking Sprint
- Tasks: Domain research, stakeholder interviews, problem tree refinement, tech stack finalization, architecture documentation
- Phase: Discovery

Sprint 1 (Semanas 3-4): Data Source Exploration
- Tasks: DJI SDK research & log extraction POC, PIX4D export format analysis, IDEAM API connector, data schema design
- Phase: Data Engineering

Sprint 2 (Semanas 5-6): Data Infrastructure
- Tasks: Data Lake setup (S3/GCS), Delta Lake configuration, Airflow setup, Kafka setup, CI/CD pipeline (GitHub Actions)
- Phase: Data Engineering

Sprint 3 (Semanas 7-8): Pipeline & Data Modeling
- Tasks: Raw ingestion DAGs, data quality (Great Expectations), dbt models (Silver layer), metadata standards
- Phase: Data Engineering

Sprint 4 (Semanas 9-10): Feature Engineering
- Tasks: Curated/Gold layer, Feature Store (Feast), time-series feature extraction, NDVI baseline features, climate feature engineering
- Phase: ML

Sprint 5 (Semanas 11-12): First ML Models
- Tasks: Anomaly detection model (NDVI), flight parameter optimization baseline, MLflow integration, model registry
- Phase: ML

Sprint 6 (Semanas 13-14): API + Dashboard MVP
- Tasks: FastAPI endpoints, React dashboard (map view, mission history), integration testing, UAT with operators
- Phase: Serving

Sprint 7 (Semanas 15-16): MLOps + Production
- Tasks: Model monitoring (Prometheus/Grafana), retraining pipelines, Docker/K8s deployment, production security, load testing
- Phase: MLOps

For the HTML widget, I'll create a timeline view with sprint blocks. Each sprint is clickable and shows its tasks.

Let me design this: 
- A horizontal timeline with 8 sprint blocks
- Each block is colored by phase
- Clicking a block shows the sprint details panel below
- The details panel shows: Sprint goal, key deliverables, tech involved

Colors by phase:
- Discovery: c-amber (#FAC775 / #BA7517)
- Data Engineering: c-blue (#B5D4F4 / #185FA5)
- ML: c-purple (#CECBF6 / #534AB7)
- Serving: c-coral (#F5C4B3 / #993C1D)
- MLOps: c-teal (#9FE1CB / #0F6E56)

HTML structure:
```html
<div> <!-- timeline -->
  <div> <!-- sprint blocks row -->
    <div class="sprint-block" data-sprint="0">Sprint 0</div>
    ...
  </div>
  <div> <!-- detail panel -->
    <!-- shows when sprint clicked -->
  </div>
</div>
```

With some CSS for the sprint blocks (colored rectangles with sprint number and phase label) and a detail panel below.

OK I think I have enough to write the full response now. Let me do it.

Actually, let me reconsider: I want to create the best possible response. Let me think about what the user needs most right now.

The user said "empezando desde cero, desde las ideas, diagramas, aplicando toda la ingenieria y metodologias de desarrollo".

So they want:
1. ✅ Understand the problem deeply (I've read it)
2. ✅ Methodology proposal (Design Thinking + Scrum)
3. ✅ Architecture diagrams
4. ✅ Engineering approach (tech stack, sprints)
5. Next steps to start working

Let me also provide:
- The epics/user stories at a high level
- The key technical decisions to make
- Risk assessment

I'll now write the response. It will be rich with both text and two interactive visuals (architecture SVG + sprint roadmap HTML).

Let me also think about whether the sprint roadmap should be HTML or SVG. Given that it's interactive (click to see details), HTML is better.

Let me now write everything. Here is my plan:

**Text block 1**: Problem synthesis + methodology selection (3-4 paragraphs)
**Visual 1**: System architecture SVG (structural diagram)
**Text block 2**: Architecture layer explanation (brief)
**Visual 2**: Sprint roadmap HTML (interactive)
**Text block 3**: Technology stack + immediate next steps

Let me start writing. I'll aim for a complete, professional, forward-thinking response.

Let me now write the SVG. I need to be very precise. Let me finalize all coordinates:

ViewBox: 0 0 680 555

Sources (y=30, h=46):
- DJI: x=40, cx=100, title_y=45, sub_y=62
- PIX4D: x=190, cx=250, title_y=45, sub_y=62
- IDEAM: x=340, cx=400, title_y=45, sub_y=62
- Terreno: x=490, cx=555, title_y=45, sub_y=62

Source arrows: y1=78 → y2=113

Ingestion (x=40, y=115, w=600, h=52):
- title_y = 115 + 52*0.38 = 115+20 = 135 (but center is 115+26=141, use dominant-baseline="central")
- Actually with dominant-baseline="central": title at y=135, sub at y=151

Arrow: y1=169 → y2=185

DataLake (x=40, y=187, w=600, h=133):
- Container title y=207 (th, 20px below top)
- Inner boxes: y=218, h=80
  - title at 218+27=245, sub at 218+53=271

Inner arrows at y=258 (218+40):
- (228,258)→(244,258) — between Raw (r.edge=226) and Processed (l.edge=246)
- (414,258)→(430,258) — between Processed (r.edge=412) and Curated (l.edge=432)

Arrow: y1=322 → y2=338

ML Platform (x=40, y=340, w=600, h=120):
- Container title y=360
- Inner boxes: y=372, h=72
  - title at 372+24=396, sub at 372+47=419

Arrow: y1=462 (from each serving outlet point)

Serving (y=480, h=50):
- FastAPI: x=100, cx=190, title_y=497, sub_y=515
- Dashboard: x=400, cx=490, title_y=497, sub_y=515

ViewBox height: 480+50+25=555

Let me double-check no elements exceed x=640:
- Terreno: x=490+130=620 < 640 ✓
- Ingestion: x=40+600=640 ✓ (exactly at edge, OK)
- Curated inner: x=432+166=598 < 640 ✓
- Model Registry inner: x=432+166=598 < 640 ✓
- Dashboard serving: x=400+180=580 < 640 ✓

All good.

Now let me write the full SVG code. I'll be clean and precise.

Hmm, one issue: the inner arrows between DataLake zones - their y coordinate should be at the center of the inner boxes. Inner boxes: y=218, h=80. Center y = 218+40=258. ✓

Also: subtitle text for inner boxes at y=271 (218+53=271). The inner box bottom is 218+80=298. Is 271 within the box? 271 < 298 ✓ and 271 > 218+font_size ≈ 218+12=230 ✓.

Let me also think about whether "Limpieza · Joins · Meta" fits in w=166:
"Limpieza · Joins · Meta" = 23 chars * 5.85 = 135px < 166px ✓

But actually I realized "Metadatos" was important. Let me use:
- Raw: "Logs brutos · CSVs"
- Processed: "Limpieza · Joins"  
- Curated: "Features · Labels"

These are cleaner.

And for ML inner boxes:
- Feature Store: "Feast · variables" = 17 chars * 5.85 = 99px ✓
- ML Training: "sklearn · PyTorch" = 17 * 5.85 = 99px ✓
- Model Registry: "MLflow · versioning" = 19 * 5.85 = 111px ✓

Now let me write the actual SVG code for real this time.

Wait, I also need to think about the text for the ingestion box. The subtitle:
"Apache Kafka · Airflow · Extractores custom"
= 44 chars * 5.85 = 257px < 600px ✓

Actually at ts (12px), the Anthropic Sans scaling: 44 * 5.85 = 257px - yes that's fine for a 600px box.

Let me also reconsider the source box widths. PIX4D subtitle "Mapas NDVI · RGB" = 16 chars * 5.85 = 94px < 120px ✓. Good.

IDEAM subtitle "API clima hist." = 15 chars * 5.85 = 88px < 120px ✓.

Terreno subtitle "Suelos · Edafología" = 20 chars * 5.85 = 117px < 130px ✓.

DJI subtitle "SmartFarm · Terra" = 17 chars * 5.85 = 99px < 120px ✓.

One last thing: The "Data lake · S3 / GCS · Delta Lake / Iceberg" container title:
44 chars at th (14px, 500wt): 44 * 7.6 = 334px < 600px ✓

"Plataforma ML · MLflow · Feast" = 30 chars * 7.6 = 228px ✓

Now I'm truly ready to write the SVG. Let me also verify that the inner box title at y=245 makes sense:

Inner Raw box: x=60, y=218, h=80. Center y=258. Title at y=245 (30% from top: 218+24=242, or 218+80*0.35=218+28=246). Let me use y=244 for title and y=268 for subtitle (218+50=268). 

Actually with `dominant-baseline="central"`, the y is the center of the glyph. So:
- Title (th, 14px line height ~18px): center at y=244 means it spans 235-253
- Sub (ts, 12px line height ~15px): center at y=268 means it spans 260.5-275.5
- Inner box: y=218 to y=298
- 235 > 218+6=224 ✓ (title has room above)
- 275.5 < 298-5=293 ✓ (sub has room below)

OK. Let me finalize:
- Inner box title: y = box_y + 26 = 218+26=244
- Inner box subtitle: y = box_y + 52 = 218+52=270

For ML inner boxes (y=372, h=72):
- Title y = 372+24 = 396
- Sub y = 372+46 = 418

These fit: title top = 396-9=387 > 372+5=377 ✓, sub bottom = 418+6=424 < 372+72-5=439 ✓

OK. One absolute last thing: The c-blue group for DataLake container. I write:
```svg
<g class="c-blue">
  <rect x="40" y="187" width="600" height="133" rx="12" stroke-width="0.5"/>
  <text class="th" x="340" y="207" text-anchor="middle" dominant-baseline="central">...</text>
</g>
```

The `c-blue` class makes the rect have 50-stop fill (very light blue). The text is a direct child of `c-blue` g, so it gets 800-stop color (dark blue). ✓

For ML Platform:
```svg
<g class="c-purple">
  <rect x="40" y="340" width="600" height="120" rx="12" stroke-width="0.5"/>
  <text class="th" x="340" y="360" text-anchor="middle" dominant-baseline="central">...</text>
</g>
```

Same logic. c-purple gives light purple background (50 stop) and dark purple text (800 stop). ✓

For ingestion box (c-gray):
```svg
<g class="node c-gray" ...>
  <rect x="40" y="115" width="600" height="52" rx="8" stroke-width="0.5"/>
  <text class="th" x="340" y="135" text-anchor="middle" dominant-baseline="central">Capa de ingesta</text>
  <text class="ts" x="340" y="151" text-anchor="middle" dominant-baseline="central">Apache Kafka · Airflow · Extractores custom</text>
</g>
```

Hmm, 135 and 151. The box is y=115, h=52, center=141. Title at y=135 (26px from top = 49.5% up from center), subtitle at y=151 (36px from top = 69% from top). Let me use:
- Title at y=133 (18px from top)
- Sub at y=149 (34px from top)

With dominant-baseline="central":
- These positions should work for a 2-line layout in h=52 box
- Title center at 133 spans 133±7 = 126-140 — well within 115-167 ✓
- Sub center at 149 spans 149±6 = 143-155 — well within 115-167 ✓
- Gap between them: 149-133=16px — comfortable ✓

Alright, I'm going to write the SVG now. For real. No more planning.

Actually wait - I also need the `class="arr"` on lines to include `fill="none"`. Looking at the spec again: "class='arr' = arrow line (1.5px, open chevron head)". The `arr` class already handles fill. Lines don't need fill=none anyway (only paths do). But to be safe: for `<line>` elements, fill doesn't apply visually. For `<path>` used as connectors, `fill="none"` is required. I'm using `<line>` elements, so no explicit `fill="none"` needed.

OK here's my final SVG:

```svg
<svg width="100%" viewBox="0 0 680 555" role="img">
<title>AgroUAV Data Platform — arquitectura de 5 capas</title>
<desc>Arquitectura de datos para agricultura de precisión en Colombia: fuentes UAV y clima, ingesta, Data Lake medallion, plataforma ML y serving.</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<!-- LAYER 1 · FUENTES -->
<g class="node c-green" onclick="sendPrompt('¿Cómo extraemos los flight logs de DJI SmartFarm y DJI Terra para ingestarlos al Data Lake?')">
<rect x="40" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="100" y="45" text-anchor="middle" dominant-baseline="central">DJI logs</text>
<text class="ts" x="100" y="62" text-anchor="middle" dominant-baseline="central">SmartFarm · Terra</text>
</g>
<g class="node c-green" onclick="sendPrompt('¿Cómo exportamos misiones y mapas NDVI de PIX4D hacia el Data Lake?')">
<rect x="190" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="250" y="45" text-anchor="middle" dominant-baseline="central">PIX4D</text>
<text class="ts" x="250" y="62" text-anchor="middle" dominant-baseline="central">Mapas NDVI · RGB</text>
</g>
<g class="node c-green" onclick="sendPrompt('¿Qué datos y APIs provee el IDEAM para series climáticas históricas en Colombia?')">
<rect x="340" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="400" y="45" text-anchor="middle" dominant-baseline="central">IDEAM</text>
<text class="ts" x="400" y="62" text-anchor="middle" dominant-baseline="central">Clima histórico</text>
</g>
<g class="node c-green" onclick="sendPrompt('¿Qué fuentes de datos de suelos y edafología existen para Colombia y cómo las integramos?')">
<rect x="490" y="30" width="130" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="555" y="45" text-anchor="middle" dominant-baseline="central">Terreno</text>
<text class="ts" x="555" y="62" text-anchor="middle" dominant-baseline="central">Suelos · Edafología</text>
</g>

<!-- Source → Ingestion arrows -->
<line x1="100" y1="78" x2="100" y2="113" class="arr" marker-end="url(#arrow)"/>
<line x1="250" y1="78" x2="250" y2="113" class="arr" marker-end="url(#arrow)"/>
<line x1="400" y1="78" x2="400" y2="113" class="arr" marker-end="url(#arrow)"/>
<line x1="555" y1="78" x2="555" y2="113" class="arr" marker-end="url(#arrow)"/>

<!-- LAYER 2 · INGESTA -->
<g class="node c-gray" onclick="sendPrompt('¿Cuál es la arquitectura detallada del pipeline de ingesta con Kafka y Airflow para los datos de drones agrícolas en Colombia?')">
<rect x="40" y="115" width="600" height="52" rx="8" stroke-width="0.5"/>
<text class="th" x="340" y="133" text-anchor="middle" dominant-baseline="central">Capa de ingesta</text>
<text class="ts" x="340" y="150" text-anchor="middle" dominant-baseline="central">Apache Kafka · Apache Airflow · Extractores custom (DJI SDK · PIX4D API · IDEAM REST)</text>
</g>

<!-- Ingestion → DataLake arrow -->
<line x1="340" y1="169" x2="340" y2="185" class="arr" marker-end="url(#arrow)"/>

<!-- LAYER 3 · DATA LAKE (outer container) -->
<g class="c-blue">
<rect x="40" y="187" width="600" height="133" rx="12" stroke-width="0.5"/>
<text class="th" x="340" y="207" text-anchor="middle" dominant-baseline="central">Data lake · AWS S3 / GCS · Delta Lake / Iceberg — arquitectura medallion</text>
</g>
<!-- Inner zones -->
<g class="node c-gray" onclick="sendPrompt('¿Qué esquema de datos y formatos usamos en la zona Raw del Data Lake para telemetría de UAVs?')">
<rect x="60" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
<text class="th" x="143" y="244" text-anchor="middle" dominant-baseline="central">Raw · Bronze</text>
<text class="ts" x="143" y="269" text-anchor="middle" dominant-baseline="central">Logs brutos · CSVs · Rasters</text>
</g>
<g class="node c-teal" onclick="sendPrompt('¿Cómo transformamos los datos con dbt y Spark en la zona Silver del Data Lake?')">
<rect x="246" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
<text class="th" x="329" y="244" text-anchor="middle" dominant-baseline="central">Processed · Silver</text>
<text class="ts" x="329" y="269" text-anchor="middle" dominant-baseline="central">Limpieza · Joins · Metadatos</text>
</g>
<g class="node c-amber" onclick="sendPrompt('¿Cómo estructuramos los Features y Labels en la zona Gold del Data Lake para entrenar modelos ML?')">
<rect x="432" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
<text class="th" x="515" y="244" text-anchor="middle" dominant-baseline="central">Curated · Gold</text>
<text class="ts" x="515" y="269" text-anchor="middle" dominant-baseline="central">Features · Labels · Series</text>
</g>
<!-- Inner zone arrows -->
<line x1="228" y1="258" x2="244" y2="258" class="arr" marker-end="url(#arrow)"/>
<line x1="414" y1="258" x2="430" y2="258" class="arr" marker-end="url(#arrow)"/>

<!-- DataLake → ML arrow -->
<line x1="340" y1="322" x2="340" y2="338" class="arr" marker-end="url(#arrow)"/>

<!-- LAYER 4 · ML PLATFORM (outer container) -->
<g class="c-purple">
<rect x="40" y="340" width="600" height="120" rx="12" stroke-width="0.5"/>
<text class="th" x="340" y="360" text-anchor="middle" dominant-baseline="central">Plataforma ML · MLflow · Feast Feature Store</text>
</g>
<!-- Inner ML components -->
<g class="node c-teal" onclick="sendPrompt('¿Cómo implementamos un Feature Store con Feast para variables temporales de clima y telemetría UAV?')">
<rect x="60" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
<text class="th" x="143" y="396" text-anchor="middle" dominant-baseline="central">Feature store</text>
<text class="ts" x="143" y="416" text-anchor="middle" dominant-baseline="central">Feast · time-series vars</text>
</g>
<g class="node c-coral" onclick="sendPrompt('¿Qué modelos ML entrenamos para predecir anomalías NDVI y optimizar parámetros de vuelo?')">
<rect x="246" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
<text class="th" x="329" y="396" text-anchor="middle" dominant-baseline="central">ML training</text>
<text class="ts" x="329" y="416" text-anchor="middle" dominant-baseline="central">sklearn · PyTorch · MLflow</text>
</g>
<g class="node c-amber" onclick="sendPrompt('¿Cómo gestionamos el ciclo de vida de modelos y el versionado con MLflow Model Registry?')">
<rect x="432" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
<text class="th" x="515" y="396" text-anchor="middle" dominant-baseline="central">Model registry</text>
<text class="ts" x="515" y="416" text-anchor="middle" dominant-baseline="central">MLflow · versioning · CI/CD</text>
</g>

<!-- ML → Serving arrows -->
<line x1="190" y1="462" x2="190" y2="478" class="arr" marker-end="url(#arrow)"/>
<line x1="490" y1="462" x2="490" y2="478" class="arr" marker-end="url(#arrow)"/>

<!-- LAYER 5 · SERVING -->
<g class="node c-coral" onclick="sendPrompt('¿Cómo diseñamos los endpoints de FastAPI para servir recomendaciones de configuración de misiones UAV?')">
<rect x="100" y="480" width="180" height="50" rx="8" stroke-width="0.5"/>
<text class="th" x="190" y="498" text-anchor="middle" dominant-baseline="central">REST API</text>
<text class="ts" x="190" y="516" text-anchor="middle" dominant-baseline="central">FastAPI · mission endpoints</text>
</g>
<g class="node c-amber" onclick="sendPrompt('¿Qué visualizaciones geoespaciales necesita el dashboard para operadores de drones agrícolas en Colombia?')">
<rect x="400" y="480" width="180" height="50" rx="8" stroke-width="0.5"/>
<text class="th" x="490" y="498" text-anchor="middle" dominant-baseline="central">Dashboard</text>
<text class="ts" x="490" y="516" text-anchor="middle" dominant-baseline="central">React · Deck.gl · geospatial</text>
</g>

</svg>
```

Wait, let me verify the container and the closing of viewbox height. The serving boxes end at y=480+50=530. ViewBox height set to 555. Remaining space: 555-530=25px padding. ✓

Let me also check: do any arrows cross through boxes?
- Source arrows: (100,78)→(100,113) — these are outside any boxes (between source boxes at y=30-76 and ingestion at y=115) ✓
- Ingestion→DataLake: (340,169)→(340,185) — between ingestion (y=115-167) and DataLake (y=187-320), the arrow is in the gap (y=169-185). 340 is within no box horizontally ✓
- DataLake→ML: (340,322)→(340,338) — between DataLake (187-320) and ML (340-460). Gap: y=322-338. Checks out ✓
- ML→Serving (190,462)→(190,478) — between ML (340-460) and Serving (480-530). Gap: y=462-478. x=190 — not within any serving box (FastAPI is x=100-280, so 190 IS within FastAPI box x range, but FastAPI starts at y=480, and the arrow goes to y=478, so it stops just before the box ✓)
- ML→Serving (490,462)→(490,478) — x=490, Dashboard is x=400-580, y=480-530. Arrow stops at y=478, before y=480 ✓

Inner DataLake arrows: (228,258)→(244,258) — these are in the gap between Raw (x=60-226) and Processed (x=246-412). y=258 is within the inner boxes (y=218-298) but the arrows are in the horizontal gap, not inside any box ✓

Wait: x=228 to x=244. Gap between Raw right edge (226) and Processed left edge (246) is 20px. Arrow starts at 228 (2px from Raw right edge) and ends at 244 (2px from Processed left edge). So the arrow is in the 20px gap. ✓

Similarly for Proc→Curated: (414,258)→(430,258). Gap between Processed right (412) and Curated left (432) = 20px. Arrow: 414 to 430. ✓

No crossings. 

Let me also verify that no inner box text overflows:
- "Limpieza · Joins · Metadatos" (29 chars at 12px, 5.85px/char) = 170px > 166px width ❌

Oh, that's an issue. Let me shorten:
- "Limpieza · Joins" = 17 chars * 5.85 = 99px ✓

Let me update subtitle for Processed zone to "Limpieza · Joins" and add "Metadatos" to the title perhaps? No, the title is "Processed · Silver". Let me keep it as "Limpieza · Joins · Meta" = 23 chars * 5.85 = 135px ✓.

Actually I was being too conservative. Let me re-check with better numbers. From the font calibration table:
- "Authentication Service" = 22 chars, 14px, 500wt = 167px → ~7.6px/char at 14px 500wt
- For 12px 400wt: scale by (12/14) * (400/500 factor ~0.88) ≈ 0.755. So 7.6 * 0.755 = 5.74px/char

"Limpieza · Joins · Metadatos" = 29 chars * 5.74 = 166px. It's right at the edge! With 24px padding (12px each side), the text needs 166px in a 166px box. That's zero padding. Way too tight.

Let me use: "Limpieza · Joins" (17 chars * 5.74 = 98px, fits easily) ✓
Or: "Limpieza, joins, meta" = 22 chars * 5.74 = 126px ✓

I'll use "Limpieza · Joins · meta" = 23 * 5.74 = 132px ✓ (with 17px padding each side). Good.

What about "MLflow · versioning · CI/CD" = 26 chars * 5.74 = 149px < 166px ✓ (17px each side)

What about the DataLake container title "Data lake · AWS S3 / GCS · Delta Lake / Iceberg — arquitectura medallion" ?
= 72 chars at 14px 500wt = 72 * 7.6 = 547px < 600px ✓

And "Plataforma ML · MLflow · Feast Feature Store" = 44 chars * 7.6 = 334px < 600px ✓

And ingestion subtitle "Apache Kafka · Apache Airflow · Extractores custom (DJI SDK · PIX4D API · IDEAM REST)" = 85 chars * 5.74 = 488px < 600px ✓

Great. Everything fits. Let me now write the full, clean SVG.

Actually, I realize there might be a problem with the DataLake container `c-blue` group. If I use:
```svg
<g class="c-blue">
  <rect .../>
  <text class="th" ...>...</text>
</g>
```

The text is a direct child of `c-blue`, so it gets 800-stop color (dark blue for light mode). This is correct.

But then when I draw the inner boxes separately (not inside this `<g>`), they appear on top of the DataLake rect because they come later in the SVG. This is correct SVG z-ordering.

However, the inner boxes have different c-* classes. The `node` class adds hover effect. Let me make sure the inner boxes are drawn AFTER the outer container group closes.

Let me structure the SVG properly:

1. DataLake outer container group (c-blue with rect + title text)
2. Inner Raw zone (c-gray, node)
3. Inner Processed zone (c-teal, node)
4. Inner Curated zone (c-amber, node)
5. Inner arrows between zones

This order ensures inner boxes render on top of the outer container background. ✓

Same for ML Platform.

OK I'm writing the final SVG now. Let me also account for one more thing: the `node` class adds "cursor: pointer" and hover effects. I should only add `node` to clickable groups, which is all of them. The outer DataLake and ML containers — should they be clickable? I'll make them non-node (just structural containers) and make the inner boxes and the serving boxes node+clickable.

For the ingestion box and source boxes: make them node+clickable. ✓

OK here is the truly final SVG (writing it carefully):

Note about the ingestion subtitle: I need to check "Apache Kafka · Apache Airflow · Extractores custom (DJI SDK · PIX4D API · IDEAM REST)" at 12px in a 600px box. Let me count: 84 chars * 5.74 = 482px < 600px ✓

Hmm wait, is `·` wider than normal characters? The middle dot (·) should be about the same width as a regular character in Anthropic Sans. Let me count just to be sure:
"Apache Kafka · Apache Airflow · Extractores custom" = 50 chars ≈ 287px < 600px ✓
Easy.

For the DataLake container title "Data lake · AWS S3 / GCS · Delta Lake / Iceberg — arquitectura medallion" - actually let me shorten this to avoid it being too long and potentially wrapping:
"Data lake · S3 / GCS · Delta Lake — arquitectura medallion" = 59 chars * 7.6 = 448px < 600px ✓

Actually the full title with "AWS" is 72 chars = 547px which is still < 600px. Let me keep it or simplify to:
"Data lake · S3 / GCS · Delta Lake / Iceberg" = 44 chars * 7.6 = 334px ✓ (plenty of room)

Let me simplify the title and put "arquitectura medallion" as a subtitle? No, two-line format in the outer container header would be complex. Keep it single-line and short:
"Data lake · AWS S3 · Delta Lake" = 31 chars * 7.6 = 236px ✓

Or even better - just show the key concept:
"Data lake · arquitectura medallion (Raw → Silver → Gold)" = 57 chars * 7.6 = 433px < 600px ✓

Perfect. That communicates the pattern. Let me use this.

OK now I'm absolutely writing it. The key subtitles are:
- Raw inner: "Logs brutos · rasters · CSVs"
  - 28 chars * 5.74 = 161px < 166px (barely fits, ~2.5px padding each side). Let me shorten: "Logs · rasters · CSVs" = 21 chars * 5.74 = 121px ✓
- Processed inner: "Limpieza · joins · meta" = 23 chars * 5.74 = 132px ✓
- Curated inner: "Features · labels · series" = 26 chars * 5.74 = 149px ✓ (just fits with 8.5px padding)

For ML inner:
- Feature Store subtitle: "Feast · time-series vars" = 24 chars * 5.74 = 138px ✓
- ML Training subtitle: "sklearn · PyTorch · MLflow" = 26 chars * 5.74 = 149px ✓
- Model Registry subtitle: "MLflow · versioning · CI/CD" = 27 chars * 5.74 = 155px ✓ (fits with 5.5px padding each side)

Hmm that's a bit tight. Let me use "MLflow · CI/CD" = 14 chars * 5.74 = 80px ✓

Actually I want to show more information. Let me use "MLflow · versioning" = 19 chars * 5.74 = 109px ✓. Clean.

OK. FINAL FINAL SVG (I promise I'll just write it now):

Source boxes:
- DJI: x=40, w=120
- PIX4D: x=190, w=120
- IDEAM: x=340, w=120
- Terreno: x=490, w=130

Let me also double-check: right edge of Terreno = 490+130=620. Safe area end = 640. OK ✓.
But 620 is close to the edge. Gap from edge: 640-620=20px. That's fine.

But wait, for source boxes, they're not centered in the 680px width:
- Total span: from x=40 to x=620 = 580px
- Available width: 640-40=600px (40px safe margin on left, same on right should be 680-640=40px)
- Left margin: 40px, right margin: 680-620=60px. Not symmetric. 

To center all 4 source boxes: total width needed = 4 boxes + 3 gaps.
- 4 * 120 + 1 * 130 = 480 + 130 = 610... wait, 3 boxes are 120 and 1 is 130, total = 3*120+1*130=360+130=490, plus 3 gaps of 15px = 45, total = 535
- Center: (640-40)/2+40 = 340 center point
- Start: 340 - 535/2 = 340 - 267.5 = 72.5 ≈ 73

Let me re-plan with centered layout:
- DJI: x=73, w=120, end=193
- Gap: 73+120=193, +15=208
- PIX4D: x=208, w=120, end=328
- Gap: 328+15=343
- IDEAM: x=343, w=120, end=463
- Gap: 463+15=478
- Terreno: x=478, w=130, end=608
- Right margin: 640-608=32px, left margin=73px

Not perfectly symmetric but close enough. Let me try equal gap:
- 4 * 120 = 480, 3 gaps = (600-480)/3 = 40px each
- x: 40, 200, 360, 520, all w=120, right edge = 640 ✓ (symmetric with left margin = 40px)

But Terreno box is slightly wider (130 vs 120). If all 4 are 120px:
- "Suelos · Edafología" = 20 chars * 5.74 = 115px < 120px ✓ (just barely, 2.5px padding each side)

Actually let me just make all 4 boxes 120px wide with equal 40px gaps:
- x: 40, 200, 360, 520
- Centers: 100, 260, 420, 580
- Right edges: 160, 320, 480, 640 (exact edge of safe area ✓)

For Terreno subtitle "Suelos · Edafología": Let me verify 20 chars at 12px:
20 * 5.74 = 115px. Box is 120px. Padding = (120-115)/2 = 2.5px. That's very tight but should work in practice since some characters are narrower.

Actually, I realize the spec says the character width estimates are averages. "Edafología" has é and í which might be slightly wider. Let me just shorten the subtitle to "Suelos · edaf." = 14 chars * 5.74 = 80px ✓.

OK with the equal 40px gaps:
- DJI: x=40, w=120, cx=100
- PIX4D: x=200, w=120, cx=260
- IDEAM: x=360, w=120, cx=420
- Terreno: x=520, w=120, cx=580

Arrows from: x=100, 260, 420, 580 going down to y=113.

This is cleaner and more symmetric. Let me use this layout.

And the DataLake/ML containers: x=40, w=600. Right edge = 640. ✓
Inner boxes (3 per container): 
- Available width inside container: 600 - 2*20 = 560px (20px padding each side)
- 3 boxes + 2 gaps: 3*w + 2*g = 560
- If w=166, g=14: 3*166+2*14=498+28=526 < 560, leftover=34px, extra margin=17px each side
- So inner boxes: x=57, 237, 417, w=166, right edge=583 < 620 ✓
- Centers: 57+83=140, 237+83=320, 417+83=500

Hmm let me re-check: inner box x positions with 20px container padding:
- Container: x=40, so inner x_start = 60
- With 3 boxes (w=166) and gaps:
  - Gap = (560 - 3*166) / 2 = (560-498)/2 = 31px
  - x: 60, 60+166+31=257, 257+166+31=454
  - Right edge: 454+166=620 < 640 ✓
  - Centers: 143, 340, 537

Wait: 60+166=226, +31=257, +166=423, +31=454, +166=620. Container right edge=640. Inner right edge=620. Padding=20 ✓.
Centers: 60+83=143, 257+83=340, 454+83=537.

These are better! Centers at 143, 340, 537. Much more symmetric (close to thirds of 600px).

Inner zone arrows:
- Raw→Processed: from (226+2=228, center_y) to (257-2=255, center_y)
  - Arrow from (228, 258) to (255, 258)
- Processed→Curated: from (423+2=425, center_y) to (454-2=452, center_y)
  - Arrow from (425, 258) to (452, 258)

Let me recalculate center_y: inner boxes y=218, h=80, center=258 ✓

Source arrow x positions: 100, 260, 420, 580

Do these align with ingestion box? Ingestion: x=40, w=600, x_range=40-640. All arrow x (100,260,420,580) are within this range ✓.

But now source boxes are at x=40,200,360,520 while ingestion x starts at 40. The arrow from x=100 goes to x=100 at the ingestion box. Fine. The arrow from x=580 goes to x=580 which is within the ingestion box (640). Fine.

But the arrow from x=580 would be at the far right of the ingestion box. Is there any overlap with the ingestion box's edge? Ingestion box: x=40-640. x=580 < 640 ✓.

OK. Truly writing the SVG now. Let me just do it.

One more edge case: the serving boxes.
For FastAPI and Dashboard to be "below" the ML platform:
ML container: x=40, w=600, inner boxes at x=60,257,454.
Feature Store center: 143. Training center: 340. Registry center: 537.

FastAPI should be roughly below Feature Store and Training (x=143 and x=340). Let me center it at ~242.
Dashboard should be roughly below Training and Registry (x=340 and x=537). Center at ~438.

- FastAPI: x=142, w=200, cx=242 — hmm 142+200=342, so from Feature Store into Training area
- Dashboard: x=362, w=200, cx=462 — 362+200=562

Let me do:
- FastAPI: x=100, w=200, cx=200
- Dashboard: x=380, w=200, cx=480
- Gap between: 380-300=80px. Plenty of space.

Right edge of Dashboard: 380+200=580 < 640 ✓

ML→Serving arrows:
- (200, 462) → (200, 478) — below Training area
- (480, 462) → (480, 478) — below Registry area

Are these within the ML container? ML: x=40-640. 200 ✓, 480 ✓.

Alright I'm actually writing the code now. Full SVG:

Actually I realize I should also check: the ingestion subtitle text 
"Apache Kafka · Apache Airflow · Extractores custom (DJI SDK · PIX4D API · IDEAM REST)"
= ~84 chars * 5.74 ≈ 482px. Box width 600px. Fits ✓.

But wait, this might actually be wider than I think. Let me count more carefully:
"Apache Kafka · Apache Airflow · Extractores custom (DJI SDK · PIX4D API · IDEAM REST)"
 A-p-a-c-h-e- -K-a-f-k-a- -·- -A-p-a-c-h-e- -A-i-r-f-l-o-w- -·- -E-x-t-r-a-c-t-o-r-e-s- -c-u-s-t-o-m- -(D-J-I- -S-D-K- -·- -P-I-X-4-D- -A-P-I- -·- -I-D-E-A-M- -R-E-S-T-)
= 6+1+5+3+6+1+8+3+10+1+6+1+1+3+1+3+3+6+1+4+2
Let me just count: 86 characters * 5.74 = 494px < 600px ✓

OK. Writing. Now. For real.

Let me also decide on a shorter ingestion subtitle to reduce cognitive load:
"Airflow DAGs · Kafka streams · extractores SDK" = 47 chars * 5.74 = 270px ✓

Much cleaner. Use this.

For DataLake title (th, 14px): "Data lake · arquitectura medallion · S3/GCS · Delta Lake" 
= 57 chars * 7.6 = 433px < 600px ✓

For ML title: "Plataforma ML · Feast Feature Store · MLflow" = 44 chars * 7.6 = 334px ✓

Writing it. Now.

Here's what I'll actually produce in show_widget:

```svg
<svg width="100%" viewBox="0 0 680 555" role="img">
<title>AgroUAV Data Platform — arquitectura de 5 capas</title>
<desc>...</desc>
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>

<!-- 1. SOURCES -->
[4 source boxes c-green]

<!-- Arrows source → ingestion -->
[4 vertical lines]

<!-- 2. INGESTION -->
[1 wide box c-gray]

<!-- Arrow ingestion → datalake -->
[1 line]

<!-- 3. DATA LAKE -->
[outer c-blue container]
[3 inner boxes: c-gray, c-teal, c-amber]
[2 inter-zone arrows]

<!-- Arrow datalake → ml -->
[1 line]

<!-- 4. ML PLATFORM -->
[outer c-purple container]
[3 inner boxes: c-teal, c-coral, c-amber]

<!-- Arrows ml → serving -->
[2 lines]

<!-- 5. SERVING -->
[2 boxes: c-coral, c-amber]
</svg>
```

Now for real. Here's the complete, final SVG code that I'll put in show_widget:

```svg
<svg width="100%" viewBox="0 0 680 555" role="img">
<title>AgroUAV Data Platform — arquitectura de 5 capas</title>
<desc>Diagrama estructural de la plataforma de datos para agricultura de precisión con UAVs en Colombia: capas de fuentes, ingesta, Data Lake medallion, ML Platform y serving.</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>

<!-- === LAYER 1: DATA SOURCES === -->
<g class="node c-green" onclick="sendPrompt('¿Cómo extraemos los flight logs y telemetría de DJI SmartFarm y DJI Terra?')">
<rect x="40" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="100" y="46" text-anchor="middle" dominant-baseline="central">DJI logs</text>
<text class="ts" x="100" y="62" text-anchor="middle" dominant-baseline="central">SmartFarm · Terra</text>
</g>

<g class="node c-green" onclick="sendPrompt('¿Qué formatos exporta PIX4D y cómo los ingestamos al Data Lake?')">
<rect x="200" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="260" y="46" text-anchor="middle" dominant-baseline="central">PIX4D</text>
<text class="ts" x="260" y="62" text-anchor="middle" dominant-baseline="central">Mapas NDVI · RGB</text>
</g>

<g class="node c-green" onclick="sendPrompt('¿Qué endpoints y variables provee la API del IDEAM para datos climáticos históricos en Colombia?')">
<rect x="360" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="420" y="46" text-anchor="middle" dominant-baseline="central">IDEAM</text>
<text class="ts" x="420" y="62" text-anchor="middle" dominant-baseline="central">Clima histórico</text>
</g>

<g class="node c-green" onclick="sendPrompt('¿Qué fuentes de datos de suelos, edafología y verdad terreno existen para Colombia?')">
<rect x="520" y="30" width="120" height="46" rx="8" stroke-width="0.5"/>
<text class="th" x="580" y="46" text-anchor="middle" dominant-baseline="central">Terreno</text>
<text class="ts" x="580" y="62" text-anchor="middle" dominant-baseline="central">Suelos · edaf.</text>
</g>

<!-- Source → Ingestion arrows -->
<line x1="100" y1="78" x2="100" y2="113" class="arr" marker-end="url(#arrow)"/>
<line x1="260" y1="78" x2="260" y2="113" class="arr" marker-end="url(#arrow)"/>
<line x1="420" y1="78" x2="420" y2="113" class="arr" marker-end="url(#arrow)"/>
<line x1="580" y1="78" x2="580" y2="113" class="arr" marker-end="url(#arrow)"/>

<!-- === LAYER 2: INGESTION === -->
<g class="node c-gray" onclick="sendPrompt('¿Cuál es la arquitectura completa del pipeline de ingesta con Airflow y Kafka para datos de drones agrícolas?')">
<rect x="40" y="115" width="600" height="52" rx="8" stroke-width="0.5"/>
<text class="th" x="340" y="133" text-anchor="middle" dominant-baseline="central">Capa de ingesta</text>
<text class="ts" x="340" y="151" text-anchor="middle" dominant-baseline="central">Airflow DAGs · Kafka streams · extractores SDK (DJI, PIX4D, IDEAM REST)</text>
</g>

<!-- Ingestion → DataLake arrow -->
<line x1="340" y1="169" x2="340" y2="185" class="arr" marker-end="url(#arrow)"/>

<!-- === LAYER 3: DATA LAKE (outer) === -->
<g class="c-blue">
<rect x="40" y="187" width="600" height="133" rx="12" stroke-width="0.5"/>
<text class="th" x="340" y="207" text-anchor="middle" dominant-baseline="central">Data lake · arquitectura medallion · S3 / GCS · Delta Lake / Iceberg</text>
</g>

<!-- Raw / Bronze -->
<g class="node c-gray" onclick="sendPrompt('¿Qué esquema y formatos usamos en la zona Raw/Bronze del Data Lake para logs de UAVs y clima?')">
<rect x="60" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
<text class="th" x="143" y="244" text-anchor="middle" dominant-baseline="central">Raw · Bronze</text>
<text class="ts" x="143" y="269" text-anchor="middle" dominant-baseline="central">Logs · rasters · CSVs</text>
</g>

<!-- Processed / Silver -->
<g class="node c-teal" onclick="sendPrompt('¿Cómo transformamos datos con dbt y Spark en la zona Silver? ¿Cuáles son los modelos dbt para UAVs?')">
<rect x="257" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
<text class="th" x="340" y="244" text-anchor="middle" dominant-baseline="central">Processed · Silver</text>
<text class="ts" x="340" y="269" text-anchor="middle" dominant-baseline="central">Limpieza · joins · meta</text>
</g>

<!-- Curated / Gold -->
<g class="node c-amber" onclick="sendPrompt('¿Cómo estructuramos los features, labels y series temporales en la zona Gold para entrenamiento ML?')">
<rect x="454" y="218" width="166" height="80" rx="8" stroke-width="0.5"/>
<text class="th" x="537" y="244" text-anchor="middle" dominant-baseline="central">Curated · Gold</text>
<text class="ts" x="537" y="269" text-anchor="middle" dominant-baseline="central">Features · labels · series</text>
</g>

<!-- Inner zone arrows -->
<line x1="228" y1="258" x2="255" y2="258" class="arr" marker-end="url(#arrow)"/>
<line x1="425" y1="258" x2="452" y2="258" class="arr" marker-end="url(#arrow)"/>

<!-- DataLake → ML arrow -->
<line x1="340" y1="322" x2="340" y2="338" class="arr" marker-end="url(#arrow)"/>

<!-- === LAYER 4: ML PLATFORM (outer) === -->
<g class="c-purple">
<rect x="40" y="340" width="600" height="120" rx="12" stroke-width="0.5"/>
<text class="th" x="340" y="360" text-anchor="middle" dominant-baseline="central">Plataforma ML · Feast Feature Store · MLflow</text>
</g>

<!-- Feature Store -->
<g class="node c-teal" onclick="sendPrompt('¿Cómo implementamos Feast Feature Store para variables de clima, telemetría UAV y series temporales?')">
<rect x="60" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
<text class="th" x="143" y="396" text-anchor="middle" dominant-baseline="central">Feature store</text>
<text class="ts" x="143" y="416" text-anchor="middle" dominant-baseline="central">Feast · series temporales</text>
</g>

<!-- ML Training -->
<g class="node c-coral" onclick="sendPrompt('¿Qué modelos ML entrenamos para anomalías NDVI, optimización de parámetros de vuelo y predicción climática?')">
<rect x="257" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
<text class="th" x="340" y="396" text-anchor="middle" dominant-baseline="central">ML training</text>
<text class="ts" x="340" y="416" text-anchor="middle" dominant-baseline="central">sklearn · PyTorch · MLflow</text>
</g>

<!-- Model Registry -->
<g class="node c-amber" onclick="sendPrompt('¿Cómo gestionamos el ciclo de vida de modelos con MLflow Model Registry y automatizamos el reentrenamiento?')">
<rect x="454" y="372" width="166" height="72" rx="8" stroke-width="0.5"/>
<text class="th" x="537" y="396" text-anchor="middle" dominant-baseline="central">Model registry</text>
<text class="ts" x="537" y="416" text-anchor="middle" dominant-baseline="central">MLflow · versioning</text>
</g>

<!-- ML → Serving arrows -->
<line x1="200" y1="462" x2="200" y2="478" class="arr" marker-end="url(#arrow)"/>
<line x1="490" y1="462" x2="490" y2="478" class="arr" marker-end="url(#arrow)"/>

<!-- === LAYER 5: SERVING === -->
<g class="node c-coral" onclick="sendPrompt('¿Cómo diseñamos los endpoints de FastAPI para servir configuraciones óptimas de misiones UAV a los operadores?')">
<rect x="100" y="480" width="200" height="50" rx="8" stroke-width="0.5"/>
<text class="th" x="200" y="498" text-anchor="middle" dominant-baseline="central">REST API</text>
<text class="ts" x="200" y="516" text-anchor="middle" dominant-baseline="central">FastAPI · mission endpoints</text>
</g>

<g class="node c-amber" onclick="sendPrompt('¿Qué visualizaciones geoespaciales necesita el dashboard para análisis de cultivos con NDVI y rutas de vuelo?')">
<rect x="380" y="480" width="200" height="50" rx="8" stroke-width="0.5"/>
<text class="th" x="480" y="498" text-anchor="middle" dominant-baseline="central">Dashboard</text>
<text class="ts" x="480" y="516" text-anchor="middle" dominant-baseline="central">React · Deck.gl · NDVI maps</text>
</g>

</svg>
```

Wait, let me verify the new inner box positions:
- Raw: x=60, w=166, right=226. Center x=143. ✓
- Processed: x=257, w=166, right=423. Center x=340. ✓ (symmetric!)
- Curated: x=454, w=166, right=620. Center x=537. ✓

Container inner padding check:
- Left padding: 60-40=20px ✓
- Right padding: 640-620=20px ✓
- Gap between Raw and Processed: 257-226=31px ✓
- Gap between Processed and Curated: 454-423=31px ✓

Beautiful symmetry! Centers are at 143, 340, 537.

For ML inner:
- Feature Store: x=60, center=143 ✓
- Training: x=257, center=340 ✓  
- Registry: x=454, center=537 ✓

Inner zone arrows for DataLake:
- Raw→Processed: (226+2=228, 258) → (257-2=255, 258). Length=27px ✓
- Processed→Curated: (423+2=425, 258) → (454-2=452, 258). Length=27px ✓

Inner zone arrows center y = 218+40=258 ✓

Source boxes (w=120):
- DJI: x=40, right=160, cx=100
- PIX4D: x=200, right=320, cx=260
- IDEAM: x=360, right=480, cx=420
- Terreno: x=520, right=640, cx=580

Gaps between sources: 200-160=40, 360-320=40, 520-480=40. All 40px ✓

Source arrows at x=100, 260, 420, 580 going to y=113 from y=78 ✓

Serving boxes:
- FastAPI: x=100, w=200, right=300, cx=200
- Dashboard: x=380, w=200, right=580, cx=480

Gap between serving boxes: 380-300=80px ✓

ML→Serving arrows:
- (200, 462) → (200, 478): x=200 is cx of FastAPI ✓
- (490, 462) → (490, 478): x=490 is within Dashboard (380-580) ✓

ViewBox: 0 0 680 555
Last element bottom: 480+50=530. Plus 25px buffer = 555 ✓.

Now let me check for potential text overflow one more time:

ts texts (12px ≈ 5.74px/char):
- "SmartFarm · Terra" = 17 chars * 5.74 = 98px < 120px ✓ (11px padding each)
- "Mapas NDVI · RGB" = 16 chars * 5.74 = 92px < 120px ✓
- "Clima histórico" = 15 chars * 5.74 = 86px < 120px ✓
- "Suelos · edaf." = 14 chars * 5.74 = 80px < 120px ✓
- "Airflow DAGs · Kafka streams · extractores SDK (DJI, PIX4D, IDEAM REST)" = 72 chars * 5.74 = 413px < 600px ✓
- "Logs · rasters · CSVs" = 21 chars * 5.74 = 121px < 166px ✓
- "Limpieza · joins · meta" = 23 chars * 5.74 = 132px < 166px ✓
- "Features · labels · series" = 26 chars * 5.74 = 149px < 166px ✓
- "Feast · series temporales" = 25 chars * 5.74 = 143px < 166px ✓
- "sklearn · PyTorch · MLflow" = 26 chars * 5.74 = 149px < 166px ✓
- "MLflow · versioning" = 19 chars * 5.74 = 109px < 166px ✓
- "FastAPI · mission endpoints" = 27 chars * 5.74 = 155px < 200px ✓
- "React · Deck.gl · NDVI maps" = 27 chars * 5.74 = 155px < 200px ✓

th texts (14px, 500wt ≈ 7.6px/char):
- "DJI logs" = 8 * 7.6 = 61px < 120px ✓
- "PIX4D" = 5 * 7.6 = 38px < 120px ✓
- "IDEAM" = 5 * 7.6 = 38px < 120px ✓
- "Terreno" = 7 * 7.6 = 53px < 120px ✓
- "Capa de ingesta" = 15 * 7.6 = 114px < 600px ✓
- "Data lake · arquitectura medallion · S3 / GCS · Delta Lake / Iceberg" = 68 * 7.6 = 517px < 600px ✓ (barely)

Actually 68 chars at 7.6 = 517px. Box is 600px wide. Center at x=340. Text extends from 340-258.5=81.5 to 340+258.5=598.5. That's 598.5 which is < 640 ✓ but very close to the right safe area edge. The left edge is 81.5 which is > 40 ✓.

But wait, let me count the actual characters:
"Data lake · arquitectura medallion · S3 / GCS · Delta Lake / Iceberg"
D-a-t-a-_-l-a-k-e-_-·-_-a-r-q-u-i-t-e-c-t-u-r-a-_-m-e-d-a-l-l-i-o-n-_-·-_-S-3-_-/-_-G-C-S-_-·-_-D-e-l-t-a-_-L-a-k-e-_-/-_-I-c-e-b-e-r-g = 70 chars

70 * 7.6 = 532px. Still < 600px ✓. Centered at 340, extends 340±266 = 74 to 606. Left=74>40 ✓, Right=606<640 ✓. 

But this is tight. Let me shorten: "Data lake · medallion · S3 / GCS · Delta Lake / Iceberg" = 57 chars * 7.6 = 433px. Centered at 340, extends 340±216.5 = 123.5 to 556.5. Comfortable ✓.

Or even cleaner: "Data lake · medallion architecture · S3 / GCS · Delta Lake" = 59 chars * 7.6 = 448px ✓.

Actually let me use Spanish throughout: "Data lake · arquitectura medallion · AWS S3 · Delta Lake" = 57 * 7.6 = 433px ✓.

Alright. Now truly writing the SVG in the show_widget. After that, I'll write text explaining the architecture, then do the sprint roadmap HTML. Let me structure this clearly.

RESPONSE PLAN:
1. Opening problem synthesis (text)
2. Methodology framing (text)
3. Architecture SVG diagram
4. Architecture explanation (text, one paragraph per layer)
5. Sprint roadmap HTML widget
6. Tech stack + next steps (text)

Total output will be comprehensive but focused. Let me write it now.

For the sprint roadmap HTML, let me plan the structure:

8 sprints in 2 phases:
- Phase A (Discovery + Infrastructure): Sprints 0-3
- Phase B (ML + Serving): Sprints 4-7

HTML Structure:
- Header with legend (color = phase)
- 8 sprint cards in a grid (4 columns, 2 rows)
- Click to expand details
- Details panel below with tasks and tech

Sprint data:
```javascript
const sprints = [
  {
    id: 0, weeks: "Sem 1–2", title: "Discovery", phase: "discovery",
    goal: "Definir el problema, validar fuentes de datos y cerrar la arquitectura",
    deliverables: ["Problem statement validado", "Data inventory (DJI, IDEAM, PIX4D)", "Architecture Decision Record", "Stack tecnológico cerrado"],
    tech: ["Draw.io/Miro", "Python", "Jupyter", "Git"]
  },
  {
    id: 1, weeks: "Sem 3–4", title: "Conectores fuentes", phase: "dataeng",
    goal: "POC de extracción de logs DJI, datos IDEAM y salidas PIX4D",
    deliverables: ["DJI log parser (Python)", "IDEAM API connector", "PIX4D export pipeline", "Schema inicial del Data Lake"],
    tech: ["Python", "requests", "pandas", "Git", "DJI SDK"]
  },
  {
    id: 2, weeks: "Sem 5–6", title: "Infraestructura", phase: "dataeng",
    goal: "Data Lake, CI/CD, orquestación base",
    deliverables: ["S3/GCS bucket structure", "Airflow en Kubernetes", "Kafka cluster", "GitHub Actions CI/CD", "Terraform IaC"],
    tech: ["Terraform", "Kubernetes", "Airflow", "Kafka", "AWS/GCP"]
  },
  {
    id: 3, weeks: "Sem 7–8", title: "Pipelines & modelado", phase: "dataeng",
    goal: "Pipelines Raw→Silver con dbt, calidad de datos, metadatos",
    deliverables: ["DAGs Airflow para ingesta", "modelos dbt Silver", "Great Expectations suite", "Catálogo de metadatos (DataHub)"],
    tech: ["dbt", "Apache Spark", "Great Expectations", "DataHub", "Airflow"]
  },
  {
    id: 4, weeks: "Sem 9–10", title: "Feature engineering", phase: "ml",
    goal: "Zona Gold del Data Lake + Feature Store operativo",
    deliverables: ["Gold layer (series temporales)", "Feast Feature Store", "NDVI baseline features", "Climate lag features", "Feature documentation"],
    tech: ["Feast", "dbt", "PySpark", "numpy", "pandas"]
  },
  {
    id: 5, weeks: "Sem 11–12", title: "Modelos ML v1", phase: "ml",
    goal: "Primer ciclo de entrenamiento de modelos de detección de anomalías",
    deliverables: ["Anomaly detection model (NDVI)", "Flight param optimizer v1", "MLflow tracking", "Model Registry v1", "Notebooks de EDA"],
    tech: ["scikit-learn", "PyTorch", "MLflow", "SHAP", "optuna"]
  },
  {
    id: 6, weeks: "Sem 13–14", title: "API + Dashboard MVP", phase: "serving",
    goal: "Serving layer: API REST y dashboard geoespacial MVP",
    deliverables: ["FastAPI endpoints", "React dashboard MVP", "Deck.gl NDVI maps", "UAT con operadores", "Documentación API"],
    tech: ["FastAPI", "React", "Deck.gl", "Docker", "PostgreSQL"]
  },
  {
    id: 7, weeks: "Sem 15–16", title: "MLOps + Producción", phase: "mlops",
    goal: "Hardening, monitoreo de modelos y despliegue en producción",
    deliverables: ["Model drift monitoring", "Retraining pipelines", "Kubernetes prod deploy", "Prometheus/Grafana", "Load testing", "Security audit"],
    tech: ["Prometheus", "Grafana", "Kubernetes", "Locust", "Evidently AI"]
  }
];
```

Phase colors:
- discovery: amber (#FAC775 bg, #633806 text)
- dataeng: blue (#B5D4F4 bg, #0C447C text)
- ml: purple (#CECBF6 bg, #3C3489 text)
- serving: coral (#F5C4B3 bg, #712B13 text)
- mlops: teal (#9FE1CB bg, #085041 text)

The HTML widget will have:
- A row of 8 sprint pills/cards (compact)
- Click = shows details in a panel below
- Currently selected sprint highlighted

Let me design the sprint widget:

```html
<style>
.sprint-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 16px; }
.sprint-card { 
  padding: 10px 8px; 
  border-radius: var(--border-radius-md); 
  border: 0.5px solid var(--color-border-tertiary);
  cursor: pointer;
  transition: border-color 0.15s;
}
.sprint-card.active { border-width: 1.5px; border-color: var(--active-color, #333); }
.sprint-card:hover { border-color: var(--color-border-secondary); }
.sprint-num { font-size: 10px; color: var(--color-text-tertiary); margin-bottom: 2px; }
.sprint-title { font-size: 12px; font-weight: 500; color: var(--color-text-primary); }
.sprint-weeks { font-size: 10px; color: var(--color-text-secondary); }
.phase-badge { ... }
.detail-panel { ... }
</style>
```

Actually, let me make this more visually rich. Each sprint card shows:
- Sprint number + weeks
- Title
- Phase badge (color coded)

Clicking shows:
- Sprint goal
- Deliverables list
- Tech icons/tags

Let me write the full HTML for the sprint roadmap widget. I'll use CSS variables for theming and keep it clean.

Let me think about the layout more carefully. 8 sprints in a 4x2 grid. Each card about 150px wide. Total: 4 * 150 + 3 * 8 = 624px < 680px ✓.

With `grid-template-columns: repeat(4, 1fr)` and gap=8px: each cell ≈ (680-3*8)/4 = 656/4 = 164px. With ~12px internal padding, content area ≈ 140px.

Sprint card height: ~70-80px (number+title+weeks+badge).

Detail panel: 200-250px tall showing selected sprint's info.

Total widget height: ~80*2 + 16 (gap) + 8 + 250 = ~522px.

Let me write the HTML now:

```html
<h2 class="sr-only">Sprint roadmap — AgroUAV Platform, 16 semanas</h2>

<div style="font-size:13px;color:var(--color-text-secondary);margin-bottom:12px">
  Haz clic en cualquier sprint para ver detalles · 16 semanas · 8 sprints de 2 semanas
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px" id="sprint-grid">
</div>

<div id="detail" style="background:var(--color-background-secondary);border-radius:var(--border-radius-lg);padding:16px;min-height:180px">
  <p style="color:var(--color-text-tertiary);font-size:13px;text-align:center;margin:60px 0">← Selecciona un sprint para ver el detalle</p>
</div>

<script>
const phases = {
  discovery: { label: 'Discovery', bg: '#FAC775', text: '#633806', border: '#BA7517' },
  dataeng:   { label: 'Data Engineering', bg: '#B5D4F4', text: '#0C447C', border: '#185FA5' },
  ml:        { label: 'ML Platform', bg: '#CECBF6', text: '#3C3489', border: '#534AB7' },
  serving:   { label: 'Serving', bg: '#F5C4B3', text: '#712B13', border: '#993C1D' },
  mlops:     { label: 'MLOps + Prod', bg: '#9FE1CB', text: '#085041', border: '#0F6E56' },
};

const sprints = [
  { id:0, weeks:'Sem 1–2', title:'Discovery', phase:'discovery',
    goal:'Validar fuentes de datos, cerrar arquitectura y definir estándares de metadatos.',
    deliverables:['Problem statement + árbol de problemas validado','Data inventory (DJI, IDEAM, PIX4D, IGAC)','Architecture Decision Record (ADR)','Stack tecnológico cerrado y justificado'],
    tech:['Python','Jupyter','Miro','Git','Draw.io'] },
  { id:1, weeks:'Sem 3–4', title:'Conectores de fuentes', phase:'dataeng',
    goal:'POC funcional de extracción de logs DJI, datos climáticos IDEAM y mapas PIX4D.',
    deliverables:['DJI log parser en Python','IDEAM REST API connector','PIX4D export pipeline','Schema inicial del Data Lake definido'],
    tech:['Python','pandas','requests','DJI SDK','Parquet'] },
  { id:2, weeks:'Sem 5–6', title:'Infraestructura base', phase:'dataeng',
    goal:'Data Lake, orquestación, streaming y CI/CD en funcionamiento.',
    deliverables:['S3/GCS bucket structure + IAM','Airflow en Kubernetes','Kafka cluster configurado','GitHub Actions CI/CD','Terraform IaC'],
    tech:['Terraform','Kubernetes','Airflow','Kafka','AWS/GCP'] },
  { id:3, weeks:'Sem 7–8', title:'Pipelines & modelado', phase:'dataeng',
    goal:'Pipelines Raw → Silver operativos con calidad de datos y catálogo de metadatos.',
    deliverables:['DAGs de ingesta Airflow','Modelos dbt Silver','Great Expectations suite','Catálogo de datos (DataHub/Amundsen)'],
    tech:['dbt','Apache Spark','PySpark','Great Expectations','DataHub'] },
  { id:4, weeks:'Sem 9–10', title:'Feature engineering', phase:'ml',
    goal:'Zona Gold del Data Lake y Feature Store con variables temporales de clima y UAV.',
    deliverables:['Gold layer con series temporales','Feast Feature Store operativo','NDVI baseline features','Climate lag/rolling features','Feature documentation'],
    tech:['Feast','dbt','PySpark','numpy','pandas'] },
  { id:5, weeks:'Sem 11–12', title:'Modelos ML v1', phase:'ml',
    goal:'Primer ciclo de entrenamiento: detección de anomalías NDVI y optimizador de vuelo.',
    deliverables:['Anomaly detection model (NDVI)','Flight param optimizer v1','MLflow experiment tracking','Model Registry v1','Notebooks EDA + SHAP'],
    tech:['scikit-learn','PyTorch','MLflow','SHAP','Optuna'] },
  { id:6, weeks:'Sem 13–14', title:'API + Dashboard MVP', phase:'serving',
    goal:'Capa de serving: API REST y dashboard geoespacial para operadores de drones.',
    deliverables:['FastAPI endpoints + Swagger','React dashboard MVP','Deck.gl NDVI maps','UAT con operadores','Documentación OpenAPI'],
    tech:['FastAPI','React','Deck.gl','Docker','PostgreSQL'] },
  { id:7, weeks:'Sem 15–16', title:'MLOps + Producción', phase:'mlops',
    goal:'Hardening, monitoreo de modelos, despliegue en producción y seguridad.',
    deliverables:['Model drift monitoring (Evidently)','Retraining pipelines automáticos','Kubernetes prod deploy','Prometheus + Grafana','Load testing + security audit'],
    tech:['Prometheus','Grafana','Kubernetes','Locust','Evidently AI'] },
];

let selected = null;
const grid = document.getElementById('sprint-grid');
const detail = document.getElementById('detail');

function render() {
  grid.innerHTML = sprints.map(s => {
    const p = phases[s.phase];
    const isSelected = selected === s.id;
    return `<div 
      class="sprint-card" 
      data-id="${s.id}"
      style="
        background:${p.bg}22;
        border-radius:var(--border-radius-md);
        border:${isSelected ? '1.5px' : '0.5px'} solid ${isSelected ? p.border : 'var(--color-border-tertiary)'};
        padding:10px 10px;
        cursor:pointer;
        transition:border-color 0.15s, transform 0.1s;
      "
    >
      <div style="font-size:10px;color:var(--color-text-tertiary);margin-bottom:4px">Sprint ${s.id} · ${s.weeks}</div>
      <div style="font-size:13px;font-weight:500;color:var(--color-text-primary);margin-bottom:6px">${s.title}</div>
      <span style="
        display:inline-block;
        font-size:10px;
        background:${p.bg};
        color:${p.text};
        border-radius:4px;
        padding:2px 6px;
      ">${p.label}</span>
    </div>`;
  }).join('');

  document.querySelectorAll('.sprint-card').forEach(card => {
    card.addEventListener('click', () => {
      selected = +card.dataset.id;
      render();
      renderDetail();
    });
  });
}

function renderDetail() {
  if (selected === null) return;
  const s = sprints[selected];
  const p = phases[s.phase];
  detail.innerHTML = `
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
      <span style="background:${p.bg};color:${p.text};border-radius:4px;padding:3px 8px;font-size:11px;font-weight:500">${p.label}</span>
      <span style="font-size:18px;font-weight:500;color:var(--color-text-primary)">Sprint ${s.id} — ${s.title}</span>
      <span style="color:var(--color-text-tertiary);font-size:12px">${s.weeks}</span>
    </div>
    <p style="font-size:13px;color:var(--color-text-secondary);margin-bottom:14px;line-height:1.5">${s.goal}</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div>
        <div style="font-size:11px;font-weight:500;color:var(--color-text-tertiary);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px">Entregables</div>
        ${s.deliverables.map(d => `<div style="font-size:12px;color:var(--color-text-primary);margin-bottom:5px;padding-left:10px;border-left:2px solid ${p.border}">${d}</div>`).join('')}
      </div>
      <div>
        <div style="font-size:11px;font-weight:500;color:var(--color-text-tertiary);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px">Stack</div>
        <div style="display:flex;flex-wrap:wrap;gap:5px">
          ${s.tech.map(t => `<span style="background:var(--color-background-tertiary);border:0.5px solid var(--color-border-tertiary);border-radius:4px;padding:3px 7px;font-size:11px;color:var(--color-text-secondary)">${t}</span>`).join('')}
        </div>
        <button 
          onclick="sendPrompt('Detalla el Sprint ${s.id} (${s.title}) con épicas, user stories, criterios de aceptación y Definition of Done para la plataforma AgroUAV.')"
          style="margin-top:14px;font-size:12px;padding:6px 12px;cursor:pointer;border-radius:var(--border-radius-md)"
        >Ver user stories ↗</button>
      </div>
    </div>
  `;
}

render();
</script>
```

Wait, I need to avoid `letter-spacing` and `text-transform: uppercase` since those are not in the spec... actually those are CSS properties for text, not prohibited. Let me keep them for section labels.

Also, I used `${p.bg}22` for background which is a hex color with 22 alpha. This should work in modern browsers.

One issue: `0.5px solid ${isSelected ? p.border : 'var(--color-border-tertiary)'}` - I'm mixing template literals with CSS. This should be fine.

Another issue: the `class="sprint-card"` in the innerHTML - I can use this in querySelectorAll later. ✓

Also: I need to not use form elements. The button I have uses `onclick="sendPrompt(...)"` which is an inline handler. This should be fine.

Let me also check: the spec says "Never use localStorage, sessionStorage". I'm not using those. ✓

Also: "No tabs, carousels, or display: none sections during streaming - hidden content streams invisibly." The detail panel initially shows a placeholder text (not hidden). When a sprint is clicked, it updates the innerHTML. Since scripts execute after streaming, this is fine. ✓

One more thing: "No DOCTYPE, <html>, <head>, or <body>". My HTML starts with `<h2 class="sr-only">`. ✓

The button in the detail panel uses `sendPrompt()`. ✓

Let me also check: "Buttons: pre-styled with transparent bg, 0.5px border-secondary, hover bg-secondary, active scale(0.98). If it triggers sendPrompt, append a ↗ arrow." My button already has "Ver user stories ↗". ✓

The background color `${p.bg}22` adds transparency. In dark mode, this might look different. Let me instead use `color-mix(in srgb, ${p.bg} 15%, transparent)` or just accept the hardcoded color. Since the sprint cards use hardcoded colors that don't adapt to dark mode, this is a potential issue. 

Actually, looking at the illustrative diagram example, it uses hardcoded colors for physical-color scenes. For UI elements (like the sprint cards), I should use CSS variables. But the phase colors are custom and I need them to be specific. 

The spec says: "Physical-color scenes: Use ALL hardcoded hex — never mix with c-* theme classes." But for UI elements, it says to use CSS variables.

The phase badges with hardcoded colors won't adapt to dark mode. This is a trade-off. Let me:
1. For the badge background: use the hardcoded hex (it's a design choice for phase identification)
2. For the card border and text: use CSS variables where possible

The cards will have `background: ${p.bg}22` which is a very light tint. In dark mode, this light tint on a dark background might be barely visible. That's acceptable for now.

Alternatively, I could use CSS variables for the card backgrounds and just hardcode the badge colors. Let me do:
- Card background: `var(--color-background-primary)` with hardcoded left border
- Badge: hardcoded colors

```
background: var(--color-background-secondary);
border-left: 3px solid ${p.border};
```

This would work well in both light and dark mode. Let me use this approach.

Actually, looking at the sprint roadmap, the most important visual differentiation is the phase color. Let me keep:
- Card: white/secondary bg with colored left accent border
- Badge: hardcoded color for phase label
- Selected: colored border all around

This is the clearest design.

Let me update the sprint card rendering:

```javascript
return `<div 
  data-id="${s.id}"
  style="
    background:var(--color-background-primary);
    border-radius:var(--border-radius-md);
    border:${isSelected ? '1.5px' : '0.5px'} solid ${isSelected ? p.border : 'var(--color-border-tertiary)'};
    border-left:3px solid ${p.border};
    padding:10px 10px;
    cursor:pointer;
    position:relative;
  "
>
```

Hmm, I can't use `border` and `border-left` together in inline styles reliably (border-left would override). Let me use a wrapper approach or just use all-around border with a different card design.

Actually: I can set `border: ... solid ...; border-left-width: 3px;` to get thick left border. Or I can use `outline` for the selected state and keep just the left border.

Or more simply: for non-selected cards, just left border. For selected, all-around colored border.

Let me use:
```javascript
border: isSelected 
  ? `2px solid ${p.border}` 
  : `0.5px solid var(--color-border-tertiary)`,
borderLeft: `3px solid ${p.border}`,
```

In inline style objects (as part of a style string), I can do:
`style="border: 0.5px solid var(--color-border-tertiary); border-left: 3px solid ${p.border}"`

This should work. The border-left shorthand overrides only the left side of the border shorthand.

Actually in CSS, `border-left` is a shorthand that sets border-left-width, border-left-style, and border-left-color. Writing:
```css
border: 0.5px solid var(--color-border-tertiary);
border-left: 3px solid #BA7517;
```
The second declaration overrides the left border from the first. This is valid CSS. ✓

For selected state, I'll change the all-around border to colored:
For non-selected: `border: 0.5px solid var(--color-border-tertiary); border-left: 3px solid ${p.border}`
For selected: `border: 2px solid ${p.border}`

Let me implement this. Actually I realize this is getting complex for the card rendering in template literals. Let me simplify:

```javascript
const borderStyle = isSelected
  ? `border:1.5px solid ${p.border}`
  : `border:0.5px solid var(--color-border-tertiary);border-left:3px solid ${p.border}`;
```

OK. Let me now write the actual final HTML. I'll keep it concise and functional.

Also, I realize I should check: does the sprint roadmap title "Sprint ${s.id}" contain any XSS risk? Since I'm constructing this from hardcoded data in JavaScript (not user input), there's no XSS risk. ✓

Let me also think about the overall page height. The sprint grid (4x2 = 8 cards, each ~80px tall) + gap(16px) + detail panel (~250px) = 80*2+16+16+250 = 522px. Plus the header text (~30px) = ~552px. That's a reasonable widget height.

Let me write the HTML:

```html
<h2 class="sr-only">Sprint roadmap — AgroUAV Platform, 16 semanas, 8 sprints</h2>

<div style="font-size:13px;color:var(--color-text-secondary);margin:0 0 12px">
  16 semanas · 8 sprints · haz clic en un sprint para ver el detalle
</div>

<!-- Legend -->
<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px">
  <span style="font-size:11px;color:var(--color-text-tertiary)">Fases:</span>
  <!-- legend items -->
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px" id="sg"></div>

<div id="dp" style="background:var(--color-background-secondary);border-radius:var(--border-radius-lg);padding:16px;min-height:200px">
  <p style="text-align:center;color:var(--color-text-tertiary);font-size:13px;margin:60px 0">Selecciona un sprint ↑</p>
</div>

<script>
// ... sprint data and render logic
</script>
```

OK. Let me now write everything together. I'll write the complete response now.

---

Let me also think about the technology stack presentation. Rather than a table (which I should put in markdown, not the tool), I'll describe it in prose with key technologies:

**Data Infrastructure**: AWS S3 (or GCS) + Delta Lake/Iceberg for the Data Lake; Apache Kafka for streaming; Apache Airflow (on Kubernetes) for orchestration; Terraform for IaC.

**Data Transformation**: Apache Spark (PySpark) for batch processing; dbt (data build tool) for Silver-layer transformations; Great Expectations for data quality; DataHub for the metadata catalog.

**ML Platform**: Feast as the Feature Store; scikit-learn and PyTorch for model training; MLflow for experiment tracking and model registry; Optuna for hyperparameter optimization; SHAP for explainability.

**Serving Layer**: FastAPI for the REST API; React + Deck.gl for the geospatial dashboard; PostgreSQL for operational metadata; Docker + Kubernetes for deployment.

**MLOps & Observability**: Prometheus + Grafana for infrastructure monitoring; Evidently AI for model drift detection; Locust for load testing; GitHub Actions for CI/CD.

**Programming Languages**: Python (primary), SQL (dbt models), TypeScript/JavaScript (dashboard).

---

Now, let me think about the three key epics (user stories at a high level):

**Epic 1: Data Lineage Foundation**
- As an operator, I want all past mission configurations stored and retrievable, so I can compare current missions with historical performance.
- As a data engineer, I want a schema that unifies climate variables with UAV telemetry, so ML models have consistent features.

**Epic 2: ML-Powered Mission Intelligence**
- As an agronomist, I want anomaly alerts for unusual NDVI patterns compared to historical baseline, so I can investigate potential crop issues early.
- As an operator, I want recommended flight parameters based on current weather and historical mission performance for similar terrain.

**Epic 3: Agronomic Knowledge Accumulation**
- As a farm manager, I want a dashboard showing the historical NDVI evolution of each field alongside climate events, so I can track crop health trends.
- As a data scientist, I want an automated retraining pipeline that triggers when new mission data becomes available, so models stay current.

---

OK. Now I'm truly writing the full response. Here goes.

The response will be:

**Section 1 (text)**: Problem synthesis + immediate reading of the document
**Section 2 (text)**: Methodology choice
**Section 3 (SVG)**: Architecture diagram
**Section 4 (text)**: Architecture explanation
**Section 5 (HTML)**: Sprint roadmap
**Section 6 (text)**: Tech stack + epics + next steps

Let me now write this. I'll be concise but thorough.

Actually, one thing I want to add to the architecture diagram: I should also show the cross-cutting concerns (observability, orchestration). Let me add a small side note in the SVG or mention it in text.

I'll mention it in text:

"Two cross-cutting concerns span all layers: (1) **Orchestration** (Apache Airflow manages the DAG lifecycle across ingestion, transformation, and retraining pipelines) and (2) **Observability** (Prometheus/Grafana for infra metrics, Great Expectations for data quality, Evidently AI for ML drift detection). These are not shown as separate layers in the diagram but run vertically across all of them."

OK. Let me write it all now. I promise this is the last time I'm planning. Let me just write.

---

Here's my full response structure:

---

El documento plantea con precisión una problemática crítica de **Data Lineage** en un contexto AgroTech UAV. Antes de iniciar el diseño, permíteme sintetizarlo en sus tres dimensiones esenciales:

**Problema central**: Los operadores de UAVs agrícolas en Colombia no tienen una arquitectura de datos que persista el conocimiento histórico de cada misión. Cada vuelo parte desde cero — sin correlacionar variables exógenas (clima IDEAM) con variables de control (configuración del dron) ni con los resultados previos (índices NDVI, rendimiento del cultivo).

**Causa raíz técnica**: Silos propietarios (DJI SmartFarm, PIX4D, DJI Terra) no tienen integración nativa entre sí ni hacia un Data Lake externo. No existen pipelines de ingestión retrospectiva ni estándares de metadatos de misión.

**Consecuencia científica**: Sin features (variables predictoras) ni labels (resultados históricos etiquetados), es matemáticamente imposible entrenar modelos supervisados para detección de anomalías NDVI u optimización de parámetros de vuelo.

---

**Metodología seleccionada**: Dado que el problema involucra tanto descubrimiento de dominio (entender los microclimas colombianos, los flujos de trabajo de los operadores de drones, las APIs del IDEAM) como construcción de software complejo, la combinación óptima es:

1. **Design Thinking** para las semanas 1–2: empatizar con operadores y agrónomos, definir el árbol de problemas con más detalle, prototipar conceptos de interfaz antes de construir.
2. **Scrum** (sprints de 2 semanas) para las semanas 3–16: construcción iterativa e incremental con entregas funcionales al final de cada sprint.
3. **MLOps como disciplina transversal**: desde el Sprint 4 en adelante, todo código de ML vive en pipelines reproducibles con versionado automático.

---

Aquí está la arquitectura de datos propuesta de 5 capas:

[SVG DIAGRAM]

---

**Explicación de las capas:**

La **capa de fuentes** concentra cuatro dominios de datos: (1) telemetría y logs de vuelo de DJI (SmartFarm y Terra), (2) mapas NDVI/RGB de PIX4D, (3) series climáticas históricas del IDEAM (temperatura, precipitación, humedad, velocidad del viento) y (4) datos de suelos y edafología del IGAC/FAO.

La **capa de ingesta** usa Apache Kafka para eventos en tiempo real (telemetría de vuelo activo) y Apache Airflow para DAGs batch (extracción periódica de IDEAM, importación de proyectos PIX4D completados). Los extractores custom implementan los SDKs propietarios de DJI y PIX4D para superar el silo propietario.

El **Data Lake** sigue la arquitectura medallion: zona Raw (datos como llegan, sin transformar), zona Silver (datos limpios, jointeados con metadatos de misión estandarizados) y zona Gold (features engineering completo: lag features climáticos, rolling NDVI, series temporales etiquetadas).

La **plataforma ML** comprende el Feature Store (Feast, para servir features consistentes entre entrenamiento y predicción), el entorno de training (MLflow tracking + scikit-learn/PyTorch) y el Model Registry (versionado automático de modelos productivos).

La **capa de serving** expone dos puntos de consumo: una API REST (FastAPI) que los sistemas de misión pueden consultar para obtener configuraciones recomendadas de vuelo, y un dashboard geoespacial (React + Deck.gl) para análisis visual de NDVI histórico y comparación de misiones.

---

[SPRINT ROADMAP]

---

**Stack tecnológico consolidado**: Python como lenguaje principal; AWS S3 o GCS como object storage; Delta Lake/Apache Iceberg como formato de tabla transaccional sobre el Data Lake; Apache Airflow 2.x en Kubernetes como orquestador; Apache Kafka para streaming; dbt para modelado SQL de la zona Silver; Apache Spark/PySpark para transformaciones batch; Feast como Feature Store; MLflow para tracking y registry; FastAPI para la API REST; React + Deck.gl para el dashboard geoespacial; PostgreSQL como base operacional; Terraform para IaC; GitHub Actions para CI/CD; Prometheus + Grafana para observabilidad; Evidently AI para monitoreo de drift en modelos.

**Tres epics principales** para el backlog inicial:
1. **Data Lineage Foundation**: construir la infraestructura que garantice que cada misión UAV quede completamente trazada (parámetros de vuelo + condiciones climáticas + resultado NDVI + metadatos de campo).
2. **ML-Powered Mission Intelligence**: modelos de detección de anomalías NDVI contra baseline histórico y optimizador de parámetros de vuelo basado en condiciones similares pasadas.
3. **Agronomic Knowledge Accumulation**: dashboard y API que transformen el Data Lake en valor operativo para agrónomos y operadores.

**Próximos pasos inmediatos** (antes del Sprint 0):
1. Inventario de fuentes: solicitar acceso a las APIs del IDEAM y documentar el formato de exportación de proyectos DJI SmartFarm y PIX4D de al menos 3 misiones reales.
2. Definir el schema de metadatos de misión: qué variables de contexto debe registrar cada vuelo (hora, coordenadas, cultivo, operador, condiciones climáticas al momento del vuelo, configuración del sensor).
3. Seleccionar el cloud provider (AWS vs GCP) basado en disponibilidad en la región SA-East-1 o similar para Colombia.
4. Organizar una sesión de Design Thinking con al menos un operador de drones y un agrónomo para validar los casos de uso antes de construir.

---

OK that's the plan. Let me write it now in the actual response, clean and organized. I'll call show_widget twice (once for SVG, once for HTML). Let me write the actual code carefully.

I realize I've been spending too much time planning. Let me just write the code now, being careful with the most important parts (coordinates, text overflow). I'll write concisely.Con base en el documento, puedo sintetizar el problema en tres dimensiones antes de proponer la solución:

**Problema central**: Los UAVs agrícolas en Colombia operan con un *cold-start permanente*. Cada misión parte desde cero porque no existe una arquitectura que correlacione variables exógenas (clima IDEAM, edafología) con variables de control (configuración del dron) y los resultados históricos (NDVI, rendimiento de cultivo).

**Causa raíz técnica**: Los ecosistemas propietarios (DJI SmartFarm, PIX4D, DJI Terra) son silos cerrados sin integración hacia un Data Lake externo. Ausencia de pipelines de ingestión retrospectiva y de estándares de metadatos de misión.

**Consecuencia científica**: Sin *features* ni *labels* históricos, es matemáticamente imposible entrenar modelos supervisados para detección de anomalías NDVI u optimización de parámetros de vuelo.

**Metodología seleccionada**: Design Thinking (semanas 1–2) para empatizar con operadores y agrónomos y cerrar el problem statement. Luego **Scrum con sprints de 2 semanas** (semanas 3–16) para construcción iterativa. MLOps como disciplina transversal desde el Sprint 4.

Aquí está la arquitectura de datos propuesta en 5 capas. Haz clic en cualquier componente para profundizar:
```
This block is not supported on your current device yet.
```



