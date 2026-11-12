# Streamy Backend Dynamic Behavioral Modeling
## System Architecture Interaction Streams

### 1. Architectural Core Mechanics
This tracking document details how application payloads pass between data layers before structural code layers are compiled. By designing how inputs move through software boundaries beforehand, we ensure development velocity remains high.

### 2. Media Playback Transaction Loop
The sequence model below outlines how the system validates viewer access permissions before initiating video file playback:

```mermaid
---
title: Streamy Playback Initialization Sequence Analysis
---
sequenceDiagram
    actor Viewer as 👤 Platform Viewer
    participant Auth as 🔒 Auth Token Validator
    participant Catalog as 🎬 Media Catalog Engine

    Viewer->>Auth: 1. Request Playback Route (stream_id, token)
    Auth->>Auth: 2. Check token expiration state
    alt token is expired / invalid
        Auth-->>Viewer: 3a. Return 401 Unauthorized Payload
    else token is active
        Auth->>Catalog: 3b. Request Streaming Meta-payload (stream_id)
        Catalog->>Catalog: 4. Fetch content encryption descriptors
        Catalog-->>Viewer: 5. Handshake OK (Return 200 OK + HLS Stream URL)
    end
```
### 3. Advanced Code Flow: User Registration
The following sequence diagram models the code-level interactions for a user registration request. It demonstrates loops for validation, alternative branches for conflict handling, and parallel execution blocks for asynchronous tasks like email notification and event publishing.

```mermaid
---
title: Streamy POST /users Registration
---
sequenceDiagram
    autonumber
    participant C as UserController
    participant S as CreateUserService
    participant R as UserRepository
    participant M as WelcomeEmailService
    participant E as EventPublisher

    C->>+S: create_user(email: String) : Result
    S->>R: find_by_email(email: String) : User[]
    R-->>S: existingUsers: User[]
    
    loop each existingUser
        S->>S: is_active(existingUser) : Boolean
    end
    
    alt active account exists
        S-->>C: conflict: RegistrationError
    else registration permitted
        S->>R: insert_user(email: String) : User
        R-->>S: newUser: User
        par welcome email
            S->>M: send_welcome_email(newUser) : Boolean
            M-->>S: emailAccepted: Boolean
        and creation event
            S->>E: publish_user_created(newUser) : Boolean
            E-->>S: eventAccepted: Boolean
        end
        S-->>C: newUser: User
    end
    deactivate S
```