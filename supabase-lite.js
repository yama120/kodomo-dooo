(function () {
  const authListeners = [];

  function createClient(projectUrl, anonKey) {
    const baseUrl = projectUrl.replace(/\/$/, '');
    const storageKey = `sb-lite-${new URL(baseUrl).hostname}-auth`;

    function readSession() {
      try {
        return JSON.parse(localStorage.getItem(storageKey) || 'null');
      } catch (_) {
        return null;
      }
    }

    function writeSession(session) {
      if (session) localStorage.setItem(storageKey, JSON.stringify(session));
      else localStorage.removeItem(storageKey);
    }

    function notify(event, session) {
      authListeners.forEach(callback => {
        try { callback(event, session); } catch (error) { console.error(error); }
      });
    }

    async function request(path, options = {}) {
      const session = readSession();
      const headers = new Headers(options.headers || {});
      headers.set('apikey', anonKey);
      headers.set('Authorization', `Bearer ${session?.access_token || anonKey}`);
      if (options.body && !(options.body instanceof FormData) && !(options.body instanceof Blob)) {
        headers.set('Content-Type', 'application/json');
      }

      const response = await fetch(`${baseUrl}${path}`, { ...options, headers });
      const text = await response.text();
      const json = text ? JSON.parse(text) : null;
      if (!response.ok) {
        return { data: null, error: json || { message: `Request failed: ${response.status}` } };
      }
      return { data: json, error: null };
    }

    async function authRequest(path, body) {
      const response = await fetch(`${baseUrl}${path}`, {
        method: 'POST',
        headers: {
          apikey: anonKey,
          Authorization: `Bearer ${anonKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      const text = await response.text();
      const json = text ? JSON.parse(text) : null;
      if (!response.ok) return { data: null, error: json };
      return { data: json, error: null };
    }

    async function normalizeSession(data) {
      const session = data?.access_token ? {
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        expires_at: data.expires_in ? Math.floor(Date.now() / 1000) + data.expires_in : data.expires_at,
        user: data.user || null,
      } : data?.session || null;

      if (session && !session.user) {
        const userResult = await getUserWithToken(session.access_token);
        session.user = userResult.data?.user || userResult.data || null;
      }
      return session;
    }

    async function getUserWithToken(token) {
      const response = await fetch(`${baseUrl}/auth/v1/user`, {
        headers: {
          apikey: anonKey,
          Authorization: `Bearer ${token}`,
        },
      });
      const text = await response.text();
      const json = text ? JSON.parse(text) : null;
      if (!response.ok) return { data: null, error: json };
      return { data: json, error: null };
    }

    async function sessionFromUrlHash() {
      const params = new URLSearchParams(location.hash.replace(/^#/, ''));
      const accessToken = params.get('access_token');
      if (!accessToken) return null;
      const session = await normalizeSession({
        access_token: accessToken,
        refresh_token: params.get('refresh_token'),
        expires_in: Number(params.get('expires_in') || 0),
      });
      writeSession(session);
      history.replaceState(null, '', location.pathname + location.search);
      return session;
    }

    class QueryBuilder {
      constructor(table) {
        this.table = table;
        this.method = 'GET';
        this.params = new URLSearchParams();
        this.filters = [];
        this.body = null;
        this.singleResult = false;
      }

      select(columns) {
        this.method = 'GET';
        this.params.set('select', columns);
        return this;
      }

      insert(values) {
        this.method = 'POST';
        this.body = values;
        this.params.set('select', '*');
        return this.execute();
      }

      update(values) {
        this.method = 'PATCH';
        this.body = values;
        return this;
      }

      delete() {
        this.method = 'DELETE';
        return this;
      }

      eq(column, value) {
        this.filters.push([column, value]);
        if (this.method === 'PATCH' || this.method === 'DELETE') return this.execute();
        return this;
      }

      order(column, options = {}) {
        this.params.set('order', `${column}.${options.ascending === false ? 'desc' : 'asc'}`);
        return this.execute();
      }

      single() {
        this.singleResult = true;
        return this.execute();
      }

      then(resolve, reject) {
        return this.execute().then(resolve, reject);
      }

      async execute() {
        this.filters.forEach(([column, value]) => this.params.set(column, `eq.${value}`));
        const query = this.params.toString();
        const path = `/rest/v1/${this.table}${query ? `?${query}` : ''}`;
        const headers = { Prefer: 'return=representation' };
        const result = await request(path, {
          method: this.method,
          headers,
          body: this.body ? JSON.stringify(this.body) : undefined,
        });
        if (!result.error && this.singleResult) {
          result.data = Array.isArray(result.data) ? result.data[0] || null : result.data;
          if (!result.data) result.error = { message: 'No rows returned' };
        }
        return result;
      }
    }

    function storageBucket(bucket) {
      return {
        async upload(path, file, options = {}) {
          const headers = {
            'Content-Type': options.contentType || file.type || 'application/octet-stream',
          };
          if (options.upsert) headers['x-upsert'] = 'true';
          return request(`/storage/v1/object/${bucket}/${encodeURI(path)}`, {
            method: 'POST',
            headers,
            body: file,
          });
        },
        getPublicUrl(path) {
          return {
            data: {
              publicUrl: `${baseUrl}/storage/v1/object/public/${bucket}/${path}`,
            },
          };
        },
        async remove(paths) {
          return request(`/storage/v1/object/${bucket}`, {
            method: 'DELETE',
            body: JSON.stringify({ prefixes: paths }),
          });
        },
      };
    }

    return {
      auth: {
        async signUp({ email, password }) {
          const result = await authRequest('/auth/v1/signup', { email, password });
          const session = await normalizeSession(result.data);
          if (session) {
            writeSession(session);
            notify('SIGNED_IN', session);
          }
          return { data: { user: result.data?.user || session?.user || null, session }, error: result.error };
        },
        async signInWithPassword({ email, password }) {
          const result = await authRequest('/auth/v1/token?grant_type=password', { email, password });
          if (result.error) return result;
          const session = await normalizeSession(result.data);
          writeSession(session);
          notify('SIGNED_IN', session);
          return { data: { session, user: session.user }, error: null };
        },
        async signInWithOAuth({ provider, options = {} }) {
          const redirectTo = encodeURIComponent(options.redirectTo || location.href);
          location.href = `${baseUrl}/auth/v1/authorize?provider=${encodeURIComponent(provider)}&redirect_to=${redirectTo}`;
          return { data: null, error: null };
        },
        async resetPasswordForEmail(email, options = {}) {
          const body = { email };
          if (options.redirectTo) body.redirect_to = options.redirectTo;
          return authRequest('/auth/v1/recover', body);
        },
        async updateUser(values) {
          const session = readSession() || await sessionFromUrlHash();
          if (!session?.access_token) return { data: null, error: { message: 'Not logged in' } };
          const response = await fetch(`${baseUrl}/auth/v1/user`, {
            method: 'PUT',
            headers: {
              apikey: anonKey,
              Authorization: `Bearer ${session.access_token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(values),
          });
          const text = await response.text();
          const json = text ? JSON.parse(text) : null;
          if (!response.ok) return { data: null, error: json };
          session.user = json;
          writeSession(session);
          return { data: { user: json }, error: null };
        },
        async getUser() {
          const session = readSession() || await sessionFromUrlHash();
          if (!session?.access_token) return { data: { user: null }, error: null };
          const result = await getUserWithToken(session.access_token);
          const user = result.data?.user || result.data || null;
          if (user) {
            session.user = user;
            writeSession(session);
          }
          return { data: { user }, error: result.error };
        },
        async getSession() {
          const hashSession = await sessionFromUrlHash();
          const session = hashSession || readSession();
          return { data: { session }, error: null };
        },
        async signOut() {
          const hadSession = !!readSession();
          writeSession(null);
          if (hadSession) notify('SIGNED_OUT', null);
          return { error: null };
        },
        onAuthStateChange(callback) {
          authListeners.push(callback);
          return {
            data: {
              subscription: {
                unsubscribe() {
                  const index = authListeners.indexOf(callback);
                  if (index >= 0) authListeners.splice(index, 1);
                },
              },
            },
          };
        },
      },
      from(table) {
        return new QueryBuilder(table);
      },
      storage: {
        from: storageBucket,
      },
    };
  }

  window.supabase = { createClient };
})();
