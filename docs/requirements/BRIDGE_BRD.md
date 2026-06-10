# Business Requirements Document (BRD) — Bridge Portal

## Bridge Portal — Product Edition v1.2

| Field | Details |
| :--- | :--- |
| **Document Name** | Bridge Portal BRD |
| **Version** | 1.2 |
| **Product Name** | Bridge Portal — Teacher Lifecycle Management System |
| **Prepared By** | Insphere Solutions Pvt. Ltd. |
| **Organisation** | Insphere Solutions Pvt. Ltd. |
| **Classification** | Confidential — Pre-Sales / Proposal |
| **Date** | May 2026 |
| **Project Type** | Web Portal |
| **Reference ID** | ISPL/2026/BRIDGE/001 |

---

## Revision History

| Version | Date | Author | Description |
| :--- | :--- | :--- | :--- |
| **1.0** | April 2026 | Insphere Solutions Pvt. Ltd. | Initial release. Bridge Portal BRD covering 9 core functional modules. |
| **1.1** | April 16, 2026 | Insphere Solutions Pvt. Ltd. | Updated with detailed requirements, business rules, process flows, and traceability matrix. |
| **1.2** | May 1, 2026 | Insphere Solutions Pvt. Ltd. | Comprehensive update: added UDISE+ verification, multi-gateway payments (CCAvenue, SabPaisa), exam registration & hall ticket generation, bulk result processing pipeline, advanced RBAC, bilingual support, AWS cloud integrations, course content management, async data exports, and expanded security NFRs. |

---

## 1. Executive Summary
The **Bridge Portal** is a centralized, high-performance digital platform designed to manage the entire lifecycle of a teacher-student — from initial school verification and multi-step online registration, through fee payment, academic activities (TMA submission and evaluation, exam registration), to result declaration and post-admission services (e-services).

The platform serves multiple stakeholder groups: teacher-students (frontend portal at `bridge.nios.ac.in`), school coordinators, regional centre staff, and NIOS/HQ administrators (backend admin panel at `bridge-admin.nios.ac.in`), with automated background processing for payments, results, and data exports.

Beyond a structured 7-stage registration workflow, the portal offers: real-time Application Status tracking, UDISE+ national database verification for school and teacher credentials, Financial Transparency with multi-gateway payment history tracking (SabPaisa/BOI, and CCAvenue), direct access to Academic Resources such as study material and TMA downloads, exam registration with hall ticket generation, a bulk result processing pipeline, and a centralized Grievance Redressal system with 16 distinct E-Services.

---

## 2. Business Objectives

| Objective ID | Business Objective | Expected Outcome |
| :--- | :--- | :--- |
| **BO-01** | Single Source of Truth | Unified, immutable database eliminating data redundancy across departments. |
| **BO-02** | End-to-End Digital Transformation | Automate registration, verification, and certification lifecycle; remove physical paperwork. |
| **BO-03** | Operational Efficiency | Reduce manual processing time and errors via real-time validation and automated approvals. |
| **BO-04** | Security & Trust | OTP-based multi-factor authentication and TOTP (admin) for sensitive profile modifications. |
| **BO-05** | Data Integrity via UDISE+ | Verify school UDISE codes and teacher credentials against the national UDISE+ database before admission. |
| **BO-06** | Automated Fee Collection | Integrate multiple payment gateways for secure online fee payment with double-payment detection. |
| **BO-07** | Scalable Result Processing | Process bulk result data files through a chunked pipeline (SQS) for large-scale result declaration. |
| **BO-08** | Future Scalability | Modular, bilingual (English/Hindi) framework for payroll integrations and performance tracking in future phases. |

---

## 3. Scope Definition

