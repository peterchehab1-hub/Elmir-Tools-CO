import os
import json
from PIL import Image

# Mapping from batch2 files to items 241..258
BATCH2_ITEMS = [
    {
        "id": 241,
        "ref_no": "REF #241",
        "part_number": "ET-241",
        "name_en": "Handheld Vacuum Pump & Brake Bleeder Tester Kit",
        "name_ar": "فرد تنفيس فرام يدوي مع ساعة ضغط",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Multi-functional hand held vacuum pump and brake bleeder tester set. Features precision vacuum gauge (-1 to 3 bar / -30 to 0 inHg), transfer hoses, fluid reservoir jars, and multi-vehicle bleed adapters in heavy-duty blow mold case.",
        "description_ar": "طقم فرد سحب وتنفيس زيت الفرامل يدوي متعدد الاستخدامات. مزود بساعة قياس دقيقة (-١ إلى ٣ بار)، خراطيم شفافة، علب تجميع السوائل، ووصلات تناسب مختلف أنواع السيارات في حقيبة بلاستيكية متينة.",
        "image": "images/products/241.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.46 PM.jpeg",
        "specs": ["Vacuum Tester", "Brake Bleeder", "Manual Pump", "Gauge -1 to 3 bar", "Universal Adapters"]
    },
    {
        "id": 242,
        "ref_no": "REF #242",
        "part_number": "ET-242",
        "name_en": "SANOSCO Pneumatic Air Grease Pump 12L (TB-12L-G)",
        "name_ar": "مشحمة هواء ضغط عالي سعة ١٢ ليتر سانوسكو",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Professional mobile pneumatic grease pump by Sanosco (Model: TB-12L-G). 12-liter barrel capacity with 0.85 L/min high pressure grease output, air pressure regulator, dial gauge, wheeled base, and heavy duty hydraulic delivery hose.",
        "description_ar": "مشحمة هواء متحركة احترافية ماركة سانوسكو (موديل: TB-12L-G). سعة الخزان ١٢ ليتر ومعدل ضخ عالي ٠.٨٥ ليتر/دقيقة، مزودة بساعة ومنظم ضغط هواء، قاعدة دواليب لسهولة الحركة، وخرطوم هيدروليك ضغط عالي.",
        "image": "images/products/242.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.46 PM (1).jpeg",
        "specs": ["12L Capacity", "Pneumatic 0.85L/min", "SANOSCO TB-12L-G", "Pressure Regulator", "Mobile Wheeled"]
    },
    {
        "id": 243,
        "ref_no": "REF #243",
        "part_number": "ET-243",
        "name_en": "SANOSCO Heavy Duty Air Grease Pump 40L (TB-40L-G)",
        "name_ar": "مشحمة هواء صناعية كبيرة سعة ٤٠ ليتر سانوسكو",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Heavy duty industrial mobile air grease pump unit by Sanosco (Model: TB-40L-G). Large 40-liter capacity barrel with high pressure pneumatic pump head, airtight clamp lid, regulator gauge, and heavy duty reinforced hose for high-volume automotive & commercial vehicle workshops.",
        "description_ar": "مشحمة هواء صناعية ثقيلة سعة ٤٠ ليتر ماركة سانوسكو (موديل: TB-40L-G). مناسبة لكراجات الشاحنات والسيارات ذات الاستهلاك العالي، مزودة بمضخة ضغط عالي، غطاء محكم الإغلاق بكلابات، منظم ضغط هواء، وقاعدة عجلات متينة.",
        "image": "images/products/243.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.47 PM.jpeg",
        "specs": ["40L Workshop Capacity", "SANOSCO TB-40L-G", "High Pressure Air", "Heavy Duty Hose", "Wheeled Tank"]
    },
    {
        "id": 244,
        "ref_no": "REF #244",
        "part_number": "ET-244",
        "name_en": "Oil Suction Gun (1000cc) & Fluid Extractor Syringe Set",
        "name_ar": "فرد سحب زيت ١٠٠٠ سي سي + شفاطة سوائل شفافة",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Heavy duty manual oil suction gun with 1000 c.c. capacity along with a transparent graduated fluid transfer syringe (1.5L). Ideal for quick draining and filling of gearbox, differential, engine, and transmission oils.",
        "description_ar": "طقم سحب وضخ الزيوت مكوّن من فرد سحب زيت معدني سعة ١٠٠٠ سي سي مع حقنة شفاطة شفافة مدرجة سعة ١.٥ ليتر. مثالي لتفريغ وتعبئة زيوت الفتيس، الدفرنس، والمحركات بسرعة وسهولة.",
        "image": "images/products/244.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.47 PM (1).jpeg",
        "specs": ["1000 c.c. Gun", "1.5L Syringe", "Dual Tool Set", "Oil Transfer", "Gearbox & Diff"]
    },
    {
        "id": 245,
        "ref_no": "REF #245",
        "part_number": "ET-245",
        "name_en": "Fluid & Fuel Transfer Syringe Pump (1.5L) with Quick Couplers",
        "name_ar": "حقنة سحب وضخ الوقود والزيوت ١.٥ ليتر مع وصلات سريعة",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Transparent 1500ml graduated fluid evacuation and injection syringe pump. Includes quick-release snap-lock vehicle fuel line connectors (compatible with European/Asian fuel lines), dual Viton seals, and flexible extension hoses.",
        "description_ar": "حقنة سحب وتعبئة وقود وسوائل شفافة ومدرجة سعة ١٥٠٠ مل. مزودة بوصلات سريعة متوافقة مع خطوط وقود السيارات الحديثة، حلقات إحكام مزدوجة، وخراطيم مرنة للوصول للأماكن الضيقة.",
        "image": "images/products/245.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.47 PM (2).jpeg",
        "specs": ["1.5L (1500ml)", "Quick Fuel Couplers", "Graduated Body", "Dual Seal Piston", "Multi-Fluid Safe"]
    },
    {
        "id": 246,
        "ref_no": "REF #246",
        "part_number": "ET-246",
        "name_en": "45-Piece High Quality Tungsten Steel Tap and Die Set",
        "name_ar": "طقم ذكر ومقلاوي لولبة تسنين ٤٥ قطعة تنجستن ستيل",
        "category_id": "wrenches_hand_tools",
        "category_en": "Wrenches & Hand Tools",
        "category_ar": "المفاتيح والطربوشات",
        "description_en": "Complete 45-piece master tap and die thread repair set made of heat-treated Tungsten Steel. Includes adjustable tap handle wrench, T-handle tap wrench, die stock handle, thread pitch gauge, screwdriver, and full range of metric & fractional taps and dies in molded carry case.",
        "description_ar": "طقم شامل لتسنين وتصليح اللوالب ٤٥ قطعة مصنع من تنجستن ستيل المعالج حرارياً ضد التآكل. يحتوي على مقابض تدوير، مقياس درجات السن، ومجموعة كاملة من الذكور والمقلاوي بمختلف المقاسات في حقيبة منظمة.",
        "image": "images/products/246.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.47 PM (3).jpeg",
        "specs": ["45 Pieces Set", "Tungsten Steel", "Metric & SAE", "Tap Wrenches & Die Stocks", "Molded Carry Case"]
    },
    {
        "id": 247,
        "ref_no": "REF #247",
        "part_number": "ET-247",
        "name_en": "King Tony Chain Oil Filter Wrench (Ø 60~140mm)",
        "name_ar": "مفتاح فك فلتر زيت جنزير ٦٠-١٤٠ ملم كينغ توني",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "King Tony professional chain-type oil filter wrench with 225mm drop-forged chrome alloy steel handle. High-tensile duplex roller chain provides non-slip grip around cylindrical filters from 60mm up to 140mm diameter in tight engine bays.",
        "description_ar": "مفتاح فك فلاتر زيت جنزير احترافي ماركة كينغ توني. يد فولاذية بطول ٢٢٥ ملم مع جنزير متين يمسك بإحكام حول الفلاتر بقطر من ٦٠ إلى ١٤٠ ملم، مثالي للوصول في الأماكن المحصورة داخل حجرة المحرك.",
        "image": "images/products/247.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.47 PM (4).jpeg",
        "specs": ["King Tony Brand", "Capacity Ø 60-140mm", "225mm Handle", "Duplex Roller Chain", "Drop Forged Steel"]
    },
    {
        "id": 248,
        "ref_no": "REF #248",
        "part_number": "ET-248",
        "name_en": "Manual Lever Grease Gun & Chrome Oil Suction Gun Set",
        "name_ar": "مشحمة يدوية ضغط عالي + فرد سحب زيت كروم",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Professional workshop lubrication duo featuring a heavy duty manual lever-action grease gun with rigid steel nozzle tube, alongside a knurled chrome-plated cylinder fluid suction gun for precision fluid transfer.",
        "description_ar": "ثنائي التزييت والتشحيم الاحترافي للورش، يتضمن مشحمة يدوية بمقبض رافعة وفوهة معدنية، مع فرد سحب وضخ زيوت كروم منقوش ضد الانزلاق لتعبئة وسحب الزيوت بكفاءة.",
        "image": "images/products/248.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.48 PM.jpeg",
        "specs": ["Lever Grease Gun", "Chrome Suction Gun", "High Pressure Seal", "Knurled Grip", "Dual Workshop Set"]
    },
    {
        "id": 249,
        "ref_no": "REF #249",
        "part_number": "ET-249",
        "name_en": "JESAN No.1 High Pressure Air Grease Lubricator (50:1 Ratio)",
        "name_ar": "مشحمة هواء جيسان رقم ١ ضغط عالي نسبة ٥٠:١",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "JESAN No. 1 professional mobile pneumatic high pressure grease lubricator (Model: TC-12L). Features 50:1 pump pressure intensification ratio, inline air filter & water-trap regulator with pressure gauge, heavy duty hose, and mobile wheels.",
        "description_ar": "مشحمة هواء صناعية جيسان رقم ١ ضغط فائق بنسبة مضاعفة ٥٠:١ (موديل: TC-12L). مزودة بوحدة فلترة هواء مع مصيدة ماء ومنظم ضغط بساعة، خرطوم ضغط عالي، وقاعدة عجلات متينة.",
        "image": "images/products/249.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM.jpeg",
        "specs": ["JESAN No.1 TC-12L", "50:1 Pressure Ratio", "Water-Trap Regulator", "High Pressure Output", "Mobile Base"]
    },
    {
        "id": 250,
        "ref_no": "REF #250",
        "part_number": "ET-250",
        "name_en": "Portable Pneumatic Grease Pump with Handle & Drum Clamps",
        "name_ar": "مشحمة هواء محمولة مع مسكة علوية وقفل محكم",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Compact portable air-operated grease pump unit with ergonomic tubular carry handle, quick-locking drum clamps, pressure gauge regulator, and flexible high-pressure delivery hose.",
        "description_ar": "مشحمة هواء مدمجة وسهلة الحمل مزودة بمقبض علوي مريح، كلابات قفل محكمة للغطاء، منظم ضغط هواء مع ساعة قياس، وخرطوم مرن عالي التحمل.",
        "image": "images/products/250.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM (1).jpeg",
        "specs": ["Compact Portable", "Tubular Handle", "Air Regulator & Gauge", "Quick-Latch Lid", "Pneumatic Action"]
    },
    {
        "id": 251,
        "ref_no": "REF #251",
        "part_number": "ET-251",
        "name_en": "Pneumatic Waste Oil Drainer & Extractor with Glass Inspection Chamber",
        "name_ar": "مفرغة وشفاطة زيت محرك بالهواء مع بيلر زجاجي وصينية رفع",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "All-in-one professional pneumatic waste oil drainer and vacuum suction extractor (70L/80L). Equipped with transparent graduated inspection glass chamber for visual oil quality & volume checks, telescopic height-adjustable drain basin, probe kit, and mobile wheeled tank.",
        "description_ar": "جهاز متكامل لشفط وتفريغ زيت المحركات بالهواء سعة ٧٠-٨٠ ليتر. مزود ببيلر زجاجي شفاف مدرج لمعاينة كمية ونظافة الزيت المسحوب، صينية تجميع علوية قابلة لتعديل الارتفاع، طقم مجسات سحب، وخزان متحرك على عجلات.",
        "image": "images/products/251.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM (2).jpeg",
        "specs": ["70L/80L Tank", "Glass Inspection Chamber", "Pneumatic Vacuum Suction", "Telescopic Catch Pan", "Mobile Wheels"]
    },
    {
        "id": 252,
        "ref_no": "REF #252",
        "part_number": "ET-252",
        "name_en": "30-Piece Master Oil Filter Cap Socket Set with 3-Leg Claw Wrench",
        "name_ar": "طقم طرابيش فك فلاتر زيت ٣٠ قطعة مع عصفورة ثلاثية",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Complete 30-piece cup-type oil filter socket wrench set covering all automotive flutes and diameters with 3/8\" square drive. Includes 3-prong adjustable two-way claw filter wrench and adapter in heavy-duty molded case.",
        "description_ar": "طقم طرابيش احترافي لفك فلاتر الزيت ٣٠ قطعة يغطي مختلف قياسات وأشكال الفلاتر للسيارات الأمريكية، الأوروبية، واليابانية (توصيل ٣/٨ بوصة)، مع مفتاح عصفورة ثلاثي الأرجل قابل للتعديل في حقيبة متينة.",
        "image": "images/products/252.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM (3).jpeg",
        "specs": ["30 Pieces Set", "Cup Type Sockets (3/8\" Drive)", "3-Leg Claw Wrench", "Universal Fitment", "Heavy Duty Case"]
    },
    {
        "id": 253,
        "ref_no": "REF #253",
        "part_number": "ET-253",
        "name_en": "SJM Industrial Belt-Driven Twin Cylinder Air Compressor",
        "name_ar": "كمبريسور هواء صناعي قشاط سلندرين ماركة SJM",
        "category_id": "pneumatic_air_tools",
        "category_en": "Pneumatic & Air Tools",
        "category_ar": "معدات الهواء والكمبريسور",
        "description_en": "Heavy duty industrial belt-driven air compressor by SJM. Features high efficiency twin-cylinder finned cast-aluminum pump head, 100% copper wire electric motor, protective steel wire belt guard, automatic pressure switch, and pressure regulator with quick couplings.",
        "description_ar": "كمبريسور هواء صناعي بنظام القشاط ماركة SJM. مزود برأس ضخ مزدوج السلندر تبريد عالي، محرك كهربائي بأسلاك نحاس ١٠٠٪، شبك حماية للقشاط، مفتاح أوتوماتيك للضغط، وساعة تنظيم مع مخارج هواء سريعة.",
        "image": "images/products/253.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM (4).jpeg",
        "specs": ["SJM Brand", "Belt-Driven Twin Cylinder", "100% Copper Motor", "Automatic Pressure Switch", "Industrial Air Supply"]
    },
    {
        "id": 254,
        "ref_no": "REF #254",
        "part_number": "ET-254",
        "name_en": "Pneumatic Brake Fluid Bleeder & Exchanger Machine (LCH-F002)",
        "name_ar": "جهاز تبديل وتنسيم زيت الفرامل بالهواء (LCH-F002)",
        "category_id": "tire_wheel_service",
        "category_en": "Tire & Wheel Service",
        "category_ar": "خدمة الإطارات والمكابح",
        "description_en": "Professional pressurized pneumatic brake fluid bleeder and exchanger machine (Model: LCH-F002). Features chrome pressure vessel lid, spiral coiled hose with shut-off valve, quick-connect coupler, and complete master cylinder adapter set in hard case.",
        "description_ar": "جهاز احترافي لتبديل وتنسيم سائل الفرامل بالضغط الهوائي (موديل: LCH-F002). مزود بوعاء ضغط علوي كروم، خرطوم حلزوني مع صمام إغلاق، وصلة سريعة، وطقم كامل من وصلات أغطية طرمبة الفرامل في حقيبة مخصصة.",
        "image": "images/products/254.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM (5).jpeg",
        "specs": ["Model LCH-F002", "Pneumatic Pressure Bleeder", "Spiral Coil Hose", "Quick Coupler", "Master Cylinder Adapter Kit"]
    },
    {
        "id": 255,
        "ref_no": "REF #255",
        "part_number": "ET-255",
        "name_en": "King Tony Band Type Oil Filter Wrench (Up to 110mm - 9AE32-110)",
        "name_ar": "مفتاح فك فلتر زيت طوق صاج كينغ توني (حتى ١١٠ ملم)",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "King Tony heavy duty band-type oil filter wrench (Model: 9AE32-110). Made of high-grade stainless spring steel band with knurled adjustment knob and hex drive, designed for spin-on filters up to 110mm diameter.",
        "description_ar": "مفتاح فك فلاتر زيت طوق صاج احترافي ماركة كينغ توني (موديل: 9AE32-110). مصنع من سوار صاج ستانلس ستيل قوي مع برغي تعديل دقيق ورأس مسدس، مخصص للفلاتر حتى قطر ١١٠ ملم.",
        "image": "images/products/255.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM (6).jpeg",
        "specs": ["King Tony 9AE32-110", "Capacity Up to 110mm", "Stainless Steel Band", "Knurled Adjustment", "Hex Drive Compatible"]
    },
    {
        "id": 256,
        "ref_no": "REF #256",
        "part_number": "ET-256",
        "name_en": "TUFTUL Mechanic Magnetic Wing / Fender Protector Cover",
        "name_ar": "جلد حماية رفراف سيارات مغناطيس تفتول",
        "category_id": "body_repair_welding",
        "category_en": "Body Repair & Welding",
        "category_ar": "الحدادة والتجليس واللحام",
        "description_en": "Heavy duty padded vinyl mechanic wing and fender protective cover by Tuftul. Features strong embedded magnets and metal grommet eyelets to firmly protect vehicle paintwork against scratches, dents, and oil during engine repair.",
        "description_ar": "غطاء حماية جلد سميك ومبطن لرفارف السيارات ماركة تفتول. مزود بمغناطيسات قوية مدمجة وثقوب تثبيت لحماية طلاء وهيكل السيارة من الخدوش، الصدمات، وبقع الزيوت أثناء أعمال الصيانة.",
        "image": "images/products/256.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.49 PM (7).jpeg",
        "specs": ["TUFTUL Brand", "Magnetic Attachment", "Padded Heavy Vinyl", "Paint Scratch Protection", "Oil & Grease Resistant"]
    },
    {
        "id": 257,
        "ref_no": "REF #257",
        "part_number": "ET-257",
        "name_en": "Swivel Handle Steel Band Oil Filter Wrench",
        "name_ar": "مفتاح فك فلتر زيت مقبض متحرك كوتشوك",
        "category_id": "engine_oil_service",
        "category_en": "Engine & Fluid Service",
        "category_ar": "خدمة المحرك وسحب السوائل",
        "description_en": "Heavy duty oil filter wrench with 180-degree swiveling ergonomic cushioned grip handle and dimpled non-slip stainless steel tension band for maximum torque on stubborn spin-on automotive oil filters.",
        "description_ar": "مفتاح فك فلاتر زيت بمقبض مريح قابل للدوران ١٨٠ درجة مع طوق صاج ستانلس منقر مانع للانزلاق، يمنح قوة عزم عالية لفك الفلاتر المستعصية في زوايا المحرك الصعبة.",
        "image": "images/products/257.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.50 PM.jpeg",
        "specs": ["Swivel Handle 180°", "Dimpled Steel Band", "Cushion Grip", "Anti-Slip Action", "Universal Spin-On"]
    },
    {
        "id": 258,
        "ref_no": "REF #258",
        "part_number": "ET-258",
        "name_en": "JONNESWAY Pneumatic Brake Bleeder & Fluid Extractor Set (AE300176)",
        "name_ar": "جهاز تنفيس وسحب زيت الفرامل هواء جونسواي (AE300176)",
        "category_id": "tire_wheel_service",
        "category_en": "Tire & Wheel Service",
        "category_ar": "خدمة الإطارات والمكابح",
        "description_en": "Jonnesway professional 2L pneumatic brake fluid bleeder and fluid evacuation unit (Model: AE300176). Features ergonomic trigger air valve, integrated silencer, flexible suction line, and multi-adapter master cylinder connection kits in hard cases.",
        "description_ar": "جهاز سحب وتنسيم زيت الفرامل بالهواء سعة ٢ ليتر احترافي ماركة جونسواي (موديل: AE300176). مزود بمقبض ضخ سريع مع كاتم صوت، خراطيم شفافة، وطقم وصلات متعدد القياسات لعلب الفرامل في حقائب مخصصة.",
        "image": "images/products/258.jpg",
        "source_file": "WhatsApp Image 2026-09-02 at 8.49.50 PM (1).jpeg",
        "specs": ["JONNESWAY AE300176", "2L Fluid Reservoir", "Pneumatic Venturi Suction", "Silenced Air Exhaust", "Master Adapter Kits"]
    }
]

