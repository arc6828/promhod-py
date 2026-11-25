import os
import re
import io
import zipfile
import docx
from PIL import Image
from docx.oxml.ns import qn
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table

DOCX_FILE = r"docx/5_พ.ค_69 Edit_รายงานฉบับสมบูรณ์ Ch1_Ch5.docx"
OUTPUT_DIR = r"docx/markdown"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

os.makedirs(IMAGES_DIR, exist_ok=True)

print("Opening docx...")
doc = docx.Document(DOCX_FILE)
rels = doc.part.rels
body_elements = list(doc.element.body)

# Step 1: Image mapping
image_map = {}
with zipfile.ZipFile(DOCX_FILE, 'r') as z:
    for filename in z.namelist():
        if filename.startswith('word/media/'):
            base_name = os.path.basename(filename)
            ext = os.path.splitext(base_name)[1].lower()
            
            out_filename = base_name
            if ext == '.emf':
                out_filename = os.path.splitext(base_name)[0] + '.png'
                out_path = os.path.join(IMAGES_DIR, out_filename)
                if not os.path.exists(out_path):
                    raw_data = z.read(filename)
                    try:
                        img = Image.open(io.BytesIO(raw_data))
                        img.save(out_path, format='PNG')
                    except Exception as e:
                        out_path = os.path.join(IMAGES_DIR, base_name)
                        with open(out_path, 'wb') as f:
                            f.write(raw_data)
                        out_filename = base_name
            else:
                out_path = os.path.join(IMAGES_DIR, out_filename)
                if not os.path.exists(out_path):
                    raw_data = z.read(filename)
                    with open(out_path, 'wb') as f:
                        f.write(raw_data)
            
            image_map[f"media/{base_name}"] = f"images/{out_filename}"
            image_map[f"word/media/{base_name}"] = f"images/{out_filename}"

print(f"Mapped {len(image_map)} image targets.")

# Step 2: Helper for table conversion
def format_table(tbl):
    rows_data = []
    # Fast row cell extraction
    for row in tbl.rows:
        row_cells = []
        for cell in row.cells:
            t = " ".join(cell.text.split())
            row_cells.append(t)
        rows_data.append(row_cells)
    
    if not rows_data or not rows_data[0]:
        return ""
    
    num_cols = len(rows_data[0])
    cleaned_rows = [r[:num_cols] for r in rows_data]
    h0 = cleaned_rows[0]
    
    lines = []
    header = [c if c else f"คอลัมน์ {i+1}" for i, c in enumerate(h0)]
    
    seen = {}
    for i, h in enumerate(header):
        if h in seen:
            seen[h] += 1
            header[i] = f"{h} ({seen[h]})"
        else:
            seen[h] = 1
            
    sep = [":---"] * len(header)
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(sep) + " |")
    
    for row in cleaned_rows[1:]:
        non_empty = [c for c in row if c]
        if non_empty and all(c == non_empty[0] for c in non_empty) and len(non_empty) > 1:
            span_row = [f"**{non_empty[0]}**"] + [""] * (num_cols - 1)
            lines.append("| " + " | ".join(span_row) + " |")
        else:
            lines.append("| " + " | ".join(row) + " |")
            
    return "\n" + "\n".join(lines) + "\n"

# Step 3: Helper for OMML equations
def get_equation(p):
    eqs = p._element.xpath('.//m:oMath | .//m:oMathPara')
    if not eqs:
        return None
    m_texts = [t.text.strip() for t in p._element.xpath('.//m:t') if t.text and t.text.strip()]
    math_str = " ".join(m_texts)
    
    if 'X X N' in math_str or 'X = X N' in math_str or ('X' in m_texts and 'N' in m_texts and len(m_texts) <= 5):
        return r"$$\bar{X} = \frac{\sum X}{N}$$"
    elif 'SD=' in math_str or 'SD' in math_str:
        return r"$$SD = \sqrt{\frac{N \sum X^2 - (\sum X)^2}{N(N - 1)}}$$"
    elif 'IOC=' in math_str or 'IOC' in math_str:
        return r"$$IOC = \frac{\sum R}{N}$$"
    elif 'α =' in math_str or 'α' in math_str or 'S i 2' in math_str:
        return r"$$\alpha = \frac{n}{n - 1} \left(1 - \frac{\sum S_i^2}{S_t^2}\right)$$"
    elif math_str:
        return f"$${math_str}$$"
    return None

