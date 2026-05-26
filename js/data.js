const DataManager = {
  data: {},
  loaded: false,

  async loadAll() {
    const files = [
      'weapons', 'mods', 'armor', 'armor-sets', 'armor-mods',
      'clothing', 'outfits', 'consumables', 'perks', 'skills',
      'calibers', 'effects', 'components',
      'headgear', 'dog-armor', 'robot-mods', 'robot-armor', 'books', 'misc'
    ];

    const craftingFiles = [
      'crafting/workbenches',
      'crafting/chem-recipes',
      'crafting/cooking-recipes',
      'crafting/power-armor-recipes'
    ];

    const promises = files.map(async (file) => {
      const response = await fetch(`data/${file}.json`);
      if (!response.ok) throw new Error(`Failed to load ${file}.json`);
      this.data[file] = await response.json();
    });

    const craftingPromises = craftingFiles.map(async (file) => {
      const response = await fetch(`data/${file}.json`);
      if (!response.ok) throw new Error(`Failed to load ${file}.json`);
      const key = file.split('/').pop();
      this.data[key] = await response.json();
    });

    await Promise.all([...promises, ...craftingPromises]);
    this.buildLookups();
    this.buildRecipeLookups();
    this.loaded = true;
  },

  buildLookups() {
    this.lookups = {};

    Object.entries(this.data).forEach(([key, items]) => {
      if (Array.isArray(items)) {
        this.lookups[key] = {};
        items.forEach(item => {
          if (item.id) {
            this.lookups[key][item.id] = item;
          }
        });
      }
    });

    this.lookups.effects = this.data.effects || {};
  },

  buildRecipeLookups() {
    this.recipeByProducedName = {};
    this.consumableByName = {};

    ['chem-recipes', 'cooking-recipes'].forEach(collection => {
      (this.data[collection] || []).forEach(recipe => {
        const key = recipe.name.toLowerCase();
        if (!this.recipeByProducedName[key]) {
          this.recipeByProducedName[key] = [];
        }
        this.recipeByProducedName[key].push({ recipe, collection });
      });
    });

    (this.data.consumables || []).forEach(item => {
      this.consumableByName[item.name.toLowerCase()] = item;
    });
  },

  getRecipeForItem(itemName) {
    const key = itemName.toLowerCase();
    const matches = this.recipeByProducedName[key];
    return matches && matches.length ? matches[0] : null;
  },

  findConsumableByName(name) {
    return this.consumableByName[name.toLowerCase()] || null;
  },

  findComponentByName(name) {
    const tiers = this.data.components?.tiers || [];
    return tiers.find(c => c.name.toLowerCase() === name.toLowerCase()) || null;
  },

  getRecipesByIngredient(itemName) {
    const results = [];
    const seen = new Set();
    const q = itemName.toLowerCase();
    ['chem-recipes', 'cooking-recipes'].forEach(collection => {
      (this.data[collection] || []).forEach(recipe => {
        (recipe.ingredients || []).forEach(ing => {
          const parsed = this.parseIngredient(ing);
          if (parsed && parsed.name.toLowerCase() === q && !seen.has(recipe.id)) {
            seen.add(recipe.id);
            results.push({ recipe, collection });
          }
        });
      });
    });
    return results;
  },

  parseIngredient(ingredientStr) {
    const m = ingredientStr.match(/^(.+?)\s*[×x]\s*(.+)$/);
    if (m) return { name: m[1].trim(), quantity: m[2].trim() };
    return null;
  },

  getById(collection, id) {
    return this.lookups[collection]?.[id] || null;
  },

  getAll(collection) {
    return this.data[collection] || [];
  },

  getEffectCategory(category) {
    return this.data.effects?.[category] || {};
  },

  getEffectByName(category, name) {
    return this.data.effects?.[category]?.[name] || null;
  },

  search(query) {
    const results = [];
    const q = query.toLowerCase();

    const collections = [
      { key: 'weapons', label: 'Weapon', nameKey: 'name' },
      { key: 'mods', label: 'Weapon Mod', nameKey: 'name' },
      { key: 'armor', label: 'Armor', nameKey: 'name' },
      { key: 'armor-sets', label: 'Armor Set', nameKey: 'name' },
      { key: 'armor-mods', label: 'Armor Mod', nameKey: 'name' },
      { key: 'clothing', label: 'Clothing', nameKey: 'name' },
      { key: 'outfits', label: 'Outfit', nameKey: 'name' },
      { key: 'headgear', label: 'Headgear', nameKey: 'name' },
      { key: 'dog-armor', label: 'Dog Armor', nameKey: 'name' },
      { key: 'robot-mods', label: 'Robot Mod', nameKey: 'name' },
      { key: 'robot-armor', label: 'Robot Armor', nameKey: 'name' },
      { key: 'books', label: 'Publication', nameKey: 'name' },
      { key: 'misc', label: 'Miscellany', nameKey: 'name' },
      { key: 'consumables', label: 'Consumable', nameKey: 'name' },
      { key: 'perks', label: 'Perk', nameKey: 'name' },
      { key: 'skills', label: 'Skill', nameKey: 'name' },
      { key: 'calibers', label: 'Caliber', nameKey: 'name' },
      { key: 'workbenches', label: 'Workbench', nameKey: 'name' },
      { key: 'chem-recipes', label: 'Chem Recipe', nameKey: 'name' },
      { key: 'cooking-recipes', label: 'Cooking Recipe', nameKey: 'name' },
      { key: 'power-armor-recipes', label: 'PA Recipe', nameKey: 'name' }
    ];

    collections.forEach(({ key, label, nameKey }) => {
      const items = this.getAll(key);
      items.forEach(item => {
        const searchable = Object.values(item)
          .filter(v => typeof v === 'string' || typeof v === 'number')
          .join(' ')
          .toLowerCase();

        if (searchable.includes(q)) {
          results.push({
            type: label,
            collection: key,
            id: item.id,
            name: item[nameKey] || item.id
          });
        }
      });
    });

    return results.slice(0, 20);
  }
};
