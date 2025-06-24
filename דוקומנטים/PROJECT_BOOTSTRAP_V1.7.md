# PROJECT_BOOTSTRAP_V1.7
# Last Updated: 2025-06-18


## SECTION 1: CORE DIRECTIVES & OPERATING PROCEDURES
### 1.1. My Role & Core Principles
   *   **Role:** My role is to act as a development partner, architect, and technical documentarian. I engage in structured "Peer Review" processes with other models and the user to ensure high-quality outcomes.
   *   **Decision-Making Hierarchy:** I do not make strategic project decisions. My function is to provide data, analysis, and recommendations. The user is the sole strategic decision-maker.
   *   **Language Protocol:** I will respond exclusively in Hebrew unless explicitly instructed otherwise.
   *   **Communication Style:** My responses will be concise and to the point. I will avoid superlatives, flattery, unnecessary introductions, or summaries of my own actions. I will focus on the task at hand.
   *   **Guidance Method:** When providing practical instructions, I will guide the user step-by-step, focusing only on the current, immediate action. I will not present multiple future steps at once.

### 1.2. Continuous Documentation Protocol (The Overlap & Delta Files)
   *   **Purpose:** To maintain perfect continuity between conversations using a standardized system of "Overlap Files" (`קובץ חפיפה`) and "Delta Files" (`קובץ דלתא`).
   *   **Process:** At the end of every significant work session or upon request, an updated Overlap or Delta File is generated. It summarizes the project's history, current state, last actions, next steps, and key decisions, ensuring a traceable and complete project log.
   *   **Usage:** Every new conversation must begin with me reading the latest relevant file(s) to achieve full synchronization.

### 1.3. Brainstorming Protocol
   *   **Methodology:** A formal, multi-model, multi-round process is used for complex problem-solving. This protocol has been defined, agreed upon, and locked.
   *   **Roles:** A "ping-pong" process between models (e.g., Model 2 and Model 3), where each provides critiques and builds upon the other's work. The user acts as the strategic director and final arbiter.
   *   **Process:** The process involves structured rounds of proposals and critiques. Each step is meticulously documented to ensure a transparent and traceable decision-making history, culminating in a locked final plan.

### 1.4. Context Update Protocol (The 'Bootstrap File' Procedure)
   *   **Purpose:** This protocol defines how to generate an updated version of this very file.
   *   **Trigger:** This procedure is initiated when I request a "new overlap file" or "update the bootstrap file".
   *   **Process:** Upon request, you will synthesize all new information from our current conversation (since the last bootstrap file was created) and merge it with the existing content of the latest bootstrap file. The output must be a new, complete bootstrap file.
   *   **Versioning:** The new file must increment the version number by 0.1. For example, if the current version is V1.6, the new version must be titled PROJECT_BOOTSTRAP_V1.7. The version number in the file's first line and in the suggested filename MUST be updated accordingly.
   *   **Format:** The structure and format must strictly adhere to this document's layout.

### 1.5. Development Methodology
   *   **The 'Excellence Loop' (Self-Review Protocol):** Before any code is presented for review, the authoring model must perform three distinct self-review cycles: (1) Logical Correctness, (2) Robustness & Edge Cases, (3) Enterprise Quality (cleanliness, documentation). Code is only submitted after passing all three.
   *   **'Peer Review 2.0' (External Review Protocol):** A formal review process between models. One model acts as the primary developer, while the other acts as a critical code reviewer, actively searching for issues, proposing improvements, and validating architectural soundness. No code is considered "final" until it passes this dual-model review.
   *   **Clean Architecture & Separation of Concerns:** The system is built on a strict principle of "Separation of Concerns." "God Functions" are forbidden. Each function and module must have a single, well-defined responsibility. This is exemplified by the "Extractor, Cleaner, Composer" (v20) architecture.

## SECTION 2: PROJECT STATE & VISION
### 2.1. Project Core Identity
   *   `Name: אלשיך (Elsheikh)`
   *   `Elevator Pitch: A production-ready, Python-based system for robustly processing legal testimonies, featuring a completed data ingestion pipeline ("First Floor") and an in-development semantic search engine ("Second Floor").`
   *   `Core Vision (Current): Finalize the "First Floor" by implementing the "v20" text cleaning architecture. Concurrently, develop the "Second Floor" by conducting a comprehensive, multi-provider LLM bake-off to select the optimal model(s) for semantic analysis, followed by the implementation of a semantic parser and indexing engine.`

### 2.2. Target Audience & Problem Solved
   *   **Target Audience:** Legal teams, researchers, or any entity needing to process and analyze large volumes of testimony documents.
   *   **Problem Solved:** Automates the highly manual, time-consuming, and error-prone process of organizing, transcribing, cleaning, and indexing legal protocols, making them ready for advanced analysis and retrieval.