### 3.1 In Scope
- **Teacher/Student Registration**: A comprehensive multi-step data collection wizard with UDISE+ pre-verification, sequential stages, real-time validation, and progress saving.
- **Multi-Channel Authentication**: Secure OTP-based login via SMS and Email, TOTP MFA for admin users, single active session enforcement, and auto-logout after 1 hour of inactivity.
- **UDISE+ Verification**: Pre-registration verification of school UDISE codes and teacher details against the national UDISE+ API; registration blocked on failure.
- **Workflow Management**: Configurable multi-step approval workflows (school → regional → HQ) with override, multi-hop, round-robin assignment, overdue escalation, and full audit trails.
- **E-Service Lifecycle**: End-to-end handling of 16+ profile modification services each with structured approval workflows and configurable fee structures.
- **Multi-Gateway Payment**: Integration with SabPaisa/BOI (primary), and CCAvenue (secondary), automatic reconciliation, double-payment detection, and refund processing.
- **TMA Management**: Assignment question paper management, subject expert allocation/reallocation, evaluation, marks submission, and student marks visibility.
- **Exam Management**: Exam registration with fee payment, late registration support, hall ticket generation as downloadable PDFs.
- **Result Processing Pipeline**: Bulk DBF result file upload, staged pipeline processing via SQS (upload → basket → processing → insert), retry logic, and student result card downloads.
- **Identity & Form Printing**: Generation of dynamic, QR-coded Identity Cards (Icard) and Application Forms available for download post-approval.
- **Subject Expert Management**: 8-step expert self-registration, subject specialization, allocation/reallocation to student TMAs, evaluation interface.
- **Master Data Management**: Academic years, courses, subjects, regions, mediums, document types, study centres, and all configurable reference data.
- **Reports & Async Exports**: Admission, TMA, and expert reports filterable by academic year/region/status; async export jobs processed via background worker with S3 storage.
- **Grievance Redressal**: Searchable ticketing system with status updates (Open, Resolved), unique ticket IDs, and email acknowledgment within 5 minutes.
- **Course Content Management**: Upload and manage course chapters and content accessible by students via the frontend portal.
- **Dynamic Dashboard**: Tile-based landing page showing real-time application progress, payment history, study materials, exam results, TMA status, and grievance access.
- **Bilingual Support**: All student-facing interfaces available in English and Hindi.
- **AWS Cloud Integrations**: S3 (document storage), SQS (async job queue), SES (email), CloudFront (CDN), Secrets Manager (credentials).
- **RBAC**: Granular role-based access control with named permissions for every module action; configurable and auditable.

### 3.2 Out of Scope
- **Offline Data Entry**: Manual processing of paper-based applications or offline document submissions.
- **Direct Bank Transfers**: Manual NEFT/RTGS without a gateway integration is excluded; only gateway-based payments are supported.
- **Mobile Native Applications**: iOS/Android native apps are not in scope; the system is web-only.
- **Video Conferencing / Live Teaching**: Live classroom or video conferencing features are not included.
- **Third-Party LMS Integrations**: Integration with external Learning Management Systems is out of scope.
- **State Department System Integration**: Direct integration with state education department systems (beyond UDISE+) is excluded.

---

## 4. Stakeholders

| Stakeholder | Role | Department | Responsibility |
| :--- | :--- | :--- | :--- |
| **Project Sponsor** | Sponsor | Management | Funding & approvals |
| **Product Owner** | Business Owner | Operations | Requirements validation |
| **Tech Team** | Developers | IT | System development |
| **Teachers / Teacher-Students** | Primary End Users | External | Register, pay fees, submit TMAs, register for exams, view results, raise e-service requests |
| **Students** | End Users | External | Registration, document upload, assignment access, marks and result viewing |
| **School Admin / Principal / Coordinator** | School-Level Admin | Administration | School-level document verification, student approval, UDISE-based coordination |
| **Regional Centre Staff** | Regional Admin | Administration | Regional-level verification and approval of applications |
| **State-Level Officer** | State-Level Admin | Administration | State-level verification, final student approval, and oversight of school-level operations |
| **NIOS HQ Administrators** | Central Admin | Administration | Final approval, system configuration, reporting |
| **Subject Expert** | Evaluator / SME | External | Self-registration, subject expertise selection, TMA assignment evaluation, and marks submission |
| **Super Admin** | Platform Owner | IT | Master configuration, module control, full administrative oversight, RBAC management |
| **Finance Team** | Fee Management | Finance | Monitor transactions, process refunds, fee structure configuration |
| **AWS / Infrastructure** | Cloud Provider | IT | Hosting, storage (S3), queuing (SQS), email (SES), CDN (CloudFront) |

---

## 5. Current State Analysis (As-Is)

