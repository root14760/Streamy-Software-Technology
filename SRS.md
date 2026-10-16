# Software Requirements Specification (SRS)
## Project Baseline: Streamy Video Streaming Core Engine

### 1. Functional Requirements (FR)
The Streamy core processing layer must execute the following functional automation features:

* **FR-1:** The system must process an individual media catalog database searchable by categorical Genre taxonomies.
* **FR-2:** The system must handle multi-season episodic indexing structures for mapped TV Show entities.
* **FR-3:** The system must allow users to log numerical and text-based Review metrics against media elements.
* **FR-4:** The system must track viewer consumption metrics for metadata analytics extraction.
* **FR-5:** The system must support data serialization schemas for media item state inheritance.

### 2. Non-Functional Requirements (NFR)
The application architecture is constrained by the following systemic performance parameters:

* **NFR-1 (Runtime Environment):** The final functional system must compile exclusively inside a pure Python 3.x execution environment.
* **NFR-2 (Maintainability Paradigm):** All system design schematics, relationship maps, and entity models must render natively inline via plain-text syntax.
* **NFR-3 (Data Integrity):** The underlying database must enforce cascading deletion operations across nested entity constraints.

### 3. Functional System Boundary Diagram
The diagram below plots the structural use-case interactions crossing the Streamy application boundaries:

```mermaid
---
title: Streamy System Boundary & Functional Use Cases
---
flowchart LR
    ViewerActor(("External Actor: Platform Viewer"))

    subgraph ExternalApp [Client Application Interface]
        UI[Web Dashboard UI]
    end

    subgraph SystemPerimeter [Streamy Core System Perimeter]
        FR1[FR-1: Browse Catalog by Genre]
        FR2[FR-2: Initialize Media Streaming]
        FR3[FR-3: Log User Review Metrics]
    end

    ViewerActor --> UI
    UI -- Ingests Genre Metadata --> FR1
    UI -- Triggers Playback Route --> FR2
    UI -- Submits Rating Payload --> FR3
```
## 4. C4 Architecture Model: System Context
The following high-level C4 System Context diagram illustrates the core Listing Service and its interactions with external supporting microservices.

```mermaid
---
title: Listing Service C4 Model System Context
---
flowchart TD
    User["Premium Member<br>[Person]<br><br>A user of the website who has purchased a subscription"]
    LS["Listings Service<br>[Software System]<br><br>Serves web pages displaying title listings to the end user"]
    TS["Title Service<br>[Software System]<br><br>Provides an API to retrieve title information"]
    RS["Review Service<br>[Software System]<br><br>Provides an API to retrieve and submit reviews"]
    SS["Search Service<br>[Software System]<br><br>Provides an API to search for titles"]

    User -- "Views titles, searches titles and reviews titles using" --> LS
    LS -- "Retrieves title information from" --> TS
    LS -- "Retrieves from and submits reviews to" --> RS
    LS -- "Searches for titles using" --> SS

    classDef person fill:#08427b,stroke:#052e56,color:#ffffff
    classDef focusSystem fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef supportingSystem fill:#666666,stroke:#0b4884,color:#ffffff

    class User person
    class LS focusSystem
    class TS,RS,SS supportingSystem
```