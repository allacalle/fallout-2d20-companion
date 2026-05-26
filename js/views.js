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
    const count = (c) => DataManager.getAll(c).length;
    const total = count('weapons') + count('mods') + count('armor') + count('armor-sets') +
      count('armor-mods') + count('clothing') + count('outfits') + count('headgear') +
      count('dog-armor') + count('consumables') + count('perks') + count('skills') +
      count('calibers') + count('robot-mods') + count('robot-armor') + count('misc') +
      count('books');

    const effectCount = Object.values(DataManager.data.effects || {}).reduce((sum, cat) => {
      if (typeof cat === 'object' && !Array.isArray(cat)) return sum + Object.keys(cat).length;
      return sum;
    }, 0);
    const craftingTotal = count('workbenches') + count('chem-recipes') + count('cooking-recipes') + count('power-armor-recipes');
    const weaponsTotal = count('weapons') + count('mods');

    const sections = [
      {
        label: 'Equipment Registry',
        cards: [
          { name: 'Weapons', icon: '⚔️', route: 'weapons', desc: 'Firearms, melee, energy & explosives with modular modifications', stamp: 'restricted' },
          { name: 'Armor', icon: '🛡️', route: 'armor', desc: 'Raider, metal, combat & synth pieces with full set configurations', stamp: 'approved' },
          { name: 'Headgear', icon: '🎩', route: 'headgear', desc: 'Hats, masks & visors for head protection', stamp: 'approved' },
          { name: 'Dog Armor', icon: '🐕', route: 'dog-armor', desc: 'Protective gear for canine companions', stamp: 'approved' },
          { name: 'Robot Mods', icon: '⚡', route: 'robot-mods', desc: 'Upgrade modules for Mister Handy robots', stamp: 'restricted' },
          { name: 'Robot Armor', icon: '⚙️', route: 'robot-armor', desc: 'Plating & frames for robot chassis', stamp: 'restricted' },
          { name: 'Miscellany', icon: '🧰', route: 'misc', desc: 'Tools, backpacks & utility items for the wasteland', stamp: 'common' },
          { name: 'Consumables', icon: '💊', route: 'consumables', desc: 'Chems, foods & drinks — experimental compounds under observation', stamp: 'experimental' },
        ]
      },
      {
        label: 'Personnel File',
        cards: [
          { name: 'Perks', icon: '⭐', route: 'perks', desc: 'Character perks with ranks, attribute requirements & full effect descriptions', stamp: 'approved' },
          { name: 'Skills', icon: '🎯', route: 'skills', desc: 'Core skills organized by governing SPECIAL attribute', stamp: 'approved' },
        ]
      },
      {
        label: 'Workshop',
        cards: [
          { name: 'Crafting', icon: '🔧', route: 'crafting', desc: 'Workbenches, chem/cooking/PA recipes with material costs & complexity', stamp: 'pending' },
          { name: 'Effects', icon: '☢️', route: 'effects', desc: 'Damage types, weapon qualities, chem effects & conditions glossary', stamp: 'restricted' },
        ]
      },
      {
        label: 'Archive',
        cards: [
          { name: 'Books & Magazines', icon: '📚', route: 'books', desc: '20 pre-War publications with issue tables & perks', stamp: 'common' },
        ]
      }
    ];

    const stampHtml = (s) => s ? `<span class="vt-stamp vt-stamp--${s}">${s}</span>` : '';

    const sectionsHtml = sections.map(s => `
      <div class="home-section">
        <div class="home-section-label">${s.label}</div>
        <div class="home-grid">
          ${s.cards.map(c => `
            <a href="#${c.route}" class="home-card">
              <div class="home-card-top">
                <span class="home-card-icon">${c.icon}</span>
                ${stampHtml(c.stamp)}
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
            <span class="home-badge-line"></span>
            VAULT-TEC® INDUSTRIES
            <span class="home-badge-line"></span>
          </div>
          <h1 class="home-title">Database Terminal</h1>
          <p class="home-subtitle">${total} items · 12 databases · ${weaponsTotal} weapons · ${craftingTotal} recipes</p>
        </div>
        ${sectionsHtml}
      </div>
    `;
  },

  tabs(active, items) {
    return `
      <div class="vt-tabs">
        ${items.map(t => `
          <a href="#${t.route}" class="vt-tab ${t.route === active ? 'active' : ''}">
            ${t.label}
            ${t.count !== undefined ? `<span class="vt-tab-count">${t.count}</span>` : ''}
          </a>
        `).join('')}
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
          <th colspan="${columns.length}"><span class="cat-arrow">▶</span> ${group} (${groupItems.length})</th>
        </tr>
        <tr class="category-rows hidden">
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
          <th colspan="${columns.length}"><span class="cat-arrow">▶</span> ${group} (${groupItems.length})</th>
        </tr>
        <tr class="category-rows hidden">
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
          <th colspan="2"><span class="cat-arrow">▶</span> ${category} (${Object.keys(items).length})</th>
        </tr>
        <tr class="category-rows hidden">
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