| Challenge | Description |
| :--- | :--- |
| **Manual Registration Process** | Teacher registration performed via paper forms with no structured digital workflow; prone to delays and data loss. |
| **No UDISE+ Verification** | School and teacher credentials not verified against the national database, leading to fraudulent or erroneous registrations. |
| **Data Inconsistencies** | Multiple disconnected data stores across departments lead to duplicate and conflicting teacher records. |
| **Delayed Approvals** | Multi-tier approval handled via physical files and emails, causing significant processing delays. |
| **Lack of Centralized Database** | No single source of truth for teacher data; queries require manual cross-referencing of multiple systems. |
| **Limited Visibility** | No real-time tracking of registration status, exam results, or certification progress for teachers or administrators. |
| **Manual Payment Collection** | Fee collection via cash or bank challans with no online gateway, leading to reconciliation errors. |
| **No Bulk Result Processing** | Exam results entered manually with high error probability and no automated pipeline for large-scale processing. |

---

## 6. Proposed Solution (To-Be)
- **UDISE+ Pre-Registration Verification**: Registration blocked unless school UDISE code and teacher details are verified against the national UDISE+ API.
- **Fully Digital Registration System**: Complete 10-step structured wizard (UDISE → Eligibility → Auth → OTP → Basic Details → Personal Info → Address → Subject → Document Upload → Fee Payment) with real-time validation, progress saving, and sequential data capture.
- **Configurable Workflow Engine**: Multi-step approval workflows (school → regional → HQ) with override, round-robin, overdue escalation, and full audit trails per action.
- **Multi-Gateway Payment Platform**: SabPaisa/BOI (primary), and CCAvenue (secondary) with background reconciliation scheduler, double-payment detection, and BOI refund API.
- **TMA & Evaluation Pipeline**: End-to-end TMA question paper management, subject expert allocation, online evaluation, marks submission, and student marks visibility.
- **Exam & Hall Ticket Module**: Exam registration (with late fee support), fee payment gating, and downloadable PDF hall ticket generation.
- **Bulk Result Processing via SQS**: DBF file upload → staged pipeline (Basket Creation → Chunk Processing via SQS → DB Insert) with retry logic and real-time status counters.
- **Integrated E-Services Dashboard**: Centralized portal for 16+ profile modification services, payment history, study materials, TMA, and exam results.
- **Bilingual Interface**: All student-facing pages available in English and Hindi via language toggle.
- **AWS Cloud Architecture**: S3 for document storage, SQS for async jobs, SES for email, CloudFront CDN for static assets, Secrets Manager for credentials.
- **Advanced Security**: TOTP MFA for admins, OTP for students, AES-256 at rest, TLS 1.3 in transit, Hybrid RSA+AES AJAX payload encryption, CSRF tokens, CSP headers, Aadhaar/mobile masking.
- **Async Reports & Exports**: Column-selectable export jobs processed by background workers; files stored on S3 with time-limited download tokens.

---

## 7. Functional Requirements

### 7.1 User Management & Authentication
- **Admin User Management**: The system shall allow administrators to create, edit, activate/deactivate, and delete admin/staff user accounts. Granular RBAC permissions govern access.
- **Authentication (Admin/Staff)**: Username/password with CAPTCHA verification; Multi-Factor Authentication (MFA) via TOTP (Google Authenticator) is mandatory for sensitive modules; single active session enforcement and auto-logout after 1 hour of inactivity.
- **Authentication (Students)**: Login using email/password or OTP (6-digit, 10-minute expiry with resend cooldown). Auto-login link (valid 10 minutes) available for administrator support.
- **School Coordinator Login**: Dedicated login flow that redirects to OTP verification.
- **RBAC**: Granular roles with named permissions for every action (view, add, edit, delete, and special actions).

### 7.2 Student Admission & Registration (UDISE+ Verified)
- **UDISE+ Verification**: Before registration, verifies the school’s UDISE code and teacher's employment details via the national UDISE+ API. Blocks registration on failure.
- **Multi-Step Online Registration Wizard**:
  1. UDISE code entry and school verification (UDISE+ API)
  2. Eligibility check
  3. Authentication setup (email/mobile)
  4. OTP verification
  5. Partial registration (saves basic details, generates Application Number)
  6. Personal information (name, parents, DOB, Aadhaar, gender)
  7. Address details (with pincode auto-fill via API)
  8. Subject selection
  9. Document upload (JPG/PDF, max 2 MB per file)
  10. Review and fee payment (generates Reference Number, and Enrollment Number on final HQ approval)