# Step 4: Sections definition
SECTION_RANGES = [
    {
        "id": "00_front_matter",
        "title": "ปกหน้าและบทคัดย่อ (Front Matter)",
        "file": "00_front_matter.md",
        "start": 0,
        "end": 126
    },
    {
        "id": "01_chapter1_introduction",
        "title": "บทที่ 1 บทนำ",
        "file": "01_chapter1_introduction.md",
        "start": 126,
        "end": 200
    },
    {
        "id": "02_chapter2_literature_review",
        "title": "บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง",
        "file": "02_chapter2_literature_review.md",
        "start": 200,
        "end": 562
    },
    {
        "id": "03_chapter3_methodology",
        "title": "บทที่ 3 วิธีการดำเนินการวิจัย",
        "file": "03_chapter3_methodology.md",
        "start": 562,
        "end": 734
    },
    {
        "id": "04_chapter4_results",
        "title": "บทที่ 4 ผลการวิจัย",
        "file": "04_chapter4_results.md",
        "start": 734,
        "end": 1006
    },
    {
        "id": "05_chapter5_conclusion",
        "title": "บทที่ 5 สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ",
        "file": "05_chapter5_conclusion.md",
        "start": 1006,
        "end": 1055
    },
    {
        "id": "06_references",
        "title": "บรรณานุกรม",
        "file": "06_references.md",
        "start": 1055,
        "end": 1129
    },
    # 1129 to 1359 is Appendix (ภาคผนวก) - omitted as requested
    {
        "id": "07_researchers",
        "title": "ประวัติผู้วิจัย",
        "file": "07_researchers.md",
        "start": 1359,
        "end": len(body_elements)
    }
]

# Helper to process a range of body elements into markdown text
def process_range(start_idx, end_idx, sec_id):
    md_output = []
    
    idx = start_idx
    while idx < end_idx:
        child = body_elements[idx]
        
        if isinstance(child, CT_Tbl):
            tbl = Table(child, doc)
            tbl_md = format_table(tbl)
            md_output.append(tbl_md)
            idx += 1
            continue
            
        elif isinstance(child, CT_P):
            p = Paragraph(child, doc)
            text = p.text.strip()
            
            # Check drawings/images inside paragraph
            blips = child.xpath('.//a:blip')
            if blips:
                for b in blips:
                    rId = b.get(qn('r:embed'))
                    if rId and rId in rels:
                        target = rels[rId].target_ref
                        mapped_path = image_map.get(target, image_map.get(f"word/{target}", ""))
                        if mapped_path:
                            cap_text = ""
                            for ahead in range(idx + 1, min(end_idx, idx + 4)):
                                if isinstance(body_elements[ahead], CT_P):
                                    at = Paragraph(body_elements[ahead], doc).text.strip()
                                    if re.match(r'^(ภาพที่|รูปที่)\s*\d+', at):
                                        cap_text = at
                                        break
                            if cap_text:
                                md_output.append(f"\n![{cap_text}]({mapped_path})\n")
                            else:
                                md_output.append(f"\n![]({mapped_path})\n")
            
            # Check equation
            eq = get_equation(p)
            if eq:
                md_output.append(f"\n{eq}\n")
                idx += 1
                continue
                
            if not text:
                idx += 1
                continue
                
            # Formatting headings based on text patterns
            if re.match(r'^บทที่\s+\d+', text):
                next_title = ""
                if idx + 1 < end_idx and isinstance(body_elements[idx+1], CT_P):
                    nt = Paragraph(body_elements[idx+1], doc).text.strip()
                    if nt and not re.match(r'^\d+\.\d+', nt):
                        next_title = nt
                        idx += 1
                if next_title:
                    md_output.append(f"\n# {text} {next_title}\n")
                else:
                    md_output.append(f"\n# {text}\n")
            elif text in ['บรรณานุกรม', 'ประวัติผู้วิจัย']:
                md_output.append(f"\n# {text}\n")
            elif text in ['บทคัดย่อ', 'Abstract', 'กิตติกรรมประกาศ', 'สารบัญ', 'สารบัญตาราง', 'สารบัญภาพ']:
                md_output.append(f"\n## {text}\n")
            elif re.match(r'^\d+\.\d+\.\d+\.\d+', text):
                md_output.append(f"\n#### {text}\n")
            elif re.match(r'^\d+\.\d+\.\d+', text):
                md_output.append(f"\n### {text}\n")
            elif re.match(r'^\d+\.\d+\s+', text) or re.match(r'^\d+\.\d+$', text):
                md_output.append(f"\n## {text}\n")
            elif re.match(r'^(ภาพที่|รูปที่|ตารางที่)\s*\d+', text):
                md_output.append(f"\n**{text}**\n")
            elif re.match(r'^(ชื่อ\s*[-–]\s*สกุล)\s*', text):
                md_output.append(f"\n### {text}\n")
            elif re.match(r'^(ตำแหน่งทางวิชาการ|สังกัด/หน่วยงาน|ประวัติการศึกษา|งานวิจัย)', text):
                md_output.append(f"\n**{text}**\n")
            elif text.startswith('คำสำคัญ:') or text.startswith('Keywords:'):
                md_output.append(f"\n**{text}**\n")
            elif re.match(r'^\(?\d+\)?\s+', text) or text.startswith('- ') or text.startswith('• '):
                md_output.append(f"{text}\n")
            else:
                md_output.append(f"{text}\n\n")
                
            idx += 1
        else:
            # Other elements like sectPr, bookmark, etc.
            idx += 1
            
    raw_content = "".join(md_output)
    cleaned = re.sub(r'\n{3,}', '\n\n', raw_content).strip()
    return cleaned

