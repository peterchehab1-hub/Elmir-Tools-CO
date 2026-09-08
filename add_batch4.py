import os
import json
from PIL import Image

BATCH4_ITEMS = [
    {
        "id": 277,
        "ref_no": "REF #277",
        "part_number": "ET-277",
        "name_en": "JBM 3-Ton Heavy Duty Low Profile Hydraulic Floor Jack",
        "name_ar": "كوريك تمساح هيدروليكي واطي 3 طن ماركة JBM",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM professional 3-ton low profile hydraulic trolley floor jack. Engineered with ultra-low clearance entry (75mm - 505mm lifting range) ideal for lowered chassis and sports cars, heavy gauge reinforced steel construction, dual pump rapid lift mechanism, overload protection valve, and 360-degree rear swivel casters.",
        "description_ar": "كوريك وعفريت تمساح هيدروليكي احترافي حمولة 3 طن ماركة JBM الإسبانية. يتميز بتصميم منخفض واطي للسيارات الرياضية والمنخفضة (ارتفاع يبدأ من 75 مم وحتى 505 مم)، طرمبة مزدوجة للرفع السريع، هيكل فولاذي شديد التحمل، صمام أمان هيدروليكي، وعجلات خلفية دوارة لسهولة المناورة في الورشة.",
        "image": "images/products/277.jpg",
        "source_file": "5837126925300731750.jpg",
        "specs": ["JBM 3 Ton", "Low Profile (75-505mm)", "Dual Pump Rapid Lift", "Heavy Gauge Steel", "Overload Safety Valve", "Swivel Casters"]
    },
    {
        "id": 278,
        "ref_no": "REF #278",
        "part_number": "ET-278",
        "name_en": "Audi & VW 3.0 V6 30V Engine Camshaft Alignment & Timing Tool Kit",
        "name_ar": "طقم زبط وتثبيت تايمينج وكاتينة محركات أودي وفولكس فاجن 3.0 V6",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Professional engine camshaft alignment and timing locking tool set for Audi and Volkswagen 3.0L V6 30-valve petrol engines (ASN, AVK, BBJ). Includes left and right camshaft locking holders, crankshaft locking pin, camshaft adjuster socket tool, and tensioner pins for precise timing belt replacement and cylinder head servicing.",
        "description_ar": "طقم عيار وتثبيت تايمينج وكاتينة محركات أودي وفولكس فاجن 3.0 لتر V6 ذات الـ 30 صباب (أكواد ASN, AVK, BBJ). يتضمن مساكات وقوافل قفل عمود الكامات اليمين واليسار، خابور تثبيت عمود الكرنك، حبة ضبط بكرات الكامات، وتيل قفل بلية الشداد لتغيير حزام التايمينج بدقة بالغة.",
        "image": "images/products/278.jpg",
        "source_file": "5837126925300731751.jpg",
        "specs": ["Audi / VW 3.0 V6 30V", "Engine Codes: ASN, AVK, BBJ", "Camshaft Locking Fixtures", "Crankshaft TDC Pin", "Cam Adjuster Socket", "Heavy Duty Case"]
    },
    {
        "id": 279,
        "ref_no": "REF #279",
        "part_number": "ET-279",
        "name_en": "JBM 13-Piece 1/4\" Drive 12-Point Metric Socket Set (4-14mm) - REF. 52717",
        "name_ar": "طقم لقم طربوش مسنن مشرشر 1/4 بوصة 13 قطعة JBM 52717",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 52717 13-piece 1/4-inch square drive 12-point (bi-hex / multi-tooth) metric socket set with metal storage rail. Forged from mirror-polished Chrome Vanadium steel with knurled gripping bands. Includes complete range from 4mm up to 14mm (4, 4.5, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13, 14 mm).",
        "description_ar": "طقم حبات ولقم طربوش مشرشرة 12 سن مقاس 1/4 بوصة 13 قطعة ماركة JBM الإسبانية (كود 52717). مصنوعة من فولاذ الكروم فانديوم عالي الجودة Cr-V مع مسطرة معدنية لحفظ اللقم. تشمل المقاسات: 4، 4.5، 5، 5.5، 6، 7، 8، 9، 10، 11، 12، 13، 14 مم.",
        "image": "images/products/279.jpg",
        "source_file": "5837126925300731752.jpg",
        "specs": ["JBM REF. 52717", "1/4\" Drive 12-Point (Bi-Hex)", "13 Pieces (4mm to 14mm)", "Chrome Vanadium Cr-V", "Knurled Grip Band", "Metal Socket Rail"]
    },
    {
        "id": 280,
        "ref_no": "REF #280",
        "part_number": "ET-280",
        "name_en": "JBM 46-Piece 1/4\" Drive Ratchet, Socket & Screwdriver Bit Set",
        "name_ar": "طقم لقم وسيستم راشيت 1/4 بوصة 46 قطعة مع مفكات ووصلات JBM",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM comprehensive 46-piece 1/4-inch drive mechanics socket and ratchet set. Features fine-tooth ergonomic quick-release ratchet, complete metric socket range (4mm-14mm), Torx/Hex/Phillips/Slotted bit sockets, flexible spring extension bar, sliding T-handle, spinner handle, and universal joint in heavy-duty molded case.",
        "description_ar": "طقم عدة ميكانيك متكامل 46 قطعة مقاس 1/4 بوصة ماركة JBM. يتضمن يد سيستم راشيت سريعة الفك، لقم مقاسات من 4 حتى 14 مم، لقم مفكات ألنكيه وتوركس وعادة وصليبة، وصلة مرنة سوستة للأماكن الضيقة، وصلات تطويلة، يد مفك، يد حرف T، ومفصلة كاردان في شنطة صلبة منظمة.",
        "image": "images/products/280.jpg",
        "source_file": "5837126925300731753.jpg",
        "specs": ["46 Pieces Complete Set", "1/4\" Quick-Release Ratchet", "Sockets 4mm - 14mm", "Torx / Hex / PH / PZ / SL Bits", "Flexible Extension Bar", "Molded Carry Case"]
    },
    {
        "id": 281,
        "ref_no": "REF #281",
        "part_number": "ET-281",
        "name_en": "BMW Mini Cooper & Peugeot Citroen N12 / N14 Engine Timing Locking Tool Kit",
        "name_ar": "طقم زبط وتثبيت تايمينج محركات ميني كوبر وبيجو وستروين N12 / N14",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Professional engine camshaft timing and alignment locking tool kit for BMW Mini Cooper (R55, R56, R57) and PSA Peugeot/Citroen 1.4 & 1.6 16V Valvetronic engines (N12, N14, EP3, EP6). Includes camshaft locking bridges, crankshaft timing pin, and dummy chain tensioner tool in rugged case.",
        "description_ar": "طقم عيار وتثبيت تايمينج وكاتينة محركات ميني كوبر (BMW Mini) ومحركات بيجو وستروين 1.4 و 1.6 فالفترونيك N12 و N14 و EP6. يتضمن قفل عمود الكامات، قفل الحدافة والكرنك، وشداد جنزير الكاتينة لضبط توقيت المحرك بدقة تامة.",
        "image": "images/products/281.jpg",
        "source_file": "5837126925300731754.jpg",
        "specs": ["BMW Mini Cooper N12/N14", "Peugeot / Citroen EP3/EP6", "Camshaft Locking Blocks", "Flywheel Timing Pin", "Chain Tensioner Tool", "Heavy Duty Case"]
    },
    {
        "id": 282,
        "ref_no": "REF #282",
        "part_number": "ET-282",
        "name_en": "JBM 6-Plate Universal MacPherson Coil Spring Compressor Set - REF. 52227",
        "name_ar": "طقم زرجينة ضغط يايات ومساعدين مكفرسون مع 6 صحون JBM 52227",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 52227 professional universal MacPherson strut coil spring compressor set. Features heavy-duty single-action safety compressor shaft with 3 pairs (6 pieces) of interchangeable forged alloy jaws covering coil spring diameters from 80mm to 195mm. Suitable for BMW, Mercedes, VW, Audi, Ford, Toyota, and Honda suspension struts.",
        "description_ar": "طقم زرجينة وكباس سوست ومساعدين مكفرسون احترافي مزود بـ 6 صحون مقاسات مختلفة ماركة JBM الإسبانية (كود 52227). يحتوي على 3 أزواج من الفكوك الفولاذية المطروقة لتغطية اليايات من قطر 80 مم حتى 195 مم، مناسب لجميع أنواع السيارات الأوروبية والآسيوية مع حقيبة حمل قوية.",
        "image": "images/products/282.jpg",
        "source_file": "5837126925300731755.jpg",
        "specs": ["JBM REF. 52227", "6 Interchangeable Yoke Plates", "Spring Range: 80mm - 195mm", "Telescopic Safety Shaft", "Universal MacPherson Strut", "Heavy Duty Case"]
    },
    {
        "id": 283,
        "ref_no": "REF #283",
        "part_number": "ET-283",
        "name_en": "JBM 131-Piece Metric Thread Repair Helicoil Kit (M5 - M12) - REF. 51896",
        "name_ar": "طقم تصليح وتنزيل سن القلاووظ هيلوكويل 131 قطعة M5-M12 ماركة JBM 51896",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 51896 131-piece master metric thread repair set. Specifically designed for repairing stripped, worn, or cross-threaded internal screw threads in engine blocks, cylinder heads, spark plugs, and gearboxes. Covers M5x0.8, M6x1.0, M8x1.25, M10x1.5, and M12x1.75 with HSS drill bits, taps, installation tools, and stainless wire inserts.",
        "description_ar": "طقم تنزيل وتصليح سنون المسامير والقلاووظ التالفة (هيلوكويل) 131 قطعة ماركة JBM الإسبانية (كود 51896). مثالي لإصلاح السنون التالفة في بلوك المحرك، وش السلندر، وعلب السرعات. يغطي المقاسات M5, M6, M8, M10, M12 مع بنط التخريم، دكر القلاووظ، أدوات التركيب وسوست الاستانلس ستيل في صندوق حديد.",
        "image": "images/products/283.jpg",
        "source_file": "5837126925300731756.jpg",
        "specs": ["JBM REF. 51896", "131 Pieces Metric", "Sizes: M5, M6, M8, M10, M12", "HSS Taps & Drill Bits", "Stainless Steel Wire Inserts", "Metal Workshop Box"]
    },
    {
        "id": 284,
        "ref_no": "REF #284",
        "part_number": "ET-284",
        "name_en": "Universal Disc Brake Caliper Piston Wind-Back Rewind Tool Kit",
        "name_ar": "طقم برسة وزرجينة إرجاع بستم فرامل وديسكات السيارات يمين ويسار",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Master disc brake caliper piston rewind and wind-back tool set. Includes right-hand and left-hand threaded thrust bolt assemblies with magnetic reaction plates and multi-pin drive adapters to retract brake caliper pistons when servicing brake pads and rotors. Prevents damage to rubber seals and internal mechanisms.",
        "description_ar": "طقم زرجينة وكباس إرجاع وضغط بستم الفرامل الكاليبر يمين وشمال. يحتوي على يدين لولبيتين يمين ويسار مع مجموعة شاملة من المحولات الدائرية المغناطيسية المتوافقة مع كاليبرات فرامل معظم السيارات لحماية الجلود وسلندرات الفرامل عند استبدال الفحمات وتيل الفرامل.",
        "image": "images/products/284.jpg",
        "source_file": "5837126925300731757.jpg",
        "specs": ["Universal Caliper Wind-Back", "Left & Right Hand Thrust Bolts", "18+ Multi-Pin Adapters", "Magnetic Drive Plates", "Prevents Piston/Boot Damage", "Molded Carry Case"]
    },
    {
        "id": 285,
        "ref_no": "REF #285",
        "part_number": "ET-285",
        "name_en": "JBM 12-Piece Stubby Flex-Head Ratcheting Combination Wrench Set (8-19mm) - REF. 54032",
        "name_ar": "طقم مفاتيح ريتش قصيرة مفصلية متحركة (قزم طقطاق مخلع) 12 قطعة JBM 54032",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 54032 premium 12-piece metric stubby flexible-head ratcheting combination wrench set housed in carbon-finish EVA foam tray. Features ultra-compact stubby handles and 180-degree pivoting flex heads for maneuvering in tight engine bays. 72-tooth fine ratcheting mechanism in sizes: 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, and 19 mm.",
        "description_ar": "طقم مفاتيح ميلة ريتش مشرشرة قصيرة بمفصلة متحركة 180 درجة (قزم مخلع) 12 قطعة ماركة JBM الإسبانية (كود 54032). مصممة خصيصاً للوصول إلى الأماكن الضيقة والمحشورة في محركات السيارات الحديثة، مع سيستم طقطاق 72 سن ومقاسات من 8 حتى 19 مم في صينية فوم كربون منظمة.",
        "image": "images/products/285.jpg",
        "source_file": "5837126925300731758.jpg",
        "specs": ["JBM REF. 54032", "12 Pieces (8mm to 19mm)", "180° Flexible Pivoting Head", "72-Tooth Micro Ratchet", "Stubby Compact Length", "Carbon-Finish EVA Foam Tray"]
    },
    {
        "id": 286,
        "ref_no": "REF #286",
        "part_number": "ET-286",
        "name_en": "JBM 4-Piece 8\" Heavy-Duty Circlip Snap Ring Pliers Set - REF. 15454",
        "name_ar": "طقم بنسات تيل وسكمان 8 بوصة 4 قطع ماركة JBM 15454 في صينية فوم",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 15454 professional 4-piece 8-inch heavy-duty circlip and snap ring pliers set in carbon-fiber styled EVA foam tool tray. Includes 8\" straight tip internal, 8\" bent tip internal, 8\" straight tip external, and 8\" bent tip external pliers made from heat-treated chrome vanadium steel with ergonomic non-slip handles.",
        "description_ar": "طقم بنسات فك وتركيب تيل وسكمان 4 قطع مقاس كبير 8 بوصة ماركة JBM الإسبانية (كود 15454). يشتمل على بنسة سكمان داخلي مستقيمة، داخلي معوجة 90 درجة، خارجي مستقيمة، وخارجي معوجة 90 درجة، مصنوعة من الكروم فانديوم المقسى مع مقابض مريحة مانعة للانزلاق في صينية فوم كربون.",
        "image": "images/products/286.jpg",
        "source_file": "5837126925300731759.jpg",
        "specs": ["JBM REF. 15454", "4 Pieces 8-Inch (200mm)", "Internal Straight & Bent 90°", "External Straight & Bent 90°", "Drop-Forged Cr-V Steel", "Carbon-Finish EVA Foam Tray"]
    },
    {
        "id": 287,
        "ref_no": "REF #287",
        "part_number": "ET-287",
        "name_en": "Land Rover & Jaguar 2.0 GTDi / Si4 Engine Camshaft Timing Tool Set (Evoque)",
        "name_ar": "طقم زبط وتثبيت تايمينج محركات رنج روفر إيفوك وجاكوار وفورد 2.0 توربو",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Engine camshaft alignment and timing locking tool set for Range Rover Evoque, Land Rover Freelander 2, Discovery Sport, Jaguar XE/XF/XJ, and Ford 2.0 GTDi EcoBoost / Si4 turbocharged petrol engines. Ensures accurate camshaft and crankshaft alignment when changing timing chain or servicing variable valve timing systems.",
        "description_ar": "طقم عيار وقفل تايمينج وكاتينة محركات رينج روفر إيفوك (Range Rover Evoque)، لاند روفر ديسكفري، وجاكوار وفورد 2.0 لتر توربو GTDi / Si4 EcoBoost. يشمل مساطر وقوالب تثبيت عمود الكامات، خابور ميزان الكرنك، وأدوات تثبيت جنزير التايمينج بدقة تامة.",
        "image": "images/products/287.jpg",
        "source_file": "5837126925300731760.jpg",
        "specs": ["Range Rover Evoque / Discovery", "Jaguar & Ford 2.0 GTDi / Si4", "Camshaft Alignment Fixtures", "Crankshaft Timing Pin", "Heavy Duty Case", "OEM Equivalent Tools"]
    },
    {
        "id": 288,
        "ref_no": "REF #288",
        "part_number": "ET-288",
        "name_en": "JBM 12-Piece Go-Through Strike-Cap Screwdriver Set with Hex Bolster",
        "name_ar": "طقم مفكات دق ركبة حديد 12 قطعة ماركة JBM للطرق والرباط القوي",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM professional 12-piece go-through (through-tang) impact screwdriver set. Features continuous hardened Cr-V steel shafts extending through ergonomic shock-resistant handles to heavy steel striking end caps, with integrated hexagonal bolsters for applying additional wrench torque. Includes 6 Slotted and 6 Phillips drivers with stubby and extra-long sizes.",
        "description_ar": "طقم مفكات دق احترافي 12 قطعة ركبة حديد كاملة ماركة JBM. يتميز بساق فولاذية ممتدة بالكامل حتى الكعب الفولاذي للطرق بالشاكوش لفك المسامير المصدية والمستعصية، مع صامولة سداسية أسفل المقبض لزيادة عزم الشد بالمفتاح. يشمل 6 مفكات عادة و 6 مفكات صليبة بأطوال ومقاسات متنوعة في شنطة صلبة.",
        "image": "images/products/288.jpg",
        "source_file": "5837126925300731761.jpg",
        "specs": ["12 Pieces Go-Through", "Steel Striking End Caps", "Hex Bolsters for Extra Torque", "Magnetic Hardened Tips", "Stubby to 200mm Long", "Heavy Duty Case"]
    },
    {
        "id": 289,
        "ref_no": "REF #289",
        "part_number": "ET-289",
        "name_en": "JBM 6-Piece Metric Flare Nut Spanner Wrench Set (8-19mm) - REF. 54081",
        "name_ar": "طقم مفاتيح مواسير وبايب فرامل 6 قطع كروم فانديوم JBM 54081",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 54081 professional 6-piece metric flare nut brake line wrench set in heavy-duty roll-up canvas pouch. Specially forged from mirror-polished Chrome Vanadium steel with 15-degree offset heads designed to securely grip hexagonal pipe fittings and brake line flare nuts without rounding delicate corners. Sizes: 8x9, 10x11, 12x13, 14x15, 16x17, and 18x19 mm.",
        "description_ar": "طقم مفاتيح مواسير وفرامل 6 قطع ماركة JBM الإسبانية (كود 54081) في جراب قماش متين معلق. مصممة بفتحة حلقة مشقوقة بزاوية 15 درجة لإحكام القبضة على صواميل مواسير الفرامل والبنزين النحاسية وتجنب تلف أركان الصامولة. المقاسات: 8x9، 10x11، 12x13، 14x15، 16x17، 18x19 مم.",
        "image": "images/products/289.jpg",
        "source_file": "5837126925300731762.jpg",
        "specs": ["JBM REF. 54081", "6 Pieces Double Open Flare", "Sizes: 8x9 to 18x19 mm", "Brake & Fuel Line Specialist", "Chrome Vanadium Cr-V", "Heavy-Duty Roll-Up Pouch"]
    },
    {
        "id": 290,
        "ref_no": "REF #290",
        "part_number": "ET-290",
        "name_en": "BMW N51 / N52 / N53 / N54 / N55 Engine Camshaft Alignment & Timing Tool Kit",
        "name_ar": "طقم زبط وتثبيت تايمينج محركات بي إم دبليو N51 و N52 و N53 و N54 و N55",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Master engine camshaft timing and alignment tool kit for BMW 2.5L and 3.0L inline 6-cylinder engines (N51, N52, N53, N54, N55). Includes precision color-coded camshaft alignment bars (Red for N55, White for N53/N54, Blue for N51/N52), VANOS sensor wheel timing plates, flywheel alignment pin, and timing chain pre-tensioner tool in heavy-duty molded case.",
        "description_ar": "طقم عيار وتثبيت تايمينج وكاتينة محركات بي إم دبليو (BMW) المتطورة 6 سلندر 2.5 و 3.0 لتر (N51, N52, N53, N54, N55). يشمل مساطر ألومنيوم ملونة مخصصة لكل محرك (أحمر لـ N55، أبيض لـ N53/N54، أزرق لـ N51/N52)، أدوات ضبط عجلات حساسات الفانوس VANOS، خابور ميزان الحدافة، وشداد جنزير الكاتينة.",
        "image": "images/products/290.jpg",
        "source_file": "5837126925300731763.jpg",
        "specs": ["BMW N51/N52/N53/N54/N55", "Color-Coded Cam Alignment Bars", "VANOS Sensor Alignment Fixture", "Flywheel TDC Pin", "Chain Pre-Tensioner", "Heavy Duty Case"]
    },
    {
        "id": 291,
        "ref_no": "REF #291",
        "part_number": "ET-291",
        "name_en": "Mercedes-Benz M270 & M274 1.6L / 2.0L Engine Camshaft Timing Tool Set",
        "name_ar": "طقم زبط وتثبيت تايمينج محركات مرسيدس بنز M270 و M274",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Professional engine camshaft timing alignment and locking tool set for Mercedes-Benz M270 (transverse) and M274 (longitudinal) 1.6L & 2.0L chain-driven petrol engines. Includes precision camshaft holding clamps, interchange clamp blocks, and specialized camshaft socket for A-Class, B-Class, C-Class, CLA, and GLA models.",
        "description_ar": "طقم عيار وقفل تايمينج عمود الكامات لمحركات مرسيدس بنز M270 و M274 سعة 1.6 و 2.0 لتر بنزين (أكواد المحرك العرضي والطولي لموديلات مرسيدس A-Class, B-Class, C-Class, CLA, GLA). يتضمن زرادات وملاقط تثبيت الكامات، قوالب تبديل مقاسات، وحبة خاصة لفك وربط ترس الكامات.",
        "image": "images/products/291.jpg",
        "source_file": "5837126925300731764.jpg",
        "specs": ["Mercedes-Benz M270 & M274", "1.6L & 2.0L Petrol Turbo", "Camshaft Holding Clamps", "Interchangeable Clamp Inserts", "Camshaft Rotating Socket", "Heavy Duty Case"]
    },
    {
        "id": 292,
        "ref_no": "REF #292",
        "part_number": "ET-292",
        "name_en": "JBM Locksmith Machinist Hammer with Genuine Hickory Wood Handle - REF. 51674",
        "name_ar": "شاكوش حداد وميكانيكي بيد خشب زان هيد صلب JBM 51674",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 51674 professional German-pattern locksmith and machinist hammer. Features drop-forged, precision ground high-carbon steel head with rust-resistant black coating, reinforced protective steel collar, and genuine contoured Hickory wood handle for maximum impact absorption and working balance.",
        "description_ar": "شاكوش حداد وميكانيكي احترافي طراز ألماني ماركة JBM الإسبانية (كود 51674). يتميز برأس مطروق من الفولاذ الكربوني عالي الصلابة، طوق حماية فولاذي حول عنق الرأس، ويد مصنوعة من خشب الزان الهيكوري المعالج لامتصاص الصدمات وتقليل الاهتزازات أثناء الطرق في الورش.",
        "image": "images/products/292.jpg",
        "source_file": "5837126925300731765.jpg",
        "specs": ["JBM REF. 51674", "Machinist / Locksmith Pattern", "Forged High-Carbon Steel", "Genuine Hickory Wood Handle", "Reinforced Steel Collar", "Anti-Vibration Design"]
    },
    {
        "id": 293,
        "ref_no": "REF #293",
        "part_number": "ET-293",
        "name_en": "BMW & Mercedes-Benz Fuel Injector Removal Extractor Puller Kit with Slide Hammer",
        "name_ar": "طقم زرجينة نزع وفك بخاخات وانجكترات بي إم دبليو ومرسيدس بنز مع همر سحب",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Master common-rail and direct injection fuel injector removal and extractor puller kit for BMW and Mercedes-Benz engines. Features high-impact steel slide hammer, pulling bridges, threaded adaptors, and gripping claws designed to safely extract stubborn, carbon-seized petrol and diesel injectors without causing damage to the cylinder head or injector body.",
        "description_ar": "طقم زرجينة وهمر نزع وفك رشاشات وانجكترات الوقود المستعصية والمكربنة لسيارات بي إم دبليو ومرسيدس بنز ديزل وبنزين. مزود بشاكوش انزلاقي (همر سحب ثقيل)، كباري وقواعد ارتكاز، ومحولات مسننة لخلع البخاخات العالقة بسهولة ودون التسبب في كسر أو إتلاف وش السلندر.",
        "image": "images/products/293.jpg",
        "source_file": "5837126925300731766.jpg",
        "specs": ["BMW & Mercedes Specialist", "Heavy-Duty Slide Hammer", "Pulling Bridges & Adapters", "For Seized / Carbonized Injectors", "Diesel CDI & Petrol GDI/EFI", "Heavy Duty Case"]
    },
    {
        "id": 294,
        "ref_no": "REF #294",
        "part_number": "ET-294",
        "name_en": "40-Piece Master Torx, Spline & Hex Bit Socket Set (Short & Long) with 3/8\" & 1/2\" Adapters",
        "name_ar": "طقم لقم ومفاتيح ألنكيه ونجمه ومشرشر 40 قطعة (توركس وألن ومشرشر) مع محولات",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Comprehensive 40-piece master bit socket assortment featuring Torx Star, Metric Hex Allen, and XZN Spline bits in both 30mm short and 75mm extended long lengths. Forged from high-grade S2 alloy steel with 3/8-inch and 1/2-inch Chrome Vanadium drive bit adaptors in fitted storage case.",
        "description_ar": "طقم لقم ومفاتيح متكامل 40 قطعة يجمع بين مفاتيح ألنكيه مسدس (Hex)، لقم نجمة توركس (Torx)، ولقم مشرشر (Spline XZN) بأطوال قصيرة (30 مم) وطويلة (75 مم) للوصول للأماكن العميقة، مع محولين مقاس 3/8 و 1/2 بوصة مصنوعة من فولاذ S2 المقاوم للالتواء.",
        "image": "images/products/294.jpg",
        "source_file": "5837126925300731767.jpg",
        "specs": ["40 Pieces Complete Assortment", "Torx T20 - T60 (Short & Long)", "Hex 4mm - 12mm (Short & Long)", "Spline M5 - M12 (Short & Long)", "3/8\" & 1/2\" Drive Adapters", "Heavy Duty Case"]
    },
    {
        "id": 295,
        "ref_no": "REF #295",
        "part_number": "ET-295",
        "name_en": "JBM 11-Piece 1/2\" Drive Deep Metric Impact Socket Set (10-24mm) Cr-Mo",
        "name_ar": "طقم حبات طربوش دق أسود طويل 1/2 بوصة كروم موليبدينوم JBM",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM professional 11-piece 1/2-inch drive deep metric impact socket set. Drop-forged from premium heat-treated Chrome Molybdenum (Cr-Mo) alloy steel with black phosphate finish for extreme torque applications on air impact guns and battery wrenches. Includes sizes: 10, 11, 12, 13, 14, 16, 17, 19, 21, 22, and 24 mm in molded carry case.",
        "description_ar": "طقم لقم وحبات طربوش دق طويل 1/2 بوصة 11 قطعة ماركة JBM الإسبانية. مصنعة من حديد الكروم موليبدينوم Cr-Mo فائق التحمل المعالج حرارياً ومطلي بطبقة فوسفات سوداء مقاومة للصدأ والتآكل للاستخدام الشاق مع دريل الهواء ومسدسات الدق. المقاسات: 10، 11، 12، 13، 14، 16، 17، 19، 21، 22، 24 مم.",
        "image": "images/products/295.jpg",
        "source_file": "5837126925300731768.jpg",
        "specs": ["JBM Chrome Molybdenum (Cr-Mo)", "1/2\" Drive Deep Impact", "11 Sizes: 10mm to 24mm", "Phosphate Anti-Corrosion Finish", "For Pneumatic & Electric Guns", "Heavy Duty Case"]
    },
    {
        "id": 296,
        "ref_no": "REF #296",
        "part_number": "ET-296",
        "name_en": "5-Piece Front End Service Ball Joint Separator & Pitman Arm Puller Kit",
        "name_ar": "طقم زراجين فك بيض ومقصات وبارات دركسيون وتيش الميزان 5 قطع",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Professional 5-piece front end service kit for separating stubborn ball joints, tie rod ends, pitman arms, and steering linkage components. Features heavy drop-forged alloy steel construction with precision-threaded forcing screws. Allows damage-free separation of steering and suspension assemblies on passenger cars and light trucks.",
        "description_ar": "طقم زراجين صيانة عفشة ومقصات السيارات 5 قطع (برسة بيضة). مخصص لفك ونزع بيض المقصات، بارات الدركسيون، أذرع الشاسيه وتيش الميزان دون تمزيق كاوتش الغبار أو إتلاف سنون المقص. مصنوع من سبائك الفولاذ المطروق عالي المتانة في حقيبة منظمة.",
        "image": "images/products/296.jpg",
        "source_file": "5837126925300731769.jpg",
        "specs": ["5-Piece Front End Kit", "Ball Joint Separator", "Pitman Arm Puller", "Tie Rod End Puller", "Drop-Forged Alloy Steel", "Molded Carry Case"]
    },
    {
        "id": 297,
        "ref_no": "REF #297",
        "part_number": "ET-297",
        "name_en": "JBM Heavy Duty CV Boot Clamp Banding Tool with Cutter - REF. 54376",
        "name_ar": "بنسة شد وقطع أفيز الكوبلن والرباط الحديد مع مقص JBM 54376",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 54376 heavy-duty CV joint boot clamp banding tool with integrated winding lever and cutting mechanism. Designed for fast tensioning, securing, and flush trimming of stainless steel banding straps on drive axle CV boots, steering rack bellows, and radiator hoses.",
        "description_ar": "بنسة وأداة شد وتثبيت أفيز كبلن حديد ومعدني ماركة JBM الإسبانية (كود 54376). مزودة برافعة لف لشد كوليهات وأربطة الكوبلن الاستانلس ستيل بإحكام شديد مع سكين مدمجة لقص الزيادات بدقة لحماية كاوتش الكوبلن من تسريب الشحم ودخول الأتربة.",
        "image": "images/products/297.jpg",
        "source_file": "5837126925300731770.jpg",
        "specs": ["JBM REF. 54376", "CV Boot Banding Tool", "Integrated Winding Crank", "Built-In Cutter Mechanism", "Ergonomic Rubber Grip", "For Stainless Steel Straps"]
    },
    {
        "id": 298,
        "ref_no": "REF #298",
        "part_number": "ET-298",
        "name_en": "BMW M52TU / M54 / M56 Double VANOS Engine Camshaft Timing Tool Kit",
        "name_ar": "طقم عيار وقفل تايمينج محركات بي إم دبليو دبل فانوس M52TU / M54 / M56",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "Master engine camshaft timing and alignment locking tool kit for BMW M52TU, M54, and M56 Double VANOS 6-cylinder petrol engines (E46 3-Series, E39/E60 5-Series, E83 X3, E53 X5, Z3/Z4). Features precision camshaft alignment bridge, VANOS assembly setting fixtures, secondary sprocket tool, and TDC flywheel locking pin.",
        "description_ar": "طقم عيار وتثبيت تايمينج عمود الكامات لمحركات بي إم دبليو (BMW) دبل فانوس 6 سلندر M52TU و M54 و M56 (موديلات الفئة الثالثة E46، الفئة الخامسة E39/E60، إكس 3، وإكس 5). يشتمل على قوالب ومساطر ضبط وحدات الفانوس المزدوجة، مسطرة عيار الكامات، خابور ميزان الكرنك، وشداد الجنزير في حقيبة منظمة.",
        "image": "images/products/298.jpg",
        "source_file": "5837126925300731771.jpg",
        "specs": ["BMW M52TU / M54 / M56", "Double VANOS 6-Cylinder", "Camshaft Alignment Fixture", "VANOS Setup Plates", "Flywheel TDC Pin", "Heavy Duty Case"]
    },
    {
        "id": 299,
        "ref_no": "REF #299",
        "part_number": "ET-299",
        "name_en": "JBM 5-Piece 1/2\" Drive Wobble Extension Bar Set (50-510mm) - REF. 51448",
        "name_ar": "طقم وصلات تطويلة سيستم مفصلية (مخلع / wobble) مقاس 1/2 بوصة 5 قطع JBM 51448",
        "category_id": "new_items",
        "category_en": "New Items",
        "category_ar": "الأصناف الجديدة",
        "description_en": "JBM 51448 premium 5-piece 1/2-inch drive wobble extension bar set in carbon-finish EVA foam module. Features dual-function wobble drive ends offering up to 15-degree angular deflection for off-axis access to confined fasteners, or locks fully into standard rigid mode. Forged from mirror-polished Chrome Vanadium steel with knurled gripping rings. Includes lengths: 50mm (2\"), 125mm (5\"), 250mm (10\"), 380mm (15\"), and extra-long 510mm (20\").",
        "description_ar": "طقم وصلات تطويلة سيستم راشيت مفصلية متحركة (مخلع / Wobble) مقاس 1/2 بوصة 5 قطع ماركة JBM الإسبانية (كود 51448) في صينية فوم كربون. تتميز برؤوس مفصلية تسمح بميلان بزاوية 15 درجة لفك وربط المسامير في الزوايا الصعبة، أو التثبيت التام كوصلة مستقيمة. مصنوعة من الكروم فانديوم Cr-V بأطوال: 50 مم، 125 مم، 250 مم، 380 مم، وتطويلة عملاقة 510 مم.",
        "image": "images/products/299.jpg",
        "source_file": "5837126925300731772.jpg",
        "specs": ["JBM REF. 51448", "5 Pieces 1/2\" Drive", "15° Two-Way Wobble Action", "Lengths: 50mm to 510mm", "Mirror Chrome Vanadium", "Carbon-Finish EVA Foam Tray"]
    }
]

def main():
    os.makedirs('images/products', exist_ok=True)
    
    print('Processing 23 Batch 4 images...')
    for item in BATCH4_ITEMS:
        src_path = os.path.join('batch 4', item['source_file'])
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
        
    print(f"Catalog before batch 4 has {len(catalog)} items.")
    
    # Filter out any entries with ids >= 277 to prevent duplicates if re-run
    catalog = [c for c in catalog if c['id'] < 277]
    
    for item in BATCH4_ITEMS:
        item_copy = dict(item)
        item_copy.pop('source_file', None)
        catalog.append(item_copy)
        
    print(f"New catalog has {len(catalog)} items.")
    
    # Verify no price field
    for it in catalog:
        assert 'price' not in it, f"Item {it.get('id')} has a forbidden price field!"
        
    with open('catalog.json', 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        
    print("Successfully updated catalog.json with items 1 through 299!")

if __name__ == '__main__':
    main()