- **Application Management**: Search, filter, print applications/ID cards; bulk workflow actions (approve, assign, reassign).
- **Application Statuses**:
  - `PENDING (0)`: Application submitted, awaiting verification.
  - `APPROVED (1)`: Application fully approved.
  - `REJECTED (2)`: Application rejected.
  - `DOC_REQUIRED (3)`: Additional documents requested.
  - `VERIFIED (4)`: Verified at one level, pending further approval.
  - `PROVISIONAL_APPROVED (5)`: Provisionally approved.
  - `PERMANENTLY_REJECTED (6)`: Permanently rejected.

### 7.3 Workflow Management
- **Workflow Definition**: Configure multi-step sequential steps assignable to roles; supports step override (skipping), multi-hop (jumping), and round-robin.
- **Workflow Actions**: Approve, Reject, Pause (Document Required), Reassign, Round-Robin Reassign, Overdue Processing (auto-escalation on time limit breach).
- **Audit Trail**: Every action logged with timestamp, user, IP address, user agent, and device type.

### 7.4 Fee & Payment Management
- **Fee Configuration**: Fee structures configurable per academic year, course, and scenario; supports short fee payments (partial top-ups).
- **Payment Gateways**:
  - *SabPaisa / BOI* (Primary): AES-encrypted; supports refunds via BOI API.
  - *CCAvenue* (Secondary): Production configured.
  - *Razorpay* (Tertiary): Test keys configured.
- **Transaction Statuses**: `CREATED`, `PENDING` (Awaiting gateway), `PAID` (Confirmed), `FAILED`, `REFUNDED`.
- **Processing**: Cron scheduler processes pending transactions; double-payment detection flags duplicate transactions for refunds.

### 7.5 TMA (Tutor Marked Assignment) Management
- **Assignment Management**: Create TMA question papers per subject, medium, and block; documents uploadable per medium; configurable maximum marks.
- **Subject Expert Allocation**: Dynamically allocate/reallocate subject experts to student submissions.
- **TMA Evaluation**: Evaluation interface for experts; marks recorded per question; published evaluated marks instantly visible to students.

### 7.6 Exam Management
- **Exam Registration**: Students register and pay fees; late registration support with automatic late fees; PDF hall ticket generation post-registration.

### 7.7 Result Management
- **Result Processing Pipeline**:
  1. *Upload*: DBF file uploaded, `ResultStat` record created.
  2. *Basket Creation*: Raw data parsed into `ResultBasket` staging.
  3. *Basket Processing*: Basket chunk jobs processed asynchronously via AWS SQS.
  4. *Insert Job Creation*: Insert chunk jobs created.
  5. *Insert Processing*: Data inserted into `Result` and `ResultSubject` tables.
  6. *Retry*: Failed records retryable.
- **Access**: Real-time status counters for admin; students search and download PDF result cards.

### 7.8 E-Services
- **E-Service Definition**: Configure 16+ profile modifications (e.g., name correction, change address, subject change, certificate issuance) with specific fee structures and document requirements.
- **Verification**: OTP verification required before any e-service request is activated.

### 7.9 Subject Expert Management
- **Expert Registration**: 8-step wizard (Basic info, Credentials, Address, Qualifications, Employment, Specializations, Documents, Review).
- **Allocation**: Assigned based on school, regional centre, and subject availability.

### 7.10 Master Data Management
Configures Geographic Masters (Country, State, District, Block), Academic Years, Course Definitions, Subjects, Mediums, NIOS Regional and Study Centres, Event milestones, Document templates, Registration date blocks, and Assignment schedules.

### 7.11 Reports & Exports
Admission, TMA, and expert reports filterable; asynchronous column-selectable exports handled by background workers, uploaded to AWS S3, and shared via secure time-limited tokens.

---

## 8. Non-Functional Requirements (NFRs)

