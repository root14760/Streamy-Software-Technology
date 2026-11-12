# Streamy Core Domain Structural Architecture
## Advanced Object-Oriented System Entity Specifications
### 1. Complex System Relationships Analysis
This structural document acts as the definitive blueprint for the Streamy runtime
system. It establishes core hierarchies, lifecycle coupling, and cardinality rules,
dictating how object models must inherit attributes and clear space allocations out
of memory.
### 2. Comprehensive Production Class Diagram
The advanced structural design schematic below details all inheritance, composition,
and aggregation parameters for the Streamy domain engine:

```mermaid
---
title: Streamy Production Structural Domain Model
---
classDiagram
direction TB
%% Core Classes
class Title {
    <<abstract>>
    +String name
    +int releaseYear
    +playMedia() Boolean
}
class Film {
    +int lengthMinutes
}
class TVShow {
    +int seasonsCount
}
class Season {
    +int seasonNumber
}
class Episode {
    +String episodeTitle
    +int durationSeconds
}
class Review {
    +int ratingStars
    +String reviewText
}
class Actor {
    +String fullName
}
class Genre {
    +String genreName
}

%% Relationships and multiplicities
Title "0..*" -- "1..*" Genre: categorized_under
TVShow "1" *-- "0..*" Season: owns
Title "1" -- "0..*" Review: receives
Season "1" *-- "1..*" Episode: contains
Title "0..*" o-- "0..*" Actor: features

%% Inheritance
Film --|> Title : extends
TVShow --|> Title : extends
```
class Film {
    +int lengthMinutes
}
class TVShow {
    +int seasonsCount
}
class Sea
## 3. Relational Database Schema (ERD)
The following Entity Relationship Diagram specifies the relational database schema, mapping primary/foreign keys, cardinalities, and identifying vs non-identifying entity associations:

```mermaid
---
title: Streamy Entity Relationship Diagram
---
erDiagram
    TITLE {
        int title_id PK
        int type_id FK
        string name
        datetime release_date
    }
    TITLE_TYPE {
        int type_id PK
        string type
    }
    ACTOR {
        int actor_id PK
        string name
        date date_of_birth
    }
    TITLE_ACTOR {
        int title_id PK "FK"
        int actor_id PK "FK"
    }
    GENRE {
        int genre_id PK
        string name
    }
    TITLE_GENRE {
        int title_id PK "FK"
        int genre_id PK "FK"
    }
    EPISODE {
        int episode_id PK
        int season_id FK
        string name
        int season_number
        int episode_number
        datetime release_date
    }
    SEASON {
        int season_id PK
        int title_id FK
        int season_number
        date release_year
    }
    REVIEW {
        int review_id PK
        int title_id FK
        int episode_id FK
        int season_id FK
        string review_by
        datetime review_date
        string review_text
    }

    TITLE }|..|| TITLE_TYPE: has
    TITLE ||--o{ TITLE_GENRE: "belongs to"
    TITLE ||--|{ TITLE_ACTOR: features
    TITLE ||..|{ SEASON: contains
    TITLE_GENRE }o--|| GENRE: references
    TITLE_ACTOR }|--|| ACTOR: references
    EPISODE }|..|| SEASON: contains
    REVIEW }o..o| TITLE: "made against"
    REVIEW }o..o| EPISODE: "made against"
    REVIEW }o..o| SEASON: "made against"
```