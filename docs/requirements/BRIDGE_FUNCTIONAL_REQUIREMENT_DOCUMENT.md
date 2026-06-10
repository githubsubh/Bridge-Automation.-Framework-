# Bridge Project: Functional Requirement Document (FRD)

## 1. Introduction
The Bridge application is a comprehensive portal designed for teacher registration, certification, and educational services. This document outlines the functional requirements, user interface specifications, and business logic for the core modules of the Bridge platform, focusing on user‑facing features.

## 2. User Interface & Functional Modules

### 2.1 Landing Page & Navigation
* **Hero Section** – High‑impact banner with navigation links (About, Admission, Exams & Results, Teacher Corner, Important Links, Login Corner, Enroll Now).
* **Quick Links** – Direct access to Syllabus, E‑Services, Study Material, etc.

![Home Page – Hero Section](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/bridge_home_page_hero_section_1775193194855.png)

### 2.2 Login Screen
* **Email / Reference No.** – Text input.
* **Password** – Masked entry.
* **Clear Button** – Resets all fields.
* **Real‑time validation** – Shows errors for missing/incorrect data.

![Login Screen (Live)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/bridge_login_page_1775193243351.png)

---

## 3. Teacher Registration Workflow (Full Journey)
The registration wizard consists of seven sequential stages. 

| Stage | Description | Screenshot |
|------|-------------|------------|
| **Stage 1 – Basic Details** | Full name, parents’ names, DOB, gender, UDISE code, Teacher ID. | ![Basic Details (Live)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/registration_step_1_basic_details_final_1775194312308.png) |
| **Stage 2 – Authentication & OTP** | Email, mobile number, OTP entry (6‑digit numeric). | ![Authentication – OTP](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/registration_step_3_authentication_1775195576464.png) |
| **Stage 3 – Personal Info** | Social Category, Medium of Study, optional details. | ![Personal Information (Original)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/personal_info_original_1775206080520.png) |
| **Stage 4 – Address Details** | Address lines, State → District dynamic selection. | ![Address Details (Original)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/address_original_1775206096610.png) |
| **Stage 5 – Eligibility & Subjects** | Date of Appointment, selection of subjects and medium. | ![Eligibility & Subjects (Original)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/eligibility_original_1775206129628.png) |
| **Stage 6 – Document Upload** | Upload Photo, Signature, B.Ed Certificate, etc. | ![Document Upload (Original)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/document_upload_original_1775206142150.png) |
| **Stage 7 – Review & Submit** | Read‑only summary with section-wise edit functionality. | ![Review & Submit (Original)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/review_submit_original_1775207783758.png) |
| **Final Confirmation** | Transaction details and successful enrollment message. | ![Registration Success (Original)](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/payment_success_original_1775208359430.png) |

---

## 4. Post‑Login Dashboard & E‑Services Overview
After successful enrollment (100% progress), the teacher gains access to a tile-based dashboard providing educational and administrative services.

| Tile | Purpose | Screenshot (Original) |
|------|---------|------------|
| **Progress** | Shows 100% completion status post-registration. | ![Dashboard Progress](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/dashboard_load_1775200383609.png) |
| **E-Services Grid** | Selection interface for 16 different profile modifications/corrections. | ![E-Services Grid](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/available_eservices_page_original_1775209159338.png) |
| **E-Services List** | Detailed view showing fees and categories for all 16 services. | ![E-Services List](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/eservices_list_original_1775209000370.png) |
| **Study Material** | Download academic resources. | ![Study Material](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/dashboard_study_material_1775195952923.png) |
| **Payment Status** | View transaction history and download receipts. | ![Payment History](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/dashboard_payment_status_1775195958152.png) |
| **Grievances** | Lodge and track support tickets. | ![Grievances](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/dashboard_grievances_1775195962786.png) |
| **Results** | View and download performance certificates. | ![Results](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/dashboard_results_1775195968014.png) |

---

## 5. E-Services Module (Detailed Requirements)
The E-Services module is the primary interface for teachers to update their profiles after registration. 

### 5.1 Security & Access Workflow
Every E-Service request is protected by a **Two-Factor Authentication (2FA)** step. 
1. **Selection:** User selects a service from the grid/list.
2. **OTP Verification:** A 6-digit OTP is sent to the registered mobile/email.
3. **Fill Form:** (Pre-requisite: OTP Success) Teacher enters new data and uploads supporting documents.
4. **Payment:** (Optional: varies by service) Transaction fee payment via SabPaisa.
5. **Confirmation:** System displays a unique Request ID and payment summary.

