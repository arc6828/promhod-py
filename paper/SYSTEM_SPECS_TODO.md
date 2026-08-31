# บันทึกข้อกำหนดสเปกเครื่องคอมพิวเตอร์และเวอร์ชันซอฟต์แวร์สำหรับการทดลอง (Hardware & Software Specifications)

> **บันทึกเมื่อ:** 31 สิงหาคม 2569  
> **ไฟล์เป้าหมายที่จะนำไปอัปเดต:** [paper/README.md](file:///e:/chavalit/python/promhod-env2/promhod-py/paper/README.md), [paper/Readme2.md](file:///e:/chavalit/python/promhod-env2/promhod-py/paper/Readme2.md) และเอกสารต้นฉบับบทความ (Word / Paper2.docx)  
> **วัตถุประสงค์:** ระบุรายละเอียดสภาพแวดล้อมเชิงวิศวกรรมคอมพิวเตอร์ (CPU, RAM, GPU, OS, Node.js, n8n, Gemini API) เพื่อตอบข้อเสนอแนะของผู้ทรงคุณวุฒิ และเพิ่มความน่าเชื่อถือทางวิชาการในการทำซ้ำการทดลอง (Reproducibility)

---

## 1. ข้อมูลสเปกเครื่องประมวลผลและสภาพแวดล้อมที่ใช้จริง (Actual Environment Specs)

จากข้อมูลการตรวจสอบระบบคอมพิวเตอร์ที่ใช้ในการทดลอง (เครื่องหลัก DESKTOP-N6LMV26):

| รายการทรัพยากร | รายละเอียดคุณสมบัติ (Specifications) | หมายเหตุเชิงเทคนิคในงานวิจัย |
| :--- | :--- | :--- |
| **หน่วยประมวลผล (CPU)** | Intel(R) Core(TM) i5-10500 CPU @ 3.10 GHz | สถาปัตยกรรม 6 Cores, 12 Threads (Base 3.10 GHz, Turbo Boost สูงสุด 4.50 GHz) |
| **หน่วยความจำหลัก (RAM)** | 12.0 GB DDR4 (ความเร็วบัส 3,200 MHz) | ใช้งานได้จริงประมาณ 11.8 GB |
| **หน่วยประมวลผลกราฟิก (GPU)** | Intel(R) UHD Graphics 630 (Integrated GPU แบบออนบอร์ด 128 MB) | **ไม่มีการติดตั้งการ์ดจอแยก (Discrete GPU)** ทำให้การรันโมเดล WangchanBERTa เป็นการรันบน CPU-only mode ทั้งหมด |
| **หน่วยจัดเก็บข้อมูล (Storage)** | 240 GB SSD (WDC) + 2.0 TB HDD (Seagate) | ระบบรันไทม์และสคริปต์ทำงานบนไดรฟ์ SSD ความเร็วสูง |
| **ระบบปฏิบัติการ (OS)** | Microsoft Windows 10 Pro 64-bit | - |
| **Node.js Runtime** | Node.js v22.21.1 (LTS) | ใช้งานสถาปัตยกรรม Asynchronous Non-blocking I/O และ Event Loop |
| **Workflow Engine** | n8n (Visual Workflow Automation) | ควบคุมลำดับการสกัดและส่งข้อมูลข้ามแพลตฟอร์ม |
| **Large Language Model API** | Google Gemini API (โมเดล `gemini-1.5-flash`) | เรียกใช้ผ่าน Google AI Studio REST API แบบ Zero-shot Prompting |
| **Baseline Model (ระบบเดิม)** | `airesearch/wangchanberta-base-att-spm-uncased` | รันผ่าน Python 3.10+, PyTorch (CPU Inference) และ Transformers |

---

## 2. ตำแหน่งที่ต้องนำข้อมูลไปใส่ในบทความวิจัย

### 📌 ตำแหน่งที่ 1: หัวข้อ `3.4 ระเบียบวิธีการทดลองและประเมินผล` (Methodology)
* **จุดประสงค์:** กำหนดเป็นหัวข้อย่อยหรือตารางระบุสภาพแวดล้อมการทดลอง (Experimental Setup) เพื่อแสดงความรัดกุมเชิงวิทยาศาสตร์
* **เนื้อหาและตารางที่เตรียมไว้ใส่:**

```markdown
### 3.4 ระเบียบวิธีการทดลองและสภาพแวดล้อมการทดสอบ (Experimental Setup)

ในการประเมินประสิทธิภาพของระบบกึ่งอัตโนมัติที่เสนอ ได้ดำเนินการทดลองเปรียบเทียบร่วมกับระบบเดิม (Python Script ร่วมกับแบบจำลองภาษา WangchanBERTa) บนชุดข้อมูลข่าวอุทกภัยออนไลน์ปี พ.ศ. 2567 จำนวน 555 ข่าว ภายใต้สภาพแวดล้อมฮาร์ดแวร์และซอฟต์แวร์เครื่องประมวลผลเดียวกันทั้งหมด เพื่อให้ผลการทดลองมีความเที่ยงตรงและสามารถทำการทดลองซ้ำได้ (Reproducibility) โดยมีรายละเอียดข้อกำหนดดังแสดงในตารางที่ X

ตารางที่ X ข้อกำหนดสภาพแวดล้อมระบบฮาร์ดแวร์และซอฟต์แวร์ที่ใช้ในการทดลอง

| องค์ประกอบระบบ | รายการอุปกรณ์ / เครื่องมือ | ข้อมูลจำเพาะและเวอร์ชัน (Specifications & Versions) |
| :--- | :--- | :--- |
| **สภาพแวดล้อมฮาร์ดแวร์** | หน่วยประมวลผลกลาง (CPU) | Intel(R) Core(TM) i5-10500 @ 3.10 GHz (6 Cores / 12 Threads) |
| | หน่วยความจำหลัก (RAM) | 12.0 GB DDR4 (3,200 MHz) |
| | หน่วยประมวลผลกราฟิก (GPU) | Intel(R) UHD Graphics 630 (Integrated GPU 128 MB / CPU Inference) |
| | หน่วยจัดเก็บข้อมูล (Storage) | 240 GB Solid State Drive (SSD) |
| | ระบบปฏิบัติการ (OS) | Microsoft Windows 10 Pro (64-bit) |
| **ระบบเดิม (Baseline)** | รันไทม์และสภาพแวดล้อม | Python 3.10+ (Jupyter Environment) |
| | ตัวแบบภาษาและการสกัดคำ | WangchanBERTa (`airesearch/wangchanberta-base-att-spm-uncased`) รันบน PyTorch (CPU-only) |
| **ระบบใหม่ที่เสนอ (Proposed)**| รันไทม์หลัก (Runtime) | Node.js v22.21.1 |
| | แพลตฟอร์มเวิร์กโฟลว์ | n8n Workflow Automation Engine |
| | โมเดลภาษาขนาดใหญ่ (LLM) | Google Gemini API (โมเดล `gemini-1.5-flash` ผ่าน REST API) |
```

---

### 📌 ตำแหน่งที่ 2: คำอธิบายประกอบ `ตารางที่ 1` ในหัวข้อ `4.1 เปรียบเทียบเวลาในการประมวลผล (Durations)`
* **จุดประสงค์:** ชี้แจงเหตุผลทางเทคนิคคอมพิวเตอร์ว่าทำไม WangchanBERTa ถึงใช้เวลา 862 วินาที ขณะที่ Gemini API ใช้เวลา 672 วินาที (ตอบข้อคิดเห็นของผู้ทรงคุณวุฒิ)
* **ข้อความที่เตรียมไว้ใส่:**

> "เมื่อพิจารณาในขั้นตอนการประมวลผลโมเดลภาษา (NER vs. LLM) สาเหตุที่ระบบใหม่ใช้เวลาน้อยกว่าระบบเดิม (ลดลงจาก 862 วินาที เหลือ 672 วินาที) มีความสัมพันธ์โดยตรงกับข้อจำกัดทางสถาปัตยกรรมฮาร์ดแวร์ โดยในระบบเดิมนั้น ตัวแบบภาษา WangchanBERTa ซึ่งเป็นโครงข่ายประสาทแบบ Transformer ถูกประมวลผลภายในเครื่องทดสอบที่ใช้หน่วยประมวลผล Intel Core i5-10500 โดย**ไม่มีหน่วยประมวลผลกราฟิกแยก (Discrete GPU Acceleration)** ทำให้ต้องพึ่งพาการคำนวณเวกเตอร์พารามิเตอร์ผ่านซีพียูเพียงอย่างเดียว (CPU-only inference) จึงก่อให้เกิดภาระความหน่วงสะสมสูง ในขณะที่ระบบใหม่ใช้การ Offload ภาระการคำนวณโมเดลภาษาขนาดใหญ่ไปยัง Gemini 1.5 Flash API ซึ่งทำงานบนระบบคลาวด์คลัสเตอร์สมรรถนะสูงของ Google ร่วมกับสถาปัตยกรรม Asynchronous Non-blocking I/O ของ Node.js v22 ที่ส่งคำร้องขอแบบขนานพร้อมกันได้ ทำให้สามารถก้าวข้ามข้อจำกัดของฮาร์ดแวร์ระดับเครื่องคอมพิวเตอร์ส่วนบุคคลได้อย่างมีประสิทธิภาพ"

---

## 3. รายการสิ่งที่ต้องทำต่อไป (Checklist)

- [ ] 1. นำตารางสเปกฮาร์ดแวร์/ซอฟต์แวร์ ไปใส่ในหัวข้อ `3.4` ของ [paper/README.md](file:///e:/chavalit/python/promhod-env2/promhod-py/paper/README.md)
- [ ] 2. นำคำอธิบายข้อจำกัด CPU/GPU ไปเสริมในหัวข้อ `4.1` ใต้ตารางที่ 1 ของ [paper/README.md](file:///e:/chavalit/python/promhod-env2/promhod-py/paper/README.md)
- [ ] 3. ตรวจสอบเวอร์ชันเจาะจงของ n8n (กรณีรันผ่าน Docker หรือ Desktop Application) เพื่อเติมเลข Release ย่อย (เช่น v1.x)
- [ ] 4. อัปเดตข้อมูลชุดเดียวกันนี้ลงในไฟล์ต้นฉบับบทความ Microsoft Word (`Paper2.docx`)
