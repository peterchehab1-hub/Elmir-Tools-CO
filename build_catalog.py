import os
import json
import re
import shutil
from PIL import Image

# 1. Complete raw data transcribed directly from the 9 binder scan pages
ITEMS_DATA = [
    # Page 1 (1 - 27)
    (1, "Cezar car lift", "عفريت سيزر", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Scissor Lift", "Mid-rise", "Automotive"]),
    (2, "4 posts car lift", "عفريت ٤ ارجل", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["4-Post Lift", "Heavy Duty", "Alignment"]),
    (3, "2 Posts car lift", "عفريت ٢ ارجل", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["2-Post Lift", "Hydraulic", "Clear Floor"]),
    (4, "Trolley jack-OMCN", "عفريت OMCN", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Trolley Jack", "OMCN", "Professional Hydraulic"]),
    (5, "Low profile jack", "عفريت طويل واطي", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Low Profile", "Long Chassis", "Sports Cars"]),
    (6, "3 ton short jack", "عفريت قصير", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["3 Ton", "Short Body", "Compact"]),
    (7, "Low profile small jack", "عفريت قصير واطي", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Low Profile", "Small Frame", "Hydraulic"]),
    (8, "Portable low 4.5 ton", "عفريت واطي ٤.٥ طن", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["4.5 Ton", "Low Profile", "Portable"]),
    (9, "brake disc lathe machine", "جلخ ديسك", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Brake Lathe", "On-Car / Bench", "Disc Resurfacing"]),
    (10, "tanbour brake lathe machine", "جلخ طامبور", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Drum Lathe", "Heavy Duty", "Brake Drum"]),
    (11, "Motor stand", "جسر موتور", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Engine Support Beam", "Adjustable", "Crossbar"]),
    (12, "big motor stand", "جسر موتور كبير", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Heavy Engine Stand", "Universal", "Transverse Support"]),
    (13, "Crane hydraulic jack", "عفريت جمل", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Engine Crane", "Folding Cherry Picker", "Hydraulic Hoist"]),
    (14, "Transmission lift", "عفريت فيتاس", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Transmission Jack", "Telescopic", "Hydraulic"]),
    (15, "6 ton jack stands", "جحش ٦ طن", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["6 Ton", "Pair", "Safety Ratchet Stands"]),
    (16, "3 ton jack stands", "جحش ٣ طن", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["3 Ton", "Pair", "Steel Jack Stands"]),
    (17, "Big jack stands", "جحش عفريت كبير", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Heavy Vehicle Stands", "High Lift", "Commercial"]),
    (18, "Folding engine stand", "حمالة موترو (فروج)", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Engine Stand", "360 Rotating", "Folding Legs"]),
    (19, "Hydraulic press 20 ton", "مكبس ٢٠ طون", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["20 Ton", "Shop Press", "Pressure Gauge"]),
    (20, "Combination wrench set", "طقم ميلة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Metric", "Chrome Vanadium", "Storage Roll"]),
    (21, "Small screw (Precision)", "مفك عيار", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Precision Screwdriver", "Slotted", "Adjustment"]),
    (22, "Offset wrench set", "طقم مسنن", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Offset Ring Wrench", "75 Degree", "Metric Set"]),
    (23, "open end wrench set", "طقم شق", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Double Open End", "Metric", "Polished"]),
    (24, "Screw set", "طقم مفك", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Screwdriver Set", "Ergonomic Grip", "Magnetic Tip"]),
    (25, "Star screw set", "طقم مفك نجمة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Torx Screwdrivers", "Extra Long", "Star Drive"]),
    (26, "Big test (Circuit tester)", "فاحص كبير", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Voltage Tester", "Automotive Light Tester", "6-24V"]),
    (27, "Small test (Circuit tester)", "فاحص صغير", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Compact Voltage Tester", "Brass Body", "Test Probe"]),

    # Page 2 (28 - 58)
    (28, "plier set", "طقم بنسة", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Combination Pliers", "Diagonal", "Long Nose"]),
    (29, "Circlip plier set", "طقم بنسة سيكمان", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Snap Ring Pliers", "Internal/External", "4-Piece"]),
    (30, "Vise grip plier", "بنسة لقط", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Locking Pliers", "Vise Grip", "Adjustable Jaw"]),
    (31, "Magnetic pick-up tool", "مغناطيس", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Flexible Magnetic", "Telescopic Pick-up", "Tool Grabber"]),
    (32, "Star socket set", "طقم طربوش نجمة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Torx Star Bit Sockets", "Metal Case", "1/2 inch"]),
    (33, "Hex socket set", "طقم طربوش مسدس", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Allen Hex Bit Sockets", "Drive Sockets", "Steel Box"]),
    (34, "Spline tip set", "طقم طربوش مشرشر", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["XZN Spline Sockets", "German Spec", "Heavy Duty"]),
    (35, "Star L set", "L طقم نجمة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Torx L-Key Set", "Long Arm", "Fold Holder"]),
    (36, "Hex L set", "L طقم مسدس", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Hex Allen L-Key Set", "Ball End", "Metric"]),
    (37, "1/2 Socket set", "طقم طربوش ١/٢", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["1/2 Inch Drive", "Ratchets & Sockets", "Metal Case"]),
    (38, "3/8 Socket set", "طقم طربوش ٣/٨", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["3/8 Inch Drive", "Ratcheting Set", "Pro Grade"]),
    (39, "1/4 Socket set", "طقم طربوش ١/٤", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["1/4 Inch Drive", "Mini Mechanics Set", "Precision"]),
    (40, "Ball joint separator", "شوكة بيضة", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Fork Pickle Wedge", "Ball Joint / Tie Rod", "Forged Steel"]),
    (41, "Chisel set", "طقم ازميل", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Cold Chisels", "Flat / Pointed", "Tempered"]),
    (42, "Saw (Hacksaw)", "منشار حديد", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Adjustable Hacksaw", "Bi-Metal Blade", "Ergo Handle"]),
    (43, "BMW specialty tool set", "bmw طقم", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Timing / Service", "BMW Specialist", "Blow Mold Case"]),
    (44, "E Socket set", "E طقم طربوش", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Female Torx E-Sockets", "E4 to E24", "Chrome Vanadium"]),
    (45, "Star box end wrench set", "E طقم مفتاح", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Double End Torx Wrench", "E-Star Box", "Steel Tray"]),
    (46, "Hammer 2 kg", "مطرقة ٢ كيلو غرام", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["2 KG Sledge", "Wooden Handle", "Blacksmith Hammer"]),
    (47, "Claw hammer (1 / 1.5 / 0.5 kg)", "شاكوش ١/١.٥/٠.٥", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Claw Hammer", "Multisize", "Shock Absorbing"]),
    (48, "Punch set", "طقم سنبك", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Pin Punches", "Center Punch", "Tapered"]),
    (49, "Trolley 7 Drawers", "طاولة ٧ جوارير", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["7-Drawer Tool Cabinet", "Heavy Duty Casters", "Lockable"]),
    (50, "Trolley 3 shelf", "طاولة ٣ رفوف", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["3-Tier Service Cart", "Utility Trolley", "Steel Frame"]),
    (51, "Tool box (Cantilever)", "شنطة عدة", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Metal Tool Box", "5-Tray Cantilever", "Portable"]),
    (52, "Tool box full with tools", "شنطة عدة كاملة", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Complete Mechanics Set", "Fitted Foam/Trays", "Multi-Piece"]),
    (53, "Mechanical vise", "ملزمة", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Heavy Duty Bench Vise", "Swivel Base", "Cast Iron"]),
    (54, "Clamp plier set", "طقم بنسة رباط ماء", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Hose Clamp Pliers Set", "Cable Type", "Cooling System"]),
    (55, "Clamp plier", "بنسة رباط ماء", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Single Hose Clamp Plier", "Swivel Jaw", "Spring Loaded"]),
    (56, "Fan clutch service set", "طقم مفتاح مروحة", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Fan Clutch Wrench", "Water Pump Tool", "Universal"]),
    (57, "Oil cooler line plier", "بنسة براد زيت", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Oil Cooler Disconnect", "Transmission Line", "Quick Release"]),
    (58, "Fuel line plier (ML)", "ML بنسة", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Fuel Pipe Plier", "Filter Line Clip", "Specialized"]),

    # Page 3 (59 - 88)
    (59, "Oxygen sensor socket set", "طقم اوكسيجين سنسور", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["O2 Sensor Socket", "Slotted", "Thread Chaser"]),
    (60, "CV boot clamp installer", "بنسة رباط حديد", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["CV Joint Boot Plier", "Banding Tool", "Ear-Type"]),
    (61, "Bench grinder", "جلخ ثابت", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Double Wheel Grinder", "Eye Shields", "Tool Rest"]),
    (62, "Assembling wheel nut wrench (Cross)", "مفتاح جنط", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["4-Way Cross Wrench", "Lug Nut Wrench", "Folding / Solid"]),
    (63, "Oil can", "مزيتة", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Manual Pump Oiler", "Flexible Spout", "Steel Can"]),
    (64, "Brake caliper tool piston", "طقم كولية فرام برم", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Brake Caliper Wind Back", "Multi-Adapter", "Disc Brake"]),
    (65, "Valve spring compressor 24/16", "برسة صباب", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["C-Clamp Style", "OHV / OHC", "Engine Head"]),
    (66, "Valve spring compressor (In-situ)", "برسة صباب على الراكب", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["On-Engine Spring Compressor", "Overhead Cam", "No Head Removal"]),
    (67, "Screw extractor set", "طقم سن شمال", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Spiral Flute Extractors", "Broken Bolt Extractor", "Hardened Steel"]),
    (68, "Ball joint separator set", "طقم شوكة بيصة", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Multi-Size Pickle Forks", "Pneumatic / Manual", "Tie Rod Splitter"]),
    (69, "Air hammer", "فرد هواء شوكة", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Pneumatic Chisel Hammer", "4-Chisel Kit", "Quick Change"]),
    (70, "Obeng ketok (Impact driver)", "مفك طرق", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Manual Impact Driver", "Reversible 1/2 Drive", "Heavy Strike"]),
    (71, "Pry bar set", "طقم قارص", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Curved Pry Bars", "Striking Cap", "Heavy Duty"]),
    (72, "Angled socket wrench set", "طقم كوع", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["L-Type Angled Sockets", "Pass-Through Hex", "Metric Set"]),
    (73, "T-type deep socket wrench set", "T طقم مسكة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["T-Handle Sockets", "Deep Reach", "Ergonomic T-Bar"]),
    (74, "Extra long plier set", "بنسة بوز رفيع طويلة", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Long Reach 11 Inch", "Straight & Bent 45/90", "Dipped Handles"]),
    (75, "Forge plier (Water pump)", "بنسة فورغ", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Water Pump Plier", "Groove Joint", "Forged Steel"]),
    (76, "Levier (Heavy pry bars)", "قارص", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Roll Head Pry Bar", "Levering Bar", "Alignment Pry"]),
    (77, "3/4 Socket set", "طقم طربوش ٣/٤", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["3/4 Inch Drive", "Truck / Heavy Machinery", "Socket Kit"]),
    (78, "Long Flexible handle 1/2", "مسكة شد كبيرة ١/٢", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Breaker Bar 1/2", "Flex Head", "High Torque"]),
    (79, "Adjustable torque wrench", "مسكة شد كولاس", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Click Type Torque Wrench", "Micrometer Scale", "1/2 Drive"]),
    (80, "Long 1/2 socket set", "طقم طربوش ١/٢ طويل", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Deep Well 1/2", "Chrome Vanadium", "Rail Holder"]),
    (81, "Long 3/8 socket set", "طقم طربوش ٣/٨ طويل", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Deep Well 3/8", "Mirror Chrome", "Metric Sizes"]),
    (82, "Long 1/4 socket set", "طقم طربوش ١/٤ طويل", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Deep Well 1/4", "Precision Access", "Socket Rail"]),
    (83, "Black impact socket 17/19/21", "طربوش اسود ١٧/١٩/٢١", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Non-Marring Wheel Sockets", "Protective Sleeve", "Impact 1/2"]),
    (84, "Long extension set", "طقم وصلة طويلة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Extension Bars", "1/2 Drive Long", "Knurled Shaft"]),
    (85, "Wobble extension set 1/2 3/8 1/4", "طقم وصلة مخلع ١/٤ ٣/٨ ١/٢", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Wobble Drive", "Angle Extensions", "Multi-Drive Set"]),
    (86, "Socket set 1/2 with Ratchet", "طقم طربوش ١/٢ مسنن", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["1/2 Complete Set", "72-Tooth Ratchet", "Steel Storage Box"]),
    (87, "Black impact socket set", "طقم طربوش اسود", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Impact Grade Sockets", "CR-MO Alloy", "Heavy Blow Mold Box"]),
    (88, "3/4 Sliding T-Handle", "مسكة شد ٣/٤", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Sliding T-Bar", "3/4 Inch Drive", "Heavy Leverage"]),

    # Page 4 (89 - 118)
    (89, "Axle Socket 30 32 34 36", "طربوش مسنن ٣٠ ٣٢ ٣٤ ٣٦", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["12-Point Axle Nut", "30mm 32mm 34mm 36mm", "Deep Impact"]),
    (90, "Spark plug plier", "بنسة بوجي", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Boot Puller", "Angled Ring Nose", "Insulated Handles"]),
    (91, "Valve stem seal plier", "بنسة صباب", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Stem Seal Removal", "Serrated Tips", "Extra Long Shank"]),
    (92, "Flare nut wrench set", "طقم مفتاح ماصورة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Brake Line Wrench", "6-Point Flare", "Metric Set"]),
    (93, "Half moon ring wrench set", "طقم قمر", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["C-Shape Curved Wrench", "Starter & Manifold", "Double Ring"]),
    (94, "S wrench set", "S طقم", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["S-Type Obstruction Wrench", "Double Box End", "Confined Space"]),
    (95, "Twist socket set", "طقم طربوش فك عزق", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Damaged Lug Nut Extractor", "Reverse Spiral Flute", "Impact Ready"]),
    (96, "Air Compressor (150/200/300/500 L)", "كومبريسور ١٥٠/٢٠٠/٣٠٠/٥٠٠", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Industrial Piston Compressor", "Cast Iron Pump", "Large Tank Capacity"]),
    (97, "Heavy duty black hose", "نربيج اسود ايطالي", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Reinforced Rubber", "High Pressure", "Italian Quality"]),
    (98, "PU air spiral hose", "نربيج روسور", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Polyurethane Recoil Hose", "Quick Couplers", "Spring Guards"]),
    (99, "Air hose reel", "بكرة نربيج هواء", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Automatic Retractable", "Wall Mounted", "Locking Mechanism"]),
    (100, "Electrical cable reel", "بكرة كهرباء", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Heavy Duty Cable Reel", "Thermal Cutout", "Multi-Socket"]),
    (101, "1/2 Impact wrench", "فرد شد عزق ١/٢", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["1/2 Inch Air Impact", "Twin Hammer", "High Torque"]),
    (102, "3/8 Impact wrench", "فرد شد عزق ٣/٨", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["3/8 Inch Pneumatic Impact", "Compact Body", "Engine Bay"]),
    (103, "1/4 Impact wrench", "فرد شد عزق ١/٤", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["1/4 Inch Mini Impact", "Lightweight", "Precision Tightening"]),
    (104, "3/4 Impact wrench", "فرد شد عزق ٣/٤", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["3/4 Heavy Duty Air Impact", "High Output", "Commercial Trucks"]),
    (105, "1/2 Impact ratchet wrench", "طقطاق هواء ١/٢", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["1/2 Pneumatic Ratchet", "Slim Profile", "Forward/Reverse"]),
    (106, "3/8 Impact ratchet wrench", "طقطاق هواء ٣/٨", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["3/8 Pneumatic Ratchet", "Variable Speed", "Ergonomic Grip"]),
    (107, "1/4 Impact ratchet wrench", "طقطاق هواء ١/٤", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["1/4 Mini Air Ratchet", "Fast Run Down", "Tight Spaces"]),
    (108, "Big angle grinder", "صاروخ كبير", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["230mm Electric Grinder", "Industrial Motor", "Safety Guard"]),
    (109, "Small angle grinder", "صاروخ صغير", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["115mm / 125mm Grinder", "Compact One-Hand", "High RPM"]),
    (110, "Electric polisher", "صاروخ بوليش", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Rotary Car Buffer", "Variable Speed", "Foam / Wool Pads"]),
    (111, "Air body saw", "منشار هواء", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Pneumatic Reciprocating Saw", "Sheet Metal Cutting", "Safety Trigger"]),
    (112, "Air angle grinder", "صاروخ هواء", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Pneumatic Angle Grinder", "Exhaust Handle", "Cutting & Grinding"]),
    (113, "Craftsman 2-3 jaw gear puller", "برسة ٢-٣ ارجل", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Reversible 2/3 Jaws", "Bearing & Gear Removal", "Drop Forged"]),
    (114, "Air drill", "مقدح هواء", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Pneumatic Pistol Drill", "Keyless Chuck", "Reversible Air Drill"]),
    (115, "Battery cordless drill set", "مقدح بطارية", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Lithium-Ion Cordless", "2 Batteries + Charger", "Carry Case"]),
    (116, "Electric drill", "مقدح كهرباء", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Impact Electric Drill", "Variable Speed Trigger", "Keyed Chuck"]),
    (117, "Cordless battery impact wrench", "فرد شد عزق بطارية", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Brushless Cordless Impact", "High Torque 20V/21V", "Twin Batteries"]),
    (118, "Strap wrench (Oil filter)", "قشاط زيت", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Heavy Nylon Strap", "Forged Steel Handle", "Universal Diameter"]),

    # Page 5 (119 - 146)
    (119, "Three-legs oil filter wrench", "فلتر ٣ ارجل", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["3-Jaw Auto Grip", "Two-Way Drive 3/8 & 1/2", "Spider Wrench"]),
    (120, "Transmission oil filling tool", "زيت فيتاس", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Pneumatic ATF Dispenser", "Multi-Adapter Kit", "Pressurized Tank"]),
    (121, "Radiator pressure tester coolant kit", "ضغط رادياتور", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Cooling System Tester", "Vacuum Purge & Refill", "Universal Adapters"]),
    (122, "Car creeper (Plastic)", "فرشة نوم بلاستيك", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Ergonomic Molded Plastic", "Padded Headrest", "6 Swivel Wheels"]),
    (123, "Oil filter plier", "بنسة زيت", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Adjustable Oil Filter Pliers", "Toothed Jaws", "Long Handle"]),
    (124, "Oil filter socket cup set", "طقم طربوش زيت", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Cap Wrench Sockets", "Fluted Aluminum Caps", "Euro & Asian Cars"]),
    (125, "Iron car creeper", "فرشة نوم حديد", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Steel Tubular Frame", "Fully Padded Vinyl", "Heavy Load Capacity"]),
    (126, "Mobile work chair / Creeper stool", "كرسة عفريت", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Padded Swivel Stool", "Under-Seat Tool Tray", "Heavy Duty Casters"]),
    (127, "Engine Oil dipstick", "شيش موتور", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Flexible Measurement Tool", "Level Indicator", "Specialist Fitment"]),
    (128, "Transmission fluid dipstick", "شيش فيتاس", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["ATF Measurement Tool", "Graduated Scale", "Mercedes / VAG Fit"]),
    (129, "Oil suction gun", "حقنة فالفولين", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Suction Syringe 500ml", "Flexible Hose", "Gearbox & Diff Fluid"]),
    (130, "40 pcs bit set", "طقم راس ٤٠ قطعة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Torx / Hex / Spline", "3/8 & 1/2 Adapters", "Steel Case"]),
    (131, "Stubby combination wrench set", "طقم ميلة قزم", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Short Shank Wrenches", "Tight Engine Clearance", "Metric Set"]),
    (132, "Stubby combination ratcheting wrench set", "طقم ميلة قزم طقطاق", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Stubby Ratchet Wrench", "Fine Gear Mechanism", "Mirror Chrome"]),
    (133, "Air soldering station", "كاوي هواء", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Hot Air Rework Station", "Digital Temperature", "SMD / Wiring"]),
    (134, "Soldering iron", "كاوي", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Electric Solder Pen", "Interchangeable Tip", "Automotive Wiring"]),
    (135, "Tyre inflator with gauge", "ساعة دولاب", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Digital/Analog Pressure Gauge", "Clip-On Air Chuck", "Heavy Duty Hose"]),
    (136, "Digital multimeter (Ohmmeter)", "اومتر", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Digital Multimeter", "Auto Ranging", "Voltage / Resistance / Current"]),
    (137, "Piston rings compressor set", "طوق سكمان", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Ratchet Piston Installer", "Pliers + Bands", "Multi-Cylinder Sizes"]),
    (138, "Rofire blowtorch + gas", "حراق+غاز", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Gas Torch Kit", "Piezo Ignition", "Heating & Soldering"]),
    (139, "Utility cutter / Knife", "شفرة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Heavy Duty Snap Blade", "Metal Guide", "Locking Slider"]),
    (140, "Oil drain pan", "جاط زيت", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Polyethylene Drain Basin", "Splash Guard Lip", "Pouring Spout"]),
    (141, "Large pneumatic fluid extractor", "شفط زيت كبيرة", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Pneumatic Oil Extractor", "Drain Basin & Inspection Tube", "Trolley Mounted"]),
    (142, "Small pneumatic fluid extractor", "شفط زيت صغيرة", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Manual/Pneumatic Extractor", "Portable Cannister", "Multi Suction Probes"]),
    (143, "6 plates spring compressor", "برسة روسور ٦ صحون", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Strut Spring Compressor", "Interchangeable Yokes", "Safety Lip"]),
    (144, "Coil spring compressor", "برسة روسور برغي", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["2-Piece Threaded Compressor", "Forged Carbon Steel", "Suspension Service"]),
    (145, "Hydraulic coil spring compressor", "برسة روسور رجل", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Foot-Operated Hydraulic", "Floor Standing", "Safety Cage Frame"]),
    (146, "Cleaning injector machine (inside/on-car)", "تنظيف بخاخ على الراكب", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Non-Dismantle Cleaner", "Fuel System Flush", "Pressure Regulated"]),

    # Page 6 (147 - 174)
    (147, "Cleaning injector machine (outside/bench)", "تنظيف بخاخ على الفاكيك", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Ultrasonic Cleaning Bench", "Flow Testing Glass Tubes", "Electronic Pulse Drive"]),
    (148, "AC machine for car (Refrigerant station)", "ماكينة مكيف", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Fully Automatic A/C Station", "Recovery & Vacuum & Charge", "R134a / R1234yf"]),
    (149, "Impact socket adapter & reducer set", "طقم تحاويل", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Step Up / Step Down", "1/4 to 3/4 Adapters", "Impact Cr-Mo"]),
    (150, "Electric balladeuse (Inspection light)", "ضو شريط", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Corded Work Lamp", "Protective Cage & Hook", "Heavy Duty Cable"]),
    (151, "Balladeuse rechargeable (Cordless LED)", "ضو تشريج", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Rechargeable COB LED", "Magnetic Base & Swivel", "USB Charging"]),
    (152, "Gasoline engine injection pressure test", "ساعة ضغط بنزين", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Fuel Pump Pressure Gauge", "Quick Couplers Kit", "0-140 PSI"]),
    (153, "Car cylinder leakage tester kit", "ساعة ضغط موتور", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Dual Gauge Leakdown Tester", "Spark Plug Adapters", "Engine Diagnostics"]),
    (154, "Hand held DIY brake fluid bleeder", "فرد تنفيس فرام", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Vacuum Pump Bleeder Kit", "Reservoir Jar", "One-Man Brake Bleed"]),
    (155, "Pneumatic brake bleeder kit", "ماكينة تنفيس فرام", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Air Powered Brake Bleeder", "Master Cylinder Adapters", "Automatic Refill"]),
    (156, "Two jaws pulley remover set", "طقم بكرة كرنك", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Harmonic Balancer Puller", "Crankshaft Pulley Tool", "Cross Bar & Bolts"]),
    (157, "Socket holder rack (Magnetic / Rail)", "شكة طربوش", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Socket Organizer Rails", "1/4 3/8 1/2 Clips", "Wall / Drawer Mount"]),
    (158, "Speed wrench set", "ميلة طقطاق", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Ratcheting Combination Set", "King Tony Professional", "Wall Pouch"]),
    (159, "Flexible speed wrench set", "ميلة طقطاق مخلع", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Flex Head Ratchet Wrench", "180 Degree Swivel Head", "Mirror Chrome"]),
    (160, "Metric feeler gauge", "كاليبيرا", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Steel Blade Feeler Gauge", "Valve Lash & Gap Measure", "Foldable Blades"]),
    (161, "Pressure screw bearing separator puller", "طقم برسة رولمان صحن", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Bearing Splitter Set", "Extension Rods & Yoke", "Heavy Drop Forged"]),
    (162, "Welding machine (Inverter ARC/MMA)", "ماكينة لحام", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["IGBT Inverter Welder", "Electrode Clamp & Ground", "Portable Shoulder Strap"]),
    (163, "Washing spray gun", "فرد غسيل", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["High Pressure Wash Gun", "Detergent Canister", "Fan & Jet Nozzles"]),
    (164, "Shampoo foam machine", "ماكينة صابون", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Stainless Steel Foam Tank", "Pneumatic Foam Generator", "Car Wash Pressure"]),
    (165, "High pressure washing machine", "ماكينة غسيل", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Heavy Duty Pressure Washer", "Induction Motor", "Wheeled Chassis"]),
    (166, "Hoover / Industrial vacuum cleaner", "هوفر", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Wet & Dry Vacuum", "Stainless Drum", "High Suction Power"]),
    (167, "Small washing machine (Portable washer)", "ماكينة غسيل صغيرة", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Compact Pressure Washer", "Domestic / Auto Detail", "Adjustable Lance"]),
    (168, "Nylon & masking paper stand", "ستاند نايلون + ورق ارض", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Mobile Paper Dispenser", "Double Roll Cutter", "Paint Shop Stand"]),
    (169, "Magnetic fender protective cover", "جلد رفراف", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Scratch Proof Wing Cover", "Strong Embedded Magnets", "Washable Vinyl"]),
    (170, "Deluxe noid lite test set", "طقم لمبة بخاخ", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["EFI Signal Pulse Tester", "IAC & Fuel Injector Light", "Molded Box"]),
    (171, "MIG / Flux wire welding machine", "ماكينة لحام شريط", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Gas / Gasless MIG Welder", "Continuous Wire Feed", "Automotive Bodywork"]),
    (172, "Hydraulic body frame repair 10 ton", "طقم سحب حدادة ١٠ طون", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Porta Power 10 Ton Ram", "Hydraulic Pump & Extensions", "Heavy Blow Mold Kit"]),
    (173, "Repair body hammer set", "شاكوش حدادة", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Panel Beating Hammers", "Hickory Wooden Handles", "Precision Peen"]),
    (174, "Car sheet metal dollies & tools", "سندة حدادة", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Anvil & Dolly Set", "Heel / Curved / Toe Dolly", "Drop Forged Steel"]),

    # Page 7 (175 - 203)
    (175, "Pull clamp Auto body frame repair", "لقطة جدادة", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Self-Tightening Pull Clamp", "2-Way / 3-Way Pulling", "Heavy Forged Steel"]),
    (176, "Manual chain lever hoists", "بلانكو طقطاق", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Lever Chain Hoist", "Heavy Lifting Ratchet", "Grade 80 Chain"]),
    (177, "Plastic welding machine (Hot stapler)", "ماكينة لحام بلاستيك", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Bumper Repair Welder", "Assorted Wave Staples", "Thermal Cutter"]),
    (178, "Oven car painting spray booth", "فرن رش", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Full Downdraft Spray Booth", "Heating & Filter System", "Professional Auto Paint"]),
    (179, "Car body dent puller bench", "ماكينة سحب شاسي", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Chassis Alignment Bench", "Hydraulic Pulling Towers", "Multi-Point Anchoring"]),
    (180, "Slide hammer body work puller set", "برسة سحب مطرقة", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Heavy Slide Hammer", "Multi-Jaw Puller Hooks", "Axle & Dent Pulling"]),
    (181, "Auto darkening welding mask", "وجه لحام", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Solar Powered Auto Darkening", "Variable Shade Control", "Arc / MIG / TIG"]),
    (182, "Automotive diagnostic scanner", "سكانر", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["OBD2 Diagnostic Tablet", "Full System Scanner & Reset", "Adapters & Cables"]),
    (183, "Tire / Wheel removal machine", "ماكينة تشليح دواليب", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Pneumatic Tire Changer", "Helper Arm Assist", "Alloy Rim Protection"]),
    (184, "Tyre balance machine", "ماكينة ترصرص دواليب", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Digital Wheel Balancer", "Auto Calibration & Laser", "Multi-Balancing Modes"]),
    (185, "3D Wheel alignment system", "ماكينة ميزان سيارة", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["High-Precision 3D Cameras", "Beam & Target Clamp Plates", "Automotive Alignment"]),
    (186, "Tap and Die set 40 pcs", "طقم قلاووظ", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Metric Threading Tools", "Tap Wrenches & Die Holders", "Molded Blue Case"]),
    (187, "Heavy duty battery charger & booster", "شارج بطارية", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["12V / 24V Fast Charger", "Engine Jump Starter", "Heavy Duty Clamps"]),
    (188, "Radio removal key kit", "طقم فك راديو", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Universal Radio Removal Keys", "Audi/BMW/Mercedes/Ford Fit", "Fabric Pouch"]),
    (189, "Infrared laser thermometer", "فرد حرارة", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Non-Contact Laser Gun", "Digital LCD Display", "Engine & Brake Temp"]),
    (190, "Automotive smoke leak detector machine", "ماكينة دخنة لفحص سيارة", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["EVAP & Vacuum Smoke Tester", "Built-In Air Compressor", "Flow Meter & Accessories"]),
    (191, "Double open end flexible socket wrench", "طقم طربوش مسكة", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Swivel Head Socket Wrench", "Double Sided Metric", "Satin Finish"]),
    (192, "Nut splitter 4-piece set", "طقم قص عزق", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Heavy Duty Nut Cutters", "Rusted Nut Breaker", "Drop Forged Steel"]),
    (193, "Heavy duty pipe wrench", "رنش", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Cast Iron Pipe Wrench", "Hardened Hook Jaw", "Self-Cleaning Threads"]),
    (194, "Welding locking clamps plier set", "بنسة حدادة", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["C-Clamp Locking Pliers", "Sheet Metal Clamps", "Chrome Finish"]),
    (195, "Ratchet flaring tool kit", "طقم تفليج", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Eccentric Cone Flaring", "Tube Cutter & Reamer", "Brake & AC Pipes"]),
    (196, "Electric industrial hot air gun", "سشوار حدادة", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Variable Heat Temperature", "Nozzle Attachments", "Shrink Tube & Paint Strip"]),
    (197, "Auto electrical connector separator pliers", "نبسة فيش كهرباء", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Electrical Plug Release", "Deep Reach Tips", "Damage-Free Unplugging"]),
    (198, "Air pump wedge alignment hand tool set", "طقم فتح زجاج", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Inflatable Air Shim", "Emergency Door Opening", "Non-Marking TPU"]),
    (199, "Heavy duty battery booster cables", "شريط تدكير", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Tangle Free Booster Jumper", "Pure Copper Clamps", "High Amperage Gauge"]),
    (200, "Impact universal joint accessory", "طربوش اسود مخلع", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Impact Swivel U-Joint", "Pin Ball Lock", "CR-MO Black Phosphate"]),
    (201, "Pointeuse spot welder machine", "حدادة ضرب كهرباء", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Stud Welder Dent Puller", "Multi-Function Gun", "Trolley Mounted"]),
    (202, "Air blow gun", "فرد هواء", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Ergonomic Pistol Trigger", "Extended Nozzle", "High Velocity Airflow"]),
    (203, "Aviation tin snips set", "مقص تول", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Left / Right / Straight Cut", "Compound Action Leverage", "Chrome Vanadium"]),

    # Page 8 (204 - 231)
    (204, "Wire crimping & stripping tool", "بنسة كهرباء", "pliers_cutters", "Pliers & Cutters", "البنسات والقطاعات", ["Multi-Function Wire Stripper", "Terminal Crimper", "Cushion Grip"]),
    (205, "Dead blow hammer", "شكوش رمل", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Non-Marring Polyurethane", "Steel Shot Filled Cavity", "No Bounce"]),
    (206, "Spark plug socket 14 / 16 / 21 mm", "طربوش بوجي ١٤/١٦/٢١", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Thin Wall Magnetic Socket", "Universal Swivel Core", "14mm 16mm 21mm"]),
    (207, "Tool trolley set 7 drawer complete with tools", "طاولة ٧ جوارير كاملة", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Fully Loaded Tool Chest", "7 Foam Inlay Drawers", "Comprehensive Auto Master Set"]),
    (208, "AC leak detection copper adapters & fittings", "طقم راكور AC", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Air Conditioning Test Fittings", "Brass & Copper Connectors", "Storage Case"]),
    (209, "AC diagnostic manifold gauge set", "ساعة فحص AC", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["3-Way Manifold Gauges", "Color Coded Charging Hoses", "R134a Quick Couplers"]),
    (210, "Auto trim & upholstery removal tool set", "طقم فك فرش", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Non-Scratch Nylon Pry Tools", "Clip Pliers & Removers", "Canvas Storage Pouch"]),
    (211, "Pneumatic paint spray gun kit", "فرد رش سيارة", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["HVLP Professional Spray Gun", "Gravity Feed Cup", "Adjustable Pattern"]),
    (212, "S-Pipe wrench 90 / 45 degree", "بنسة S رنش", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Swedish S-Jaw Pipe Wrench", "3-Point Contact", "Induction Hardened Teeth"]),
    (213, "Hand heavy duty blind riveter", "بنسة تبشيم", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Hand Rivet Gun", "Interchangeable Nozzles", "Rivet Collection Bottle"]),
    (214, "Blind nut threaded insert riveter set", "بنسة تبشيم عزق", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Rivet Nut Tool Kit", "Mandrels M3-M10", "Assorted Rivnut Inserts"]),
    (215, "Vernier caliper (Normal / Digital)", "كليبرة عادي / رقمي", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["High Precision Vernier Caliper", "Stainless Steel", "Inside/Outside/Depth Gauge"]),
    (216, "Round magnetic parts tray & tool holder", "صحن مغناطيس", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Stainless Steel Magnetic Dishes", "Rubber Coated Base", "Holds Nuts, Bolts, Screws"]),
    (217, "Roller stud extractor socket set", "طربوش كوجون", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Cam Action Stud Extractors", "Hex Drive Sockets", "Damaged Stud Removal"]),
    (218, "Mechanics steel file set", "طقم مبرد", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["Flat / Round / Half Round / Triangle", "High Carbon Steel", "Ergonomic Handles"]),
    (219, "Wheel nut thin wall impact socket set", "طقم طربوش جنط", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Alloy Wheel Protective Sleeves", "17mm, 19mm, 21mm", "Color Coded CR-MO"]),
    (220, "Marking letter and number punch set", "طقم ارقام واحرف", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Hardened Steel Stamp Punches", "A-Z Letters & 0-9 Numbers", "Index Case"]),
    (221, "Tyre changer wheel balancer & lift assist", "ماكينة تجليس دولاب", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Rim Straightening Machine", "Hydraulic Lathe & Clamp", "Alloy Wheel Repair"]),
    (222, "Press and pull sleeve kit bushing repair", "برسة باغ", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Universal Bush / Bearing Sleeves", "Pulling Spindles & Nuts", "Silent Block Tool"]),
    (223, "Oil seal puller screwdriver tool", "مفك السييل", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Dual Hook Head", "Heavy Leverage Shaft", "Crank & Camshaft Seals"]),
    (224, "Remover install 4x4 ball joint & wheel bearing kit", "برسة باغ ورولمان ٤*٤", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Heavy Duty C-Frame Press", "4WD Adapters & Receiving Tubes", "Brake Anchor Pins"]),
    (225, "Auto ball joint separator tool set", "طقم برسة بيضة", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Adjustable Ball Joint Press", "Tie Rod Extractor Set", "Drop Forged"]),
    (226, "Car HVAC AC valve service couplers", "مفتاح AC سيارة", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["High & Low Side Quick Couplers", "Flow Control Knobs", "R134a Valve Cores"]),
    (227, "AC compressor clutch hub puller installer set", "برسة راس AC سيارة", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["A/C Clutch Hub Remover", "Reversible Hub Arbor", "Domestic & Import Case"]),
    (228, "Mechanics stethoscope for car engine", "سماعة", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["Engine Diagnostic Sound Scope", "Metal Probe & Earpieces", "Detects Bearing & Valvetrain Noises"]),
    (229, "Rudder wrench inner tie rod removal tool", "برسة زند بواط", "tire_wheel_service", "Tire & Wheel Service", "خدمة الإطارات والمكابح", ["Inner Tie Rod Steering Wrench", "Universal 27-42mm", "High Torque Grip"]),
    (230, "Telescoping inspection mirror", "قلم مراة", "diagnostic_testing", "Diagnostic & Electrical", "الفحص والتشخيص والكهرباء", ["360 Degree Swivel Mirror", "Extendable Telescopic Shaft", "Pocket Clip"]),
    (231, "10/20/30/50 ton hydraulic bottle jack", "عفريت قنينة", "lifting_equipment", "Lifts & Lifting", "معدات الرفع والهيدروليك", ["Hydraulic Bottle Jack", "Heavy Tonnage Capacity", "Cast Base & Extension Screw"]),

    # Page 9 (232 - 240)
    (232, "High power windproof copper hot flame welding torch", "شليمون لحام", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Oxy-Acetylene Cutting Torch", "All-Brass & Copper Head", "High Heat Resistance"]),
    (233, "PVC twin tube hose for oxygen & acetylene", "نبريج الاكسجين", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Dual Oxygen / Acetylene Hose", "Color Coded Red & Blue", "High Pressure"]),
    (234, "Pressure regulator for oxygen & gas cylinders", "ساعة الاكسجين", "body_repair_welding", "Body Repair & Welding", "الحدادة والتجليس واللحام", ["Dual Pressure Gauges", "Heavy Brass Body", "Inlet Safety Valve"]),
    (235, "Air filter regulator and lubricator dryer", "فلتر هواء", "pneumatic_air_tools", "Pneumatic & Air Tools", "معدات الهواء والكمبريسور", ["Air Compressor Line Filter", "Water Separator & Oiler", "Pressure Gauge Unit"]),
    (236, "Tripod LED work light stand", "ضو عامود", "workshop_storage", "Workshop & Press Tools", "معدات ومكابس الورشة", ["Telescopic Tripod Stand", "High Lumen Floodlight", "360 Degree Swivel"]),
    (237, "Car pick and hook tool set", "مفك سييل", "wrenches_hand_tools", "Wrenches & Sockets", "المفاتيح والطربوشات", ["4-Piece Precision Hooks", "Straight / 90 / Full / Angle Hook", "O-Ring & Gasket Remover"]),
    (238, "O-Ring rubber seal assortment set", "طقم سييل", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Nitrile Rubber O-Rings", "Oil / Fuel / Heat Resistant", "Multi-Compartment Case"]),
    (239, "Manual pistol grip greasing machine", "مشحمة عادي", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Manual Grease Gun", "Flexible Hose & Rigid Tube", "Cartridge / Bulk Fill"]),
    (240, "Pneumatic grease injector dispenser", "مشحمة هواء", "engine_oil_service", "Engine & Fluid Service", "خدمة المحرك وسحب السوائل", ["Air Operated Grease Pump", "Wheeled Steel Container", "High Pressure Delivery Hose"])
]

# Ensure output directory for standardized product images
os.makedirs("images/products", exist_ok=True)

# 2. Build map of existing standalone images
existing_files = os.listdir("images")
image_file_map = {}

for f in existing_files:
    if f.startswith("IMG_2020") or f.startswith("Screenshot_") or os.path.isdir(os.path.join("images", f)):
        continue
    base = f.split(".")[0]
    if f == "IMG_20230922_225127.jpg":
        image_file_map[3] = f
        continue
    nums = re.findall(r"\b\d+\b", base.replace("@", " ").replace("-", " ").replace("_", " "))
    valid_nums = [int(n) for n in nums if 1 <= int(n) <= 240]
    for n in valid_nums:
        # Prefer direct match or store
        if n not in image_file_map or base == str(n):
            image_file_map[n] = f

print(f"Direct mapped images: {len(image_file_map)}/240")

# Copy direct images into images/products/{id}.jpg (or png)
for item_id, filename in image_file_map.items():
    src = os.path.join("images", filename)
    ext = os.path.splitext(filename)[1].lower()
    dest = os.path.join("images", "products", f"{item_id}{ext}")
    shutil.copy2(src, dest)

# 3. For any missing item, crop cleanly from the grid screenshots
# Grid coordinate layout:
# Each screenshot is 1080 x 2312
# The grid area in 1080x2312 is approximately:
# Top header ends around y=500, bottom navigation around y=1680
# Let's define grid lookup by page:
# Screenshot 1: 1..21 (4 cols x ~5-6 rows)
# Screenshot 2: 22..42
# Screenshot 3: 43..63
# Screenshot 4: 64..83 (4x5)
# Screenshot 5: 84..111
# Screenshot 6: 112..132
# Screenshot 7: 133..152
# Screenshot 8: 153..174
# Screenshot 9: 173..193
# Screenshot 10: 194..213
# Screenshot 11: 214..233
# Screenshot 12: 234..240

# Map missing items to screenshot crops if not copied yet:
missing_items = [i for i in range(1, 241) if not any(os.path.exists(f"images/products/{i}{e}") for e in [".jpg", ".png", ".jpeg"])]
print("Missing items to generate crops for:", missing_items)

# Define grid screenshot locations and crop areas (col 0..3, row 0..N)
SCREENSHOT_MAP = {
    # (page, item_id): (col, row, total_cols, total_rows, grid_box (left, top, right, bottom))
}

# Grid boundaries standard in 1080x2312 screenshots:
# left=78, top=500, right=1000, bottom=1630 (approx 4 cols, 5 or 6 rows)
grid_shots = {
    1: "Screenshot_20200527_142730_com.google.android.apps.docs@1233913452.jpg",
    2: "Screenshot_20200527_142746_com.google.android.apps.docs@522411751.jpg",
    3: "Screenshot_20200527_142800_com.google.android.apps.docs@-1992228984.jpg",
    4: "Screenshot_20200527_142811_com.google.android.apps.docs@758743912.jpg",
    5: "Screenshot_20200527_142818_com.google.android.apps.docs@-652746687.jpg",
    6: "Screenshot_20200527_142825_com.google.android.apps.docs@-2003741787.jpg",
    7: "Screenshot_20200527_142832_com.google.android.apps.docs@940230409.jpg",
    8: "Screenshot_20200527_142839_com.google.android.apps.docs@-471260190.jpg",
    9: "Screenshot_20200527_142847_com.google.android.apps.docs@-796763291.jpg",
    10: "Screenshot_20200527_142900_com.google.android.apps.docs@-41928729.jpg",
    11: "Screenshot_20200527_142908_com.google.android.apps.docs@-427927329.jpg",
    12: "Screenshot_20200527_142917_com.google.android.apps.docs@272061569.jpg"
}

# Crop logic for missing items:
# Let's map specific missing items precisely:
CROPS = {
    11: (1, 2, 2, 4, 6, (77, 500, 1000, 1630)), # item 11 on shot 1 (row 2, col 2)
    20: (1, 3, 4, 4, 6, (77, 500, 1000, 1630)),
    35: (2, 2, 3, 4, 6, (77, 500, 1000, 1630)),
    36: (2, 3, 3, 4, 6, (77, 500, 1000, 1630)),
    47: (3, 3, 0, 4, 6, (77, 500, 1000, 1630)),
    57: (3, 1, 3, 4, 6, (77, 500, 1000, 1630)),
    58: (3, 2, 3, 4, 6, (77, 500, 1000, 1630)),
    59: (3, 3, 3, 4, 6, (77, 500, 1000, 1630)),
    101: (5, 3, 3, 4, 6, (77, 500, 1000, 1630)),
    102: (5, 3, 3, 4, 6, (77, 500, 1000, 1630)),
    103: (5, 3, 3, 4, 6, (77, 500, 1000, 1630)),
    104: (5, 3, 3, 4, 6, (77, 500, 1000, 1630)),
    133: (7, 0, 0, 4, 6, (77, 455, 1000, 1585)),
    136: (7, 3, 0, 4, 6, (77, 455, 1000, 1585)),
    139: (7, 2, 1, 4, 6, (77, 455, 1000, 1585)),
    158: (8, 1, 1, 4, 6, (77, 490, 1000, 1420)),
    181: (9, 3, 1, 4, 6, (77, 345, 1000, 1465)),
    194: (10, 0, 0, 4, 6, (77, 500, 1000, 1630)),
    195: (10, 1, 0, 4, 6, (77, 500, 1000, 1630)),
    202: (10, 0, 2, 4, 6, (77, 500, 1000, 1630)),
    205: (10, 3, 2, 4, 6, (77, 500, 1000, 1630)),
    216: (11, 2, 0, 4, 6, (77, 320, 1000, 1420)),
    218: (11, 0, 1, 4, 6, (77, 320, 1000, 1420)),
    221: (11, 3, 1, 4, 6, (77, 320, 1000, 1420)),
    225: (11, 3, 2, 4, 6, (77, 320, 1000, 1420))
}

for item_id in missing_items:
    if item_id in CROPS:
        page, c, r, total_cols, total_rows, (gx1, gy1, gx2, gy2) = CROPS[item_id]
        shot_name = grid_shots[page]
        img = Image.open(os.path.join("images", shot_name))
        cell_w = (gx2 - gx1) / total_cols
        cell_h = (gy2 - gy1) / total_rows
        x1 = int(gx1 + c * cell_w) + 4
        y1 = int(gy1 + r * cell_h) + 4
        x2 = int(gx1 + (c + 1) * cell_w) - 4
        y2 = int(gy1 + (r + 1) * cell_h) - 4
        cropped = img.crop((x1, y1, x2, y2))
        dest = os.path.join("images", "products", f"{item_id}.jpg")
        cropped.save(dest, "JPEG", quality=92)
        print(f"Generated crop for #{item_id} -> {dest}")

# 4. Generate catalog.json
catalog = []

for item_id, name_en, name_ar, cat_id, cat_en, cat_ar, tags in ITEMS_DATA:
    # find image path
    image_rel = None
    for ext in [".jpg", ".png", ".jpeg"]:
        p = f"images/products/{item_id}{ext}"
        if os.path.exists(p):
            image_rel = p
            break
    if not image_rel:
        image_rel = f"images/products/{item_id}.jpg"

    part_number = f"ET-{item_id:03d}"
    
    # generate rich description
    desc_en = f"Professional grade {name_en.lower()} designed for demanding automotive workshop and mechanical service operations. Engineered with high-strength materials, precision tolerances, and exceptional durability."
    desc_ar = f"{name_ar} ذات جودة احترافية عالية مصممة خصيصاً للاستخدام الشاق في ورش صيانة وتصليح السيارات وميكانيك المركبات. مصنوعة من مواد متينة عالية التحمل مع دقة فائقة في الأداء."

    item_obj = {
        "id": item_id,
        "ref_no": str(item_id),
        "part_number": part_number,
        "name_en": name_en,
        "name_ar": name_ar,
        "category_id": cat_id,
        "category_en": cat_en,
        "category_ar": cat_ar,
        "description_en": desc_en,
        "description_ar": desc_ar,
        "image": image_rel,
        "specs": tags
    }
    catalog.append(item_obj)

# Ensure strictly NO price field exists anywhere
for it in catalog:
    assert "price" not in it, "Price field must not exist!"

with open("catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"Successfully generated catalog.json with {len(catalog)} items!")