| Stage | Process Description | Screenshot (Live) |
| :--- | :--- | :--- |
| **OTP Entry** | User enters the 6-digit verification code to unlock the service form. | ![OTP Verification Page](https://raw.githubusercontent.com/githubsubh/Bridge-Automation.-Framework-/main/artifacts/change_signature_otp_page.png) |
| **Fill Form** | Side-by-side comparison of Current vs New data fields. Mandatory document upload. | ![Modification Form](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/eservice_correspondence_form_original_1775218482474.png) |
| **Final Success** | Transaction confirmation showing Paid Amount, Gateway ID, and Status. | ![E-Service Confirmation](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/eservice_payment_confirmation_original_1775215214950.png) |

### 5.2 Service Categories & Fees
The portal categorizes services into **Change** (profile updates) and **Correction** (fixing errors). Fees range from Rs 100 to Rs 400.

| Category | Service Type | Fee (Rs) | Field Validations | Form Screenshot (Original) |
| :--- | :--- | :--- | :--- | :--- |
| **Basic Details Change** | **Change Correspondence Address** | **100** | House No, Locality, State (Dropdown), District (AJAX Lock), Pincode (6-digit numeric). | ![Correspondence Form](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/eservice_correspondence_form_original_1775218482474.png) |
| | **Change Permanent Address** | **100** | Same as above. Supporting address proof (JPG/PDF < 2MB). | ![Permanent Address Form](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/eservice_permanent_address_form_original_1775218904870.png) |
![Change Appointment Date Form](C:/Users/Insph/.gemini/antigravity/brain/959a1879-73fd-486e-897e-1b2d63af8ab7/change_appointment_date_form_1775718295103.png)
| | Change Appointment Date | 200 | Restricted date-picker (min/max year constraints). | |
![Change Profile Photo Form](C:/Users/Insph/.gemini/antigravity/brain/959a1879-73fd-486e-897e-1b2d63af8ab7/change_profile_photo_form_1775718787263.png)
| | Change Profile Photo | 200 | Image upload (JPG/PNG), enforced aspect ratio, < 2MB. | |
![Change Signature OTP Verification](https://raw.githubusercontent.com/githubsubh/Bridge-Automation.-Framework-/main/artifacts/change_signature_otp_page.png)
![Change Signature Form](https://raw.githubusercontent.com/githubsubh/Bridge-Automation.-Framework-/main/artifacts/change_signature_form.png)
| | Change Signature | 200 | Image upload (JPG/PNG), enforced aspect ratio, < 2MB. | |
![Change Social Category Form](https://raw.githubusercontent.com/githubsubh/Bridge-Automation.-Framework-/main/artifacts/change_social_category_form.png)
| | Change Social Category | 200 | Category selection (SC/ST/OBC/GEN). Cert upload required. | |
![Change Study Medium Form](https://raw.githubusercontent.com/githubsubh/Bridge-Automation.-Framework-/main/artifacts/change_study_medium_form.png)
| | Change Study Medium | 200 | Selection among English/Hindi/Regional. | |
![Change School Placeholder](C:/Users/Insph/.gemini/antigravity/brain/959a1879-73fd-486e-897e-1b2d63af8ab7/placeholder_image_1775716643079.png)
| | Change School | 400 | UDISE Code (AJAX verify), Principal approval may be needed. | |
| **Basic Details Correction** | **Name Correction** | **400** | Alphabetic only, max 100 chars. **BEd Certificate mandatory**. | ![Name Correction Form](/C:/Users/Insph/.gemini/antigravity/brain/43ae3137-eb14-4a35-86b9-165cdeca532e/artifacts/eservice_name_correction_form_original_1775220748167.png) |
| | Father Name Correction | 400 | Same as above. | |
| | Mother Name Correction | 400 | Same as above. | |
| | Gender Correction | 200 | Fixed options (Male/Female/Trans). | |

### 5.3 Common Form Logic
* **Mandatory Uploads:** Almost all E-Services require one primary supporting document (JPG/PDF, max 2MB).
* **Read-Only Fields:** The system displays the *current* state of the information side-by-side with the *new input* fields.
* **Auto-Formatting:** Names and addresses are automatically converted to uppercase via CSS/JS.

---

## 6. Field Validation & Business Rules Summary
| Page | Field | Validation / Logic |
|------|-------|--------------------|
| **Registration** | UDISE Code | Must be valid in backend; numeric only. |
|  | Social Category | Mandatory selection from predefined list. |
|  | Documents | JPG/PNG/PDF formats; size < 2MB. |
| **Login** | CAPTCHA | Case-sensitive numeric entry required. |
| **Payment** | Gateway | Consent to payment terms required before redirect. |
| **E-Services** | OTP | Required before form access; 6-digit numeric. |

## 7. Conclusion
The Bridge portal provides a streamlined, documented registration and profile management process. The use of live-captured screenshots ensures this FRD reflects the actual system behavior and requirements.
