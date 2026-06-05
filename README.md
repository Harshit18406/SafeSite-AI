# SafeSite-AI
## System Architecture & Technical Specifications

The SafeSite AI Engine framework decouples experimental model training from production edge execution. The system is engineered to handle parallel processing streams while maintaining low-latency inference boundaries.

### Core Architecture Modules

#### 1. Optimization & Weights Training Pipeline
* **Environment:** Distributed Cloud (Google Colab)
* **Source Module:** `Workers_Safety.ipynb`
* **Functional Scope:** Ingests raw safety compliance imagery, manages mosaic and spatial data augmentations, executes hyperparameter optimization loops, and exports optimized FP16/FP32 tensor weights upon convergence.

#### 2. Local Hardware Edge Deployment
* **Environment:** Native Local Runtime (VS Code Execution)
* **Source Module:** `webcam_inference.py`
* **Functional Scope:** Initializes a localized OpenCV hardware stream to capture physical environment inputs. Live camera frames are piped directly into the compiled YOLOv8 inference engine, applying class-specific confidence thresholds and rendering instantaneous bounding boxes without external cloud dependencies.

---

## Technical Features & Performance Standards

* **Real-Time Stream Processing:** Implements memory-efficient generator-based streaming sequences to prevent memory leaks during continuous monitoring loops.
* **Automated Telemetry Logs:** Generates structured runtime analytics (`safety_logs.csv`) tracking time-stamped compliance events and confidence statistics for audit trails.
* **Low Compute Overhead:** Designed to execute on consumer-grade CPU and GPU hardware by optimizing video frame dimensions during the pre-processing vector stage.

---

