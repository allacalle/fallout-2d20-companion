const App = {
  async init() {
    Views.init();

    try {
      await DataManager.loadAll();
      document.getElementById('loading').style.display = 'none';
    } catch (err) {
      document.getElementById('loading').innerHTML = `Error: ${err.message}`;
      return;
    }

    this.setupRoutes();
    this.setupSearch();
    this.setupMenu();
    this.setupHomeBtn();
    Router.init();
  },

  // Helper: resolve mod by ID and return formatted card
  modCard(modId, collection = 'mods') {
    const mod = DataManager.getById(collection, modId);
    if (!mod) return `<span class="clickable">${modId}</span>`;

    const perks = (mod.perksRequired || []).map(p => `${p.perkId} R${p.rank}`).join(', ') || 'None';
    const effects = mod.effects || '—';
    const cost = mod.costChange !== undefined ? `+${mod.costChange}` : (mod.cost || '—');
    const complexity = mod.complexity || '—';
    const rarity = mod.rarity || '—';
    const skill = mod.skill ? Views.link('skills', mod.skill, mod.skill) : '—';

    return `
      <div class="mod-card">
        <div class="mod-card-header">
          <a class="clickable" href="#${collection}/${mod.id}">${mod.name}</a>
          <span class="badge">${rarity}</span>
        </div>
        <div class="mod-card-body">
          <div><strong>Effects:</strong> ${effects}</div>
          <div><strong>Complexity:</strong> ${complexity} | <strong>Cost:</strong> ${cost} caps | <strong>Skill:</strong> ${skill}</div>
          <div><strong>Perks:</strong> ${perks}</div>
          ${mod.weightChange ? `<div><strong>Weight:</strong> ${mod.weightChange > 0 ? '+' : ''}${mod.weightChange} lbs</div>` : ''}
        </div>
      </div>
    `;
  },

  // Helper: render all mods for a weapon grouped by part
  weaponModsInline(weapon) {
    if (!weapon.parts) return '—';
    let html = '';
    Object.entries(weapon.parts).forEach(([part, modIds]) => {
      html += `<h4 class="mod-part-title">${part}</h4>`;
      html += `<div class="mod-grid">`;
      modIds.forEach(modId => {
        html += this.modCard(modId, 'mods');
      });
      html += `</div>`;
    });
    return html;
  },

  // Helper: render all compatible armor mods
  armorModsInline(armor) {
    if (!armor.compatibleMods) return '—';
    let html = '';
    if (Array.isArray(armor.compatibleMods)) {
      html += `<div class="mod-grid">`;
      armor.compatibleMods.forEach(modId => {
        html += this.modCard(modId, 'armor-mods');
      });
      html += `</div>`;
    } else {
      Object.entries(armor.compatibleMods).forEach(([type, modIds]) => {
        html += `<h4 class="mod-part-title">${type}</h4>`;
        html += `<div class="mod-grid">`;
        modIds.forEach(modId => {
          html += this.modCard(modId, 'armor-mods');
        });
        html += `</div>`;
      });
    }
    return html;
  },

  // ===== FILTER STATE MANAGEMENT =====

  saveListState(route, params) {
    const clean = Object.fromEntries(Object.entries(params || {}).filter(([, v]) => v));
    if (Object.keys(clean).length) {
      sessionStorage.setItem(`fl_${route}`, JSON.stringify(clean));
    } else {
      sessionStorage.removeItem(`fl_${route}`);
    }
  },

  getListState(route) {
    try {
      return JSON.parse(sessionStorage.getItem(`fl_${route}`) || '{}');
    } catch { return {}; }
  },

  setFilter(key, value) {
    const params = { ...Router.params };
    if (value === '' || value === null) {
      delete params[key];
    } else {
      params[key] = value;
    }
    const { route, id } = Router.currentRoute || {};
    const baseRoute = route || 'home';
    const newHash = Router.buildHash(baseRoute, id, params);
    window.location.hash = newHash;
  },

  toggleSortOrder() {
    const current = Router.params.order || 'asc';
    this.setFilter('order', current === 'asc' ? 'desc' : 'asc');
  },

  clearFilters() {
    const { route, id } = Router.currentRoute || {};
    window.location.hash = route || 'home';
  },

  rarityLabel(r) {
    const labels = ['Common', 'Uncommon', 'Rare', 'Very Rare', 'Legendary', 'Unique'];
    return labels[r] || r;
  },

  repairMaterials(rarity) {
    const table = DataManager.data.components?.repairTable || [];
    const r = Number(rarity);
    const entry = table.find(e => {
      const v = e.rarity;
      if (v.endsWith('+')) return r >= Number(v);
      if (v.includes('-')) { const [lo, hi] = v.split('-'); return r >= Number(lo) && r <= Number(hi); }
      return String(r) === v;
    });
    return entry ? entry.materials : '—';
  },

  setupRoutes() {
    Router.register('home', () => {
      Views.render(Views.home());
    });

    // ===== WEAPONS =====
    const weaponTabs = () => Views.tabs(Router.currentRoute?.route || 'weapons', [
      { label: 'Weapons', route: 'weapons', count: DataManager.getAll('weapons').length },
      { label: 'Mods', route: 'mods', count: DataManager.getAll('mods').length },
      { label: 'Calibers', route: 'calibers', count: DataManager.getAll('calibers').length },
    ]);

    const armorTabs = () => Views.tabs(Router.currentRoute?.route || 'armor', [
      { label: 'Armor', route: 'armor', count: DataManager.getAll('armor').length },
      { label: 'Sets', route: 'armor-sets', count: DataManager.getAll('armor-sets').length },
      { label: 'Mods', route: 'armor-mods', count: DataManager.getAll('armor-mods').length },
      { label: 'Clothing', route: 'clothing', count: DataManager.getAll('clothing').length },
      { label: 'Outfits', route: 'outfits', count: DataManager.getAll('outfits').length },
      { label: 'Headgear', route: 'headgear', count: DataManager.getAll('headgear').length },
      { label: 'Dog Armor', route: 'dog-armor', count: DataManager.getAll('dog-armor').length },
    ]);

    Router.register('weapons', (id, params) => {
      if (id) {
        const w = DataManager.getById('weapons', id);
        if (!w) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('weapons', params)}
          ${weaponTabs()}
          <div class="detail-view">
            <h2>${w.name}</h2>
            <div class="field"><span class="label">Type:</span> <span class="value">${w.weaponType}</span></div>
            <div class="field"><span class="label">Skill:</span> <span class="value">${Views.link('skills', w.skillId, w.skillId)}</span></div>
            <div class="field"><span class="label">Damage:</span> <span class="value">${w.damage}</span></div>
            <div class="field"><span class="label">Damage Type:</span> <span class="value">${w.damageType}</span></div>
            <div class="field"><span class="label">Range:</span> <span class="value">${w.range}</span></div>
            <div class="field"><span class="label">Fire Rate:</span> <span class="value">${w.fireRate}</span></div>
            <div class="field"><span class="label">Ammo:</span> <span class="value">${Views.link('calibers', w.ammo, w.ammo)}</span></div>
            <div class="field"><span class="label">Qualities:</span> <span class="value">${(w.qualities || []).map(q => `<a class="clickable" href="#effects/qualities/${encodeURIComponent(q)}">${q}</a>`).join(', ') || '—'}</span></div>
            <div class="field"><span class="label">Damage Effects:</span> <span class="value">${(w.damageEffects || []).map(e => `<a class="clickable" href="#effects/damageEffects/${encodeURIComponent(e)}">${e}</a>`).join(', ') || '—'}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${w.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${w.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${w.rarity}</span></div>
            <div class="field"><span class="label">Description:</span> <span class="value">${w.description || '—'}</span></div>
          </div>
          <h3>Compatible Mods</h3>
          ${this.weaponModsInline(w)}
        `);
      } else {
        const all = DataManager.getAll('weapons');
        const weaponFilterConfig = [
          { key: 'weaponType', label: 'Type' },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'rarity', label: 'Rarity' },
            { value: 'fireRate', label: 'Fire Rate' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, weaponFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        const typeOptions = Views.uniqueOptions(all, 'weaponType');
        weaponFilterConfig[0].options = typeOptions;
        App.saveListState('weapons', params);
        Views.render(`
          ${weaponTabs()}
          ${Views.filterBar(weaponFilterConfig, params, 'weapons')}
          ${Views.groupedTable(sorted, 'Weapons', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('weapons', i.id, v) },
            { label: 'Damage', key: 'damage' },
            { label: 'Range', key: 'range' },
            { label: 'Ammo', key: 'ammo', render: (v) => Views.link('calibers', v, v) },
            { label: 'Qualities', key: 'qualities' },
            { label: 'FR', key: 'fireRate' },
            { label: 'Weight', key: 'weight' },
            { label: 'Cost', key: 'cost' },
          ], item => item.weaponType)}
        `);
      }
    });

    // ===== WEAPON MODS =====
    Router.register('mods', (id, params) => {
      if (id) {
        const m = DataManager.getById('mods', id);
        if (!m) { Views.render(`<h2>Not Found</h2>`); return; }
        const perks = (m.perksRequired || []).map(p => Views.link('perks', p.perkId, `${p.perkId} R${p.rank}`)).join(', ');
        const compatibleWeapons = DataManager.getAll('weapons').filter(w => {
          if (!w.parts) return false;
          return Object.values(w.parts).some(arr => arr.includes(id));
        });

        Views.render(`
          ${Views.backLink('mods', params)}
          <div class="detail-view">
            <h2>${m.name}</h2>
            <div class="field"><span class="label">Part Type:</span> <span class="value">${m.partType}</span></div>
            <div class="field"><span class="label">Weapon Types:</span> <span class="value">${(m.weaponTypes || []).join(', ')}</span></div>
            <div class="field"><span class="label">Effects:</span> <span class="value">${m.effects}</span></div>
            <div class="field"><span class="label">Weight Change:</span> <span class="value">${m.weightChange > 0 ? '+' : ''}${m.weightChange} lbs</span></div>
            <div class="field"><span class="label">Cost Change:</span> <span class="value">+${m.costChange} caps</span></div>
            <div class="field"><span class="label">Skill:</span> <span class="value">${m.skill ? Views.link('skills', m.skill, m.skill) : '—'}</span></div>
            <div class="field"><span class="label">Complexity:</span> <span class="value">${m.complexity}</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${m.rarity}</span></div>
            <div class="field"><span class="label">Repair Materials:</span> <span class="value">${this.repairMaterials(m.rarity)}</span></div>
            <div class="field"><span class="label">Required Perks:</span> <span class="value">${perks || '—'}</span></div>
            <div class="field"><span class="label">Compatible Weapons:</span> <span class="value">${compatibleWeapons.length ? compatibleWeapons.map(w => Views.link('weapons', w.id, w.name)).join(', ') : 'Check weapon parts'}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('mods');
        const modFilterConfig = [
          { key: 'partType', label: 'Part' },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'costChange', label: 'Cost' },
            { value: 'complexity', label: 'Complexity' },
            { value: 'rarity', label: 'Rarity' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, modFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        modFilterConfig[0].options = Views.uniqueOptions(all, 'partType');
        App.saveListState('mods', params);
        Views.render(`
          ${weaponTabs()}
          ${Views.filterBar(modFilterConfig, params, 'mods')}
          ${Views.groupedTable(sorted, 'Weapon Mods', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('mods', i.id, v) },
            { label: 'Weapon Types', key: 'weaponTypes' },
            { label: 'Effects', key: 'effects' },
            { label: 'Skill', key: 'skill', render: (v) => v ? Views.link('skills', v, v) : '—' },
            { label: 'Complexity', key: 'complexity' },
            { label: 'Rarity', key: 'rarity' },
            { label: 'Cost', key: 'costChange', render: (v) => `+${v}` },
          ], item => item.partType)}
        `);
      }
    });

    // ===== ARMOR =====
    Router.register('armor', (id, params) => {
      if (id) {
        const a = DataManager.getById('armor', id);
        if (!a) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('armor', params)}
          <div class="detail-view">
            <h2>${a.name}</h2>
            <div class="field"><span class="label">Class:</span> <span class="value">${a.armorClass}</span></div>
            <div class="field"><span class="label">Piece:</span> <span class="value">${a.piece}</span></div>
            <div class="field"><span class="label">Variant:</span> <span class="value">${a.variant}</span></div>
            <div class="field"><span class="label">Covers:</span> <span class="value">${(a.covers || []).join(', ')}</span></div>
            <div class="field"><span class="label">Physical DR:</span> <span class="value">${a.physicalDR}</span></div>
            <div class="field"><span class="label">Energy DR:</span> <span class="value">${a.energyDR}</span></div>
            <div class="field"><span class="label">Radiation DR:</span> <span class="value">${a.radiationDR}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${a.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${a.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${a.rarity}</span></div>
            <div class="field"><span class="label">Under Armor:</span> <span class="value">${a.underArmor ? 'Yes' : 'No'}</span></div>
          </div>
          <h3>Compatible Mods</h3>
          ${this.armorModsInline(a)}
        `);
      } else {
        const all = DataManager.getAll('armor');
        const armorFilterConfig = [
          { key: 'armorClass', label: 'Class' },
          { key: 'piece', label: 'Piece' },
          { key: 'variant', label: 'Variant' },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: 'underArmor', label: 'Under Armor', options: [
            { value: 'true', label: 'Yes' },
            { value: 'false', label: 'No' },
          ], filter: (item, val) => String(item.underArmor) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'physicalDR', label: 'Phys DR' },
            { value: 'energyDR', label: 'Energy DR' },
            { value: 'rarity', label: 'Rarity' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, armorFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        armorFilterConfig[0].options = Views.uniqueOptions(all, 'armorClass');
        armorFilterConfig[1].options = Views.uniqueOptions(all, 'piece');
        armorFilterConfig[2].options = Views.uniqueOptions(all, 'variant');
        App.saveListState('armor', params);
        Views.render(`
          ${armorTabs()}
          ${Views.filterBar(armorFilterConfig, params, 'armor')}
          ${Views.groupedTable(sorted, 'Armor Pieces', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('armor', i.id, v) },
            { label: 'Piece', key: 'piece' },
            { label: 'Variant', key: 'variant' },
            { label: 'Covers', key: 'covers' },
            { label: 'Phys', key: 'physicalDR' },
            { label: 'Energy', key: 'energyDR' },
            { label: 'Rad', key: 'radiationDR' },
            { label: 'Wt', key: 'weight' },
            { label: 'Cost', key: 'cost' },
          ], item => item.armorClass)}
        `);
      }
    });

    // ===== ARMOR SETS =====
    Router.register('armor-sets', (id, params) => {
      if (id) {
        const s = DataManager.getById('armor-sets', id);
        if (!s) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('armor-sets', params)}
          <div class="detail-view">
            <h2>${s.name}</h2>
            <div class="field"><span class="label">Class:</span> <span class="value">${s.armorClass}</span></div>
            <div class="field"><span class="label">Variant:</span> <span class="value">${s.variant}</span></div>
            <div class="field"><span class="label">Pieces:</span> <span class="value">${(s.pieces || []).map(p => Views.link('armor', p, p)).join(', ')}</span></div>
            <div class="field"><span class="label">Total Weight:</span> <span class="value">${s.totalWeight} lbs</span></div>
            <div class="field"><span class="label">Total Cost:</span> <span class="value">${s.totalCost} caps</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('armor-sets');
        const asFilterConfig = [
          { key: 'armorClass', label: 'Class' },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'totalCost', label: 'Cost' },
            { value: 'totalWeight', label: 'Weight' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, asFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        asFilterConfig[0].options = Views.uniqueOptions(all, 'armorClass');
        App.saveListState('armor-sets', params);
        Views.render(`
          ${armorTabs()}
          ${Views.filterBar(asFilterConfig, params, 'armor-sets')}
          ${Views.groupedTable(sorted, 'Armor Sets', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('armor-sets', i.id, v) },
            { label: 'Variant', key: 'variant' },
            { label: 'Pieces', key: 'pieces' },
            { label: 'Weight', key: 'totalWeight' },
            { label: 'Cost', key: 'totalCost' },
          ], item => item.armorClass)}
        `);
      }
    });

    // ===== ARMOR MODS =====
    Router.register('armor-mods', (id, params) => {
      if (id) {
        const m = DataManager.getById('armor-mods', id);
        if (!m) { Views.render(`<h2>Not Found</h2>`); return; }
        const perks = (m.perksRequired || []).map(p => Views.link('perks', p.perkId, `${p.perkId} R${p.rank}`)).join(', ');

        Views.render(`
          ${Views.backLink('armor-mods', params)}
          <div class="detail-view">
            <h2>${m.name}</h2>
            <div class="field"><span class="label">Type:</span> <span class="value">${m.type}</span></div>
            <div class="field"><span class="label">Armor Types:</span> <span class="value">${(m.armorType || []).join(', ')}</span></div>
            <div class="field"><span class="label">Effects:</span> <span class="value">${m.effects}</span></div>
            <div class="field"><span class="label">Weight Change:</span> <span class="value">${m.weightChange > 0 ? '+' : ''}${m.weightChange} lbs</span></div>
            <div class="field"><span class="label">Cost Change:</span> <span class="value">+${m.costChange} caps</span></div>
            <div class="field"><span class="label">Skill:</span> <span class="value">${m.skill ? Views.link('skills', m.skill, m.skill) : '—'}</span></div>
            <div class="field"><span class="label">Complexity:</span> <span class="value">${m.complexity}</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${m.rarity}</span></div>
            <div class="field"><span class="label">Repair Materials:</span> <span class="value">${this.repairMaterials(m.rarity)}</span></div>
            <div class="field"><span class="label">Required Perks:</span> <span class="value">${perks || '—'}</span></div>
            ${m.locationRestriction ? `<div class="field"><span class="label">Location:</span> <span class="value">${m.locationRestriction} only</span></div>` : ''}
          </div>
        `);
      } else {
        const all = DataManager.getAll('armor-mods');
        const amFilterConfig = [
          { key: 'type', label: 'Type' },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'costChange', label: 'Cost' },
            { value: 'complexity', label: 'Complexity' },
            { value: 'rarity', label: 'Rarity' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, amFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        amFilterConfig[0].options = Views.uniqueOptions(all, 'type');
        App.saveListState('armor-mods', params);
        Views.render(`
          ${armorTabs()}
          ${Views.filterBar(amFilterConfig, params, 'armor-mods')}
          ${Views.groupedTable(sorted, 'Armor Mods', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('armor-mods', i.id, v) },
            { label: 'Armor Types', key: 'armorType' },
            { label: 'Effects', key: 'effects' },
            { label: 'Skill', key: 'skill', render: (v) => v ? Views.link('skills', v, v) : '—' },
            { label: 'Complexity', key: 'complexity' },
            { label: 'Rarity', key: 'rarity' },
            { label: 'Cost', key: 'costChange', render: (v) => `+${v}` },
          ], item => item.type)}
        `);
      }
    });

    // ===== CLOTHING =====
    Router.register('clothing', (id, params) => {
      if (id) {
        const c = DataManager.getById('clothing', id);
        if (!c) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('clothing', params)}
          <div class="detail-view">
            <h2>${c.name}</h2>
            <div class="field"><span class="label">Covers:</span> <span class="value">${(c.covers || []).join(', ')}</span></div>
            <div class="field"><span class="label">Physical DR:</span> <span class="value">${c.physicalDR}</span></div>
            <div class="field"><span class="label">Energy DR:</span> <span class="value">${c.energyDR}</span></div>
            <div class="field"><span class="label">Radiation DR:</span> <span class="value">${c.radiationDR}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${c.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${c.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${c.rarity}</span></div>
            <div class="field"><span class="label">Under Armor:</span> <span class="value">${c.underArmor ? 'Yes' : 'No'}</span></div>
            <div class="field"><span class="label">Compatible Mods:</span> <span class="value">${(c.compatibleMods || []).map(m => Views.link('armor-mods', m, m)).join(', ') || '—'}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('clothing');
        const clothingFilterConfig = [
          { key: 'underArmor', label: 'Type', options: [
            { value: 'true', label: 'Under Armor' },
            { value: 'false', label: 'Outerwear' },
          ], filter: (item, val) => String(item.underArmor) === val },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'physicalDR', label: 'Phys DR' },
            { value: 'energyDR', label: 'Energy DR' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, clothingFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('clothing', params);
        Views.render(`
          ${armorTabs()}
          ${Views.filterBar(clothingFilterConfig, params, 'clothing')}
          ${Views.groupedTable(sorted, 'Clothing', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('clothing', i.id, v) },
            { label: 'Covers', key: 'covers' },
            { label: 'Phys', key: 'physicalDR' },
            { label: 'Energy', key: 'energyDR' },
            { label: 'Rad', key: 'radiationDR' },
            { label: 'Weight', key: 'weight' },
            { label: 'Cost', key: 'cost' },
          ], item => item.underArmor ? 'Under Armor' : 'Outerwear')}
        `);
      }
    });

    // ===== OUTFITS =====
    Router.register('outfits', (id, params) => {
      if (id) {
        const o = DataManager.getById('outfits', id);
        if (!o) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('outfits', params)}
          <div class="detail-view">
            <h2>${o.name}</h2>
            <div class="field"><span class="label">Covers:</span> <span class="value">${(o.covers || []).join(', ')}</span></div>
            <div class="field"><span class="label">Physical DR:</span> <span class="value">${o.physicalDR}</span></div>
            <div class="field"><span class="label">Energy DR:</span> <span class="value">${o.energyDR}</span></div>
            <div class="field"><span class="label">Radiation DR:</span> <span class="value">${o.radiationDR}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${o.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${o.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${o.rarity}</span></div>
            <div class="field"><span class="label">Under Armor:</span> <span class="value">${o.underArmor ? 'Yes' : 'No'}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('outfits');
        const outfitsFilterConfig = [
          { key: 'underArmor', label: 'Type', options: [
            { value: 'true', label: 'Under Armor' },
            { value: 'false', label: 'Outerwear' },
          ], filter: (item, val) => String(item.underArmor) === val },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'physicalDR', label: 'Phys DR' },
            { value: 'energyDR', label: 'Energy DR' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, outfitsFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('outfits', params);
        Views.render(`
          ${armorTabs()}
          ${Views.filterBar(outfitsFilterConfig, params, 'outfits')}
          ${Views.groupedTable(sorted, 'Outfits', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('outfits', i.id, v) },
            { label: 'Covers', key: 'covers' },
            { label: 'Phys', key: 'physicalDR' },
            { label: 'Energy', key: 'energyDR' },
            { label: 'Rad', key: 'radiationDR' },
            { label: 'Weight', key: 'weight' },
            { label: 'Cost', key: 'cost' },
          ], item => item.underArmor ? 'Under Armor' : 'Outerwear')}
        `);
      }
    });

    // ===== HEADGEAR =====
    Router.register('headgear', (id, params) => {
      if (id) {
        const h = DataManager.getById('headgear', id);
        if (!h) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('headgear', params)}
          ${armorTabs()}
          <div class="detail-view">
            <h2>${h.name}</h2>
            <div class="field"><span class="label">Covers:</span> <span class="value">${(h.covers || []).join(', ')}</span></div>
            <div class="field"><span class="label">Physical DR:</span> <span class="value">${h.physicalDR}</span></div>
            <div class="field"><span class="label">Energy DR:</span> <span class="value">${h.energyDR}</span></div>
            <div class="field"><span class="label">Radiation DR:</span> <span class="value">${h.radiationDR}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${h.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${h.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${h.rarity}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('headgear');
        const headgearFilterConfig = [
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'physicalDR', label: 'Phys DR' },
            { value: 'energyDR', label: 'Energy DR' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, headgearFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('headgear', params);
        Views.render(`
          ${armorTabs()}
          ${Views.filterBar(headgearFilterConfig, params, 'headgear')}
          ${Views.groupedTable(sorted, 'Headgear', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('headgear', i.id, v) },
            { label: 'Phys', key: 'physicalDR' },
            { label: 'Energy', key: 'energyDR' },
            { label: 'Rad', key: 'radiationDR' },
            { label: 'Weight', key: 'weight' },
            { label: 'Cost', key: 'cost' },
          ], item => 'Headgear')}
        `);
      }
    });

    // ===== DOG ARMOR =====
    Router.register('dog-armor', (id, params) => {
      if (id) {
        const d = DataManager.getById('dog-armor', id);
        if (!d) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('dog-armor', params)}
          ${armorTabs()}
          <div class="detail-view">
            <h2>${d.name}</h2>
            <div class="field"><span class="label">Covers:</span> <span class="value">${(d.covers || []).join(', ')}</span></div>
            <div class="field"><span class="label">Physical DR:</span> <span class="value">${d.physicalDR}</span></div>
            <div class="field"><span class="label">Energy DR:</span> <span class="value">${d.energyDR}</span></div>
            <div class="field"><span class="label">Radiation DR:</span> <span class="value">${d.radiationDR}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${d.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${d.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${d.rarity}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('dog-armor');
        const dogArmorFilterConfig = [
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'physicalDR', label: 'Phys DR' },
            { value: 'energyDR', label: 'Energy DR' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, dogArmorFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('dog-armor', params);
        Views.render(`
          ${armorTabs()}
          ${Views.filterBar(dogArmorFilterConfig, params, 'dog-armor')}
          ${Views.groupedTable(sorted, 'Dog Armor', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('dog-armor', i.id, v) },
            { label: 'Covers', key: 'covers' },
            { label: 'Phys', key: 'physicalDR' },
            { label: 'Energy', key: 'energyDR' },
            { label: 'Rad', key: 'radiationDR' },
            { label: 'Weight', key: 'weight' },
            { label: 'Cost', key: 'cost' },
          ], item => 'Dog Armor')}
        `);
      }
    });

    // ===== MISCELLANY =====
    Router.register('misc', (id, params) => {
      if (id) {
        const m = DataManager.getById('misc', id);
        if (!m) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('misc', params)}
          <div class="detail-view">
            <h2>${m.name}</h2>
            <div class="field"><span class="label">Effects:</span> <span class="value">${m.effects}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${m.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${m.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${m.rarity}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('misc');
        const miscFilterConfig = [
          { key: 'rarity', label: 'Rarity', options: [
            { value: '0', label: 'Common' },
            { value: '1', label: 'Uncommon' },
            { value: '2', label: 'Rare' },
            { value: '3', label: 'Very Rare' },
          ], filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'rarity', label: 'Rarity' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, miscFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('misc', params);
        Views.render(`
          ${Views.filterBar(miscFilterConfig, params, 'misc')}
          <h2>Miscellany (${sorted.length})</h2>
          <table>
            <thead><tr><th>Name</th><th>Effects</th><th>Weight</th><th>Cost</th><th>Rarity</th></tr></thead>
            <tbody>
              ${sorted.map(m => `<tr>
                <td>${Views.link('misc', m.id, m.name)}</td>
                <td>${m.effects}</td>
                <td>${m.weight}</td>
                <td>${m.cost}</td>
                <td>${m.rarity}</td>
              </tr>`).join('')}
            </tbody>
          </table>
        `);
      }
    });

    // ===== ROBOT MODS =====
    Router.register('robot-mods', (id, params) => {
      if (id) {
        const rm = DataManager.getById('robot-mods', id);
        if (!rm) { Views.render(`<h2>Not Found</h2>`); return; }
        const perks = (rm.perksRequired || []).map(p => Views.link('perks', p.perkId, `${p.perkId} R${p.rank}`)).join(', ') || '—';
        const weight = rm.weightChange !== null ? `${rm.weightChange} lbs` : '—';

        Views.render(`
          ${Views.backLink('robot-mods', params)}
          <div class="detail-view">
            <h2>${rm.name}</h2>
            <div class="field"><span class="label">Effects:</span> <span class="value">${rm.effects}</span></div>
            <div class="field"><span class="label">Weight Change:</span> <span class="value">${weight}</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${rm.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${rm.rarity}</span></div>
            <div class="field"><span class="label">Required Perks:</span> <span class="value">${perks}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('robot-mods');
        const rmFilterConfig = [
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'rarity', label: 'Rarity' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, rmFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('robot-mods', params);
        Views.render(`
          ${Views.filterBar(rmFilterConfig, params, 'robot-mods')}
          <h2>Robot Mods (${sorted.length})</h2>
          <table>
            <thead><tr><th>Name</th><th>Effects</th><th>Weight</th><th>Cost</th><th>Rarity</th></tr></thead>
            <tbody>
              ${sorted.map(m => `<tr>
                <td>${Views.link('robot-mods', m.id, m.name)}</td>
                <td>${m.effects}</td>
                <td>${m.weightChange !== null ? m.weightChange : '—'}</td>
                <td>${m.cost}</td>
                <td>${m.rarity}</td>
              </tr>`).join('')}
            </tbody>
          </table>
        `);
      }
    });

    // ===== ROBOT ARMOR =====
    Router.register('robot-armor', (id, params) => {
      if (id) {
        const ra = DataManager.getById('robot-armor', id);
        if (!ra) { Views.render(`<h2>Not Found</h2>`); return; }
        const perks = (ra.perksRequired || []).map(p => Views.link('perks', p.perkId, `${p.perkId} R${p.rank}`)).join(', ') || '—';
        const cw = ra.carryWeight > 0 ? `+${ra.carryWeight}` : ra.carryWeight < 0 ? ra.carryWeight : '—';

        Views.render(`
          ${Views.backLink('robot-armor', params)}
          <div class="detail-view">
            <h2>${ra.name}</h2>
            <div class="field"><span class="label">Location:</span> <span class="value">${ra.location}</span></div>
            <div class="field"><span class="label">Physical DR:</span> <span class="value">${ra.physicalDR}</span></div>
            <div class="field"><span class="label">Energy DR:</span> <span class="value">${ra.energyDR}</span></div>
            <div class="field"><span class="label">Carry Weight:</span> <span class="value">${cw} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${ra.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${ra.rarity}</span></div>
            <div class="field"><span class="label">Required Perks:</span> <span class="value">${perks}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('robot-armor');
        const raFilterConfig = [
          { key: 'location', label: 'Location' },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'rarity', label: 'Rarity' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, raFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        raFilterConfig[0].options = Views.uniqueOptions(all, 'location');
        App.saveListState('robot-armor', params);
        Views.render(`
          ${Views.filterBar(raFilterConfig, params, 'robot-armor')}
          ${Views.groupedTable(sorted, 'Robot Armor', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('robot-armor', i.id, v) },
            { label: 'Location', key: 'location' },
            { label: 'Phys', key: 'physicalDR' },
            { label: 'Energy', key: 'energyDR' },
            { label: 'Carry Wt', key: 'carryWeight', render: (v) => v > 0 ? `+${v}` : v < 0 ? v : '—' },
            { label: 'Cost', key: 'cost' },
          ], item => item.location)}
        `);
      }
    });

    // ===== BOOKS & MAGAZINES =====
    Router.register('books', (id, params) => {
      if (id) {
        const b = DataManager.getById('books', id);
        if (!b) { Views.render(`<h2>Not Found</h2>`); return; }

        let issuesHtml = '';
        if (b.issues && b.issues.length) {
          issuesHtml = `
            <h3>Issue Table</h3>
            <p>When you discover this magazine, roll to determine which issue you find:</p>
            <table>
              <thead><tr><th>D20 Roll</th><th>Issue</th><th>Effect</th></tr></thead>
              <tbody>
                ${b.issues.map(i => `<tr><td>${i.d20}</td><td>${i.issue}</td><td>${i.effect}</td></tr>`).join('')}
              </tbody>
            </table>
          `;
        }

        Views.render(`
          ${Views.backLink('books', params)}
          <div class="detail-view">
            <h2>${b.name}</h2>
            <div class="field"><span class="label">Description:</span> <span class="value">${b.description}</span></div>
            <div class="field"><span class="label">Perk:</span> <span class="value">${b.perk}</span></div>
          </div>
          ${issuesHtml}
        `);
      } else {
        const all = DataManager.getAll('books');
        const booksFilterConfig = [
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
          ]},
        ];
        const sorted = Views.applySort(all, params.sort, params.order);
        App.saveListState('books', params);
        Views.render(`
          ${Views.filterBar(booksFilterConfig, params, 'books')}
          <h2>Books & Magazines (${sorted.length})</h2>
          <p>All books and magazines have a weight of &lt;1, a cost of 100 caps, and a rarity of 3.</p>
          <table>
            <thead><tr><th>D20</th><th>Publication</th><th>Description</th><th>Issues</th></tr></thead>
            <tbody>
              ${sorted.map((b, i) => `<tr>
                <td>${i + 1}</td>
                <td>${Views.link('books', b.id, b.name)}</td>
                <td>${b.description.substring(0, 120)}${b.description.length > 120 ? '…' : ''}</td>
                <td>${b.issues ? `${b.issues.length} issues` : '—'}</td>
              </tr>`).join('')}
            </tbody>
          </table>
        `);
      }
    });

    // ===== CONSUMABLES =====
    Router.register('consumables', (id, params) => {
      if (id) {
        const c = DataManager.getById('consumables', id);
        if (!c) { Views.render(`<h2>Not Found</h2>`); return; }

        const recipeInfo = DataManager.getRecipeForItem(c.name);
        const usedIn = DataManager.getRecipesByIngredient(c.name);
        const routeForRecipe = (col) => col === 'chem-recipes' ? 'crafting/chem-recipes' : 'crafting/cooking-recipes';

        Views.render(`
          ${Views.backLink('consumables', params)}
          <div class="detail-view">
            <h2>${c.name}</h2>
            <div class="field"><span class="label">Type:</span> <span class="value">${c.type}</span></div>
            <div class="field"><span class="label">Effects:</span> <span class="value">${c.effects}</span></div>
            <div class="field"><span class="label">Duration:</span> <span class="value">${c.duration}</span></div>
            <div class="field"><span class="label">Addictive:</span> <span class="value">${c.addictive ? `Yes (DC ${c.addictionNum})` : 'No'}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${c.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${c.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${c.rarity}</span></div>
          </div>
          ${recipeInfo ? `<h3>Crafting Recipe</h3>${this.renderRecipeInline(recipeInfo.recipe, recipeInfo.collection)}` : ''}
          ${usedIn.length ? `
            <h3>Used in Recipes</h3>
            <div class="used-in-grid">
              ${usedIn.map(u => `
                <div class="used-in-card">
                  <a class="clickable" href="#${routeForRecipe(u.collection)}/${u.recipe.id}">${u.recipe.name}</a>
                  <span class="used-in-type">${u.collection === 'chem-recipes' ? 'Chemistry' : 'Cooking'}</span>
                </div>
              `).join('')}
            </div>
          ` : ''}
        `);
      } else {
        const all = DataManager.getAll('consumables');
        const consumablesFilterConfig = [
          { key: 'type', label: 'Category', options: [
            { value: 'chem', label: 'Chems' },
            { value: 'drink', label: 'Drinks' },
            { value: 'food', label: 'Foods' },
          ]},
          { key: 'addictive', label: 'Addictive', options: [
            { value: 'true', label: 'Yes' },
            { value: 'false', label: 'No' },
          ], filter: (item, val) => String(item.addictive) === val },
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'rarity', label: 'Rarity' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, consumablesFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('consumables', params);
        Views.render(`
          ${Views.filterBar(consumablesFilterConfig, params, 'consumables')}
          ${Views.groupedTable(sorted, 'Consumables', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('consumables', i.id, v) },
            { label: 'Effects', key: 'effects' },
            { label: 'Duration', key: 'duration' },
            { label: 'Recipe', key: 'name', render: (v, i) => {
              const ri = DataManager.getRecipeForItem(i.name);
              if (!ri) return '—';
              const route = ri.collection === 'chem-recipes' ? 'crafting/chem-recipes' : 'crafting/cooking-recipes';
              return Views.link(route, ri.recipe.id, 'View Recipe');
            }},
            { label: 'Addictive', key: 'addictive', render: (v, i) => v ? `Yes (DC ${i.addictionNum})` : 'No' },
            { label: 'Weight', key: 'weight' },
            { label: 'Cost', key: 'cost' },
          ], item => item.type === 'chem' ? 'Chems' : item.type === 'drink' ? 'Drinks' : 'Foods')}
        `);
      }
    });

    // ===== PERKS =====
    Router.register('perks', (id, params) => {
      if (id) {
        const p = DataManager.getById('perks', id);
        if (!p) { Views.render(`<h2>Not Found</h2>`); return; }
        const reqs = p.requirements ? Object.entries(p.requirements).map(([attr, val]) => `${attr} ${val}`).join(', ') : '—';
        const effects = p.effects ? Object.entries(p.effects).map(([rank, desc]) => `<div><strong>Rank ${rank}:</strong> ${desc}</div>`).join('') : '—';

        Views.render(`
          ${Views.backLink('perks', params)}
          <div class="detail-view">
            <h2>${p.name}</h2>
            <div class="field"><span class="label">Ranks:</span> <span class="value">${p.ranks}</span></div>
            <div class="field"><span class="label">Requirements:</span> <span class="value">${reqs}</span></div>
            <div class="field"><span class="label">Effects:</span> <span class="value">${effects}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('perks');
        const ranks = [...new Set(all.map(p => p.ranks))].sort();
        const perksFilterConfig = [
          { key: 'ranks', label: 'Ranks', options: ranks.map(r => ({ value: r.toString(), label: `Ranks: ${r}` })), filter: (item, val) => String(item.ranks) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'ranks', label: 'Ranks' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, perksFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('perks', params);

        const groups = {};
        sorted.forEach(perk => {
          const attrs = Object.keys(perk.requirements || {});
          if (!attrs.length) {
            if (!groups['None']) groups['None'] = [];
            groups['None'].push(perk);
            return;
          }
          attrs.forEach(attr => {
            if (!groups[attr]) groups[attr] = [];
            groups[attr].push(perk);
          });
        });

        const columns = [
          { label: 'Name', key: 'name', render: (v, i) => Views.link('perks', i.id, v) },
          { label: 'Ranks', key: 'ranks' },
          { label: 'Requirements', key: 'requirements', render: (v) => v ? Object.entries(v).map(([a, b]) => `${a} ${b}`).join(', ') : '—' },
          { label: 'Rank 1 Effect', key: 'effects', render: (v) => v ? (v['1'] || v[1] || '').substring(0, 100) : '—' },
        ];

        let perksHtml = `<h2>Perks (${sorted.length})</h2>`;
        Object.keys(groups).sort().forEach(group => {
          const groupItems = groups[group];
          perksHtml += `
            <table>
              <tr class="category-header" onclick="this.classList.toggle('open'); this.nextElementSibling.classList.toggle('hidden');">
              <th colspan="${columns.length}"><span class="cat-arrow">▶</span> ${group} (${groupItems.length})</th>
            </tr>
            <tr class="category-rows hidden">
              <td colspan="${columns.length}">
                  <table>
                    <thead><tr>${columns.map(c => `<th>${c.label}</th>`).join('')}</tr></thead>
                    <tbody>
                      ${groupItems.map(item => `<tr>${columns.map(c => `<td>${c.render ? c.render(item[c.key] !== undefined ? item[c.key] : item, item) : Views.fmt(item[c.key])}</td>`).join('')}</tr>`).join('')}
                    </tbody>
                  </table>
                </td>
              </tr>
            </table>
          `;
        });

        Views.render(`
          ${Views.filterBar(perksFilterConfig, params, 'perks')}
          ${perksHtml}
        `);
      }
    });

    // ===== SKILLS =====
    Router.register('skills', (id, params) => {
      if (id) {
        const s = DataManager.getById('skills', id);
        if (!s) { Views.render(`<h2>Not Found</h2>`); return; }

        Views.render(`
          ${Views.backLink('skills', params)}
          <div class="detail-view">
            <h2>${s.name}</h2>
            <div class="field"><span class="label">Attribute:</span> <span class="value">${s.attribute}</span></div>
            <div class="field"><span class="label">Description:</span> <span class="value">${s.description}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('skills');
        const skillsFilterConfig = [
          { key: 'attribute', label: 'Attribute' },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, skillsFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        skillsFilterConfig[0].options = Views.uniqueOptions(all, 'attribute');
        App.saveListState('skills', params);
        Views.render(`
          ${Views.filterBar(skillsFilterConfig, params, 'skills')}
          ${Views.groupedTable(sorted, 'Skills', [
            { label: 'Name', key: 'name', render: (v, i) => Views.link('skills', i.id, v) },
            { label: 'Description', key: 'description' },
          ], item => item.attribute)}
        `);
      }
    });

    // ===== CALIBERS =====
    Router.register('calibers', (id, params) => {
      if (id) {
        const c = DataManager.getById('calibers', id);
        if (!c) { Views.render(`<h2>Not Found</h2>`); return; }
        const weapons = DataManager.getAll('weapons').filter(w => w.ammo === id);

        Views.render(`
          ${Views.backLink('calibers', params)}
          <div class="detail-view">
            <h2>${c.name}</h2>
            <div class="field"><span class="label">Quantity Found:</span> <span class="value">${c.quantityFound}</span></div>
            <div class="field"><span class="label">Weight:</span> <span class="value">${c.weight} lbs</span></div>
            <div class="field"><span class="label">Cost:</span> <span class="value">${c.cost} caps</span></div>
            <div class="field"><span class="label">Rarity:</span> <span class="value">${c.rarity}</span></div>
            <div class="field"><span class="label">Description:</span> <span class="value">${c.description}</span></div>
            <div class="field"><span class="label">Used By:</span> <span class="value">${weapons.length ? weapons.map(w => Views.link('weapons', w.id, w.name)).join(', ') : 'None'}</span></div>
          </div>
        `);
      } else {
        const all = DataManager.getAll('calibers');
        const calibersFilterConfig = [
          { key: 'rarity', label: 'Rarity', options: [0,1,2,3,4,5].map(v => ({ value: v.toString(), label: App.rarityLabel(v) })), filter: (item, val) => String(item.rarity) === val },
          { key: '_sort', label: 'Sort', options: [
            { value: 'name', label: 'Name' },
            { value: 'cost', label: 'Cost' },
            { value: 'weight', label: 'Weight' },
            { value: 'quantityFound', label: 'Qty Found' },
          ]},
        ];
        const filtered = Views.applyFilters(all, params, calibersFilterConfig);
        const sorted = Views.applySort(filtered, params.sort, params.order);
        App.saveListState('calibers', params);
        Views.render(`
          ${weaponTabs()}
          ${Views.filterBar(calibersFilterConfig, params, 'calibers')}
          <h2>Calibers (${sorted.length})</h2>
          <table>
            <thead><tr><th>Name</th><th>Qty Found</th><th>Weight</th><th>Cost</th><th>Description</th></tr></thead>
            <tbody>
              ${sorted.map(c => `<tr>
                <td>${Views.link('calibers', c.id, c.name)}</td>
                <td>${c.quantityFound}</td>
                <td>${c.weight}</td>
                <td>${c.cost}</td>
                <td>${c.description?.substring(0, 100)}</td>
              </tr>`).join('')}
            </tbody>
          </table>
        `);
      }
    });

    // ===== EFFECTS GLOSSARY =====
    Router.register('effects', (id) => {
      if (id) {
        const parts = id.split('/');
        if (parts.length === 2) {
          Views.render(Views.effectDetail(parts[0], decodeURIComponent(parts[1])));
        } else {
          Views.render(Views.effectsGlossary());
        }
      } else {
        Views.render(Views.effectsGlossary());
      }
    });

    // ===== CRAFTING =====
    Router.register('crafting', (id) => {
      if (id) {
        const parts = id.split('/');
        if (parts[0] === 'workbenches') {
Views.render(this.workbenchDetail());
          } else if (parts[0] === 'chem-recipes') {
          if (parts[1]) {
            Views.render(this.recipeDetail('chem-recipes', parts[1]));
          } else {
            Views.render(this.chemRecipesList());
          }
        } else if (parts[0] === 'cooking-recipes') {
          if (parts[1]) {
            Views.render(this.recipeDetail('cooking-recipes', parts[1]));
          } else {
            Views.render(this.cookingRecipesList());
          }
        } else if (parts[0] === 'power-armor-recipes') {
          if (parts[1]) {
            Views.render(this.recipeDetail('power-armor-recipes', parts[1]));
          } else {
            Views.render(this.powerArmorRecipesList());
          }
        } else if (parts[0] === 'materials') {
          Views.render(this.materialsReference());
        } else {
          Views.render(this.craftingHome());
        }
      } else {
        Views.render(this.craftingHome());
      }
    });
  },

  // ===== CRAFTING VIEWS =====

  craftingHome() {
    const workbenches = DataManager.getAll('workbenches') || [];
    const chemRecipes = DataManager.getAll('chem-recipes') || [];
    const cookingRecipes = DataManager.getAll('cooking-recipes') || [];
    const paRecipes = DataManager.getAll('power-armor-recipes') || [];

    return `
      <h2>Crafting</h2>
      <p>Workbenches, recipes, and material costs for crafting items in the wasteland.</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div class="badge gold"><a class="clickable" href="#crafting/workbenches" style="color:inherit;text-decoration:none">${workbenches.length} Workbenches</a></div>
        <div class="badge gold"><a class="clickable" href="#crafting/materials" style="color:inherit;text-decoration:none">Materials Reference</a></div>
        <div class="badge gold"><a class="clickable" href="#crafting/chem-recipes" style="color:inherit;text-decoration:none">${chemRecipes.length} Chem Recipes</a></div>
        <div class="badge gold"><a class="clickable" href="#crafting/cooking-recipes" style="color:inherit;text-decoration:none">${cookingRecipes.length} Cooking Recipes</a></div>
        <div class="badge gold"><a class="clickable" href="#crafting/power-armor-recipes" style="color:inherit;text-decoration:none">${paRecipes.length} PA Recipes</a></div>
      </div>
    `;
  },

  workbenchDetail() {
    const workbenches = DataManager.getAll('workbenches') || [];
    let html = `
      ${Views.backLink('crafting')}
      <h2>Workbenches (${workbenches.length})</h2>
      <table>
        <thead><tr><th>Name</th><th>Required Skills</th><th>Required Perks</th><th>Used For</th></tr></thead>
        <tbody>
          ${workbenches.map(w => `<tr>
            <td>${w.name}</td>
            <td>${(w.skills || []).join(', ')}</td>
            <td>${(w.perks || []).join(', ') || '—'}</td>
            <td>${w.usedFor}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    `;
    return html;
  },

  materialsReference() {
    const components = DataManager.data.components?.tiers || [];
    const complexityTable = DataManager.data.components?.complexityTable || [];
    const repairTable = DataManager.data.components?.repairTable || [];

    let html = `
      ${Views.backLink('crafting')}
      <h2>Materials Reference</h2>
      <h3>Component Tiers</h3>
      <table>
        <thead><tr><th>Tier</th><th>Rarity</th><th>Weight</th><th>Cost</th><th>Includes</th></tr></thead>
        <tbody>
          ${components.map(c => `<tr>
            <td>${c.name}</td>
            <td>${c.rarity}</td>
            <td>${c.weight}</td>
            <td>${c.cost}</td>
            <td>${(c.includes || []).join(', ')}</td>
          </tr>`).join('')}
        </tbody>
      </table>
      <h3>Material Cost by Complexity</h3>
      <table>
        <thead><tr><th>Complexity</th><th>Materials Required</th></tr></thead>
        <tbody>
          ${complexityTable.map(r => `<tr>
            <td>${r.complexity}</td>
            <td>${r.materials}</td>
          </tr>`).join('')}
        </tbody>
      </table>
      <h3>Repair Materials by Rarity</h3>
      <table>
        <thead><tr><th>Item Rarity</th><th>Materials</th></tr></thead>
        <tbody>
          ${repairTable.map(r => `<tr>
            <td>${r.rarity}</td>
            <td>${r.materials}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    `;
    return html;
  },

  renderRecipeInline(recipe, collection) {
    const linkIngredient = (ing) => {
      const parsed = DataManager.parseIngredient(ing);
      if (parsed) {
        const item = DataManager.findConsumableByName(parsed.name);
        if (item) {
          return `<a class="clickable" href="#consumables/${item.id}">${parsed.name}</a> ×${parsed.quantity}`;
        }
        const component = DataManager.findComponentByName(parsed.name);
        if (component) {
          return `<a class="clickable" href="#crafting/materials">${parsed.name}</a> ×${parsed.quantity}`;
        }
      }
      return ing;
    };

    const group = collection === 'chem-recipes' ? 'crafting/chem-recipes' :
                  collection === 'cooking-recipes' ? 'crafting/cooking-recipes' : 'crafting/power-armor-recipes';

    return `
      <div class="recipe-inline">
        <div class="field"><span class="label">Recipe:</span> <span class="value"><a class="clickable" href="#${group}/${recipe.id}">${recipe.name}</a></span></div>
        ${recipe.ingredients ? `<div class="field"><span class="label">Ingredients:</span> <span class="value">${recipe.ingredients.map(linkIngredient).join(', ')}</span></div>` : ''}
        <div class="field"><span class="label">Complexity:</span> <span class="value">${recipe.complexity || '—'}</span></div>
        <div class="field"><span class="label">Skill:</span> <span class="value">${recipe.skill || '—'}</span></div>
        <div class="field"><span class="label">Perks:</span> <span class="value">${(recipe.perks || []).join(', ') || '—'}</span></div>
        ${recipe.workbench ? `<div class="field"><span class="label">Workbench:</span> <span class="value">${recipe.workbench}</span></div>` : ''}
      </div>
    `;
  },

  recipeDetail(collection, id) {
    const r = DataManager.getById(collection, id);
    if (!r) return `<h2>Not Found</h2>`;
    const group = collection === 'chem-recipes' ? 'crafting/chem-recipes' :
                  collection === 'cooking-recipes' ? 'crafting/cooking-recipes' : 'crafting/power-armor-recipes';

    const producedItem = DataManager.findConsumableByName(r.name);
    const producedItemHtml = producedItem
      ? `<div class="field"><span class="label">Crafted Item:</span> <span class="value">${Views.link('consumables', producedItem.id, producedItem.name)}</span></div>`
      : '';

    const linkIngredient = (ing) => {
      const parsed = DataManager.parseIngredient(ing);
      if (parsed) {
        const item = DataManager.findConsumableByName(parsed.name);
        if (item) {
          return `<a class="clickable" href="#consumables/${item.id}">${parsed.name}</a> ×${parsed.quantity}`;
        }
        const component = DataManager.findComponentByName(parsed.name);
        if (component) {
          return `<a class="clickable" href="#crafting/materials">${parsed.name}</a> ×${parsed.quantity}`;
        }
      }
      return ing;
    };

    return `
      ${Views.backLink(group)}
      <div class="detail-view">
        <h2>${r.name}</h2>
        ${producedItemHtml}
        <div class="field"><span class="label">Type:</span> <span class="value">${r.recipeType || '—'}</span></div>
        <div class="field"><span class="label">Ingredients:</span> <span class="value">${(r.ingredients || []).map(linkIngredient).join(', ')}</span></div>
        <div class="field"><span class="label">Complexity:</span> <span class="value">${r.complexity || '—'}</span></div>
        <div class="field"><span class="label">Skill:</span> <span class="value">${r.skill || '—'}</span></div>
        <div class="field"><span class="label">Perks:</span> <span class="value">${(r.perks || []).join(', ') || '—'}</span></div>
        <div class="field"><span class="label">Rarity:</span> <span class="value">${r.rarity || '—'}</span></div>
        ${r.workbench ? `<div class="field"><span class="label">Workbench:</span> <span class="value">${r.workbench}</span></div>` : ''}
        ${r.requirements ? `<div class="field"><span class="label">Requirements:</span> <span class="value">${r.requirements}</span></div>` : ''}
        ${r.effects ? `<div class="field"><span class="label">Effects:</span> <span class="value">${r.effects}</span></div>` : ''}
        ${r.description ? `<div class="field"><span class="label">Description:</span> <span class="value">${r.description}</span></div>` : ''}
      </div>
    `;
  },

  chemRecipesList() {
    const recipes = DataManager.getAll('chem-recipes') || [];
    let html = `
      ${Views.backLink('crafting')}
      <h2>Chemistry Station Recipes (${recipes.length})</h2>
      <table>
        <thead><tr><th>Name</th><th>Produces</th><th>Type</th><th>Ingredients</th><th>Workbench</th></tr></thead>
        <tbody>
          ${recipes.map(r => {
            const item = DataManager.findConsumableByName(r.name);
            return `<tr>
              <td><a class="clickable" href="#crafting/chem-recipes/${r.id}">${r.name}</a></td>
              <td>${item ? Views.link('consumables', item.id, item.name) : '—'}</td>
              <td>${r.recipeType || 'chem'}</td>
              <td>${(r.ingredients || []).join(', ')}</td>
              <td>${r.workbench || 'Chemistry Station'}</td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    `;
    return html;
  },

  cookingRecipesList() {
    const recipes = DataManager.getAll('cooking-recipes') || [];
    let html = `
      ${Views.backLink('crafting')}
      <h2>Cooking Station Recipes (${recipes.length})</h2>
      <table>
        <thead><tr><th>Name</th><th>Produces</th><th>Type</th><th>Ingredients</th><th>Description</th></tr></thead>
        <tbody>
          ${recipes.map(r => {
            const item = DataManager.findConsumableByName(r.name);
            return `<tr>
              <td><a class="clickable" href="#crafting/cooking-recipes/${r.id}">${r.name}</a></td>
              <td>${item ? Views.link('consumables', item.id, item.name) : '—'}</td>
              <td>${r.recipeType || 'food'}</td>
              <td>${(r.ingredients || []).join(', ')}</td>
              <td>${(r.description || '').substring(0, 100)}</td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    `;
    return html;
  },

  powerArmorRecipesList() {
    const recipes = DataManager.getAll('power-armor-recipes') || [];
    let html = `
      ${Views.backLink('crafting')}
      <h2>Power Armor Station Recipes (${recipes.length})</h2>
      <table>
        <thead><tr><th>Name</th><th>Type</th><th>Requirements</th><th>Effects</th></tr></thead>
        <tbody>
          ${recipes.map(r => `<tr>
            <td><a class="clickable" href="#crafting/power-armor-recipes/${r.id}">${r.name}</a></td>
            <td>${r.recipeType || 'upgrade'}</td>
            <td>${r.requirements || '—'}</td>
            <td>${(r.effects || '').substring(0, 80)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    `;
    return html;
  },

  setupSearch() {
    const input = document.getElementById('search-input');
    const results = document.getElementById('search-results');

    input.addEventListener('input', () => {
      const query = input.value.trim();
      if (query.length < 2) {
        results.classList.add('hidden');
        return;
      }

      const matches = DataManager.search(query);
      if (matches.length === 0) {
        results.innerHTML = '<div class="search-result">No results</div>';
      } else {
        results.innerHTML = matches.map(m => `
          <div class="search-result" onclick="Router.navigate('${m.collection}/${m.id}')">
            <div class="type">${m.type}</div>
            <div>${m.name}</div>
          </div>
        `).join('');
      }
      results.classList.remove('hidden');
    });

    input.addEventListener('blur', () => {
      setTimeout(() => results.classList.add('hidden'), 200);
    });
  },

  setupMenu() {
    const toggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');
    const content = document.getElementById('content');

    const closeMenu = () => {
      if (window.innerWidth <= 768) {
        sidebar.classList.remove('visible');
        backdrop.classList.remove('visible');
      }
    };

    toggle.addEventListener('click', () => {
      const isMobile = window.innerWidth <= 768;
      if (isMobile) {
        sidebar.classList.toggle('visible');
        backdrop.classList.toggle('visible');
      } else {
        sidebar.classList.toggle('hidden');
        backdrop.classList.toggle('hidden');
        content.classList.toggle('expanded');
      }
    });

    backdrop.addEventListener('click', closeMenu);
    document.querySelectorAll('#nav-list a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });
  },

  setupHomeBtn() {
    const btn = document.getElementById('home-btn');
    if (!btn) return;

    const check = () => {
      const route = Router.currentRoute?.route || window.location.hash.slice(1) || 'home';
      btn.classList.toggle('visible', route !== 'home');
    };

    window.addEventListener('hashchange', check);
    document.getElementById('content').addEventListener('scroll', check);
    window.addEventListener('scroll', check);
    check();
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