def main():
    # 1. Process and copy images
    os.makedirs('images/products', exist_ok=True)
    
    print('Processing 18 Batch 2 images...')
    for item in BATCH2_ITEMS:
        src_path = os.path.join('batch2', item['source_file'])
        dst_path = os.path.join('images', 'products', f"{item['id']}.jpg")
        
        if os.path.exists(src_path):
            img = Image.open(src_path)
            # Convert RGBA/P to RGB if needed
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            # Save normalized high quality JPG
            img.save(dst_path, 'JPEG', quality=90, optimize=True)
            print(f"  [OK] Saved {dst_path} from {item['source_file']}")
        else:
            print(f"  [WARNING] Missing {src_path}")
            
    # 2. Update catalog.json
    with open('catalog.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)
        
    print(f"Current catalog has {len(catalog)} items.")
    
    # Filter out any existing entries with ids >= 241 to avoid duplicates
    catalog = [c for c in catalog if c['id'] < 241]
    
    # Clean up item dicts (remove source_file before saving)
    for item in BATCH2_ITEMS:
        item_copy = dict(item)
        item_copy.pop('source_file', None)
        catalog.append(item_copy)
        
    print(f"New catalog has {len(catalog)} items.")
    
    with open('catalog.json', 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        
    print("Successfully updated catalog.json with items 1 through 258!")

if __name__ == '__main__':
    main()
