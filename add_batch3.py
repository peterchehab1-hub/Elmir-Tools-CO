import os
import json
from PIL import Image

BATCH3_ITEMS = [
    {
        "id": 259,
        "ref_no": "REF #259",
        "part_number": "ET-259",
        "name_en": "AUTOOL PT640 Digital GDI Fuel Pressure Gauge Kit",
        "name_ar": "جهاز فحص ضغط طرمبة البنزين GDI ديجيتال أوتول PT640",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "AUTOOL PT640 digital GDI fuel pressure tester. Engineered specifically for direct-injection (GDI) and high-pressure fuel systems, with high-accuracy pressure transducer (up to 426 PSI / 30 bar), illuminated digital LCD display, min/max recording, and quick-connect brass fittings in hard case.",
        "description_ar": "جهاز فحص ضغط الوقود وطرمبة البنزين GDI ديجيتال متطور ماركة أوتول موديل PT640. مخصص لأنظمة الحقن المباشر والبنزين عالي الضغط، شاشة رقمية بإضاءة خلفية، تسجيل أعلى وأدنى ضغط، وطقم وصلات نحاسية سريعة في حقيبة صلبة.",
        "image": "images/products/259.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.57.07 PM.jpeg",
        "specs": ["AUTOOL PT640", "GDI High Pressure", "Digital LCD Display", "Min/Max Memory", "Brass Adapters"]
    },
    {
        "id": 260,
        "ref_no": "REF #260",
        "part_number": "ET-260",
        "name_en": "THINKCAR THINKTOOL MASTER Diagnostic Station with Full Adapter Kit",
        "name_ar": "جهاز فحص السيارات الشامل ثينك تول ماستر مع حقيبة الوصلات الكاملة",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "Flagship THINKTOOL MASTER automotive diagnostic workstation. Complete package includes heavy duty rugged transport case, high-performance tablet with modular connector dock, wireless VCI, programming harness, and complete non-OBD2 vehicle adapter plugs (Mercedes 38-pin, BMW 20-pin, Fiat 3-pin, etc.).",
        "description_ar": "محطة فحص السيارات المتقدمة ثينك تول ماستر (ThinkTool Master) الشاملة. تتضمن الجهاز اللوحي، وصلة VCI اللاسلكية، حقيبة صلبة مصفحة، وطقم كامل من وصلات وفيش السيارات القديمة والحديثة (مرسيدس ٣٨ بن، بي إم دبليو ٢٠ بن، فيات، نيسان وغيرها).",
        "image": "images/products/260.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.57.07 PM (4).jpeg",
        "specs": ["ThinkTool Master", "Full Adapter Case", "Online ECU Programming", "Topology Mapping", "Non-OBD2 Harnesses", "Heavy Duty Case"]
    },
    {
        "id": 261,
        "ref_no": "REF #261",
        "part_number": "ET-261",
        "name_en": "THINKCAR THINKTOOL SE Diagnostic Scanner Package with Carry Case",
        "name_ar": "جهاز فحص وتشخيص السيارات ثينك تول SE مع حقيبة والوصلات",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "THINKCAR ThinkTool SE professional diagnostic scan tool kit. Features heavy duty shock-absorbent rubber bumper tablet, wireless diagnostic dongle, complete multi-pin adapter cables, power clamp cables, and custom blow-mold carry case.",
        "description_ar": "طقم جهاز فحص وتشخيص السيارات الاحترافي ثينك تول SE. يتميز بتابلت محمي بحواف مطاطية ضد الصدمات، دونجل فحص لاسلكي، كابلات التوصيل المتنوعة، مشابك بطارية، وحقيبة حماية مخصصة.",
        "image": "images/products/261.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.57.07 PM (5).jpeg",
        "specs": ["ThinkTool SE", "Rugged Tablet", "Full Cable Kit", "Battery Clamps", "Hard Carry Case", "OE-Level Diagnostics"]
    },
    {
        "id": 262,
        "ref_no": "REF #262",
        "part_number": "ET-262",
        "name_en": "AUTOOL EM365 Inverter Programmed Power Supply & Battery Charger (12V/100A)",
        "name_ar": "باور سبلاي وشاحن بطاريات لبرمجة كمبيوترات السيارات أوتول EM365",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "AUTOOL EM365 professional automotive inverter programmed power supply and battery recovery charger. Delivers clean, ripple-free constant voltage/current (12V / 100A, up to 3800W) essential to prevent ECU bricking during diagnostic scanning, module flashing, and key coding.",
        "description_ar": "جهاز مزود طاقة وبرمجة وشاحن بطاريات عاكس أوتول EM365. يوفر تياراً ثابتاً ونقياً بقدرة ١٢ فولت / ١٠٠ أمبير (حتى ٣٨٠٠ واط) ضروري لحماية كمبيوترات السيارات من التلف أثناء عمليات البرمجة وتحديث السوفتوير.",
        "image": "images/products/262.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.57.07 PM (6).jpeg",
        "specs": ["AUTOOL EM365", "12V / 100A Output", "ECU Flashing Power", "Battery Recovery Mode", "Color LCD Screen", "Pure Stable DC"]
    },
    {
        "id": 263,
        "ref_no": "REF #263",
        "part_number": "ET-263",
        "name_en": "AUTOOL PT620 Digital Engine Oil Pressure Tester Gauge Set",
        "name_ar": "جهاز فحص ساعة ضغط زيت المحرك ديجيتال أوتول PT620",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "AUTOOL PT620 high-accuracy digital engine oil pressure gauge test kit. Features heavy duty oil pressure transducer sensor (up to 426 PSI), backlit digital screen displaying real-time pressure, peak/minimum values, differential pressure, and 14 brass adapters in hard case.",
        "description_ar": "طقم ساعة فحص ضغط زيت محرك السيارة ديجيتال أوتول PT620. مزود بحساس ضغط عالي الدقة (حتى ٤٢٦ رطل/بوصة مربعة)، شاشة رقمية تعرض القيمة الفورية وأعلى/أدنى ضغط، مع ١٤ وصلة نحاسية تناسب أغلب محركات السيارات في حقيبة منظمة.",
        "image": "images/products/263.jpg",
        "source_file": "batch3 (1).jpeg",
        "specs": ["AUTOOL PT620", "Digital Oil Pressure", "14 Brass Adapters", "Live & Peak Readout", "Universal Compatibility"]
    },
    {
        "id": 264,
        "ref_no": "REF #264",
        "part_number": "ET-264",
        "name_en": "AUTOOL AS502 Digital Transmission Fluid (ATF) Quality & Temperature Tester",
        "name_ar": "جهاز فحص جودة ونظافة زيت الفتيس الأوتوماتيك أوتول AS502",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "AUTOOL AS502 handheld automatic transmission fluid (ATF) tester. Utilizes advanced optical transmittance and oil temperature sensor probe to accurately assess gearbox oil degradation percentage, contamination levels, and thermal condition on a 2.8\" backlit screen.",
        "description_ar": "جهاز فحص جودة وصلاحية زيت الفتيس والجير الأوتوماتيك أوتول AS502. يعمل بحساس بصري يقيس نسبة نقاء الزيت ودرجة حرارته بدقة عالية، ويعرض نسبة صلاحية الزيت المئوية على شاشة ملونة واضحة.",
        "image": "images/products/264.jpg",
        "source_file": "batch3 (2).jpeg",
        "specs": ["AUTOOL AS502", "ATF Fluid Degradation", "Optical Transmittance", "Oil Temp Display", "Handheld Probe", "2.8\" Backlit Screen"]
    },
    {
        "id": 265,
        "ref_no": "REF #265",
        "part_number": "ET-265",
        "name_en": "AUTOOL CT500 GDI / EFI / FSI 6-Cylinder Ultrasonic Fuel Injector Cleaner & Tester",
        "name_ar": "محطة تنظيف وفحص انجكترات وبخاخات أوتول CT500 التراسونيك",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "AUTOOL CT500 6-cylinder professional ultrasonic fuel injector cleaning and diagnostic machine. Supports GDI, EFI, and FSI injectors, featuring simulated engine RPM tests, spray pattern uniformity inspection, leak testing, and heated ultrasonic wave cleaning.",
        "description_ar": "جهاز تنظيف واختبار بخاخات البنزين بالموجات فوق الصوتية أوتول CT500. يدعم بخاخات GDI وEFI، يختبر رش البخاخات، كشف التسريب، محاكاة سرعات المحرك المختلفة، مع حوض تنظيف ساخن عالي التردد.",
        "image": "images/products/265.jpg",
        "source_file": "batch3 (3).jpeg",
        "specs": ["AUTOOL CT500", "GDI & EFI Testing", "6-Tube Flow Meter", "Heated Ultrasonic Bath", "Spray Pattern Check", "RPM Simulation"]
    },
    {
        "id": 266,
        "ref_no": "REF #266",
        "part_number": "ET-266",
        "name_en": "THINKCAR THINKTOOL T77 Full System Automotive Diagnostic Tablet",
        "name_ar": "جهاز فحص وتشخيص أعطال السيارات ثينك تول T77",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "THINKCAR ThinkTool T77 professional 7-inch Android diagnostic scanner. Delivers OE-level full system fault scanning, live data streams with graphic display, bidirectional actuation tests, and comprehensive reset maintenance functions for 100+ vehicle brands.",
        "description_ar": "تابلت فحص وتشخيص أعطال السيارات الاحترافي ثينك تول T77 بنظام أندرويد. يوفر كشفاً شاملاً لجميع كمبيوترات وأنظمة السيارة (المحرك، الجير، ABS، الإيرباج)، قراءة ومسح الأعطال، قراءة الحساسات الحية، ووظائف إعادة الضبط والصيانة لأكثر من ١٠٠ ماركة سيارات.",
        "image": "images/products/266.jpg",
        "source_file": "batch3 (4).jpeg",
        "specs": ["ThinkTool T77", "Direct Wired OBD2", "DTC Lookup Library", "Freeze Frame Data", "Oil/EPB/BMS Resets", "Android Tablet"]
    },
    {
        "id": 267,
        "ref_no": "REF #267",
        "part_number": "ET-267",
        "name_en": "THINKCAR THINKTOOL 8\" Advanced Diagnostic Tablet (CAN-FD & DOIP)",
        "name_ar": "كمبيوتر فحص سيارات ثينك كار متطور ٨ إنش (CAN-FD & DOIP)",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "THINKCAR ThinkTool 8-inch smart diagnostic tablet with wireless Bluetooth VCI connector. Supports cutting-edge CAN-FD and DoIP high-speed communication protocols, advanced ECU coding, 34+ maintenance reset services, full bi-directional active testing, and 64GB onboard storage.",
        "description_ar": "جهاز فحص كمبيوتر السيارات الذكي ٨ إنش من ثينك كار مع وصلة بلوتوث لاسلكية. يدعم أحدث بروتوكولات الاتصال السريع CAN-FD وDoIP، برمجة كمبيوترات ECU Coding، أكثر من ٣٤ وظيفة ريست وصيانة، واختبارات التشغيل التفاعلية مع ذاكرة ٦٤ جيجابايت.",
        "image": "images/products/267.jpg",
        "source_file": "batch3 (5).jpeg",
        "specs": ["8\" HD Display", "Wireless VCI", "AutoVIN Scan", "ECU Coding", "34+ Reset Services", "WiFi Updates"]
    },
    {
        "id": 268,
        "ref_no": "REF #268",
        "part_number": "ET-268",
        "name_en": "THINKCAR THINKTOOL MASTER Complete Workshop Diagnostic Kit",
        "name_ar": "محطة فحص السيارات المتكاملة ثينك تول ماستر مع حقيبة الوصلات",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "THINKTOOL MASTER complete workshop diagnostic bundle with rugged lockable toolbox. Supports full system diagnosis, component matching, online parameterization, live sensor telemetry, and includes complete set of proprietary vehicle diagnostic adapters.",
        "description_ar": "طقم ورش متكامل لجهاز فحص وبرمجة السيارات ثينك تول ماستر في حقيبة صلبة مقفلة. يدعم فحص كافة الأنظمة ومطابقة القطع الجديدة مع كمبيوتر السيارة، ويشمل كافة وصلات ومحولات فيش الفحص المتنوعة.",
        "image": "images/products/268.jpg",
        "source_file": "batch3 (6).jpeg",
        "specs": ["ThinkTool Master", "Full System Coverage", "Component Matching", "Comprehensive Adapters", "Molded Rugged Tool Case"]
    },
    {
        "id": 269,
        "ref_no": "REF #269",
        "part_number": "ET-269",
        "name_en": "THINKCAR THINKTOOL SE Full System Diagnostic Kit with Harness",
        "name_ar": "طقم فحص السيارات الاحترافي ثينك تول SE مع الفيش والأسلاك",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "THINKCAR ThinkTool SE complete diagnostic scanner kit. Includes 8-inch rugged touch tablet with kickstand, Bluetooth VCI, battery power leads, lighter adapter cable, non-standard OBD adapter plugs, and heavy-duty storage case.",
        "description_ar": "طقم جهاز فحص وتشخيص السيارات ثينك تول SE الكامل. يشمل تابلت ٨ إنش محمي مع مسند خلفي، فيشة بلوتوث VCI، كابلات شحن وبطارية، محولات للفيش غير القياسية، وحقيبة حفظ مخصصة.",
        "image": "images/products/269.jpg",
        "source_file": "batch3 (7).jpeg",
        "specs": ["ThinkTool SE", "8\" Rugged Tablet", "Full Wiring Harness", "Non-Standard Plugs", "Blow-Mold Case", "Wireless Bluetooth"]
    },
    {
        "id": 270,
        "ref_no": "REF #270",
        "part_number": "ET-270",
        "name_en": "AUTOOL EM365 Inverter Programmed Power Supply for ECU Flashing & Programming",
        "name_ar": "باور سبلاي رقمي عاكس أوتول EM365 لبرمجة السيارات ١٢ فولت / ١٠٠ أمبير",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "AUTOOL EM365 high-current inverter power supply unit (12V / 100A, 3800W peak). Designed for modern automotive tuning, ECU flashing, radar calibration, and battery charging, ensuring consistent voltage output without voltage drop during critical programming procedures.",
        "description_ar": "مزود طاقة عاكس احترافي عالي الأمبير أوتول EM365 (١٢ فولت / ١٠٠ أمبير، قدرة ٣٨٠٠ واط). مخصص لبرمجة كمبيوترات السيارات، معايرة الرادارات، وشحن البطاريات، مما يضمن ثبات الفولتية أثناء عمليات البرمجة الحساسة.",
        "image": "images/products/270.jpg",
        "source_file": "batch3 (8).jpeg",
        "specs": ["AUTOOL EM365", "100A Constant Output", "Inverter Technology", "ECU Flashing Safe", "Battery Charger Mode", "Overload Protection"]
    },
    {
        "id": 271,
        "ref_no": "REF #271",
        "part_number": "ET-271",
        "name_en": "AUTOOL PT640 Digital High-Pressure GDI & EFI Fuel System Tester",
        "name_ar": "ساعة فحص ضغط بنزين ديجيتال أوتول PT640 للحقن المباشر GDI",
        "category_id": "diagnostic_testing",
        "category_en": "Diagnostic & Electrical",
        "category_ar": "الفحص والتشخيص والكهرباء",
        "description_en": "AUTOOL PT640 digital automotive fuel injection pressure gauge. Designed for testing high-pressure GDI and conventional EFI fuel pump lines, featuring pressure hold, backlit LCD screen, high pressure reinforced hose, and precision threaded metal fittings in blow-mold case.",
        "description_ar": "ساعة فحص ضغط حقن الوقود ديجيتال أوتول PT640. مخصصة لاختبار طرمبات وخطوط ضغط البنزين العالي GDI والبخاخات التقليدية، مع ميزة تثبيت القراءة، شاشة LCD مضيئة، وخرطوم مقوى مع وصلات معدنية دقيقة.",
        "image": "images/products/271.jpg",
        "source_file": "batch3 (9).jpeg",
        "specs": ["AUTOOL PT640", "GDI & EFI Pressure", "Digital Readout", "High-Pressure Hose", "Quick Fittings", "Blow-Mold Case"]
    }
]

def main():
    os.makedirs('images/products', exist_ok=True)
    
    print('Processing 13 Batch 3 images...')
    for item in BATCH3_ITEMS:
        src_path = os.path.join('batch3', item['source_file'])
        dst_path = os.path.join('images', 'products', f"{item['id']}.jpg")
        
        if os.path.exists(src_path):
            img = Image.open(src_path)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(dst_path, 'JPEG', quality=90, optimize=True)
            print(f"  [OK] Saved {dst_path} from {item['source_file']}")
        else:
            print(f"  [ERROR] Missing {src_path}")
            
    with open('catalog.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)
        
    print(f"Current catalog has {len(catalog)} items.")
    
    # Filter out any entries with ids >= 259 to prevent duplicates
    catalog = [c for c in catalog if c['id'] < 259]
    
    for item in BATCH3_ITEMS:
        item_copy = dict(item)
        item_copy.pop('source_file', None)
        catalog.append(item_copy)
        
    print(f"New catalog has {len(catalog)} items.")
    
    with open('catalog.json', 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        
    print("Successfully updated catalog.json with items 1 through 271!")

if __name__ == '__main__':
    main()
