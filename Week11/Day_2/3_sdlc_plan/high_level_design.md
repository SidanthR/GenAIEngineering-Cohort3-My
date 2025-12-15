# Expense Tracking Application - High Level Design Document

---

## Table of Contents

1. System Components and Interaction Diagram  
2. Database Schema Design  
3. Data Flow Diagrams for Key User Journeys  
4. Caching Strategy and Session Management  
5. External Service Integrations  
6. Error Handling and Logging Strategies  
7. Background Job Processing Design  
8. File Storage and Media Handling Approach  
9. Performance Optimization Strategies  

---

## 1. System Components and Interaction Diagram

The Expense Tracking system is composed of multiple interacting components working together to provide a scalable, secure, and performant solution:

- **Streamlit Frontend**: A Python-based SPA that enables expense entry, reporting, and offline support. Supports local caching and sync queue for offline usage.
- **API Gateway (NGINX + FastAPI Auth Service)**: Handles TLS termination, request routing, authentication (OAuth 2.0, JWT), and rate limiting.
- **Microservices**:
  - **Auth Service**: Manages user registration, login, JWT token issuance, and validation.
  - **Expense Microservice**: Handles CRUD operations on expenses and categories with validation.
  - **Reporting Microservice**: Provides aggregated reports, chart generation, and export features.
  - **Sync Microservice**: Manages near real-time WebSocket synchronization, conflict detection, and resolution.
  - **Notification Service**: Sends budget alerts, reminders via email, SMS, or push notifications asynchronously.
- **PostgreSQL Database**: Central persistence for users, expenses, categories, audit logs, sync metadata, and conflict data.
- **External Services**:
  - OAuth 2.0 Providers (Google, Facebook) for social login.
  - SMTP, SMS, and Push notification APIs (e.g., Twilio, Firebase).

### Component Interaction Diagram

```
+-------------------+            +-----------------------+           +-------------------+
|                   |    HTTPS   |                       |           |                   |
|  Streamlit Frontend +---------->+      API Gateway      +<----------+ External Services  |
| (with offline cache)|           |  (NGINX + FastAPI)    |           | - OAuth Providers  |
|                   |            |                       |           | - Notification APIs|
+-------------------+            +-----------+-----------+           +-------------------+
                                           |
                  +------------------------+-----------------------+
                  |                        |                       |
          +-------+-------+        +-------+-------+       +-------+-------+
          | Auth Service  |        | Expense MS    |       | Reporting MS  |
          +---------------+        +---------------+       +---------------+
                  |                        |                       |
                  +-----------+------------+-----------+-----------+
                              |                        |
                    +---------+---------+      +-------+-------+
                    |   Sync Microservice|      | Notification  |
                    +--------------------+      +---------------+
                               |                          |
                          +----+----+               +-----+-----+
                          |Database  |               |External   |
                          |PostgreSQL|               |Notification|
                          +---------+                |Systems     |
                                                     +-----------+

WebSocket connection enabled between Frontend and Sync Microservice for real-time sync.
```

---

## 2. Database Schema Design

The system database uses PostgreSQL with the following core tables and relationships:

### Core Tables:

- **users**  
  - `id UUID PRIMARY KEY`  
  - `email VARCHAR UNIQUE`  
  - `hashed_password TEXT`  
  - `created_at TIMESTAMPTZ`  
  - `updated_at TIMESTAMPTZ`  

- **categories**  
  - `id UUID PRIMARY KEY`  
  - `user_id UUID FOREIGN KEY REFERENCES users(id)`  
  - `name VARCHAR`  
  - `created_at TIMESTAMPTZ`  
  - `updated_at TIMESTAMPTZ`  

- **expenses**  
  - `id UUID PRIMARY KEY`  
  - `user_id UUID FOREIGN KEY REFERENCES users(id)`  
  - `category_id UUID FOREIGN KEY REFERENCES categories(id)`  
  - `amount_cents BIGINT`  
  - `currency CHAR(3)`  
  - `description VARCHAR(255)`  
  - `expense_date DATE`  
  - `deleted BOOLEAN DEFAULT FALSE` (Soft delete)  
  - `created_at TIMESTAMPTZ`  
  - `updated_at TIMESTAMPTZ`  

- **sync_metadata**  
  - `user_id UUID`  
  - `device_id VARCHAR`  
  - `last_synced_at TIMESTAMPTZ`  
  - Composite primary key on (user_id, device_id)

- **conflict_resolution**  
  - Conflict records for sync conflict handling between devices.

- **audit_logs**  
  - Immutable logs capturing user actions with timestamps for compliance.

### Relationships:

- Users → Categories: One-to-Many  
- Users → Expenses: One-to-Many  
- Categories → Expenses: One-to-Many  
- Users → SyncMetadata: One-to-Many (per device)  
- Auditing relates to User and Expense entities  

### Additional Schema Features:

- UUIDs generated with `gen_random_uuid()` for offline uniqueness support.  
- Indexes on user_id, date, category_id for optimized queries.  
- Encryption-at-rest enabled via PostgreSQL native TDE or `pgcrypto`.  
- Soft deletes allow GDPR-compliant data management.  