| Category | Ref | Requirement |
| :--- | :--- | :--- |
| **Performance** | NFR-P-01 | Page load time < 3 seconds under normal operating conditions. |
| **Performance** | NFR-P-02 | System must support 1 lakh+ registered users with no degradation in response time. |
| **Performance** | NFR-P-03 | Background jobs (payment reconciliation, result processing) run on a 5-minute cycle without impacting frontend performance. |
| **Security** | NFR-S-01 | All sensitive data fields encrypted using AES-256 at rest; TLS 1.3 for all data in transit. |
| **Security** | NFR-S-02 | OTP-based MFA mandatory for student sensitive operations; TOTP (Google Authenticator) mandatory for all admin/staff users. |
| **Security** | NFR-S-03 | Sensitive AJAX payloads encrypted using Hybrid RSA+AES encryption (`HybridEncryptor`). |
| **Security** | NFR-S-04 | CSRF tokens on all forms; httpOnly, secure, SameSite=Lax cookies; CSP headers on all responses. |
| **Security** | NFR-S-05 | Aadhaar numbers and mobile numbers masked by default; unmaskable only by authorized users. |
| **Security** | NFR-S-06 | All credentials and API keys stored in AWS Secrets Manager; none hardcoded. |
| **Security** | NFR-S-07 | XSS prevention via input purification (`PurifyStringBehavior`) on all user-supplied data. |
| **Scalability** | NFR-SC-01 | Infrastructure must support horizontal scaling to handle spike traffic (>5,000 concurrent users) during registration deadlines. |
| **Scalability** | NFR-SC-02 | Result processing pipeline uses chunked batch processing via SQS to handle large result files. |
| **Availability** | NFR-A-01 | System availability >= 99.5%, including automated failover for document storage server. |
| **Availability** | NFR-A-02 | Maintenance mode configurable without system restart; background jobs resilient with retry mechanisms. |
| **Usability** | NFR-U-01 | All dashboard modules fully functional and accessible on desktop and tablet resolutions. |
| **Usability** | NFR-U-02 | Student registration portal available in English and Hindi; language toggle on all student-facing pages. |
| **Auditability** | NFR-AU-01 | All workflow actions logged with user, timestamp, IP address, and device information. |
| **Auditability** | NFR-AU-02 | All data modifications tracked via `created_by` / `updated_by` fields (`BlameableBehavior`). |
| **Data Integrity** | NFR-DI-01 | All entities have UUID (GUID) identifiers in addition to auto-increment IDs. |
| **Data Integrity** | NFR-DI-02 | Database transactions used for all multi-step data operations. |

---

## 9. Business Rules

| Rule ID | Rule Name | Description |
| :--- | :--- | :--- |
| **BR-R-01** | UDISE+ Gating | A student cannot register without a valid UDISE code verified against the UDISE+ national database. |
| **BR-R-02** | Sequential Completeness | Registration must follow all steps in strict order; users cannot skip to document upload without completing prior stages. |
| **BR-R-03** | Authentication Lock | Any sensitive change (Name, DOB, Payment, or Service Access) requires a 6-digit OTP that expires after 10 minutes. |
| **BR-R-04** | Validation Integrity | All name fields must be alphabetic only; address fields use dynamic State/District dropdowns; entries auto-converted to UPPERCASE. |
| **BR-R-05** | Proof-of-Eligibility | Every correction request must be accompanied by a mandatory B.Ed certificate or valid ID proof upload. |
| **BR-R-06** | Financial Clearance | Payment confirmation from the gateway is a hard pre-requisite before any service request moves to Pending Approval. |
| **BR-R-07** | Icard & Certificate Gating | Identity Cards and Academic Certificates are only generated after 100% profile approval by the State Nodal Officer. |
| **BR-R-08** | Result Immutability | Once an exam result is published, the record becomes read-only and cannot be altered via the standard interface. |
| **BR-R-09** | Enrollment Number Gen | An Enrollment Number is generated only upon final HQ approval of the application. |
| **BR-R-10** | One Active Application | A student can have only one active application per academic year and course. |
| **BR-R-11** | TMA Expert Scope | A subject expert can only evaluate TMA submissions for subjects they are allocated to. |
| **BR-R-12** | TMA Marks Cap | TMA marks cannot exceed the configured maximum marks for the assignment. |
| **BR-R-13** | Exam Eligibility | Students must have an active enrollment to register for exams; fee payment required for confirmation. |
| **BR-R-14** | Double-Payment Detection | Double payments for the same fee must be detected and flagged; refunds processed only by authorized users. |
| **BR-R-15** | MFA Enforcement | Admin users must complete MFA (TOTP) setup before accessing sensitive modules. |
| **BR-R-16** | Password History | Passwords must not match any of the last 3 used passwords. |
| **BR-R-17** | Workflow Sequence | Applications must follow the defined workflow sequence (school → regional → HQ) unless an override is authorized. |
| **BR-R-18** | Overdue Escalation | Overdue workflow steps are automatically escalated per configured time limits. |