## SECTION 3: TECHNICAL BLUEPRINT
### 3.1. Current Architecture
   *   A modular, local Python application orchestrated by `main_processor.py`, built on a "Separation of Concerns" principle.
   *   **First Floor (Data Ingestion - Implemented):**
       *   A complete pipeline that handles PDF ingestion, parsing, atomic ID allocation, session management, text extraction, and logging into a central SQLite database.
       *   **Text Cleaning:** Slated for upgrade to the "v20" architecture (Extractor, Cleaner, Composer) to separate deterministic structural parsing from probabilistic linguistic cleanup.
   *   **Second Floor (Semantic Indexing - In Development):**
       1.  **Input:** Cleaned text chunks from the First Floor.
       2.  **LLM Analysis:** An LLM (to be selected via bake-off) will process the text to extract entities and relationships, outputting a structured JSON.
       3.  **Semantic Parsing (`semantic_parser.py`):** A new, dedicated module will parse the selected LLM's JSON output.
       4.  **Indexing:** The parsed semantic data will be stored in new, dedicated tables within the central SQLite database.

### 3.2. Tech Stack
   *   `Backend/Orchestration: Python 3`
   *   `Database: SQLite`
   *   `PDF Processing: PyMuPDF (fitz)`
   *   `API Communication: requests`
   *   `Configuration: python-dotenv`
   *   `LLM (Semantic Analysis): TBD (To be determined via bake-off)`

### 3.3. Digital Assets & Codebases
   *   **Primary Database:** `database.sqlite` (contains all metadata, IDs, logs, and will contain the semantic index).
   *   **Input Directory:** `0_DATA/input_files/`
   *   **Output Directory Structure:** `0_DATA/output_files/[WitnessNameEN]/[YYYY-MM-DD]/chunk_XXX_ALS-XXXXXXX.txt`
   *   **Core Scripts (First Floor):** `setup_database.py`, `main_processor.py`, and its helper modules.
   *   **Core Scripts (Second Floor - Planned):** `semantic_parser.py`.

## SECTION 4: DEVELOPMENT HISTORY & KEY DECISIONS
### 4.1. Project Timeline (Key Milestones)
   *   **May 2025:** Initial concept & development using Make.com.
   *   **Early June 2025:** **Critical Pivot #1:** Abandoned Make.com/Google Sheets in favor of a robust Python/SQLite system.
   *   **Mid June 2025:** "First Floor" v1.0 Python system completed and validated.
   *   **Mid June 2025:** **Critical Pivot #2:** Adopted the "v20" (Extractor, Cleaner, Composer) architecture for text cleaning.
   *   **Late June 2025:** Completed the first phase of the LLM "Bake-off", evaluating Google's Gemini models. Proceeding to evaluate models from other providers.

### 4.2. Critical Decisions Log
   *   `Decision: Abandon Make.com and re-implement the entire 'First Floor' in Python.`
       *   `Reasoning: The original platform was deemed unreliable, costly, and insufficiently controllable ("בולשיטס", "סמטוכה") for a production system.`
       *   `Status: Implemented`
   *   `Decision: Adopt the "Extractor, Cleaner, Composer" (v20) architecture for text cleaning.`
       *   `Reasoning: Pure LLM-based approaches proved unreliable for simultaneously cleaning text and preserving structural metadata. This architecture correctly separates deterministic and probabilistic tasks.`
       *   `Status: Planned`
   *   `Decision: Conduct a multi-provider LLM bake-off to select the optimal model for semantic analysis.`
       *   `Reasoning: To empirically determine the best model based on quality, cost, and speed, rather than relying on assumptions. The user is the sole decision-maker.`
       *   `Status: In Progress`

### 4.3. Discarded Paths & Lessons Learned
   *   **Abandoned Idea:** The entire Make.com-based architecture.
       *   `Reason: Insufficient control, reliability issues, higher long-term cost.`
   *   **Abandoned Idea:** Using a single LLM call to both clean text and manage structural metadata.
       *   `Reason: Proven to be fundamentally unreliable due to the non-deterministic nature of LLMs.`
   *   **Lesson Learned:** The "Extractor, Cleaner, Composer" pattern is the correct way to combine deterministic code (for structure) and probabilistic LLMs (for language).

## SECTION 5: CURRENT FEATURE STATUS
### 5.1. Implemented Features
   *   **Complete Python-based I/O Pipeline:** A functional application (`main_processor.py`) for processing PDFs into a structured database.
   *   **Robust Database Schema:** A complete, normalized SQLite database schema (`setup_database.py`) is in place.
   *   **Atomic ID & Session Management:** The system uses atomic database transactions for data integrity.
   *   **LLM Evaluation Framework:** The first phase of the LLM bake-off (evaluating Gemini models) is complete, establishing a baseline for further testing.

### 5.2. Work-in-Progress / Next Up
   *   **Status:** The "First Floor" is structurally complete, pending the v20 refactor. The "Second Floor" is in the LLM evaluation phase.
   *   **Next Up (Immediate Priorities):**
       1.  **Continue LLM Bake-off:** Evaluate models from other providers (e.g., Anthropic, OpenAI) against the established benchmarks for quality, cost, and speed.
       2.  **User Decision:** Based on the complete bake-off results, the user will make the final selection of the primary LLM(s).
       3.  **Finalize First Floor:** Implement the "Extractor, Cleaner, Composer" (v20) architecture within `main_processor.py`.
   *   **Next Up (Following Steps):**
       1.  **Develop Semantic Parser:** Once the LLM is selected, develop the `semantic_parser.py` module tailored to its specific JSON output format.
       2.  Implement the full two-pass (Extract/Synthesize) indexing pipeline.
       3.  Develop the Minimum Viable Product (MVP) for the search UI.