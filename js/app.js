/**
 * ELMIR TOOLS & CO - Catalog Frontend Engine
 * Bilingual (EN/AR), Live Search, Filters, Quote Cart & WhatsApp Inquiry
 */

(function () {
  'use strict';

  // --- Constants & Config ---
  const WHATSAPP_PHONE = '96176339423';
  const STORAGE_KEY_QUOTE = 'elmir_tools_quote_list';
  const STORAGE_KEY_LANG = 'elmir_tools_lang';
  const STORAGE_KEY_THEME = 'elmir_tools_theme';

  // --- Translations Dictionary ---
  const I18N = {
    en: {
      location: 'Lebanon • Worldwide Inquiries',
      brand_sub: 'Garage Equipment & Workshop Solutions',
      quote_list: 'Quote List',
      chat_whatsapp: 'Direct Inquiry',
      hero_badge: 'Official Equipment Catalog 2024-2025',
      hero_title_1: 'Professional Automotive',
      hero_title_2: 'Tools & Garage Machinery',
      hero_desc: 'Browse our complete catalog of 240 high-precision automotive workshop tools, heavy duty vehicle lifts, pneumatic impact guns, hydraulic presses, and diagnostic equipment.',
      stat_tools: 'Tools & Machines',
      stat_cats: 'Core Categories',
      stat_verified: 'Industrial Quality',
      stat_inquiry: 'WhatsApp Support',
      all_categories: 'All Categories',
      showing: 'Showing',
      of: 'of',
      products: 'products',
      filter_by_spec: 'Filter by specification',
      all_specifications: 'All Specifications',
      sort_by: 'Sort by',
      sort_ref_asc: 'Ref Number: Low to High',
      sort_ref_desc: 'Ref Number: High to Low',
      sort_name_asc: 'Name: A to Z',
      sort_name_desc: 'Name: Z to A',
      no_results_title: 'No tools found matching your criteria',
      no_results_desc: 'Try searching for a different tool name, part number, reference number, or resetting active filters.',
      reset_filters: 'Reset All Filters',
      quote_drawer_title: 'Quote Request List',
      send_quote_whatsapp: 'Send Quote via WhatsApp',
      copy_list: 'Copy List to Clipboard',
      clear_list: 'Clear All Items',
      empty_drawer_title: 'Your quote list is empty',
      empty_drawer_desc: 'Add tools from the catalog to request pricing and availability.',
      add_to_quote: 'Add to Quote',
      in_quote_list: 'In Quote List',
      quick_view: 'Quick View',
      inquire_now: 'Inquire on WhatsApp',
      part_no: 'Part No',
      ref_no: 'REF #',
      category: 'Category',
      specifications: 'Specifications',
      description: 'Description',
      footer_about: 'Premier supplier of heavy duty automotive equipment, garage tools, and hydraulic machinery in Lebanon. Serving auto repair shops, mechanics, and dealerships with premium industrial-grade tools.',
      footer_quick_cats: 'Key Categories',
      footer_inquiry_heading: 'Direct Inquiries',
      footer_inquiry_text: 'Need a personalized quotation, bulk pricing, or international delivery details? Contact us directly via WhatsApp or phone.',
      cat_lifting: 'Lifts & Lifting Equipment',
      cat_wrenches: 'Wrenches & Socket Sets',
      cat_pneumatic: 'Pneumatic & Air Tools',
      cat_diagnostic: 'Diagnostic & Electrical',
      cat_body: 'Body Repair & Welding',
      cat_engine: 'Engine & Fluid Service',
      toast_added: 'Added to Quote List!',
      toast_removed: 'Removed from Quote List!',
      toast_copied: 'Quote list copied to clipboard!',
      mode_light: 'Light Mode',
      mode_dark: 'Dark Mode'
    },
    ar: {
      location: 'لبنان • طلبات واستفسارات لجميع المناطق',
      brand_sub: 'معدات كراجات وحلول الورش المتكاملة',
      quote_list: 'لائحة الطلب',
      chat_whatsapp: 'استفسار مباشر',
      hero_badge: 'الكتالوج الرسمي المعتمد ٢٠٢٤-٢٠٢٥',
      hero_title_1: 'معدات وعدد سيارات',
      hero_title_2: 'احترافية للورش والميكانيك',
      hero_desc: 'تصفح كتالوجنا الشامل الذي يضم ٢٤٠ أداة ومعدة عالية الدقة لكراجات السيارات، بما في ذلك عوارف الرفع، مسدسات الهواء، المكابس الهيدروليكية، وأجهزة الفحص الحديثة.',
      stat_tools: 'أداة ومعدة',
      stat_cats: 'أقسام رئيسية',
      stat_verified: 'جودة صناعية ممتازة',
      stat_inquiry: 'خدمة واتساب مباشرة',
      all_categories: 'جميع الفئات',
      showing: 'عرض',
      of: 'من أصل',
      products: 'منتج',
      filter_by_spec: 'تصفية حسب المقاس / المواصفات',
      all_specifications: 'جميع المقاسات والمواصفات',
      sort_by: 'ترتيب حسب',
      sort_ref_asc: 'رقم المرجع: من الأصغر للأكبر',
      sort_ref_desc: 'رقم المرجع: من الأكبر للأصغر',
      sort_name_asc: 'الاسم: أ إلى ي',
      sort_name_desc: 'الاسم: ي إلى أ',
      no_results_title: 'لم يتم العثور على أي أدوات مطابقة للبحث',
      no_results_desc: 'يرجى تجربة اسم أداة آخر، أو رقم مرجع مختلف، أو إعادة تعيين الفلاتر.',
      reset_filters: 'إعادة تعيين الفلاتر',
      quote_drawer_title: 'لائحة طلب الأسعار',
      send_quote_whatsapp: 'إرسال اللائحة عبر واتساب',
      copy_list: 'نسخ اللائحة للحافظة',
      clear_list: 'تفريغ اللائحة',
      empty_drawer_title: 'لائحة الطلب فارغة حالياً',
      empty_drawer_desc: 'أضف معدات وأدوات من الكتالوج لطلب الأسعار وتفاصيل التوفر.',
      add_to_quote: 'إضافة للطلب',
      in_quote_list: 'تمت الإضافة',
      quick_view: 'نظرة سريعة',
      inquire_now: 'استفسار عبر واتساب',
      part_no: 'رقم القطعة',
      ref_no: 'رقم المرجع #',
      category: 'الفئة',
      specifications: 'المواصفات',
      description: 'التفاصيل والوصف',
      footer_about: 'المورد الرائد لمعدات الكراجات الثقيلة، عدد تصليح السيارات، والآلات الهيدروليكية في لبنان. نلبي احتياجات محطات الصيانة والورش الاحترافية.',
      footer_quick_cats: 'الفئات الرئيسية',
      footer_inquiry_heading: 'استفسار مباشر',
      footer_inquiry_text: 'هل تحتاج إلى عرض أسعار مخصص أو طلبات جملة؟ تواصل معنا مباشرة عبر الواتساب أو الهاتف.',
      cat_lifting: 'معدات الرفع والهيدروليك',
      cat_wrenches: 'المفاتيح والطربوشات',
      cat_pneumatic: 'معدات الهواء والكمبريسور',
      cat_diagnostic: 'الفحص والتشخيص والكهرباء',
      cat_body: 'الحدادة والتجليس واللحام',
      cat_engine: 'خدمة المحرك وسحب السوائل',
      toast_added: 'تمت إضافة الأداة للائحة الطلب!',
      toast_removed: 'تمت الإزالة من اللائحة!',
      toast_copied: 'تم نسخ لائحة الطلب بنجاح!',
      mode_light: 'الوضع الفاتح',
      mode_dark: 'الوضع الداكن'
    }
  };

  // --- State ---
  let catalog = [];
  let currentLang = localStorage.getItem(STORAGE_KEY_LANG) || 'en';
  let currentTheme = localStorage.getItem(STORAGE_KEY_THEME) || 'dark';
  let activeCategory = 'all';
  let searchQuery = '';
  let activeTag = '';
  let sortBy = 'ref_asc';
  let viewMode = 'grid'; // 'grid' | 'list'
  let quoteItems = JSON.parse(localStorage.getItem(STORAGE_KEY_QUOTE) || '[]');

  // --- Category Definitions ---
  const CATEGORIES = [
    { id: 'all', icon: 'fa-cubes', en: 'All Categories', ar: 'جميع الفئات' },
    { id: 'lifting_equipment', icon: 'fa-arrows-up-down', en: 'Lifts & Lifting', ar: 'معدات الرفع والهيدروليك' },
    { id: 'wrenches_hand_tools', icon: 'fa-wrench', en: 'Wrenches & Sockets', ar: 'المفاتيح والطربوشات' },
    { id: 'pneumatic_air_tools', icon: 'fa-wind', en: 'Pneumatic & Air Tools', ar: 'معدات الهواء والكمبريسور' },
    { id: 'engine_oil_service', icon: 'fa-oil-can', en: 'Engine & Fluid Service', ar: 'خدمة المحرك وسحب السوائل' },
    { id: 'diagnostic_testing', icon: 'fa-gauge-high', en: 'Diagnostic & Electrical', ar: 'الفحص والتشخيص والكهرباء' },
    { id: 'body_repair_welding', icon: 'fa-car-burst', en: 'Body Repair & Welding', ar: 'الحدادة والتجليس واللحام' },
    { id: 'tire_wheel_service', icon: 'fa-circle-notch', en: 'Tire & Wheel Service', ar: 'خدمة الإطارات والمكابح' },
    { id: 'pliers_cutters', icon: 'fa-scissors', en: 'Pliers & Cutters', ar: 'البنسات والقطاعات' },
    { id: 'workshop_storage', icon: 'fa-toolbox', en: 'Workshop & Press Tools', ar: 'معدات ومكابس الورشة' }
  ];

  // --- DOM Elements ---
  const dom = {
    html: document.documentElement,
    body: document.body,
    themeToggle: document.getElementById('themeToggle'),
    themeIcon: document.getElementById('themeIcon'),
    themeLabel: document.getElementById('themeLabel'),
    langToggle: document.getElementById('langToggle'),
    langLabel: document.getElementById('langLabel'),
    searchInput: document.getElementById('searchInput'),
    clearSearchBtn: document.getElementById('clearSearchBtn'),
    categoriesContainer: document.getElementById('categoriesContainer'),
    productsContainer: document.getElementById('productsContainer'),
    resultsCount: document.getElementById('resultsCount'),
    currentCount: document.getElementById('currentCount'),
    activeFilterTags: document.getElementById('activeFilterTags'),
    tagFilterSelect: document.getElementById('tagFilterSelect'),
    sortSelect: document.getElementById('sortSelect'),
    viewGridBtn: document.getElementById('viewGridBtn'),
    viewListBtn: document.getElementById('viewListBtn'),
    emptyState: document.getElementById('emptyState'),
    resetFiltersBtn: document.getElementById('resetFiltersBtn'),
    quoteDrawerBtn: document.getElementById('quoteDrawerBtn'),
    mobileQuoteTrigger: document.getElementById('mobileQuoteTrigger'),
    quoteBadge: document.getElementById('quoteBadge'),
    mobileQuoteBadge: document.getElementById('mobileQuoteBadge'),
    quoteDrawer: document.getElementById('quoteDrawer'),
    drawerOverlay: document.getElementById('drawerOverlay'),
    closeDrawerBtn: document.getElementById('closeDrawerBtn'),
    drawerItemsList: document.getElementById('drawerItemsList'),
    drawerItemCount: document.getElementById('drawerItemCount'),
    whatsappQuoteBtn: document.getElementById('whatsappQuoteBtn'),
    copyQuoteBtn: document.getElementById('copyQuoteBtn'),
    clearQuoteBtn: document.getElementById('clearQuoteBtn'),
    productModal: document.getElementById('productModal'),
    modalBody: document.getElementById('modalBody'),
    closeModalBtn: document.getElementById('closeModalBtn'),
    toast: document.getElementById('toast'),
    homeLogo: document.getElementById('homeLogo'),
    footerCatsList: document.getElementById('footerCatsList')
  };

  // --- Initialization ---
  async function init() {
    setTheme(currentTheme);
    setLanguage(currentLang);
    bindEvents();
    await loadCatalog();
    renderCategories();
    renderProducts();
    updateQuoteUI();
    checkUrlParams();
  }

  // --- Theme Management ---
  function setTheme(theme) {
    currentTheme = theme;
    localStorage.setItem(STORAGE_KEY_THEME, theme);
    
    if (theme === 'light') {
      dom.body.classList.remove('theme-dark');
      dom.body.classList.add('theme-light');
      if (dom.themeIcon) dom.themeIcon.className = 'fa-solid fa-moon';
      if (dom.themeLabel) dom.themeLabel.textContent = I18N[currentLang].mode_dark;
    } else {
      dom.body.classList.remove('theme-light');
      dom.body.classList.add('theme-dark');
      if (dom.themeIcon) dom.themeIcon.className = 'fa-solid fa-sun';
      if (dom.themeLabel) dom.themeLabel.textContent = I18N[currentLang].mode_light;
    }
  }

  // --- Load Data ---
  async function loadCatalog() {
    try {
      const res = await fetch('catalog.json');
      if (!res.ok) throw new Error('Network error loading catalog.json');
      catalog = await res.json();
    } catch (err) {
      console.error('Failed to load catalog.json:', err);
      showToast('Error loading catalog data. Please refresh.');
    }
  }

  // --- Language Management ---
  function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY_LANG, lang);
    dom.html.setAttribute('lang', lang);
    dom.html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    dom.langLabel.textContent = lang === 'ar' ? 'English' : 'العربية';

    // Update static i18n text
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (I18N[lang][key]) {
        el.textContent = I18N[lang][key];
      }
    });

    // Update search input placeholder
    dom.searchInput.placeholder = lang === 'ar' 
      ? 'ابحث بين ٢٤٠ أداة بالاسم، رقم المرجع، أو الكود...'
      : 'Search 240+ tools by name, REF #, or part #...';

    // Update theme button label for current language
    if (dom.themeLabel) {
      dom.themeLabel.textContent = currentTheme === 'light' ? I18N[lang].mode_dark : I18N[lang].mode_light;
    }

    renderCategories();
    renderProducts();
    renderDrawerItems();
  }

  // --- Event Bindings ---
  function bindEvents() {
    // Theme toggle
    if (dom.themeToggle) {
      dom.themeToggle.addEventListener('click', () => {
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
      });
    }

    // Language toggle
    dom.langToggle.addEventListener('click', () => {
      setLanguage(currentLang === 'en' ? 'ar' : 'en');
    });

    // Search input
    dom.searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      dom.clearSearchBtn.style.display = searchQuery ? 'block' : 'none';
      renderProducts();
    });

    dom.clearSearchBtn.addEventListener('click', () => {
      dom.searchInput.value = '';
      searchQuery = '';
      dom.clearSearchBtn.style.display = 'none';
      renderProducts();
      dom.searchInput.focus();
    });

    // Spec tag filter
    dom.tagFilterSelect.addEventListener('change', (e) => {
      activeTag = e.target.value;
      renderProducts();
    });

    // Sorting
    dom.sortSelect.addEventListener('change', (e) => {
      sortBy = e.target.value;
      renderProducts();
    });

    // View mode
    dom.viewGridBtn.addEventListener('click', () => {
      viewMode = 'grid';
      dom.viewGridBtn.classList.add('active');
      dom.viewListBtn.classList.remove('active');
      dom.productsContainer.classList.remove('view-list');
      dom.productsContainer.classList.add('view-grid');
    });

    dom.viewListBtn.addEventListener('click', () => {
      viewMode = 'list';
      dom.viewListBtn.classList.add('active');
      dom.viewGridBtn.classList.remove('active');
      dom.productsContainer.classList.remove('view-grid');
      dom.productsContainer.classList.add('view-list');
    });

    // Reset filters
    dom.resetFiltersBtn.addEventListener('click', resetFilters);

    // Quote drawer triggers
    dom.quoteDrawerBtn.addEventListener('click', openDrawer);
    dom.mobileQuoteTrigger.addEventListener('click', openDrawer);
    dom.closeDrawerBtn.addEventListener('click', closeDrawer);
    dom.drawerOverlay.addEventListener('click', closeDrawer);

    // Quote drawer actions
    dom.whatsappQuoteBtn.addEventListener('click', sendWhatsAppQuote);
    dom.copyQuoteBtn.addEventListener('click', copyQuoteList);
    dom.clearQuoteBtn.addEventListener('click', clearQuoteList);

    // Product modal close
    dom.closeModalBtn.addEventListener('click', closeModal);
    dom.productModal.addEventListener('click', (e) => {
      if (e.target === dom.productModal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeModal();
        closeDrawer();
      }
    });

    // Logo reset click
    dom.homeLogo.addEventListener('click', (e) => {
      e.preventDefault();
      resetFilters();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Footer category links
    dom.footerCatsList.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (link && link.dataset.cat) {
        e.preventDefault();
        setCategory(link.dataset.cat);
        const catalogEl = document.getElementById('catalog');
        if (catalogEl) catalogEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  function resetFilters() {
    activeCategory = 'all';
    searchQuery = '';
    activeTag = '';
    dom.searchInput.value = '';
    dom.clearSearchBtn.style.display = 'none';
    dom.tagFilterSelect.value = '';
    renderCategories();
    renderProducts();
  }

  function setCategory(catId) {
    activeCategory = catId;
    renderCategories();
    renderProducts();
  }

  // --- Category Navigation ---
  function renderCategories() {
    dom.categoriesContainer.innerHTML = '';
    CATEGORIES.forEach((cat) => {
      const btn = document.createElement('button');
      btn.className = `cat-pill ${activeCategory === cat.id ? 'active' : ''}`;
      
      const count = cat.id === 'all' 
        ? catalog.length 
        : catalog.filter((item) => item.category_id === cat.id).length;

      const title = currentLang === 'ar' ? cat.ar : cat.en;
      btn.innerHTML = `
        <i class="fa-solid ${cat.icon}"></i>
        <span>${title}</span>
        <span class="cat-pill-count">${count}</span>
      `;

      btn.addEventListener('click', () => {
        setCategory(cat.id);
      });

      dom.categoriesContainer.appendChild(btn);
    });
  }

  // --- Filter & Sort Logic ---
  function getFilteredCatalog() {
    return catalog.filter((item) => {
      // Category filter
      if (activeCategory !== 'all' && item.category_id !== activeCategory) {
        return false;
      }

      // Specification / Tag filter
      if (activeTag) {
        const hasTag = (item.specs || []).some((s) => s.toLowerCase().includes(activeTag.toLowerCase())) ||
                       item.name_en.toLowerCase().includes(activeTag.toLowerCase()) ||
                       item.name_ar.includes(activeTag);
        if (!hasTag) return false;
      }

      // Search Query filter
      if (searchQuery) {
        const matchEn = item.name_en.toLowerCase().includes(searchQuery);
        const matchAr = item.name_ar.toLowerCase().includes(searchQuery);
        const matchRef = item.ref_no.toString() === searchQuery || `ref ${item.ref_no}`.includes(searchQuery);
        const matchPart = item.part_number.toLowerCase().includes(searchQuery);
        const matchSpecs = (item.specs || []).some((s) => s.toLowerCase().includes(searchQuery));
        if (!matchEn && !matchAr && !matchRef && !matchPart && !matchSpecs) {
          return false;
        }
      }

      return true;
    }).sort((a, b) => {
      if (sortBy === 'ref_asc') return a.id - b.id;
      if (sortBy === 'ref_desc') return b.id - a.id;
      if (sortBy === 'name_asc') {
        const titleA = currentLang === 'ar' ? a.name_ar : a.name_en;
        const titleB = currentLang === 'ar' ? b.name_ar : b.name_en;
        return titleA.localeCompare(titleB);
      }
      if (sortBy === 'name_desc') {
        const titleA = currentLang === 'ar' ? a.name_ar : a.name_en;
        const titleB = currentLang === 'ar' ? b.name_ar : b.name_en;
        return titleB.localeCompare(titleA);
      }
      return 0;
    });
  }

  // --- Render Product Cards ---
  function renderProducts() {
    const items = getFilteredCatalog();
    dom.currentCount.textContent = items.length;

    // Update active filter badges
    dom.activeFilterTags.innerHTML = '';
    if (activeCategory !== 'all') {
      const catObj = CATEGORIES.find((c) => c.id === activeCategory);
      if (catObj) {
        const badge = document.createElement('span');
        badge.className = 'filter-tag-badge';
        badge.innerHTML = `${currentLang === 'ar' ? catObj.ar : catObj.en} <button title="Remove"><i class="fa-solid fa-xmark"></i></button>`;
        badge.querySelector('button').addEventListener('click', () => setCategory('all'));
        dom.activeFilterTags.appendChild(badge);
      }
    }
    if (activeTag) {
      const badge = document.createElement('span');
      badge.className = 'filter-tag-badge';
      badge.innerHTML = `Spec: ${activeTag} <button title="Remove"><i class="fa-solid fa-xmark"></i></button>`;
      badge.querySelector('button').addEventListener('click', () => {
        activeTag = '';
        dom.tagFilterSelect.value = '';
        renderProducts();
      });
      dom.activeFilterTags.appendChild(badge);
    }

    if (items.length === 0) {
      dom.productsContainer.style.display = 'none';
      dom.emptyState.style.display = 'block';
      return;
    }

    dom.productsContainer.style.display = 'grid';
    dom.emptyState.style.display = 'none';
    dom.productsContainer.innerHTML = '';

    items.forEach((item) => {
      const inQuote = quoteItems.includes(item.id);
      const card = document.createElement('article');
      card.className = 'product-card';
      card.dataset.id = item.id;

      const specsHtml = (item.specs || []).map((s) => `<span class="spec-chip">${escapeHtml(s)}</span>`).join('');
      const catLabel = currentLang === 'ar' ? item.category_ar : item.category_en;

      card.innerHTML = `
        <div class="product-image-wrap" role="button" tabindex="0" title="Click to view details">
          <span class="ref-badge">REF #${String(item.id).padStart(3, '0')}</span>
          <span class="part-badge">${item.part_number}</span>
          <img src="${item.image}" alt="${escapeHtml(item.name_en)}" loading="lazy">
        </div>
        <div class="product-content">
          <span class="product-category-tag">${escapeHtml(catLabel)}</span>
          <h3 class="product-title-en">${escapeHtml(item.name_en)}</h3>
          <h4 class="product-title-ar">${escapeHtml(item.name_ar)}</h4>
          <div class="product-specs-list">${specsHtml}</div>
          <div class="product-actions">
            <button class="btn-add-quote ${inQuote ? 'in-cart' : ''}" data-id="${item.id}">
              <i class="fa-solid ${inQuote ? 'fa-check' : 'fa-plus'}"></i>
              <span>${inQuote ? I18N[currentLang].in_quote_list : I18N[currentLang].add_to_quote}</span>
            </button>
            <button class="btn-quick-view" data-id="${item.id}" title="${I18N[currentLang].quick_view}">
              <i class="fa-solid fa-eye"></i>
            </button>
          </div>
        </div>
      `;

      // Event listeners
      card.querySelector('.product-image-wrap').addEventListener('click', () => openModal(item));
      card.querySelector('.btn-quick-view').addEventListener('click', () => openModal(item));
      
      const addBtn = card.querySelector('.btn-add-quote');
      addBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleQuoteItem(item.id);
      });

      dom.productsContainer.appendChild(card);
    });
  }

  // --- Product Detail Modal ---
  function openModal(item) {
    const inQuote = quoteItems.includes(item.id);
    const catLabel = currentLang === 'ar' ? item.category_ar : item.category_en;
    const waText = encodeURIComponent(`Hello Elmir Tools & Co,\nI am inquiring about:\n- Tool: ${item.name_en} (${item.name_ar})\n- REF #: ${item.id}\n- Part No: ${item.part_number}\nPlease provide pricing and availability.`);

    dom.modalBody.innerHTML = `
      <div class="modal-grid">
        <div class="modal-image-col">
          <img src="${item.image}" alt="${escapeHtml(item.name_en)}">
        </div>
        <div class="modal-info-col">
          <div class="modal-header-badges">
            <span class="ref-badge">REF #${String(item.id).padStart(3, '0')}</span>
            <span class="part-badge">${item.part_number}</span>
          </div>
          <h2 class="modal-title-en">${escapeHtml(item.name_en)}</h2>
          <h3 class="modal-title-ar">${escapeHtml(item.name_ar)}</h3>
          
          <div class="modal-desc-box">
            <p class="desc-en">${escapeHtml(item.description_en)}</p>
            <p class="desc-ar">${escapeHtml(item.description_ar)}</p>
          </div>

          <div class="modal-specs-table">
            <div class="spec-row">
              <span class="spec-label">${I18N[currentLang].ref_no}</span>
              <span class="spec-val">#${item.id}</span>
            </div>
            <div class="spec-row">
              <span class="spec-label">${I18N[currentLang].part_no}</span>
              <span class="spec-val">${item.part_number}</span>
            </div>
            <div class="spec-row">
              <span class="spec-label">${I18N[currentLang].category}</span>
              <span class="spec-val">${escapeHtml(catLabel)}</span>
            </div>
            <div class="spec-row">
              <span class="spec-label">${I18N[currentLang].specifications}</span>
              <span class="spec-val">${(item.specs || []).join(' • ')}</span>
            </div>
          </div>

          <div class="modal-actions-box">
            <a href="https://wa.me/${WHATSAPP_PHONE}?text=${waText}" target="_blank" rel="noopener noreferrer" class="btn-modal-whatsapp">
              <i class="fa-brands fa-whatsapp"></i>
              <span>${I18N[currentLang].inquire_now}</span>
            </a>
            <button class="btn-modal-quote" id="modalQuoteBtn" data-id="${item.id}">
              <i class="fa-solid ${inQuote ? 'fa-check' : 'fa-plus'}"></i>
              <span>${inQuote ? I18N[currentLang].in_quote_list : I18N[currentLang].add_to_quote}</span>
            </button>
          </div>
        </div>
      </div>
    `;

    document.getElementById('modalQuoteBtn').addEventListener('click', () => {
      toggleQuoteItem(item.id);
      openModal(item); // re-render modal button state
    });

    dom.productModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Update URL hash
    window.location.hash = `item-${item.id}`;
  }

  function closeModal() {
    dom.productModal.style.display = 'none';
    document.body.style.overflow = '';
    if (window.location.hash.startsWith('#item-')) {
      history.replaceState(null, null, ' ');
    }
  }

  // --- Quote Drawer Management ---
  function openDrawer() {
    renderDrawerItems();
    dom.quoteDrawer.classList.add('open');
    dom.drawerOverlay.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    dom.quoteDrawer.classList.remove('open');
    dom.drawerOverlay.style.display = 'none';
    document.body.style.overflow = '';
  }

  function toggleQuoteItem(id) {
    const idx = quoteItems.indexOf(id);
    if (idx > -1) {
      quoteItems.splice(idx, 1);
      showToast(I18N[currentLang].toast_removed);
    } else {
      quoteItems.push(id);
      showToast(I18N[currentLang].toast_added);
    }
    localStorage.setItem(STORAGE_KEY_QUOTE, JSON.stringify(quoteItems));
    updateQuoteUI();
    renderProducts();
    if (dom.quoteDrawer.classList.contains('open')) {
      renderDrawerItems();
    }
  }

  function updateQuoteUI() {
    const count = quoteItems.length;
    dom.quoteBadge.textContent = count;
    dom.mobileQuoteBadge.textContent = count;
    dom.drawerItemCount.textContent = `${count} ${count === 1 ? 'item' : 'items'} selected`;
  }

  function renderDrawerItems() {
    dom.drawerItemsList.innerHTML = '';
    if (quoteItems.length === 0) {
      dom.drawerItemsList.innerHTML = `
        <div class="drawer-empty-state">
          <i class="fa-solid fa-clipboard-list"></i>
          <h4>${I18N[currentLang].empty_drawer_title}</h4>
          <p>${I18N[currentLang].empty_drawer_desc}</p>
        </div>
      `;
      dom.whatsappQuoteBtn.disabled = true;
      dom.whatsappQuoteBtn.style.opacity = '0.5';
      dom.copyQuoteBtn.disabled = true;
      dom.copyQuoteBtn.style.opacity = '0.5';
      dom.clearQuoteBtn.style.display = 'none';
      return;
    }

    dom.whatsappQuoteBtn.disabled = false;
    dom.whatsappQuoteBtn.style.opacity = '1';
    dom.copyQuoteBtn.disabled = false;
    dom.copyQuoteBtn.style.opacity = '1';
    dom.clearQuoteBtn.style.display = 'block';

    quoteItems.forEach((id) => {
      const item = catalog.find((x) => x.id === id);
      if (!item) return;

      const itemCard = document.createElement('div');
      itemCard.className = 'drawer-item-card';
      itemCard.innerHTML = `
        <img class="drawer-item-img" src="${item.image}" alt="${escapeHtml(item.name_en)}">
        <div class="drawer-item-info">
          <span class="drawer-item-ref">REF #${String(item.id).padStart(3, '0')} • ${item.part_number}</span>
          <h4 class="drawer-item-title">${escapeHtml(item.name_en)}</h4>
          <p class="drawer-item-sub">${escapeHtml(item.name_ar)}</p>
        </div>
        <button class="btn-drawer-item-remove" data-id="${item.id}" title="Remove item">
          <i class="fa-solid fa-trash-can"></i>
        </button>
      `;

      itemCard.querySelector('.btn-drawer-item-remove').addEventListener('click', () => {
        toggleQuoteItem(item.id);
      });

      dom.drawerItemsList.appendChild(itemCard);
    });
  }

  function clearQuoteList() {
    if (quoteItems.length === 0) return;
    quoteItems = [];
    localStorage.setItem(STORAGE_KEY_QUOTE, JSON.stringify(quoteItems));
    updateQuoteUI();
    renderProducts();
    renderDrawerItems();
    showToast('Quote list cleared.');
  }

  function generateQuoteSummaryText() {
    let summary = `*ELMIR TOOLS & CO - Quote Inquiry*\n`;
    summary += `------------------------------------\n`;
    quoteItems.forEach((id, index) => {
      const item = catalog.find((x) => x.id === id);
      if (item) {
        summary += `${index + 1}. [REF #${item.id}] ${item.name_en} / ${item.name_ar} (Part: ${item.part_number})\n`;
      }
    });
    summary += `------------------------------------\n`;
    summary += `Total items: ${quoteItems.length}\nPlease provide price and availability. Thank you!`;
    return summary;
  }

  function sendWhatsAppQuote() {
    if (quoteItems.length === 0) return;
    const summary = generateQuoteSummaryText();
    const url = `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(summary)}`;
    window.open(url, '_blank');
  }

  function copyQuoteList() {
    if (quoteItems.length === 0) return;
    const summary = generateQuoteSummaryText();
    navigator.clipboard.writeText(summary).then(() => {
      showToast(I18N[currentLang].toast_copied);
    }).catch(() => {
      showToast('Could not copy to clipboard.');
    });
  }

  // --- Toast Notifications ---
  let toastTimer = null;
  function showToast(msg) {
    dom.toast.textContent = msg;
    dom.toast.style.display = 'block';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      dom.toast.style.display = 'none';
    }, 2800);
  }

  // --- URL Deep Linking ---
  function checkUrlParams() {
    const hash = window.location.hash;
    if (hash && hash.startsWith('#item-')) {
      const id = parseInt(hash.replace('#item-', ''), 10);
      const item = catalog.find((x) => x.id === id);
      if (item) openModal(item);
    }
  }

  // --- Utilities ---
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
