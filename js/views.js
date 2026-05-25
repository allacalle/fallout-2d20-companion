const Views = {
  content: null,

  init() {
    this.content = document.getElementById('content');
  },

  render(html) {
    this.content.innerHTML = html;
  },

  backLink(route, params) {
    const p = params && Object.keys(params).length ? params : App.getListState(route);
    const hash = Router.buildHash(route, null, Object.keys(p).length ? p : null);
    return `<a class="back-btn" href="#${hash}">← Back</a>`;
  },

  link(collection, id, text) {
    return `<a class="clickable" href="#${collection}/${id}">${text}</a>`;
  },

  badge(text, cls = '') {
    return `<span class="badge ${cls}">${text}</span>`;
  },

  fmt(val) {
    if (val === undefined || val === null || val === '') return '—';
    if (Array.isArray(val)) return val.join(', ');
    if (typeof val === 'object') return JSON.stringify(val);
    return String(val);
  },

  home() {
    const total = [
      DataManager.getAll('weapons').length,
      DataManager.getAll('mods').length,
      DataManager.getAll('armor').length,
      DataManager.getAll('armor-sets').length,
      DataManager.getAll('armor-mods').length,
      DataManager.getAll('clothing').length,
      DataManager.getAll('outfits').length,
      DataManager.getAll('consumables').length,
      DataManager.getAll('perks').length,
      DataManager.getAll('skills').length,
      DataManager.getAll('calibers').length,
    ].reduce((a, b) => a + b, 0);

    const wCount = DataManager.getAll('weapons').length;
    const mCount = DataManager.getAll('mods').length;
    const aCount = DataManager.getAll('armor').length;
    const asCount = DataManager.getAll('armor-sets').length;
    const amCount = DataManager.getAll('armor-mods').length;
    const cCount = DataManager.getAll('clothing').length;
    const oCount = DataManager.getAll('outfits').length;
    const coCount = DataManager.getAll('consumables').length;
    const pCount = DataManager.getAll('perks').length;
    const sCount = DataManager.getAll('skills').length;
    const caCount = DataManager.getAll('calibers').length;

    const effectCount = Object.values(DataManager.data.effects || {}).reduce((sum, cat) => {
      if (typeof cat === 'object' && !Array.isArray(cat)) return sum + Object.keys(cat).length;
      return sum;
    }, 0);
    const craftingTotal = (DataManager.getAll('workbenches')?.length || 0) +
      (DataManager.getAll('chem-recipes')?.length || 0) +
      (DataManager.getAll('cooking-recipes')?.length || 0) +
      (DataManager.getAll('power-armor-recipes')?.length || 0);

    const sections = [
      {
        label: 'Combat',
        cards: [
          { name: 'Weapons', count: wCount, route: 'weapons', desc: 'Firearms, melee, energy & explosives' },
          { name: 'Weapon Mods', count: mCount, route: 'mods', desc: 'Barrels, grips, scopes & receivers' },
          { name: 'Calibers', count: caCount, route: 'calibers', desc: 'Ammunition types with rarity & cost' },
        ]
      },
      {
        label: 'Protection',
        cards: [
          { name: 'Armor', count: aCount, route: 'armor', desc: 'Raider, metal, combat & synth pieces' },
          { name: 'Armor Sets', count: asCount, route: 'armor-sets', desc: 'Complete configured armor sets' },
          { name: 'Armor Mods', count: amCount, route: 'armor-mods', desc: 'Ballistic weave, plating & utility' },
          { name: 'Clothing', count: cCount, route: 'clothing', desc: 'Base garments for under-armor wear' },
          { name: 'Outfits', count: oCount, route: 'outfits', desc: 'All-in-one outfits for any occasion' },
        ]
      },
      {
        label: 'Resources',
        cards: [
          { name: 'Consumables', count: coCount, route: 'consumables', desc: 'Chems, foods & drinks with effects' },
          { name: 'Perks', count: pCount, route: 'perks', desc: 'Perks with ranks, requirements & effects' },
          { name: 'Skills', count: sCount, route: 'skills', desc: 'Skills with associated attributes' },
        ]
      },
      {
        label: 'Workshop',
        cards: [
          { name: 'Crafting', count: craftingTotal, route: 'crafting', desc: 'Workbenches, recipes & material costs' },
          { name: 'Effects', count: effectCount, route: 'effects', desc: 'Damage types, qualities, chem effects' },
        ]
      }
    ];

    const sectionsHtml = sections.map(s => `
      <div class="home-section">
        <div class="home-section-label">${s.label}</div>
        <div class="home-grid">
          ${s.cards.map(c => `
            <a href="#${c.route}" class="home-card">
              <div class="home-card-top">
                <span class="home-card-count">${c.count}</span>
              </div>
              <div class="home-card-name">${c.name}</div>
              <div class="home-card-desc">${c.desc}</div>
            </a>
          `).join('')}
        </div>
      </div>
    `).join('');

    return `
      <div class="home-page">
        <div class="home-hero">
          <div class="home-badge">
            <span class="home-badge-line">—</span>
            VAULT-TEC® INDUSTRIES
            <span class="home-badge-line">—</span>
          </div>
          <h1 class="home-title">Wasteland<br>Reference Terminal</h1>
          <p class="home-subtitle">Fallout 2d20 RPG — ${total} indexed items across 12 databases</p>
          <div class="home-specs">
            <div class="home-spec"><span class="home-spec-val">${total}</span><span class="home-spec-lbl">Entries</span></div>
            <div class="home-spec"><span class="home-spec-val">12</span><span class="home-spec-lbl">Categories</span></div>
            <div class="home-spec"><span class="home-spec-val">${DataManager.getAll('weapons').length + DataManager.getAll('mods').length}</span><span class="home-spec-lbl">Weapons</span></div>
            <div class="home-spec"><span class="home-spec-val">${DataManager.getAll('consumables').length}</span><span class="home-spec-lbl">Consumables</span></div>
          </div>
        </div>
        ${sectionsHtml}
      </div>
    `;
  },

  table(collection, title, columns, groupBy = null) {
    const items = DataManager.getAll(collection);
    if (!items.length) return `<h2>${title}</h2><p>No data available.</p>`;

    let html = `<h2>${title} (${items.length})</h2>`;

    if (groupBy) {
      const groups = {};
      items.forEach(item => {
        const key = item[groupBy] || 'Other';
        if (!groups[key]) groups[key] = [];
        groups[key].push(item);
      });

      Object.entries(groups).sort().forEach(([group, groupItems]) => {
        html += `
          <table>
            <tr class="category-header" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('hidden');">
              <th colspan="${columns.length}">${group} (${groupItems.length})</th>
            </tr>
            <tr class="category-rows">
              <td colspan="${columns.length}">
                <table>
                  <thead><tr>${columns.map(c => `<th>${c.label}</th>`).join('')}</tr></thead>
                  <tbody>
                    ${groupItems.map(item => `<tr>${columns.map(c => `<td>${c.render ? c.render(item[c.key], item) : this.fmt(item[c.key])}</td>`).join('')}</tr>`).join('')}
                  </tbody>
                </table>
              </td>
            </tr>
          </table>
        `;
      });
    } else {
      html += `
        <table>
          <thead><tr>${columns.map(c => `<th>${c.label}</th>`).join('')}</tr></thead>
          <tbody>
            ${items.map(item => `<tr>${columns.map(c => `<td>${c.render ? c.render(item[c.key], item) : this.fmt(item[c.key])}</td>`).join('')}</tr>`).join('')}
          </tbody>
        </table>
      `;
    }

    return html;
  },

  groupedTable(items, title, columns, groupFn) {
    if (!items.length) return `<h2>${title}</h2><p>No data available.</p>`;

    const groups = {};
    items.forEach(item => {
      const key = typeof groupFn === 'function' ? groupFn(item) : item[groupFn];
      const group = key || 'Other';
      if (!groups[group]) groups[group] = [];
      groups[group].push(item);
    });

    let html = `<h2>${title} (${items.length})</h2>`;
    const sortedGroups = Object.keys(groups).sort();

    sortedGroups.forEach(group => {
      const groupItems = groups[group];
      html += `
        <table>
          <tr class="category-header" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('hidden');">
            <th colspan="${columns.length}">${group} (${groupItems.length})</th>
          </tr>
          <tr class="category-rows">
            <td colspan="${columns.length}">
              <table>
                <thead><tr>${columns.map(c => `<th>${c.label}</th>`).join('')}</tr></thead>
                <tbody>
                  ${groupItems.map(item => `<tr>${columns.map(c => `<td>${c.render ? c.render(item[c.key] !== undefined ? item[c.key] : item, item) : this.fmt(item[c.key])}</td>`).join('')}</tr>`).join('')}
                </tbody>
              </table>
            </td>
          </tr>
        </table>
      `;
    });

    return html;
  },

  detail(collection, id, fields) {
    const item = DataManager.getById(collection, id);
    if (!item) return `<h2>Not Found</h2><p>${id} not found.</p>`;

    let html = `
      ${this.backLink(collection)}
      <div class="detail-view">
        <h2>${item.name || id}</h2>
    `;

    fields.forEach(f => {
      const raw = item[f.key];
      if (raw === undefined || raw === null || raw === '') return;
      const display = f.render ? f.render(raw, item) : this.fmt(raw);
      html += `<div class="field"><span class="label">${f.label}:</span> <span class="value">${display}</span></div>`;
    });

    html += `</div>`;
    return html;
  },

  effectsGlossary() {
    const effects = DataManager.data.effects || {};
    let html = `<h2>Effects Glossary</h2>`;

    Object.entries(effects).forEach(([category, items]) => {
      if (typeof items !== 'object' || Array.isArray(items)) return;

      html += `
        <table>
          <tr class="category-header" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('hidden');">
            <th colspan="2">${category} (${Object.keys(items).length})</th>
          </tr>
          <tr class="category-rows">
            <td colspan="2">
              <table>
                <thead><tr><th>Name</th><th>Description</th></tr></thead>
                <tbody>
                  ${Object.entries(items).map(([name, effect]) => `
                    <tr>
                      <td><a class="clickable" href="#effects/${category}/${encodeURIComponent(name)}">${effect.name || name}</a></td>
                      <td>${effect.description || '—'}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </td>
          </tr>
        </table>
      `;
    });

    return html;
  },

  effectDetail(category, effectName) {
    const cat = DataManager.data.effects?.[category];
    if (!cat) return `<h2>Not Found</h2><p>Category "${category}" not found.</p>`;
    const effect = cat[effectName];
    if (!effect) return `<h2>Not Found</h2><p>Effect "${effectName}" not found.</p>`;

    return `
      ${this.backLink('effects')}
      <div class="detail-view">
        <h2>${effect.name || effectName}</h2>
        <div class="field"><span class="label">Category:</span> <span class="value">${category}</span></div>
        <div class="field"><span class="label">Description:</span> <span class="value">${effect.description || '—'}</span></div>
      </div>
    `;
  },

  // ===== FILTER & SORT HELPERS =====

  filterBar(fields, current) {
    let html = `<div class="filter-bar">`;
    fields.forEach(f => {
      if (!f.options || f.key.startsWith('_')) return;
      const val = current[f.key] || '';
      html += `<span class="filter-group">
        <label class="filter-label">${f.label}</label>
        <select class="filter-select" data-filter="${f.key}" onchange="App.setFilter('${f.key}', this.value)">
          <option value="">All</option>
          ${f.options.map(o => {
            const optVal = o.value !== undefined ? o.value : o;
            const optLabel = o.label !== undefined ? o.label : o;
            const sel = String(optVal) === String(val) ? ' selected' : '';
            return `<option value="${optVal}"${sel}>${optLabel}</option>`;
          }).join('')}
        </select>
      </span>`;
    });

    const currentSort = current.sort || '';
    const currentOrder = current.order || 'asc';
    html += `<span class="filter-group filter-sort">
      <label class="filter-label">Sort</label>
      <select class="filter-select" data-filter="sort" onchange="App.setFilter('sort', this.value)">
        <option value="">—</option>
        ${(fields.find(f => f.key === '_sort')?.options || []).map(o => {
          const optVal = o.value !== undefined ? o.value : o;
          const optLabel = o.label !== undefined ? o.label : o;
          const sel = String(optVal) === currentSort ? ' selected' : '';
          return `<option value="${optVal}"${sel}>${optLabel}</option>`;
        }).join('')}
      </select>
      <button class="sort-order-btn" onclick="App.toggleSortOrder()" title="Toggle sort order">
        ${currentOrder === 'asc' ? '↑' : '↓'}
      </button>
    </span>`;

    const hasFilters = Object.values(current).some(v => v !== '' && v !== undefined);
    if (hasFilters) {
      html += `<button class="filter-clear" onclick="App.clearFilters()">✕ Clear</button>`;
    }

    html += `</div>`;
    return html;
  },

  applyFilters(items, params, filterConfig) {
    if (!items.length) return items;
    let filtered = [...items];

    filterConfig.forEach(f => {
      if (f.key.startsWith('_')) return;
      const val = params[f.key];
      if (!val || val === '') return;

      if (f.filter) {
        filtered = filtered.filter(item => f.filter(item, val));
      } else {
        filtered = filtered.filter(item => {
          const itemVal = item[f.key];
          return String(itemVal) === String(val);
        });
      }
    });

    return filtered;
  },

  applySort(items, sortKey, order) {
    if (!sortKey || sortKey === '') return items;
    const dir = order === 'desc' ? -1 : 1;

    return [...items].sort((a, b) => {
      let va = a[sortKey];
      let vb = b[sortKey];

      if (typeof va === 'string' && typeof vb === 'string') {
        return dir * va.localeCompare(vb);
      }
      if (typeof va === 'number' && typeof vb === 'number') {
        return dir * (va - vb);
      }
      return 0;
    });
  },

  uniqueOptions(items, key, transform) {
    const set = new Set();
    items.forEach(item => {
      const val = item[key];
      if (val !== undefined && val !== null) {
        if (Array.isArray(val)) {
          val.forEach(v => set.add(typeof v === 'object' ? JSON.stringify(v) : v));
        } else {
          set.add(val);
        }
      }
    });
    return Array.from(set).sort().map(v => {
      const label = transform ? transform(v) : v;
      return { value: v, label };
    });
  }
};