---

## 3. Data Flow Diagrams for Key User Journeys

### 3.1 User Login and Session Establishment

```
[Frontend] --(email/password/OAuth)--> [API Gateway/Auth Service]  
     |                                         |  
     |<-- JWT Token ----------------------------|  
     |                                         |  
JWT stored securely in HttpOnly cookie/local storage  
```

### 3.2 Expense Entry (Online Sync)

```
[Frontend] -- (Add Expense) --> [Expense Microservice via API Gateway]  
     |                                |  
     |<-- Confirmation/Expense Data --|  
Expense saved in PostgreSQL database  
Sync Microservice notified of new data for real-time data push to other devices  
```

### 3.3 Offline Expense Entry and Sync

```
[Frontend] User adds expense while offline -> stored locally in frontend cache and sync queue  
On reconnect:  
[Frontend] -- WebSocket Sync --> [Sync Microservice] --> Updates Backend DB and resolves conflicts  
Sync status updated in SyncMetadata table  
```

### 3.4 Report Generation

```
[Frontend] User requests report export -->  
[Reporting Microservice] generates report asynchronously (CSV/XLSX) using Pandas/OpenPyXL -->  
Stores export file or generates download URL -->  
Frontend polls for job status/download link  
```

### 3.5 Notification Sending

```
[Backend Services] detect alert/reminder events -->  
[Notification Service] enqueues notification tasks -->  
Async delivery via SMTP/SMS/Push providers -->  
User receives notifications  
```

---

## 4. Caching Strategy and Session Management

- **Caching**:  
  - Redis cache deployment is planned for caching frequently accessed data such as category lists and expense summaries to reduce DB hits and latency.  
  - Expensive queries and report generation metadata can leverage cache with TTLs.  
- **Session Management**:  
  - JWT tokens are issued by Auth Service and stored securely as HttpOnly cookies on clients to mitigate XSS risks.  
  - Tokens carry expiration claims and short TTLs; refresh tokens are used to renew sessions.  
  - Rate limiting enforced per user/IP at API Gateway to prevent abuse.

---

## 5. External Service Integrations

- **OAuth 2.0 Providers**:  
  - Integrated via the Auth Service supporting Google, Facebook logins via standard OAuth flows.
- **Notification Providers**:  
  - Notification Service integrates asynchronously with third-party APIs like Twilio (SMS), Firebase (Push), SMTP servers (Email).  
  - Retries and error handling implemented for delivery failures.  
- **Real-time Sync**:  
  - Uses WebSocket protocol managed by Sync Microservice for multi-device near real-time data synchronization.  

---

## 6. Error Handling and Logging Strategies

- **Error Handling**:  
  - All microservices use consistent structured error responses with error codes, messages, and trace IDs for request tracking.  
  - Validation errors return 400 with clear messages.  
  - Authentication failures return 401 Unauthorized.  
  - Resource not found returns 404.  
  - Rate limit exceeded returns 429 with Retry-After headers.  
- **Logging**:  
  - Centralized logging via ELK stack aggregates logs from API Gateway and microservices.  
  - Logs include request metadata, error stacks, response times, and trace IDs for correlation.  
  - Audit logs stored immutably in PostgreSQL for compliance and traceability.  
  - Prometheus metrics scraping for health and performance monitoring.  

---

## 7. Background Job Processing Design

- **Task Queue**:  
  - Celery integrated for asynchronous processing of long running jobs such as notification sending and report export generation.  
  - Redis used as broker and result backend.  
- **Job Lifecycle**:  
  - Jobs enqueued via microservices API, processed by workers.  
  - Job status persisted and queryable via reporting export endpoints.  
  - Failure retries implemented with exponential backoff.  

---

## 8. File Storage and Media Handling Approach

- **Report Export Files**:  
  - Generated CSV/XLSX files stored on a shared file storage or object storage (e.g., AWS S3 or equivalent) accessible to API services.  
  - Temporary URLs served for secure download with expiry.  
- **Media Handling**:  
  - No direct media uploads planned currently; system designed for extensibility to add this if needed.  
- **Backup and Retention**:  
  - Storage includes automated retention policies and backups aligned with compliance needs.

---

## 9. Performance Optimization Strategies

- **Scalability**:  
  - Microservices horizontally scalable via container orchestration (Kubernetes/Docker Swarm).  
  - Read replicas for PostgreSQL relieve primary DB load for reporting queries.  
- **Caching**:  
  - Use Redis caching layer for frequently accessed data to reduce DB queries.  
- **Asynchronous Processing**:  
  - Offload slow/blocking tasks (notifications, exports) to background job queues to keep APIs responsive.  
- **WebSocket Sync**:  
  - Real-time sync reduces polling and redundant data fetching, lowering server and network load.  
- **API Gateway Rate Limiting**:  
  - Protect backend microservices from abuse and overload, ensuring fair usage.  
- **Database Indexing**:  
  - Strategic indexes on user_id, date, category_id speed up filtering and sorting on large datasets.  
- **Frontend Offline Support**:  
  - Minimizes server load during intermittent connectivity by enabling local cache and queued sync.

---

# End of High Level Design Document