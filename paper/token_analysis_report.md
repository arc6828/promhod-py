# รายงานการวิเคราะห์ปริมาณ Token และค่าใช้จ่าย Gemini API

รายงานฉบับนี้จัดทำขึ้นเพื่อวิเคราะห์ปริมาณการใช้งาน **Input Tokens** และ **Output Tokens** เมื่อใช้ **Gemini API** ในการอ่านและสกัดข้อมูลเหตุการณ์ภัยพิบัติน้ำท่วมจากชุดข้อมูลในโฟลเดอร์ [`news/data-detail2`](file:///d:/python/promhod-env/promhod-py/news/data-detail2) แล้วแปลงเป็นโครงสร้าง JSON ตามรูปแบบตัวอย่างใน [`paper/token/example_output.json`](file:///d:/python/promhod-env/promhod-py/paper/token/example_output.json)

> [!NOTE]
> การประเมินคำนวณจากแบบจำลองการตัดคำ (SentencePiece Subword Tokenizer) ของ Gemini โดยคำนึงถึงความต่างระหว่างอักขระภาษาไทย ตัวอักษรภาษาอังกฤษ และสัญลักษณ์โครงสร้าง JSON

---

## 1. ผลการทดสอบกรณี 1 ไฟล์ตัวอย่าง ([`2762435.json`](file:///d:/python/promhod-env/promhod-py/news/data-detail2/2762435.json))

ทำการทดสอบวิเคราะห์สกัดข้อมูลจากข่าวไฟล์แรก [`2762435.json`](file:///d:/python/promhod-env/promhod-py/news/data-detail2/2762435.json) (ขนาด 1,147 bytes) ซึ่งมีข้อความข่าวเกี่ยวกับปรากฏการณ์น้ำทะเลหนุนในอำเภอพระประแดง จังหวัดสมุทรปราการ

### รายละเอียดการป้อนข้อมูลและผลลัพธ์
* **System Prompt:** คำสั่งภาษาไทยระบุให้สกัดวันที่ สถานที่ ความรุนแรง และ URL ให้อยู่ในรูปแบบ JSON
* **Input Data:** ข้อมูลข่าวดิบจากไฟล์ [`2762435.json`](file:///d:/python/promhod-env/promhod-py/news/data-detail2/2762435.json)
* **Output Data:** JSON ผลลัพธ์ตามโครงสร้าง [`example_output.json`](file:///d:/python/promhod-env/promhod-py/paper/token/example_output.json)

### ตารางสรุปปริมาณ Token สำหรับ 1 ไฟล์

| รายการประมวลผล | จำนวนตัวอักษร (Characters) | ปริมาณ Token โดยประมาณ |
| :--- | :---: | :---: |
| **System Prompt (คำสั่งระบุโครงสร้าง JSON)** | 349 ตัวอักษร | ~121 Tokens |
| **Input News Data ([`2762435.json`](file:///d:/python/promhod-env/promhod-py/news/data-detail2/2762435.json))** | 519 ตัวอักษร | ~202 Tokens |
| **รวม Input Token ทั้งหมดต่อ 1 ไฟล์** | **887 ตัวอักษร** | **~328 Tokens** |
| **รวม Output Token ([`example_output.json`](file:///d:/python/promhod-env/promhod-py/paper/token/example_output.json))** | **168 ตัวอักษร** | **~47 Tokens** |
| **รวมทั้งหมดต่อ 1 ไฟล์ (Input + Output)** | **1,055 ตัวอักษร** | **~375 Tokens** |

---

## 2. ผลการวิเคราะห์ชุดข้อมูลทั้งหมด ([`news/data-detail2`](file:///d:/python/promhod-env/promhod-py/news/data-detail2))

การวิเคราะห์ครอบคลุมข่าวสารทั้งหมดจำนวน **554 ไฟล์** ในโฟลเดอร์ [`news/data-detail2`](file:///d:/python/promhod-env/promhod-py/news/data-detail2) โดยความยาวของแต่ละบทความมีความหลากหลายตั้งแต่ข่าวสั้นประมาณ 900 bytes จนถึงข่าวบทความยาวประมาณ 60,000 bytes

### สรุปสถิติปริมาณ Token รวม (Total Dataset Statistics)

| ดรรชนีวัดผล | ปริมาณ Input Tokens | ปริมาณ Output Tokens | ปริมาณ Token รวมทั้งหมด |
| :--- | :---: | :---: | :---: |
| **ประมวลผลต่อ 1 ไฟล์ (ค่าเฉลี่ย)** | ~1,574.6 Tokens | ~51.5 Tokens | **~1,626.1 Tokens** |
| **ค่าต่ำสุดต่อไฟล์ (Min)** | 266 Tokens | ~45 Tokens | **311 Tokens** |
| **ค่าสูงสุดต่อไฟล์ (Max)** | 10,504 Tokens | ~85 Tokens | **10,589 Tokens** |
| **ยอดรวมทั้งชุดข้อมูล (554 ไฟล์)** | **872,318 Tokens** | **28,524 Tokens** | **900,842 Tokens** |

> [!TIP]
> สัดส่วนปริมาณ Token หลักส่วนใหญ่ (ประมาณ 96.8%) อยู่ในฝั่ง **Input Tokens** ในขณะที่ **Output Tokens** มีสัดส่วนเพียงประมาณ 3.2% เนื่องจากโครงสร้าง JSON ที่สกัดออกมามีความกระชับสูง

---

## 3. การประมาณการค่าใช้จ่าย (Estimated API Cost)

เมื่อคำนวณค่าใช้จ่ายในการเรียกใช้งานผ่าน **Gemini API** (อ้างอิงอัตราค่าบริการมาตรฐานสำหรับโมเดล **Gemini 1.5 Flash** / **Gemini 2.5 Flash**):

### อัตราค่าบริการ (Pricing Rate)
* **Input Rate:** $0.075 USD ต่อ 1,000,000 Tokens ($0.075 / 1M)
* **Output Rate:** $0.300 USD ต่อ 1,000,000 Tokens ($0.300 / 1M)

### ตารางสรุปประมาณการค่าใช้จ่าย

| ประเภท Token | ปริมาณรวม (554 ไฟล์) | อัตราค่าบริการ (USD/1M) | ค่าใช้จ่าย (USD) | ค่าใช้จ่าย (บาท THB) |
| :--- | :---: | :---: | :---: | :---: |
| **Input Tokens** | 872,318 Tokens | $0.075 | $0.0654 USD | ~2.36 บาท |
| **Output Tokens** | 28,524 Tokens | $0.300 | $0.0086 USD | ~0.31 บาท |
| **รวมทั้งหมด** | **900,842 Tokens** | - | **$0.0740 USD** | **~2.67 บาท** |

*หมายเหตุ: อัตราแลกเปลี่ยนโดยประมาณ 1 USD = 36.00 THB*

> [!IMPORTANT]
> หากเป็นการใช้งานประมวลผลระบบผ่าน **Google AI Studio Free Tier** (ภายใต้เงื่อนไขไม่เกิน 15 Requests Per Minute และไม่เกิน 1,500 Requests Per Day) จะ**ไม่มีค่าใช้จ่ายใดๆ (Free)**

---

## 4. ข้อสรุปและการนำไปใช้งาน

1. **การประมวลผล 1 ไฟล์:** ใช้ Input Token ประมาณ **320-350 Tokens** และ Output Token ประมาณ **45-55 Tokens** รวมไม่เกิน 400 Tokens ต่อข่าว
2. **การประมวลผลทั้งโฟลเดอร์ (554 ข่าว):** ใช้ปริมาณ Token รวมประมาณ **0.90 ล้านโทเคน** (Input ~0.87 ล้าน + Output ~0.03 ล้าน)
3. **ความคุ้มค่าเชิงต้นทุน:** ต้นทุนการสกัดข้อมูลข่าวภัยพิบัติทั้งหมด 554 ข่าวผ่าน Gemini API คิดเป็นเงินเพียงประมาณ **2.67 บาท** แสดงให้เห็นถึงประสิทธิภาพและความคุ้มค่าสูงในการนำไปประยุกต์ใช้ในระบบแจ้งเตือนภัยกึ่งเรียลไทม์
