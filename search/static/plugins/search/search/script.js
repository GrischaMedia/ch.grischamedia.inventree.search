(function() {
  const SEARCH = window.SEARCH || {};
  const apiUrl = SEARCH.apiUrl || '';
  const csrfToken = SEARCH.csrf || '';
  
  let searchTimeout = null;

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return csrfToken || null;
  }

  function setAlert(kind, msg) {
    const el = document.getElementById('search-alert');
    if (!el) return;
    el.classList.remove('d-none', 'alert-success', 'alert-danger', 'alert-info', 'alert-warning');
    el.classList.add(`alert-${kind}`);
    el.textContent = msg;
  }

  function clearAlert() {
    const el = document.getElementById('search-alert');
    if (!el) return;
    el.classList.add('d-none');
    el.textContent = '';
  }

  function renderResults(results) {
    const container = document.getElementById('results-container');
    const list = document.getElementById('results-list');
    const noResults = document.getElementById('no-results');

    if (!container || !list || !noResults) return;

    if (results.length === 0) {
      container.classList.add('d-none');
      noResults.classList.remove('d-none');
      return;
    }

    container.classList.remove('d-none');
    noResults.classList.add('d-none');
    list.innerHTML = '';

    results.forEach(result => {
      const item = document.createElement('div');
      item.className = 'result-item';

      const title = document.createElement('h4');
      const link = document.createElement('a');
      link.href = result.url || '#';
      if (result.url) link.target = '_blank';
      link.textContent = result.name;
      title.appendChild(link);
      item.appendChild(title);

      const meta = document.createElement('div');
      meta.className = 'result-meta';
      let metaText = `<span class="badge badge-primary">${result.type}</span>`;
      if (result.ipn) {
        metaText += ` | IPN: ${result.ipn}`;
      }
      if (result.category) {
        metaText += ` | Kategorie: ${result.category}`;
      }
      meta.innerHTML = metaText;
      item.appendChild(meta);

      if (result.description) {
        const desc = document.createElement('div');
        desc.className = 'result-description';
        desc.textContent = result.description;
        item.appendChild(desc);
      }

      list.appendChild(item);
    });
  }

  async function performSearch(query) {
    if (!query || query.trim().length < 1) {
      document.getElementById('results-container')?.classList.add('d-none');
      document.getElementById('no-results')?.classList.add('d-none');
      clearAlert();
      return;
    }

    try {
      const res = await fetch(`${apiUrl}?q=${encodeURIComponent(query)}`);
      const data = await res.json();

      if (!res.ok) {
        setAlert('danger', data.error || `Fehler (${res.status})`);
        return;
      }

      const results = data.results || [];
      renderResults(results);

      if (results.length === 0) {
        clearAlert();
      }
    } catch (e) {
      setAlert('danger', 'Fehler bei der Suche: ' + (e.message || 'Unbekannter Fehler'));
    }
  }

  function bindEvents() {
    const input = document.getElementById('search-input');
    if (!input) return;

    input.addEventListener('input', (e) => {
      const query = e.target.value.trim();

      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }

      searchTimeout = setTimeout(() => {
        performSearch(query);
      }, 300);
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (searchTimeout) {
          clearTimeout(searchTimeout);
        }
        performSearch(e.target.value.trim());
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindEvents);
  } else {
    bindEvents();
  }
})();

