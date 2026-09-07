/**
 * ELMIR GARAGE EQUIPMENT - Admin Dashboard Engine
 * Full CRUD, Active/Inactive toggles, Category Management, JSON Export/Import & Persistence
 */

(function () {
  'use strict';

  // --- Constants & Storage Keys ---
  const STORAGE_KEY_CATALOG = 'elmir_tools_catalog_data';
  const STORAGE_KEY_CATEGORIES = 'elmir_tools_categories_data';
  const STORAGE_KEY_AUTH = 'elmir_tools_admin_auth';
  const STORAGE_KEY_PASS = 'elmir_tools_admin_pass';
  const DEFAULT_PASS = 'admin123';

  // --- Default Categories Fallback ---
  const DEFAULT_CATEGORIES = [
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

  // Common icons for category builder
  const POPULAR_ICONS = [
    'fa-cubes', 'fa-wrench', 'fa-arrows-up-down', 'fa-wind', 'fa-oil-can',
    'fa-gauge-high', 'fa-car-burst', 'fa-circle-notch', 'fa-scissors', 'fa-toolbox',
    'fa-car', 'fa-screwdriver-wrench', 'fa-bolt', 'fa-fire', 'fa-gas-pump',
    'fa-gear', 'fa-spray-can', 'fa-battery-full', 'fa-shield-halved', 'fa-truck-pickup'
  ];

  // --- Admin State ---
  let catalogData = [];
  let categoriesData = [];
  let currentTab = 'products';
  let adminSearchQuery = '';
  let adminCatFilter = 'all';
  let adminStatusFilter = 'all'; // 'all' | 'active' | 'inactive'
  let selectedItemIds = new Set();
  let editingProductId = null;
  let editingCategoryId = null;

  // --- DOM Elements Cache ---
  let dom = {};

  // --- Initialize Admin Engine ---
  function initAdmin() {
    loadAdminData();
    injectAdminModals();
    cacheAdminDom();
    bindAdminEvents();
  }

  // --- Data Loading & Storage Sync ---
  function loadAdminData() {
    // 1. Load Categories
    const savedCats = localStorage.getItem(STORAGE_KEY_CATEGORIES);
    if (savedCats) {
      try {
        categoriesData = JSON.parse(savedCats);
      } catch (e) {
        categoriesData = [...DEFAULT_CATEGORIES];
      }
    } else {
      categoriesData = [...DEFAULT_CATEGORIES];
    }

    // 2. Load Catalog
    const savedCatalog = localStorage.getItem(STORAGE_KEY_CATALOG);
    if (savedCatalog) {
      try {
        catalogData = JSON.parse(savedCatalog);
      } catch (e) {
        catalogData = [];
      }
    } else if (window.ElmirCatalog && Array.isArray(window.ElmirCatalog)) {
      catalogData = JSON.parse(JSON.stringify(window.ElmirCatalog));
    }
  }

  function saveCatalogData(triggerStorefrontRefresh = true) {
    try {
      localStorage.setItem(STORAGE_KEY_CATALOG, JSON.stringify(catalogData));
      if (triggerStorefrontRefresh && window.ElmirApp && typeof window.ElmirApp.reload === 'function') {
        window.ElmirApp.reload();
      }
    } catch (e) {
      console.error('Storage quota exceeded or error saving catalog:', e);
      showAdminToast('Storage error: File might be too large.', 'error');
    }
  }

  function saveCategoriesData(triggerStorefrontRefresh = true) {
    try {
      localStorage.setItem(STORAGE_KEY_CATEGORIES, JSON.stringify(categoriesData));
      if (triggerStorefrontRefresh && window.ElmirApp && typeof window.ElmirApp.reload === 'function') {
        window.ElmirApp.reload();
      }
    } catch (e) {
      console.error('Error saving categories:', e);
    }
  }

  // --- Inject Admin Markup into DOM ---
  function injectAdminModals() {
    // Check if already injected
    if (document.getElementById('adminPortalModal')) return;

    const modalHtml = `
      <!-- Admin Login PIN Modal -->
      <div class="admin-modal-overlay" id="adminLoginModal" style="display: none;">
        <div class="admin-login-card">
          <button class="admin-modal-close" id="closeAdminLoginBtn" aria-label="Close">&times;</button>
          <div class="admin-login-header">
            <div class="admin-login-icon"><i class="fa-solid fa-shield-halved"></i></div>
            <h3>Elmir Admin Portal</h3>
            <p>Enter administrative PIN to manage tools & categories</p>
          </div>
          <form id="adminLoginForm" class="admin-login-form">
            <div class="admin-form-group">
              <label for="adminPinInput">Admin Passcode</label>
              <div class="admin-pin-wrapper">
                <input type="password" id="adminPinInput" placeholder="Enter PIN (Default: admin123)" required autocomplete="current-password">
                <button type="button" id="togglePinVisibilityBtn" class="btn-pin-eye" title="Show/Hide PIN">
                  <i class="fa-solid fa-eye"></i>
                </button>
              </div>
              <span id="adminLoginError" class="admin-error-text" style="display: none;">Incorrect passcode. Please try again.</span>
            </div>
            <button type="submit" class="btn-admin-primary btn-block">
              <i class="fa-solid fa-unlock"></i> Unlock Dashboard
            </button>
          </form>
        </div>
      </div>

      <!-- Main Admin Dashboard Modal -->
      <div class="admin-modal-overlay" id="adminPortalModal" style="display: none;">
        <div class="admin-dashboard-container">
          <!-- Top Header -->
          <div class="admin-header">
            <div class="admin-header-title">
              <div class="admin-header-icon"><i class="fa-solid fa-sliders"></i></div>
              <div>
                <h2>Store Management Portal</h2>
                <span class="admin-badge-live">Live Sync Active</span>
              </div>
            </div>
            <div class="admin-header-actions">
              <button id="adminQuickDownloadBtn" class="btn-admin-outline" title="Export catalog.json file">
                <i class="fa-solid fa-download"></i> Download catalog.json
              </button>
              <button id="adminLogoutBtn" class="btn-admin-outline danger" title="Lock & Logout">
                <i class="fa-solid fa-arrow-right-from-bracket"></i> Lock
              </button>
              <button id="closeAdminDashboardBtn" class="admin-modal-close" title="Close Modal">&times;</button>
            </div>
          </div>

          <!-- Navigation Tabs -->
          <div class="admin-nav-tabs">
            <button class="admin-tab-btn active" data-tab="products">
              <i class="fa-solid fa-boxes-stacked"></i> Products Management (<span id="adminStatTotal">0</span>)
            </button>
            <button class="admin-tab-btn" data-tab="categories">
              <i class="fa-solid fa-layer-group"></i> Categories (<span id="adminStatCats">0</span>)
            </button>
            <button class="admin-tab-btn" data-tab="assignments">
              <i class="fa-solid fa-arrows-split-up-and-left"></i> Batch Assign Category
            </button>
            <button class="admin-tab-btn" data-tab="data">
              <i class="fa-solid fa-database"></i> Backup & Data
            </button>
          </div>

          <!-- Tab Content Area -->
          <div class="admin-content-area">
            
            <!-- 1. PRODUCTS TAB -->
            <div class="admin-tab-pane active" id="adminTabProducts">
              <!-- Metrics Cards -->
              <div class="admin-metrics-grid">
                <div class="admin-metric-card">
                  <div class="admin-metric-num" id="adminMetricTotal">0</div>
                  <div class="admin-metric-label">Total Items in Catalog</div>
                </div>
                <div class="admin-metric-card active-metric">
                  <div class="admin-metric-num" id="adminMetricActive">0</div>
                  <div class="admin-metric-label">Active / Live on Storefront</div>
                </div>
                <div class="admin-metric-card inactive-metric">
                  <div class="admin-metric-num" id="adminMetricInactive">0</div>
                  <div class="admin-metric-label">Inactive / Hidden Items</div>
                </div>
                <div class="admin-metric-card">
                  <div class="admin-metric-num" id="adminMetricCategories">0</div>
                  <div class="admin-metric-label">Active Categories</div>
                </div>
              </div>

              <!-- Controls Toolbar -->
              <div class="admin-toolbar">
                <div class="admin-toolbar-left">
                  <div class="admin-search-box">
                    <i class="fa-solid fa-magnifying-glass"></i>
                    <input type="text" id="adminProductSearch" placeholder="Search by name, REF #, or part #...">
                  </div>
                  <select id="adminProductCatFilter" class="admin-select">
                    <option value="all">All Categories</option>
                  </select>
                  <select id="adminProductStatusFilter" class="admin-select">
                    <option value="all">All Statuses</option>
                    <option value="active">Active Only (Visible)</option>
                    <option value="inactive">Inactive Only (Hidden)</option>
                  </select>
                </div>
                <div class="admin-toolbar-right">
                  <button id="adminAddNewProductBtn" class="btn-admin-primary">
                    <i class="fa-solid fa-plus"></i> Add New Product
                  </button>
                </div>
              </div>

              <!-- Bulk Action Bar (Visible when items selected) -->
              <div class="admin-bulk-bar" id="adminBulkBar" style="display: none;">
                <span id="adminBulkCount">0 items selected</span>
                <div class="admin-bulk-actions">
                  <button id="adminBulkActivateBtn" class="btn-bulk btn-bulk-success">
                    <i class="fa-solid fa-eye"></i> Activate Selected
                  </button>
                  <button id="adminBulkDeactivateBtn" class="btn-bulk btn-bulk-warning">
                    <i class="fa-solid fa-eye-slash"></i> Deactivate Selected
                  </button>
                  <button id="adminBulkDeleteBtn" class="btn-bulk btn-bulk-danger">
                    <i class="fa-solid fa-trash"></i> Delete Selected
                  </button>
                  <button id="adminBulkClearBtn" class="btn-bulk btn-bulk-subtle">
                    Deselect All
                  </button>
                </div>
              </div>

              <!-- Products Table -->
              <div class="admin-table-container">
                <table class="admin-table">
                  <thead>
                    <tr>
                      <th width="40"><input type="checkbox" id="adminSelectAllProducts" title="Select All"></th>
                      <th width="65">Image</th>
                      <th width="90">REF #</th>
                      <th width="110">Part #</th>
                      <th>Product Name (EN / AR)</th>
                      <th width="180">Category</th>
                      <th width="130">Status</th>
                      <th width="120" style="text-align: right;">Actions</th>
                    </tr>
                  </thead>
                  <tbody id="adminProductsTableBody">
                    <!-- Rendered via JS -->
                  </tbody>
                </table>
                <div id="adminNoProductsFound" class="admin-empty-table" style="display: none;">
                  <i class="fa-solid fa-magnifying-glass"></i>
                  <p>No products match your search or filter criteria.</p>
                </div>
              </div>
            </div>

            <!-- 2. CATEGORIES TAB -->
            <div class="admin-tab-pane" id="adminTabCategories">
              <div class="admin-cat-header-bar">
                <div>
                  <h3>Product Categories Management</h3>
                  <p>Create, rename, change icons, or reorganize catalog categories</p>
                </div>
                <button id="adminAddNewCategoryBtn" class="btn-admin-primary">
                  <i class="fa-solid fa-folder-plus"></i> Create New Category
                </button>
              </div>

              <div class="admin-categories-grid" id="adminCategoriesList">
                <!-- Rendered dynamically -->
              </div>
            </div>

            <!-- 3. BATCH CATEGORY ASSIGNMENT TAB -->
            <div class="admin-tab-pane" id="adminTabAssignments">
              <div class="admin-assignment-panel">
                <div class="admin-assignment-header">
                  <div>
                    <h3>Batch Move / Category Organizer</h3>
                    <p>Select products below and move them into a specific category in one click</p>
                  </div>
                  <div class="admin-assignment-action-group">
                    <label for="adminTargetCategorySelect">Move selected to:</label>
                    <select id="adminTargetCategorySelect" class="admin-select">
                      <!-- Populated dynamically -->
                    </select>
                    <button id="adminApplyBatchCategoryBtn" class="btn-admin-primary">
                      <i class="fa-solid fa-check"></i> Move Selected Items
                    </button>
                  </div>
                </div>

                <div class="admin-assignment-filter-row">
                  <input type="text" id="adminAssignSearch" class="admin-search-box-input" placeholder="Search items to move...">
                  <select id="adminAssignSourceCat" class="admin-select">
                    <option value="all">Filter by current category: All</option>
                  </select>
                  <span id="adminAssignSelectedCount" class="admin-badge-count">0 items checked</span>
                </div>

                <div class="admin-assignment-items-grid" id="adminAssignmentGrid">
                  <!-- Rendered dynamically -->
                </div>
              </div>
            </div>

            <!-- 4. DATA & BACKUP TAB -->
            <div class="admin-tab-pane" id="adminTabData">
              <div class="admin-data-grid">
                
                <!-- Card 1: Download catalog.json -->
                <div class="admin-data-card">
                  <div class="admin-data-icon"><i class="fa-solid fa-file-arrow-down"></i></div>
                  <h4>Download Updated catalog.json</h4>
                  <p>Exports all current products and categories as a standard <code>catalog.json</code> file. Save this to your repository and push to Cloudflare to publish changes permanently for all visitors worldwide.</p>
                  <button id="adminDownloadCatalogFileBtn" class="btn-admin-primary">
                    <i class="fa-solid fa-download"></i> Download catalog.json
                  </button>
                </div>

                <!-- Card 2: Import Backup / Replace -->
                <div class="admin-data-card">
                  <div class="admin-data-icon"><i class="fa-solid fa-file-arrow-up"></i></div>
                  <h4>Import Catalog from File</h4>
                  <p>Upload a <code>catalog.json</code> or backup JSON file to restore, update, or import multiple products and categories into your catalog.</p>
                  <label class="btn-admin-outline" style="cursor: pointer; display: inline-block;">
                    <i class="fa-solid fa-upload"></i> Upload & Import JSON
                    <input type="file" id="adminImportFileInput" accept=".json" style="display: none;">
                  </label>
                </div>

                <!-- Card 3: Security & Passcode -->
                <div class="admin-data-card">
                  <div class="admin-data-icon"><i class="fa-solid fa-key"></i></div>
                  <h4>Change Admin Passcode</h4>
                  <p>Set a custom admin passcode to protect access to your store catalog management.</p>
                  <form id="adminChangePassForm" class="admin-change-pass-form">
                    <input type="password" id="adminNewPassInput" placeholder="New passcode" required class="admin-input-sm">
                    <button type="submit" class="btn-admin-outline">
                      <i class="fa-solid fa-check"></i> Update Passcode
                    </button>
                  </form>
                </div>

                <!-- Card 4: Reset Defaults -->
                <div class="admin-data-card danger-zone">
                  <div class="admin-data-icon danger"><i class="fa-solid fa-triangle-exclamation"></i></div>
                  <h4>Reset to Default Catalog</h4>
                  <p>Clear all browser modifications and reload original catalog directly from the web server.</p>
                  <button id="adminResetDefaultCatalogBtn" class="btn-admin-outline danger">
                    <i class="fa-solid fa-rotate-left"></i> Reset to Factory Default
                  </button>
                </div>

              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- Add / Edit Product Modal -->
      <div class="admin-modal-overlay" id="adminProductModal" style="display: none; z-index: 10000;">
        <div class="admin-form-modal">
          <button class="admin-modal-close" id="closeProductFormBtn" aria-label="Close">&times;</button>
          <div class="admin-form-header">
            <h3 id="adminProductModalTitle">Add New Product</h3>
            <p>Fill out the details below to add or update a tool in the catalog</p>
          </div>
          
          <form id="adminProductForm" class="admin-product-form">
            <div class="admin-form-grid">
              
              <!-- Left Column: Primary Details -->
              <div class="admin-form-col">
                <div class="admin-form-group">
                  <label for="prodNameEn">Product Name (English) *</label>
                  <input type="text" id="prodNameEn" required placeholder="e.g. 1/2-inch Pneumatic Impact Wrench">
                </div>

                <div class="admin-form-group">
                  <label for="prodNameAr">Product Name (Arabic) *</label>
                  <input type="text" id="prodNameAr" required placeholder="e.g. مسدس هواء فك براغي ١/٢ انش" dir="rtl">
                </div>

                <div class="admin-form-row">
                  <div class="admin-form-group">
                    <label for="prodRefNo">REF # (Unique ID) *</label>
                    <input type="number" id="prodRefNo" required placeholder="e.g. 259">
                  </div>
                  <div class="admin-form-group">
                    <label for="prodPartNo">Part Number *</label>
                    <input type="text" id="prodPartNo" required placeholder="e.g. ET-259">
                  </div>
                </div>

                <div class="admin-form-group">
                  <label for="prodCategory">Category *</label>
                  <select id="prodCategory" required class="admin-select">
                    <!-- Populated dynamically -->
                  </select>
                </div>

                <div class="admin-form-group">
                  <label for="prodSpecs">Specifications / Tags (Comma separated)</label>
                  <input type="text" id="prodSpecs" placeholder="e.g. 1/2 Drive, Pneumatic, Heavy Duty, 1200 Nm">
                  <small class="admin-helper-text">Tags help users filter and search tools easily</small>
                </div>

                <div class="admin-form-group">
                  <label class="admin-checkbox-label">
                    <input type="checkbox" id="prodIsActive" checked>
                    <span><strong>Active on Storefront</strong> (Uncheck to hide tool from public view)</span>
                  </label>
                </div>
              </div>

              <!-- Right Column: Image & Descriptions -->
              <div class="admin-form-col">
                <div class="admin-form-group">
                  <label>Product Image *</label>
                  <div class="admin-image-upload-box">
                    <div class="admin-img-preview" id="prodImgPreview">
                      <img id="prodPreviewImgTag" src="images/logo.png" alt="Preview">
                    </div>
                    <div class="admin-img-inputs">
                      <input type="text" id="prodImageUrl" placeholder="Image URL (e.g. images/products/1.jpg)">
                      <div class="admin-upload-divider"><span>OR</span></div>
                      <label class="btn-admin-outline btn-sm" style="cursor: pointer; text-align: center;">
                        <i class="fa-solid fa-cloud-arrow-up"></i> Upload Image File
                        <input type="file" id="prodImageFileInput" accept="image/*" style="display: none;">
                      </label>
                    </div>
                  </div>
                </div>

                <div class="admin-form-group">
                  <label for="prodDescEn">Description (English)</label>
                  <textarea id="prodDescEn" rows="3" placeholder="Detailed product specifications, build quality, and automotive usage..."></textarea>
                </div>

                <div class="admin-form-group">
                  <label for="prodDescAr">Description (Arabic)</label>
                  <textarea id="prodDescAr" rows="3" placeholder="وصف مفصل للمعدة، الاستخدامات في الورش، وجودة التصنيع..." dir="rtl"></textarea>
                </div>
              </div>

            </div>

            <div class="admin-form-actions">
              <button type="button" id="cancelProductFormBtn" class="btn-admin-outline">Cancel</button>
              <button type="submit" class="btn-admin-primary">
                <i class="fa-solid fa-floppy-disk"></i> Save Product
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Add / Edit Category Modal -->
      <div class="admin-modal-overlay" id="adminCategoryModal" style="display: none; z-index: 10000;">
        <div class="admin-form-modal admin-form-modal-sm">
          <button class="admin-modal-close" id="closeCategoryFormBtn" aria-label="Close">&times;</button>
          <div class="admin-form-header">
            <h3 id="adminCategoryModalTitle">Create New Category</h3>
            <p>Define a new equipment category to organize tools</p>
          </div>
          
          <form id="adminCategoryForm" class="admin-product-form">
            <div class="admin-form-group">
              <label for="catSlugInput">Category ID / Slug *</label>
              <input type="text" id="catSlugInput" required placeholder="e.g. battery_chargers" pattern="[a-z0-9_]+" title="Lowercase letters, numbers, and underscores only">
              <small class="admin-helper-text">Unique identifier (e.g. tire_wheel_service)</small>
            </div>

            <div class="admin-form-group">
              <label for="catNameEnInput">Category Name (English) *</label>
              <input type="text" id="catNameEnInput" required placeholder="e.g. Battery Chargers & Jump Starters">
            </div>

            <div class="admin-form-group">
              <label for="catNameArInput">Category Name (Arabic) *</label>
              <input type="text" id="catNameArInput" required placeholder="e.g. شواحن البطاريات واجهزة الإقلاع" dir="rtl">
            </div>

            <div class="admin-form-group">
              <label for="catIconInput">FontAwesome Icon Class *</label>
              <div class="admin-icon-picker-row">
                <div class="admin-icon-preview-box" id="catIconPreview">
                  <i class="fa-solid fa-folder"></i>
                </div>
                <input type="text" id="catIconInput" required placeholder="fa-car or fa-wrench" value="fa-wrench">
              </div>
              
              <!-- Quick Icon Suggestions -->
              <div class="admin-icon-suggestions" id="adminIconSuggestions">
                <!-- Icons injected dynamically -->
              </div>
            </div>

            <div class="admin-form-actions">
              <button type="button" id="cancelCategoryFormBtn" class="btn-admin-outline">Cancel</button>
              <button type="submit" class="btn-admin-primary">
                <i class="fa-solid fa-folder-check"></i> Save Category
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Admin Toast Notification -->
      <div id="adminToast" class="admin-toast-message" style="display: none;"></div>
    `;

    const container = document.createElement('div');
    container.id = 'elmirAdminRoot';
    container.innerHTML = modalHtml;
    document.body.appendChild(container);

    // Populate Icon Suggestions
    const iconGrid = document.getElementById('adminIconSuggestions');
    if (iconGrid) {
      iconGrid.innerHTML = POPULAR_ICONS.map((icon) => `
        <button type="button" class="admin-icon-chip" data-icon="${icon}" title="${icon}">
          <i class="fa-solid ${icon}"></i>
        </button>
      `).join('');
    }
  }

  // --- Cache DOM Elements ---
  function cacheAdminDom() {
    dom = {
      // Modals
      loginModal: document.getElementById('adminLoginModal'),
      portalModal: document.getElementById('adminPortalModal'),
      productModal: document.getElementById('adminProductModal'),
      categoryModal: document.getElementById('adminCategoryModal'),
      toast: document.getElementById('adminToast'),
      
      // Login
      loginForm: document.getElementById('adminLoginForm'),
      pinInput: document.getElementById('adminPinInput'),
      pinEyeBtn: document.getElementById('togglePinVisibilityBtn'),
      loginError: document.getElementById('adminLoginError'),
      closeLoginBtn: document.getElementById('closeAdminLoginBtn'),
      
      // Portal Header & Tabs
      closePortalBtn: document.getElementById('closeAdminDashboardBtn'),
      logoutBtn: document.getElementById('adminLogoutBtn'),
      quickDownloadBtn: document.getElementById('adminQuickDownloadBtn'),
      tabBtns: document.querySelectorAll('.admin-tab-btn'),
      tabPanes: document.querySelectorAll('.admin-tab-pane'),
      
      // Product Stats & Toolbar
      statTotal: document.getElementById('adminStatTotal'),
      statCats: document.getElementById('adminStatCats'),
      metricTotal: document.getElementById('adminMetricTotal'),
      metricActive: document.getElementById('adminMetricActive'),
      metricInactive: document.getElementById('adminMetricInactive'),
      metricCats: document.getElementById('adminMetricCategories'),
      
      productSearch: document.getElementById('adminProductSearch'),
      productCatFilter: document.getElementById('adminProductCatFilter'),
      productStatusFilter: document.getElementById('adminProductStatusFilter'),
      addNewProductBtn: document.getElementById('adminAddNewProductBtn'),
      
      // Products Table & Bulk
      selectAllCheckbox: document.getElementById('adminSelectAllProducts'),
      productsTableBody: document.getElementById('adminProductsTableBody'),
      noProductsFound: document.getElementById('adminNoProductsFound'),
      bulkBar: document.getElementById('adminBulkBar'),
      bulkCount: document.getElementById('adminBulkCount'),
      bulkActivateBtn: document.getElementById('adminBulkActivateBtn'),
      bulkDeactivateBtn: document.getElementById('adminBulkDeactivateBtn'),
      bulkDeleteBtn: document.getElementById('adminBulkDeleteBtn'),
      bulkClearBtn: document.getElementById('adminBulkClearBtn'),
      
      // Product Form
      productForm: document.getElementById('adminProductForm'),
      productModalTitle: document.getElementById('adminProductModalTitle'),
      closeProductFormBtn: document.getElementById('closeProductFormBtn'),
      cancelProductFormBtn: document.getElementById('cancelProductFormBtn'),
      prodNameEn: document.getElementById('prodNameEn'),
      prodNameAr: document.getElementById('prodNameAr'),
      prodRefNo: document.getElementById('prodRefNo'),
      prodPartNo: document.getElementById('prodPartNo'),
      prodCategory: document.getElementById('prodCategory'),
      prodSpecs: document.getElementById('prodSpecs'),
      prodIsActive: document.getElementById('prodIsActive'),
      prodImageUrl: document.getElementById('prodImageUrl'),
      prodImageFileInput: document.getElementById('prodImageFileInput'),
      prodPreviewImgTag: document.getElementById('prodPreviewImgTag'),
      prodDescEn: document.getElementById('prodDescEn'),
      prodDescAr: document.getElementById('prodDescAr'),
      
      // Categories Management
      addNewCategoryBtn: document.getElementById('adminAddNewCategoryBtn'),
      categoriesList: document.getElementById('adminCategoriesList'),
      categoryModalTitle: document.getElementById('adminCategoryModalTitle'),
      categoryForm: document.getElementById('adminCategoryForm'),
      closeCategoryFormBtn: document.getElementById('closeCategoryFormBtn'),
      cancelCategoryFormBtn: document.getElementById('cancelCategoryFormBtn'),
      catSlugInput: document.getElementById('catSlugInput'),
      catNameEnInput: document.getElementById('catNameEnInput'),
      catNameArInput: document.getElementById('catNameArInput'),
      catIconInput: document.getElementById('catIconInput'),
      catIconPreview: document.getElementById('catIconPreview'),
      
      // Batch Assignments Tab
      targetCatSelect: document.getElementById('adminTargetCategorySelect'),
      applyBatchCatBtn: document.getElementById('adminApplyBatchCategoryBtn'),
      assignSearch: document.getElementById('adminAssignSearch'),
      assignSourceCat: document.getElementById('adminAssignSourceCat'),
      assignSelectedCount: document.getElementById('adminAssignSelectedCount'),
      assignmentGrid: document.getElementById('adminAssignmentGrid'),
      
      // Data Management
      downloadCatalogFileBtn: document.getElementById('adminDownloadCatalogFileBtn'),
      importFileInput: document.getElementById('adminImportFileInput'),
      changePassForm: document.getElementById('adminChangePassForm'),
      newPassInput: document.getElementById('adminNewPassInput'),
      resetDefaultCatalogBtn: document.getElementById('adminResetDefaultCatalogBtn'),
      
      // External Trigger
      externalTriggerBtn: document.getElementById('adminDiscreteTriggerBtn')
    };
  }

  // --- Event Bindings ---
  function bindAdminEvents() {
    // Discrete button click
    const trigger = document.getElementById('adminDiscreteTriggerBtn');
    if (trigger) {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        openAdminPortal();
      });
    }

    // Keyboard shortcut (Ctrl + Shift + A or Cmd + Shift + A)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'a') {
        e.preventDefault();
        openAdminPortal();
      }
    });

    // Login logic
    if (dom.loginForm) {
      dom.loginForm.addEventListener('submit', handleAdminLogin);
    }
    if (dom.closeLoginBtn) {
      dom.closeLoginBtn.addEventListener('click', () => {
        dom.loginModal.style.display = 'none';
      });
    }
    if (dom.pinEyeBtn) {
      dom.pinEyeBtn.addEventListener('click', () => {
        const isPass = dom.pinInput.type === 'password';
        dom.pinInput.type = isPass ? 'text' : 'password';
        dom.pinEyeBtn.innerHTML = `<i class="fa-solid ${isPass ? 'fa-eye-slash' : 'fa-eye'}"></i>`;
      });
    }

    // Portal actions
    if (dom.closePortalBtn) {
      dom.closePortalBtn.addEventListener('click', closeAdminPortal);
    }
    if (dom.logoutBtn) {
      dom.logoutBtn.addEventListener('click', handleAdminLogout);
    }
    if (dom.quickDownloadBtn) {
      dom.quickDownloadBtn.addEventListener('click', downloadCatalogJson);
    }

    // Tab navigation
    dom.tabBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        switchTab(btn.dataset.tab);
      });
    });

    // Product search & filters
    if (dom.productSearch) {
      dom.productSearch.addEventListener('input', (e) => {
        adminSearchQuery = e.target.value.trim().toLowerCase();
        renderAdminProductsTable();
      });
    }
    if (dom.productCatFilter) {
      dom.productCatFilter.addEventListener('change', (e) => {
        adminCatFilter = e.target.value;
        renderAdminProductsTable();
      });
    }
    if (dom.productStatusFilter) {
      dom.productStatusFilter.addEventListener('change', (e) => {
        adminStatusFilter = e.target.value;
        renderAdminProductsTable();
      });
    }

    // Product form triggers
    if (dom.addNewProductBtn) {
      dom.addNewProductBtn.addEventListener('click', openAddProductModal);
    }
    if (dom.closeProductFormBtn) {
      dom.closeProductFormBtn.addEventListener('click', closeProductModal);
    }
    if (dom.cancelProductFormBtn) {
      dom.cancelProductFormBtn.addEventListener('click', closeProductModal);
    }
    if (dom.productForm) {
      dom.productForm.addEventListener('submit', handleSaveProduct);
    }

    // Image Upload & Preview in Product Form
    if (dom.prodImageUrl) {
      dom.prodImageUrl.addEventListener('input', (e) => {
        const url = e.target.value.trim();
        dom.prodPreviewImgTag.src = url || 'images/logo.png';
      });
    }
    if (dom.prodImageFileInput) {
      dom.prodImageFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (evt) {
            const dataUrl = evt.target.result;
            dom.prodImageUrl.value = dataUrl;
            dom.prodPreviewImgTag.src = dataUrl;
          };
          reader.readAsDataURL(file);
        }
      });
    }

    // Select All Checkbox
    if (dom.selectAllCheckbox) {
      dom.selectAllCheckbox.addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        const visibleItems = getFilteredAdminItems();
        if (isChecked) {
          visibleItems.forEach((it) => selectedItemIds.add(it.id));
        } else {
          selectedItemIds.clear();
        }
        updateBulkBar();
        renderAdminProductsTable();
      });
    }

    // Bulk actions
    if (dom.bulkActivateBtn) {
      dom.bulkActivateBtn.addEventListener('click', () => handleBulkStatus(true));
    }
    if (dom.bulkDeactivateBtn) {
      dom.bulkDeactivateBtn.addEventListener('click', () => handleBulkStatus(false));
    }
    if (dom.bulkDeleteBtn) {
      dom.bulkDeleteBtn.addEventListener('click', handleBulkDelete);
    }
    if (dom.bulkClearBtn) {
      dom.bulkClearBtn.addEventListener('click', () => {
        selectedItemIds.clear();
        if (dom.selectAllCheckbox) dom.selectAllCheckbox.checked = false;
        updateBulkBar();
        renderAdminProductsTable();
      });
    }

    // Category form triggers
    if (dom.addNewCategoryBtn) {
      dom.addNewCategoryBtn.addEventListener('click', openAddCategoryModal);
    }
    if (dom.closeCategoryFormBtn) {
      dom.closeCategoryFormBtn.addEventListener('click', closeCategoryModal);
    }
    if (dom.cancelCategoryFormBtn) {
      dom.cancelCategoryFormBtn.addEventListener('click', closeCategoryModal);
    }
    if (dom.categoryForm) {
      dom.categoryForm.addEventListener('submit', handleSaveCategory);
    }
    if (dom.catIconInput) {
      dom.catIconInput.addEventListener('input', (e) => {
        const icon = e.target.value.trim() || 'fa-folder';
        dom.catIconPreview.innerHTML = `<i class="fa-solid ${icon}"></i>`;
      });
    }
    document.querySelectorAll('.admin-icon-chip').forEach((chip) => {
      chip.addEventListener('click', () => {
        const icon = chip.dataset.icon;
        dom.catIconInput.value = icon;
        dom.catIconPreview.innerHTML = `<i class="fa-solid ${icon}"></i>`;
      });
    });

    // Batch assignment filters & actions
    if (dom.assignSearch) {
      dom.assignSearch.addEventListener('input', renderBatchAssignmentGrid);
    }
    if (dom.assignSourceCat) {
      dom.assignSourceCat.addEventListener('change', renderBatchAssignmentGrid);
    }
    if (dom.applyBatchCatBtn) {
      dom.applyBatchCatBtn.addEventListener('click', handleApplyBatchCategory);
    }

    // Data Management
    if (dom.downloadCatalogFileBtn) {
      dom.downloadCatalogFileBtn.addEventListener('click', downloadCatalogJson);
    }
    if (dom.importFileInput) {
      dom.importFileInput.addEventListener('change', handleImportJson);
    }
    if (dom.changePassForm) {
      dom.changePassForm.addEventListener('submit', handleChangePasscode);
    }
    if (dom.resetDefaultCatalogBtn) {
      dom.resetDefaultCatalogBtn.addEventListener('click', handleResetCatalog);
    }
  }

  // --- Auth Controls ---
  function isAuthenticated() {
    return sessionStorage.getItem(STORAGE_KEY_AUTH) === 'true';
  }

  function openAdminPortal() {
    loadAdminData();
    if (!isAuthenticated()) {
      dom.pinInput.value = '';
      dom.loginError.style.display = 'none';
      dom.loginModal.style.display = 'flex';
      setTimeout(() => dom.pinInput.focus(), 150);
    } else {
      showDashboardModal();
    }
  }

  function handleAdminLogin(e) {
    e.preventDefault();
    const entered = dom.pinInput.value.trim();
    const currentPass = localStorage.getItem(STORAGE_KEY_PASS) || DEFAULT_PASS;
    
    if (entered === currentPass) {
      sessionStorage.setItem(STORAGE_KEY_AUTH, 'true');
      dom.loginModal.style.display = 'none';
      showDashboardModal();
      showAdminToast('Welcome to Admin Portal!', 'success');
    } else {
      dom.loginError.style.display = 'block';
      dom.pinInput.focus();
    }
  }

  function handleAdminLogout() {
    sessionStorage.removeItem(STORAGE_KEY_AUTH);
    dom.portalModal.style.display = 'none';
    showAdminToast('Logged out of Admin Portal.', 'info');
  }

  function showDashboardModal() {
    dom.portalModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    refreshAllAdminViews();
  }

  function closeAdminPortal() {
    dom.portalModal.style.display = 'none';
    document.body.style.overflow = '';
  }

  function switchTab(tabId) {
    currentTab = tabId;
    dom.tabBtns.forEach((b) => b.classList.toggle('active', b.dataset.tab === tabId));
    dom.tabPanes.forEach((p) => {
      p.classList.toggle('active', p.id === `adminTab${tabId.charAt(0).toUpperCase() + tabId.slice(1)}`);
    });

    if (tabId === 'products') renderAdminProductsTable();
    if (tabId === 'categories') renderAdminCategoriesList();
    if (tabId === 'assignments') renderBatchAssignmentGrid();
  }

  // --- Refresh All Admin Views ---
  function refreshAllAdminViews() {
    populateCategoryDropdowns();
    updateMetrics();
    renderAdminProductsTable();
    renderAdminCategoriesList();
    renderBatchAssignmentGrid();
  }

  // --- Metrics Computation ---
  function updateMetrics() {
    const total = catalogData.length;
    const activeCount = catalogData.filter((it) => it.active !== false).length;
    const inactiveCount = total - activeCount;
    const catsCount = categoriesData.filter((c) => c.id !== 'all').length;

    if (dom.statTotal) dom.statTotal.textContent = total;
    if (dom.statCats) dom.statCats.textContent = catsCount;
    if (dom.metricTotal) dom.metricTotal.textContent = total;
    if (dom.metricActive) dom.metricActive.textContent = activeCount;
    if (dom.metricInactive) dom.metricInactive.textContent = inactiveCount;
    if (dom.metricCats) dom.metricCats.textContent = catsCount;
  }

  // --- Category Dropdown Helpers ---
  function populateCategoryDropdowns() {
    // 1. Products Filter dropdown
    if (dom.productCatFilter) {
      const curVal = dom.productCatFilter.value || 'all';
      dom.productCatFilter.innerHTML = '<option value="all">All Categories</option>' +
        categoriesData
          .filter((c) => c.id !== 'all')
          .map((c) => `<option value="${c.id}">${c.en} (${c.ar})</option>`)
          .join('');
      dom.productCatFilter.value = curVal;
    }

    // 2. Product Form Category dropdown
    if (dom.prodCategory) {
      dom.prodCategory.innerHTML = categoriesData
        .filter((c) => c.id !== 'all')
        .map((c) => `<option value="${c.id}">${c.en} - ${c.ar}</option>`)
        .join('');
    }

    // 3. Batch Assignment Target Category dropdown
    if (dom.targetCatSelect) {
      dom.targetCatSelect.innerHTML = categoriesData
        .filter((c) => c.id !== 'all')
        .map((c) => `<option value="${c.id}">${c.en} - ${c.ar}</option>`)
        .join('');
    }

    // 4. Batch Assignment Source Filter dropdown
    if (dom.assignSourceCat) {
      const curVal = dom.assignSourceCat.value || 'all';
      dom.assignSourceCat.innerHTML = '<option value="all">Filter by current category: All</option>' +
        categoriesData
          .filter((c) => c.id !== 'all')
          .map((c) => `<option value="${c.id}">${c.en} (${c.ar})</option>`)
          .join('');
      dom.assignSourceCat.value = curVal;
    }
  }

  // --- Filtering Helper ---
  function getFilteredAdminItems() {
    return catalogData.filter((item) => {
      // Category filter
      if (adminCatFilter !== 'all' && item.category_id !== adminCatFilter) {
        return false;
      }

      // Status filter
      const isActive = item.active !== false;
      if (adminStatusFilter === 'active' && !isActive) return false;
      if (adminStatusFilter === 'inactive' && isActive) return false;

      // Search Query filter
      if (adminSearchQuery) {
        const matchEn = (item.name_en || '').toLowerCase().includes(adminSearchQuery);
        const matchAr = (item.name_ar || '').toLowerCase().includes(adminSearchQuery);
        const matchRef = String(item.id || item.ref_no) === adminSearchQuery || `ref ${item.id}`.includes(adminSearchQuery);
        const matchPart = (item.part_number || '').toLowerCase().includes(adminSearchQuery);
        if (!matchEn && !matchAr && !matchRef && !matchPart) {
          return false;
        }
      }

      return true;
    }).sort((a, b) => (a.id || 0) - (b.id || 0));
  }

  // --- Render Products Table ---
  function renderAdminProductsTable() {
    if (!dom.productsTableBody) return;
    const items = getFilteredAdminItems();
    dom.productsTableBody.innerHTML = '';

    if (items.length === 0) {
      dom.noProductsFound.style.display = 'block';
      return;
    }
    dom.noProductsFound.style.display = 'none';

    items.forEach((item) => {
      const isChecked = selectedItemIds.has(item.id);
      const isActive = item.active !== false;
      const catObj = categoriesData.find((c) => c.id === item.category_id);
      const catName = catObj ? `${catObj.en}` : (item.category_en || item.category_id);

      const tr = document.createElement('tr');
      tr.className = `admin-table-row ${isActive ? '' : 'row-inactive'} ${isChecked ? 'row-selected' : ''}`;
      tr.innerHTML = `
        <td>
          <input type="checkbox" class="admin-item-checkbox" data-id="${item.id}" ${isChecked ? 'checked' : ''}>
        </td>
        <td>
          <div class="admin-table-thumb">
            <img src="${item.image || 'images/logo.png'}" alt="${escapeAdminHtml(item.name_en)}" loading="lazy">
          </div>
        </td>
        <td>
          <span class="admin-ref-badge">#${item.id}</span>
        </td>
        <td>
          <span class="admin-part-code">${escapeAdminHtml(item.part_number || 'N/A')}</span>
        </td>
        <td>
          <div class="admin-table-title-en">${escapeAdminHtml(item.name_en)}</div>
          <div class="admin-table-title-ar">${escapeAdminHtml(item.name_ar)}</div>
        </td>
        <td>
          <span class="admin-cat-pill">${escapeAdminHtml(catName)}</span>
        </td>
        <td>
          <label class="admin-status-switch" title="Click to ${isActive ? 'Deactivate' : 'Activate'}">
            <input type="checkbox" class="admin-toggle-active" data-id="${item.id}" ${isActive ? 'checked' : ''}>
            <span class="status-slider"></span>
            <span class="status-label-text ${isActive ? 'text-active' : 'text-inactive'}">
              ${isActive ? 'Active' : 'Hidden'}
            </span>
          </label>
        </td>
        <td style="text-align: right;">
          <div class="admin-row-actions">
            <button class="btn-row-action btn-edit-prod" data-id="${item.id}" title="Edit Tool">
              <i class="fa-solid fa-pen-to-square"></i>
            </button>
            <button class="btn-row-action danger btn-del-prod" data-id="${item.id}" title="Delete Tool">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          </div>
        </td>
      `;

      // Event: Select Item Checkbox
      tr.querySelector('.admin-item-checkbox').addEventListener('change', (e) => {
        if (e.target.checked) {
          selectedItemIds.add(item.id);
        } else {
          selectedItemIds.delete(item.id);
        }
        updateBulkBar();
        tr.classList.toggle('row-selected', e.target.checked);
      });

      // Event: Toggle Active/Inactive
      tr.querySelector('.admin-toggle-active').addEventListener('change', (e) => {
        toggleItemActiveState(item.id, e.target.checked);
      });

      // Event: Edit Product
      tr.querySelector('.btn-edit-prod').addEventListener('click', () => {
        openEditProductModal(item.id);
      });

      // Event: Delete Product
      tr.querySelector('.btn-del-prod').addEventListener('click', () => {
        confirmDeleteProduct(item.id);
      });

      dom.productsTableBody.appendChild(tr);
    });

    updateBulkBar();
  }

  function updateBulkBar() {
    const count = selectedItemIds.size;
    if (dom.bulkBar) {
      dom.bulkBar.style.display = count > 0 ? 'flex' : 'none';
      if (dom.bulkCount) dom.bulkCount.textContent = `${count} product${count > 1 ? 's' : ''} selected`;
    }
  }

  // --- Toggle Item Active / Inactive ---
  function toggleItemActiveState(id, isActive) {
    const item = catalogData.find((x) => x.id === id);
    if (!item) return;

    item.active = isActive;
    saveCatalogData(true);
    updateMetrics();
    renderAdminProductsTable();
    showAdminToast(`Item #${id} is now ${isActive ? 'Active (Live)' : 'Deactivated (Hidden)'}`, 'success');
  }

  // --- Bulk Item Actions ---
  function handleBulkStatus(isActive) {
    if (selectedItemIds.size === 0) return;
    catalogData.forEach((it) => {
      if (selectedItemIds.has(it.id)) {
        it.active = isActive;
      }
    });

    saveCatalogData(true);
    updateMetrics();
    renderAdminProductsTable();
    showAdminToast(`${selectedItemIds.size} items updated to ${isActive ? 'Active' : 'Hidden'}.`, 'success');
  }

  function handleBulkDelete() {
    if (selectedItemIds.size === 0) return;
    const confirmMsg = `Are you sure you want to permanently delete these ${selectedItemIds.size} selected products?`;
    if (!confirm(confirmMsg)) return;

    catalogData = catalogData.filter((it) => !selectedItemIds.has(it.id));
    selectedItemIds.clear();
    saveCatalogData(true);
    updateMetrics();
    renderAdminProductsTable();
    showAdminToast('Selected products deleted successfully.', 'success');
  }

  // --- Add / Edit Product Modals ---
  function openAddProductModal() {
    editingProductId = null;
    dom.productModalTitle.textContent = 'Add New Product';
    dom.productForm.reset();

    // Auto-calculate next REF #
    const maxId = catalogData.reduce((max, it) => Math.max(max, parseInt(it.id, 10) || 0), 0);
    const nextId = maxId + 1;
    dom.prodRefNo.value = nextId;
    dom.prodPartNo.value = `ET-${String(nextId).padStart(3, '0')}`;
    dom.prodIsActive.checked = true;
    dom.prodPreviewImgTag.src = 'images/logo.png';
    dom.prodImageUrl.value = '';

    dom.productModal.style.display = 'flex';
  }

  function openEditProductModal(id) {
    const item = catalogData.find((x) => x.id === id);
    if (!item) return;

    editingProductId = id;
    dom.productModalTitle.textContent = `Edit Product #${item.id} (${item.name_en})`;
    
    dom.prodNameEn.value = item.name_en || '';
    dom.prodNameAr.value = item.name_ar || '';
    dom.prodRefNo.value = item.id;
    dom.prodPartNo.value = item.part_number || '';
    dom.prodCategory.value = item.category_id || (categoriesData[1] && categoriesData[1].id);
    dom.prodSpecs.value = (item.specs || []).join(', ');
    dom.prodIsActive.checked = item.active !== false;
    dom.prodImageUrl.value = item.image || '';
    dom.prodPreviewImgTag.src = item.image || 'images/logo.png';
    dom.prodDescEn.value = item.description_en || '';
    dom.prodDescAr.value = item.description_ar || '';

    dom.productModal.style.display = 'flex';
  }

  function closeProductModal() {
    dom.productModal.style.display = 'none';
  }

  function handleSaveProduct(e) {
    e.preventDefault();

    const id = parseInt(dom.prodRefNo.value.trim(), 10);
    const nameEn = dom.prodNameEn.value.trim();
    const nameAr = dom.prodNameAr.value.trim();
    const partNo = dom.prodPartNo.value.trim();
    const catId = dom.prodCategory.value;
    const catObj = categoriesData.find((c) => c.id === catId);
    const specs = dom.prodSpecs.value.split(',').map((s) => s.trim()).filter(Boolean);
    const isActive = dom.prodIsActive.checked;
    const imgUrl = dom.prodImageUrl.value.trim() || 'images/logo.png';
    const descEn = dom.prodDescEn.value.trim() || `Professional grade ${nameEn} for automotive service.`;
    const descAr = dom.prodDescAr.value.trim() || `معدة احترافية ${nameAr} مصممة لخدمات ورش السيارات.`;

    if (editingProductId !== null) {
      // Update existing
      const idx = catalogData.findIndex((x) => x.id === editingProductId);
      if (idx > -1) {
        catalogData[idx] = {
          ...catalogData[idx],
          id: id,
          ref_no: String(id),
          part_number: partNo,
          name_en: nameEn,
          name_ar: nameAr,
          category_id: catId,
          category_en: catObj ? catObj.en : 'General',
          category_ar: catObj ? catObj.ar : 'عام',
          description_en: descEn,
          description_ar: descAr,
          image: imgUrl,
          specs: specs,
          active: isActive
        };
        showAdminToast(`Product #${id} updated successfully!`, 'success');
      }
    } else {
      // Check duplicate ID
      if (catalogData.some((x) => x.id === id)) {
        alert(`REF #${id} already exists. Please choose a different REF number.`);
        return;
      }

      // Create new
      const newItem = {
        id: id,
        ref_no: String(id),
        part_number: partNo,
        name_en: nameEn,
        name_ar: nameAr,
        category_id: catId,
        category_en: catObj ? catObj.en : 'General',
        category_ar: catObj ? catObj.ar : 'عام',
        description_en: descEn,
        description_ar: descAr,
        image: imgUrl,
        specs: specs,
        active: isActive
      };
      catalogData.push(newItem);
      showAdminToast(`New product #${id} created successfully!`, 'success');
    }

    saveCatalogData(true);
    closeProductModal();
    updateMetrics();
    renderAdminProductsTable();
    renderAdminCategoriesList();
  }

  function confirmDeleteProduct(id) {
    const item = catalogData.find((x) => x.id === id);
    if (!item) return;

    if (confirm(`Are you sure you want to permanently delete "${item.name_en}" (REF #${id})?`)) {
      catalogData = catalogData.filter((x) => x.id !== id);
      selectedItemIds.delete(id);
      saveCatalogData(true);
      updateMetrics();
      renderAdminProductsTable();
      renderAdminCategoriesList();
      showAdminToast(`Product #${id} removed from catalog.`, 'success');
    }
  }

  // --- Categories Management View ---
  function renderAdminCategoriesList() {
    if (!dom.categoriesList) return;
    dom.categoriesList.innerHTML = '';

    categoriesData.forEach((cat) => {
      const isAll = cat.id === 'all';
      const count = isAll ? catalogData.length : catalogData.filter((x) => x.category_id === cat.id).length;
      const activeCount = isAll
        ? catalogData.filter((x) => x.active !== false).length
        : catalogData.filter((x) => x.category_id === cat.id && x.active !== false).length;

      const card = document.createElement('div');
      card.className = `admin-cat-card ${isAll ? 'admin-cat-card-all' : ''}`;
      card.innerHTML = `
        <div class="admin-cat-card-top">
          <div class="admin-cat-icon-badge">
            <i class="fa-solid ${cat.icon || 'fa-folder'}"></i>
          </div>
          <div class="admin-cat-meta">
            <h4 class="admin-cat-title-en">${escapeAdminHtml(cat.en)}</h4>
            <h5 class="admin-cat-title-ar">${escapeAdminHtml(cat.ar)}</h5>
            <span class="admin-cat-slug-pill"><code>${cat.id}</code></span>
          </div>
        </div>
        <div class="admin-cat-card-stats">
          <div class="cat-stat-badge">
            <strong>${count}</strong> total tools
          </div>
          <div class="cat-stat-badge text-success">
            <strong>${activeCount}</strong> active
          </div>
        </div>
        <div class="admin-cat-card-actions">
          ${isAll ? '<span class="admin-subtle-hint">Default System Category</span>' : `
            <button class="btn-admin-outline btn-sm btn-edit-cat" data-id="${cat.id}">
              <i class="fa-solid fa-pen"></i> Edit
            </button>
            <button class="btn-admin-outline btn-sm btn-assign-cat" data-id="${cat.id}">
              <i class="fa-solid fa-arrows-split-up-and-left"></i> Manage Items
            </button>
            <button class="btn-admin-outline btn-sm danger btn-del-cat" data-id="${cat.id}">
              <i class="fa-solid fa-trash"></i> Delete
            </button>
          `}
        </div>
      `;

      if (!isAll) {
        card.querySelector('.btn-edit-cat').addEventListener('click', () => openEditCategoryModal(cat.id));
        card.querySelector('.btn-assign-cat').addEventListener('click', () => {
          switchTab('assignments');
          if (dom.targetCatSelect) dom.targetCatSelect.value = cat.id;
          if (dom.assignSourceCat) dom.assignSourceCat.value = 'all';
        });
        card.querySelector('.btn-del-cat').addEventListener('click', () => confirmDeleteCategory(cat.id));
      }

      dom.categoriesList.appendChild(card);
    });
  }

  function openAddCategoryModal() {
    editingCategoryId = null;
    dom.categoryModalTitle.textContent = 'Create New Category';
    dom.categoryForm.reset();
    dom.catSlugInput.disabled = false;
    dom.catIconInput.value = 'fa-wrench';
    dom.catIconPreview.innerHTML = '<i class="fa-solid fa-wrench"></i>';
    dom.categoryModal.style.display = 'flex';
  }

  function openEditCategoryModal(catId) {
    const cat = categoriesData.find((c) => c.id === catId);
    if (!cat) return;

    editingCategoryId = catId;
    dom.categoryModalTitle.textContent = `Edit Category (${cat.en})`;
    dom.catSlugInput.value = cat.id;
    dom.catSlugInput.disabled = true; // prevent breaking slug references
    dom.catNameEnInput.value = cat.en;
    dom.catNameArInput.value = cat.ar;
    dom.catIconInput.value = cat.icon || 'fa-wrench';
    dom.catIconPreview.innerHTML = `<i class="fa-solid ${cat.icon || 'fa-wrench'}"></i>`;

    dom.categoryModal.style.display = 'flex';
  }

  function closeCategoryModal() {
    dom.categoryModal.style.display = 'none';
  }

  function handleSaveCategory(e) {
    e.preventDefault();
    const slug = dom.catSlugInput.value.trim().toLowerCase().replace(/\s+/g, '_');
    const nameEn = dom.catNameEnInput.value.trim();
    const nameAr = dom.catNameArInput.value.trim();
    const icon = dom.catIconInput.value.trim() || 'fa-wrench';

    if (editingCategoryId !== null) {
      // Edit category
      const idx = categoriesData.findIndex((c) => c.id === editingCategoryId);
      if (idx > -1) {
        categoriesData[idx] = {
          ...categoriesData[idx],
          en: nameEn,
          ar: nameAr,
          icon: icon
        };
        // Update product category display names
        catalogData.forEach((it) => {
          if (it.category_id === editingCategoryId) {
            it.category_en = nameEn;
            it.category_ar = nameAr;
          }
        });
        saveCatalogData(false);
        saveCategoriesData(true);
        showAdminToast(`Category "${nameEn}" updated!`, 'success');
      }
    } else {
      // Add new category
      if (categoriesData.some((c) => c.id === slug)) {
        alert(`Category ID "${slug}" already exists. Please choose a unique ID.`);
        return;
      }

      categoriesData.push({
        id: slug,
        icon: icon,
        en: nameEn,
        ar: nameAr
      });
      saveCategoriesData(true);
      showAdminToast(`New Category "${nameEn}" created!`, 'success');
    }

    closeCategoryModal();
    refreshAllAdminViews();
  }

  function confirmDeleteCategory(catId) {
    const cat = categoriesData.find((c) => c.id === catId);
    if (!cat) return;

    const count = catalogData.filter((x) => x.category_id === catId).length;
    let confirmMsg = `Are you sure you want to delete category "${cat.en}"?`;
    if (count > 0) {
      confirmMsg += `\n\nWarning: ${count} products currently belong to this category. They will be moved to the first available category.`;
    }

    if (!confirm(confirmMsg)) return;

    const fallbackCat = categoriesData.find((c) => c.id !== 'all' && c.id !== catId) || { id: 'general', en: 'General', ar: 'عام' };
    catalogData.forEach((it) => {
      if (it.category_id === catId) {
        it.category_id = fallbackCat.id;
        it.category_en = fallbackCat.en;
        it.category_ar = fallbackCat.ar;
      }
    });

    categoriesData = categoriesData.filter((c) => c.id !== catId);
    saveCatalogData(false);
    saveCategoriesData(true);
    refreshAllAdminViews();
    showAdminToast(`Category deleted and tools reassigned.`, 'success');
  }

  // --- Batch Category Assignment Management ---
  const assignCheckedIds = new Set();

  function renderBatchAssignmentGrid() {
    if (!dom.assignmentGrid) return;
    const search = (dom.assignSearch ? dom.assignSearch.value.trim().toLowerCase() : '');
    const sourceCat = (dom.assignSourceCat ? dom.assignSourceCat.value : 'all');

    const items = catalogData.filter((it) => {
      if (sourceCat !== 'all' && it.category_id !== sourceCat) return false;
      if (search) {
        const mEn = (it.name_en || '').toLowerCase().includes(search);
        const mAr = (it.name_ar || '').toLowerCase().includes(search);
        const mRef = String(it.id).includes(search);
        const mPart = (it.part_number || '').toLowerCase().includes(search);
        if (!mEn && !mAr && !mRef && !mPart) return false;
      }
      return true;
    });

    dom.assignmentGrid.innerHTML = '';
    if (items.length === 0) {
      dom.assignmentGrid.innerHTML = '<div class="admin-empty-table"><p>No items found for category assignment.</p></div>';
      return;
    }

    items.forEach((item) => {
      const isChecked = assignCheckedIds.has(item.id);
      const catObj = categoriesData.find((c) => c.id === item.category_id);
      const catName = catObj ? catObj.en : item.category_id;

      const card = document.createElement('div');
      card.className = `admin-assign-item-card ${isChecked ? 'checked' : ''}`;
      card.innerHTML = `
        <label class="admin-assign-label">
          <input type="checkbox" class="assign-checkbox" data-id="${item.id}" ${isChecked ? 'checked' : ''}>
          <img src="${item.image || 'images/logo.png'}" alt="" loading="lazy">
          <div class="assign-item-text">
            <span class="assign-item-ref">REF #${item.id} • ${item.part_number}</span>
            <div class="assign-item-title">${escapeAdminHtml(item.name_en)}</div>
            <span class="assign-item-current-cat"><i class="fa-solid fa-folder"></i> ${escapeAdminHtml(catName)}</span>
          </div>
        </label>
      `;

      card.querySelector('.assign-checkbox').addEventListener('change', (e) => {
        if (e.target.checked) {
          assignCheckedIds.add(item.id);
        } else {
          assignCheckedIds.delete(item.id);
        }
        card.classList.toggle('checked', e.target.checked);
        updateAssignSelectedCount();
      });

      dom.assignmentGrid.appendChild(card);
    });

    updateAssignSelectedCount();
  }

  function updateAssignSelectedCount() {
    if (dom.assignSelectedCount) {
      dom.assignSelectedCount.textContent = `${assignCheckedIds.size} items checked`;
    }
  }

  function handleApplyBatchCategory() {
    if (assignCheckedIds.size === 0) {
      alert('Please check at least one product to move.');
      return;
    }

    const targetId = dom.targetCatSelect.value;
    const targetObj = categoriesData.find((c) => c.id === targetId);
    if (!targetObj) return;

    catalogData.forEach((it) => {
      if (assignCheckedIds.has(it.id)) {
        it.category_id = targetObj.id;
        it.category_en = targetObj.en;
        it.category_ar = targetObj.ar;
      }
    });

    const movedCount = assignCheckedIds.size;
    assignCheckedIds.clear();
    saveCatalogData(true);
    refreshAllAdminViews();
    showAdminToast(`Successfully moved ${movedCount} products to "${targetObj.en}"!`, 'success');
  }

  // --- Data Export & Import ---
  function downloadCatalogJson() {
    try {
      // Format clean JSON output
      const cleanData = catalogData.map((item) => ({
        id: item.id,
        ref_no: String(item.id),
        part_number: item.part_number,
        name_en: item.name_en,
        name_ar: item.name_ar,
        category_id: item.category_id,
        category_en: item.category_en,
        category_ar: item.category_ar,
        description_en: item.description_en,
        description_ar: item.description_ar,
        image: item.image,
        specs: item.specs || [],
        ...(item.active === false ? { active: false } : {})
      }));

      const jsonStr = JSON.stringify(cleanData, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'catalog.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      showAdminToast('catalog.json downloaded! You can now commit it to your repository.', 'success');
    } catch (e) {
      console.error('Error downloading json:', e);
      showAdminToast('Failed to export catalog.json.', 'error');
    }
  }

  function handleImportJson(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (evt) {
      try {
        const parsed = JSON.parse(evt.target.result);
        if (Array.isArray(parsed) && parsed.length > 0 && parsed[0].name_en) {
          if (confirm(`Import ${parsed.length} products? This will replace your current catalog.`)) {
            catalogData = parsed;
            saveCatalogData(true);
            refreshAllAdminViews();
            showAdminToast(`Imported ${parsed.length} products successfully!`, 'success');
          }
        } else {
          alert('Invalid catalog.json format. Please provide a valid product array.');
        }
      } catch (err) {
        alert('Failed to parse JSON file. Please check file format.');
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  }

  function handleChangePasscode(e) {
    e.preventDefault();
    const newPass = dom.newPassInput.value.trim();
    if (newPass.length < 4) {
      alert('Passcode must be at least 4 characters long.');
      return;
    }
    localStorage.setItem(STORAGE_KEY_PASS, newPass);
    dom.newPassInput.value = '';
    showAdminToast('Admin passcode updated successfully!', 'success');
  }

  function handleResetCatalog() {
    if (confirm('Are you sure you want to reset all catalog changes to the original default catalog.json? This cannot be undone.')) {
      localStorage.removeItem(STORAGE_KEY_CATALOG);
      localStorage.removeItem(STORAGE_KEY_CATEGORIES);
      sessionStorage.removeItem(STORAGE_KEY_AUTH);
      window.location.reload();
    }
  }

  // --- Admin Toast ---
  let adminToastTimer = null;
  function showAdminToast(msg, type = 'info') {
    if (!dom.toast) return;
    dom.toast.textContent = msg;
    dom.toast.className = `admin-toast-message toast-${type}`;
    dom.toast.style.display = 'block';
    clearTimeout(adminToastTimer);
    adminToastTimer = setTimeout(() => {
      dom.toast.style.display = 'none';
    }, 3200);
  }

  // --- Utility ---
  function escapeAdminHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Export public methods for storefront integration
  window.ElmirAdmin = {
    open: openAdminPortal,
    init: initAdmin,
    getCatalogData: () => catalogData,
    getCategoriesData: () => categoriesData
  };

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdmin);
  } else {
    initAdmin();
  }

})();
