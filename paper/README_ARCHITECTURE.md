# โค้ดสำหรับสร้างแผนภาพสถาปัตยกรรมระบบ (Mermaid Code for Figure 1)

ไฟล์นี้จัดเก็บซอร์สโค้ด Mermaid ที่ใช้สร้างแผนภาพสถาปัตยกรรมระบบกึ่งอัตโนมัติและการไหลของข้อมูล (System Architecture and Data Flow Diagram) ของบทความวิจัย

## Mermaid Code

```mermaid
graph TD
    subgraph Data_Source ["1. ชั้นนำเข้าข้อมูล (Data Ingestion)"]
        A[แหล่งข่าวออนไลน์ / สื่อดิจิทัลด้านภัยพิบัติ] -->|ดึงหน้าเว็บ HTML| B(Node.js Web Scraper)
        B -->|ทำความสะอาดและแปลงเป็นข่าวดิบ Raw Text| C[n8n Workflow Orchestrator]
    end

    subgraph Processing_Layer ["2. ชั้นประมวลผลข้อมูล (Orchestration & NLP)"]
        C -->|ส่ง Raw Text + คำสั่ง Prompt| D(Google Gemini API)
        D -->|ประมวลผลวิเคราะห์และส่งออก JSON Structure| C
    end

    subgraph Output_Layer ["3. ชั้นแสดงผลข้อมูล (Data Visualization)"]
        C -->|บันทึกและรวบรวม| E[ระบบฐานข้อมูลอัจฉริยะ JSON Database]
        E --> F[แดชบอร์ดสรุปเหตุการณ์กึ่งเรียลไทม์]
        E --> G[แผนที่ความร้อนแสดงพิกัดพื้นที่ภัยพิบัติ Heat Map]
    end

    classDef source fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    classDef process fill:#efebe9,stroke:#795548,stroke-width:2px;
    classDef output fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    class A,B source;
    class C,D process;
    class E,F,G output;
```