# Step 5: Execute extraction for each section
extracted_files = []
for sec in SECTION_RANGES:
    print(f"Processing {sec['id']} (elements {sec['start']}..{sec['end']})...")
    content = process_range(sec['start'], sec['end'], sec['id'])
    
    out_file_path = os.path.join(OUTPUT_DIR, sec['file'])
    with open(out_file_path, 'w', encoding='utf-8') as f:
        f.write(content + "\n")
    
    extracted_files.append((sec['title'], sec['file'], len(content)))
    print(f" -> Wrote {sec['file']} ({len(content)} characters)")

# Step 6: Create README.md in docx/markdown/ and docx/README.md
readme_content = f"""# รายงานฉบับสมบูรณ์: การพัฒนาระบบรวบรวมข้อมูลขนาดใหญ่ พยากรณ์และแจ้งเตือนภัยจากอุทกภัย-ภัยแล้งในพื้นที่ลุ่มน้ำพรมโหด และเขตพัฒนาเศรษฐกิจพิเศษสระแก้ว

**Implementation of Big data collection system Forecasts and alerts from floods - droughts in the Phromhod Basin and SaKaeo Special Economic Zone**

---

### โครงการวิจัย
- **หัวหน้าโครงการและคณะผู้วิจัย:** 
  - อาจารย์ชวลิต โควีระวงศ์ (หัวหน้าโครงการ)
  - ผู้ช่วยศาสตราจารย์ ดร.รัตถชล อ่างมณี
  - ผู้ช่วยศาสตราจารย์ไพรินทร์ มีศรี
  - อาจารย์ ดร. ดาวรถา วีระพันธ์
  - อาจารย์นิธิพนธ์ น้อยเผ่า
- **หน่วยงาน:** คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยราชภัฏวไลยอลงกรณ์ ในพระบรมราชูปถัมภ์
- **แหล่งทุน:** สำนักงานคณะกรรมการส่งเสริมวิทยาศาสตร์ วิจัยและนวัตกรรม (สกสว.) ปีงบประมาณ 2567

---

## สารบัญเอกสาร (Table of Contents)

เอกสารฉบับนี้ได้รับการสกัดและจัดโครงสร้างเป็นไฟล์ Markdown (.md) ย่อยๆ ตามบท เพื่อความสะดวกในการอ่าน ค้นหา และนำไปประมวลผลต่อ ดังนี้:

| ลำดับ | บท / ส่วนของรายงาน | ชื่อไฟล์ | คำอธิบายสาระสำคัญ |
| :---: | :--- | :--- | :--- |
| 00 | **ปกหน้าและบทคัดย่อ** | [00_front_matter.md](00_front_matter.md) | ข้อมูลโครงการวิจัย, รายชื่อผู้วิจัย, บทคัดย่อภาษาไทย, Abstract ภาษาอังกฤษ, กิตติกรรมประกาศ, สารบัญ |
| 01 | **บทที่ 1 บทนำ** | [01_chapter1_introduction.md](01_chapter1_introduction.md) | ความเป็นมาและความสำคัญ, วัตถุประสงค์, ขอบเขตการวิจัย, นิยามศัพท์เฉพาะ, ประโยชน์ที่คาดว่าจะได้รับ |
| 02 | **บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง** | [02_chapter2_literature_review.md](02_chapter2_literature_review.md) | ข้อมูลลำน้ำและแหล่งน้ำธรรมชาติสระแก้ว, พื้นที่เสี่ยงภัยแล้ง-น้ำท่วม, แผนบริหารจัดการน้ำ, แบบจำลองทางชลศาสตร์ MIKE 21, ระบบรวบรวม Big Data, การทำเหมืองข้อความและ NLP ข่าวสารน้ำท่วม, LINE OA และ Web Application |
| 03 | **บทที่ 3 วิธีการดำเนินการวิจัย** | [03_chapter3_methodology.md](03_chapter3_methodology.md) | ประชากรและกลุ่มตัวอย่าง, เครื่องมือวิจัย, สถาปัตยกรรมระบบ, การออกแบบโมเดลพยากรณ์ฝน, การจำลองการระบายน้ำ, สูตรสถิติที่ใช้ในการประเมิน (ค่าเฉลี่ย, SD, IOC, Cronbach's Alpha) |
| 04 | **บทที่ 4 ผลการวิจัย** | [04_chapter4_results.md](04_chapter4_results.md) | ผลการพัฒนาระบบพยากรณ์ฝนจากเรดาร์ (RMSE, $R^2$), ผลแบบจำลองโครงข่ายระบายน้ำ, ผลระบบรวบรวม Big Data ข่าวสารน้ำท่วม, ผลการพัฒนาระบบ Web Platform และ LINE OA, ผลการประเมินประสิทธิภาพและความพึงพอใจ |
| 05 | **บทที่ 5 สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ** | [05_chapter5_conclusion.md](05_chapter5_conclusion.md) | สรุปผลการวิจัยทั้ง 4 ด้าน, อภิปรายผลการวิจัย, ข้อเสนอแนะเชิงนโยบายและแนวทางการพัฒนาต่อยอด |
| 06 | **บรรณานุกรม** | [06_references.md](06_references.md) | รายการเอกสารอ้างอิงและงานวิจัยที่เกี่ยวข้องทั้งภาษาไทยและภาษาอังกฤษ |
| 07 | **ประวัติผู้วิจัย** | [07_researchers.md](07_researchers.md) | ข้อมูลประวัติส่วนตัว, วุฒิการศึกษา, และผลงานวิจัย/สิ่งตีพิมพ์ทางวิชาการของคณะผู้วิจัย |

> **หมายเหตุ:** ส่วนภาคผนวก (ก, ข, ค: แบบประเมิน หนังสือขออนุญาต และภาพกิจกรรม) ได้รับการยกเว้นไม่ต้องนำมารวมตามข้อกำหนด โดยยังคงเก็บประวัตินักวิจัยไว้อย่างครบถ้วน

---

## ทรัพยากรเพิ่มเติม
- รูปภาพ แผนที่ ไดอะแกรม และแผนภาพประกอบทั้งหมดถูกจัดเก็บอยู่ในโฟลเดอร์ [`images/`](images/)
"""

