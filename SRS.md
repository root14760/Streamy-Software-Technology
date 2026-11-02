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
## 5. C4 Architecture Model: Container Diagram
The following C4 Container Diagram details the deployable system units, protocols, in-memory caches, and downstream supporting microservices.

```mermaid
---
title: Listing Service C4 Model Container Diagram
---
flowchart TD
    User["Premium Member<br>[Person]<br><br>A user of the website who has purchased a subscription"]
    WA["Web Application<br>[.NET Core MVC Application]<br><br>Allows members to view and review titles from a web browser. Also exposes an API for the mobile app"]
    MA["Mobile Application<br>[Xamarin Application]<br><br>Allows members to view and review titles from their mobile devices"]
    R[("In-Memory Cache<br>[Redis]<br><br>Titles and their reviews are cached")]
    K["Message Broker<br>[Kafka]<br><br>Important domain events are published to Kafka"]
    TS["Title Service<br>[Software System]<br><br>Provides an API to retrieve title information"]
    RS["Reviews Service<br>[Software System]<br><br>Provides an API to retrieve and submit reviews"]
    SS["Search Service<br>[Software System]<br><br>Provides an API to search for titles"]

    User -- "Views titles, searches titles and reviews titles using<br>[HTTPS]" --> WA
    User -- "Views titles, searches titles and reviews titles using<br>[HTTPS]" --> MA

    subgraph listing-service [Listing Service]
        MA -- "Makes API calls to<br>[HTTPS]" --> WA
        WA -- "Reads and writes to<br>[Redis Serialization Protocol]" --> R
    end

    WA -. "Publishes messages to<br>[Binary over TCP]" ..-> K
    WA -- "Makes API calls to<br>[HTTPS]" --> TS
    WA -- "Makes API calls to<br>[HTTPS]" ---> RS
    WA -- "Makes API calls to<br>[HTTPS]" ---> SS

    classDef container fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef person fill:#08427b,stroke:#052e56,color:#ffffff
    classDef supportingSystem fill:#666666,stroke:#0b4884,color:#ffffff

    class User person
    class WA,MA,R container
    class TS,RS,SS,K supportingSystem

    style listing-service fill:none,stroke:#CCC,stroke-width:2px,stroke-dasharray: 5 5
```
## 6. C4 Architecture Model: Component Diagram
The following C4 Component Diagram zooms into the Listing Service Web Application container to detail its internal controllers, business components, and external system dependencies.

```mermaid
---
title: Listing Service C4 Model Component Diagram
---
flowchart TD
    classDef container fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef externalSystem fill:#666666,stroke:#0b4884,color:#ffffff
    classDef component fill:#85bbf0,stroke:#5d82a8,color:#000000

    Browser["Browser<br>[Web Browser]<br><br>Used by a user to browse the website"]
    MA["Application<br>[Xamarin Application]<br><br>Allows members to view and review titles from their mobile devices"]
    R[("In-Memory Cache<br>[Redis]<br><br>Titles and their reviews are cached")]
    K["Message Broker<br>[Kafka]<br><br>Important domain events are published to Kafka"]
    TS["Title Service<br>[Software System]<br><br>Provides an API to retrieve title information"]
    RS["Review Service<br>[Software System]<br><br>Provides an API to retrieve and submit reviews"]
    SS["Search Service<br>[Software System]<br><br>Provides an API to search for titles"]

    subgraph listing-service [Listing Service Web Application]
        TCont["Title Controller<br>[ASP.NET MVC Controller]<br><br>Allows users to view details about titles"]
        SCont["Search Controller<br>[ASP.NET MVC Controller]<br><br>Allows users to search for titles"]
        RCont["Review Controller<br>[ASP.NET MVC Controller]<br><br>Allows users to read and write reviews"]
        TComp["Title Component<br>[ASP.NET Namespace]<br><br>Provides information on titles, retrieves info from Title Service and caches titles"]
        SComp["Search Component<br>[ASP.NET Namespace]<br><br>Searches titles using the Search Service"]
        RComp["Review Component<br>[ASP.NET Namespace]<br><br>Provides review info, submits new reviews and publishes domain events"]

        TCont ---> TComp
        RCont ---> TComp
        RCont ---> RComp
        SCont ---> SComp
    end

    Browser -- "Submits requests to<br>[HTTPS]" --> TCont
    Browser -- "Submits requests to<br>[HTTPS]" ---> SCont
    Browser -- "Submits requests to<br>[HTTPS]" ---> RCont
    MA -- "Submits requests to<br>[HTTPS]" ---> TCont
    MA -- "Submits requests to<br>[HTTPS]" ---> SCont
    MA -- "Submits requests to<br>[HTTPS]" ---> RCont

    TComp ---> TS
    TComp ---> R
    RComp ---> R
    RComp ---> K
    RComp ---> RS
    SComp ---> SS

    class MA,R container
    class SS,RS,TS,K,Browser externalSystem
    class RComp,SComp,TComp,RCont,SCont,TCont component

    style listing-service fill:none,stroke:#CCC,stroke-width:2px,stroke-dasharray: 5 5
```