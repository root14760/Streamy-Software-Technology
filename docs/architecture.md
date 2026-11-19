# Streamy System Architecture (C4 Container Model)

This document illustrates the container-level architecture of the **Streamy** video streaming platform, automatically compiled from Mermaid markup via GitHub Actions.

## C4 Container Diagram

```mermaid
C4Container
    title Container Diagram for Streamy Video Streaming Platform

    Person(viewer, "Viewer", "Watches movies and TV shows on Streamy")

    System_Boundary(streamy, "Streamy Platform") {
        Container(web_app, "Web & Mobile Client", "Vue.js / Mobile App", "Delivers video UI and initiates playback requests")
        Container(api_gateway, "API Gateway", "HTTPS / REST", "Routes client traffic and manages API endpoints")
        Container(auth_service, "Auth Service", "Python / JWT", "Validates access tokens and user authorization")
        Container(catalog_engine, "Media Catalog Engine", "Python", "Manages titles, seasons, episodes, and encryption descriptors")
        ContainerDb(database, "Streamy Database", "PostgreSQL", "Stores media metadata, user reviews, and actor records")
    }

    System_Ext(cdn, "HLS Streaming CDN", "Delivers encrypted adaptive video streams")

    Rel(viewer, web_app, "Browses & plays media", "HTTPS")
    Rel(web_app, api_gateway, "Sends API requests", "JSON/HTTPS")
    Rel(api_gateway, auth_service, "Verifies token", "Internal RPC")
    Rel(api_gateway, catalog_engine, "Fetches metadata & stream URL", "Internal RPC")
    Rel(catalog_engine, database, "Reads/writes domain entities", "SQL")
    Rel(web_app, cdn, "Streams HLS video", "HTTPS")
```