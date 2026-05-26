const Router = {
  routes: {},
  currentRoute: null,
  params: {},

  register(path, handler) {
    this.routes[path] = handler;
  },

  navigate(route) {
    window.location.hash = route;
  },

  buildHash(route, id, params) {
    let hash = route;
    if (id) hash += '/' + id;
    if (params && Object.keys(params).length) {
      const qs = Object.entries(params)
        .filter(([, v]) => v !== '' && v !== null && v !== undefined)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&');
      if (qs) hash += '?' + qs;
    }
    return hash;
  },

  handleRoute() {
    const hash = window.location.hash.slice(1) || 'home';

    const qIndex = hash.indexOf('?');
    let base, queryString;
    if (qIndex >= 0) {
      base = hash.slice(0, qIndex);
      queryString = hash.slice(qIndex + 1);
    } else {
      base = hash;
      queryString = '';
    }

    this.params = {};
    queryString.split('&').forEach(pair => {
      if (!pair) return;
      const [k, v] = pair.split('=');
      if (k) this.params[decodeURIComponent(k)] = decodeURIComponent(v || '');
    });

    const parts = base.split('/');
    const route = parts[0];
    const id = parts.slice(1).join('/') || null;

    const handler = this.routes[route];
    if (handler) {
      this.currentRoute = { route, id, hash, params: { ...this.params } };
      handler(id, { ...this.params });
    } else {
      this.routes['home']?.();
    }

    this.updateNav(route);
  },

  updateNav(activeRoute) {
    const parentNav = {
      'mods': 'weapons', 'calibers': 'weapons',
      'armor-sets': 'armor', 'armor-mods': 'armor', 'clothing': 'armor', 'outfits': 'armor'
    };
    const navKey = parentNav[activeRoute] || activeRoute;
    document.querySelectorAll('#nav-list a').forEach(link => {
      link.classList.toggle('active', link.dataset.nav === navKey);
    });
  },

  init() {
    window.addEventListener('hashchange', () => this.handleRoute());
    this.handleRoute();
  }
};