with open(os.path.join(OUTPUT_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

root_readme_content = f"""# ข้อมูลรายงานวิจัยฉบับสมบูรณ์ (DOCX -> Markdown)

โฟลเดอร์นี้บรรจุเอกสารรายงานฉบับสมบูรณ์เรื่อง:
**การพัฒนาระบบรวบรวมข้อมูลขนาดใหญ่ พยากรณ์และแจ้งเตือนภัยจากอุทกภัย-ภัยแล้งในพื้นที่ลุ่มน้ำพรมโหด และเขตพัฒนาเศรษฐกิจพิเศษสระแก้ว**

เอกสารถูกสกัดจากไฟล์ต้นฉบับ `5_พ.ค_69 Edit_รายงานฉบับสมบูรณ์ Ch1_Ch5.docx` และจัดแบ่งเป็นไฟล์ Markdown (.md) ย่อยๆ อย่างเป็นระเบียบในโฟลเดอร์ **`markdown/`**:

### เอกสารย่อยในโฟลเดอร์ `markdown/`:
1. [สารบัญภาพรวมและคำนำ (markdown/README.md)](markdown/README.md)
2. [ปกหน้าและบทคัดย่อ (00_front_matter.md)](markdown/00_front_matter.md)
3. [บทที่ 1 บทนำ (01_chapter1_introduction.md)](markdown/01_chapter1_introduction.md)
4. [บทที่ 2 เอกสารและงานวิจัยที่เกี่ยวข้อง (02_chapter2_literature_review.md)](markdown/02_chapter2_literature_review.md)
5. [บทที่ 3 วิธีการดำเนินการวิจัย (03_chapter3_methodology.md)](markdown/03_chapter3_methodology.md)
6. [บทที่ 4 ผลการวิจัย (04_chapter4_results.md)](markdown/04_chapter4_results.md)
7. [บทที่ 5 สรุปผลการวิจัย อภิปรายผล และข้อเสนอแนะ (05_chapter5_conclusion.md)](markdown/05_chapter5_conclusion.md)
8. [บรรณานุกรม (06_references.md)](markdown/06_references.md)
9. [ประวัติผู้วิจัย (07_researchers.md)](markdown/07_researchers.md)

*หมายเหตุ: ไม่รวมภาคผนวก (Appendix) ตามที่ได้รับมอบหมาย โดยคงประวัตินักวิจัยไว้ครบถ้วน*
"""

with open(os.path.join("docx", "README.md"), "w", encoding="utf-8") as f:
    f.write(root_readme_content)

print("All files generated successfully!")