---

## 10. Process Flow / Workflow

### 10.1 End-to-End Teacher Lifecycle Workflow
1. **UDISE+ Verification**: School UDISE code and teacher details verified against national UDISE+ API.
2. **Multi-Step Registration**: 10-step wizard with automatic progress saving.
3. **OTP Verification**: Dual-channel (Email/SMS) OTP verification.
4. **Fee Payment**: Payment via SabPaisa/BOI or CCAvenue; Reference Number generated.
5. **Document Upload**: Multi-format JPG/PDF verification.
6. **Administrative Review**: Multi-tier approval flow (School → Regional → HQ/SNO).
7. **Dashboard Activation**: Enrollment Number generated; student gains portal access.
8. **Academic Lifecycle**: TMA download, student submission, and expert evaluation.
9. **Exam Registration**: Exam fee payment and hall ticket download.
10. **Evaluation & Marking**: Result compilation via SQS chunked DBF result pipeline.
11. **Certification**: Result card downloadable.
12. **Maintenance**: Continued profile updates via 16+ E-Services.

---

## 11. Data & Integration Requirements

### 11.1 Key Data Entities
- **Biographical Data**: Permanent record of full name, parentage, Aadhaar, DOB, and social category.
- **Professional & Educational Records**: Permanent record of UDISE codes, School mappings, Date of Appointment, and eligibility certifications.
- **Academic Deliverables**: TMA submission papers and expert marks logs (retained per academic year).
- **Exam & Results Data**: Registrations, payment IDs, hall tickets, result subject scores (Result & ResultSubject).
- **Audit Trails**: Payment logs, SHA-256 transaction IDs, OTP attempt histories, and async S3 export queues.

### 11.2 Integration Grid

| System | Purpose | Integration Type | Priority |
| :--- | :--- | :--- | :--- |
| **UDISE+ API** | Pre-registration verification; JWT + AES-ECB encrypted payload | HTTPS REST API | Critical |
| **SabPaisa / BOI** | Primary gateway; AES encrypted requests; BOI refund API | HTTP API | Critical |
| **CCAvenue** | Secondary payment gateway | HTTP API | High |
| **Razorpay** | Tertiary gateway (test keys configured) | HTTP API | Medium |
| **AWS S3** | Secure storage for documents, TMAs, exports, expert files | AWS SDK | Critical |
| **AWS SQS** | Async job queue for payment scheduler and result pipeline | AWS SDK | Critical |
| **AWS SES** | Transactional email delivery (OTP, passwords, notifications) | SMTP / HTTP | High |
| **CloudFront** | CDN for static assets with 30-min secure signed cookies | AWS SDK | High |
| **Secrets Manager** | Centralized storage of credentials, encryption, and API keys | AWS SDK | Critical |
| **SMS Gateway** | OTP delivery; Sender ID: HQNIOS | HTTP API | High |
| **Pincode API** | Auto-fill address fields based on pincode lookup | HTTP API | Medium |

---

## 12. Key Risks & Mitigation

| Risk ID | Risk | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **R-01** | OTP Delivery Failure | High | Medium | Secondary email OTP delivery and a dynamic resend timer cooldown. |
| **R-02** | Payment Gateway Timeout | Medium | Medium | "Check Payment Status" dashboard trigger + automated background cron reconciler. |
| **R-03** | Concurrent Load Spike | High | Medium | Database indexing, SQS async batch queues, horizontal scaling, and read-replicas. |
| **R-04** | UDISE+ Unavailability | High | Low | Cache historical valid UDISE codes; emergency manual administrative bypass mode. |
| **R-05** | Double Payments | Medium | Medium | Hard gateway token double-spend check; automatic flagging for manual approval prior to refund processing via BOI API. |
| **R-06** | Gateway Outage | High | Low | Automated multi-gateway routing and failover flow (SabPaisa → CCAvenue → Razorpay). |

---

© 2026 Insphere Solutions Pvt. Ltd. | Confidential - Pre-Sales / Proposal
