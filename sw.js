// チビスポ Service Worker（PWA用・ネットワーク優先）
// 方針：常に最新を取りに行き、成功したら控えにキャッシュ。オフライン時だけキャッシュを返す。
//       → 「古いページを掴む」事故を避けつつ、インストール可能＆オフライン耐性を確保。
// 対象：同一オリジンのGETのみ（Supabase/Googleマップ/フォント等の外部通信は素通し）。
const CACHE = 'chibispo-v4';

self.addEventListener('install', (e) => { self.skipWaiting(); });

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    // 古いバージョンのキャッシュを掃除
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url); } catch (_) { return; }
  if (url.origin !== self.location.origin) return; // 外部通信はSWを通さない

  // 画像：控えがあれば即返し、裏で取り直して控えを更新する（stale-while-revalidate）。
  //   画像は差し替え頻度が低く、毎回ネットワーク待ちにすると2回目以降も表示が遅い。
  //   差し替えた画像は次の訪問で新しくなる。すぐ反映したいときはファイル名か ?v= を変える。
  if (req.destination === 'image') {
    e.respondWith((async () => {
      const c = await caches.open(CACHE);
      const cached = await c.match(req);
      const fresh = fetch(req).then((res) => {
        if (res && res.ok) c.put(req, res.clone()).catch(() => {});
        return res;
      }).catch(() => null);
      if (cached) { e.waitUntil(fresh); return cached; }
      return (await fresh) || Response.error();
    })());
    return;
  }

  e.respondWith((async () => {
    try {
      const res = await fetch(req);
      // 成功したGETだけオフライン用に控える（404などは控えない）
      if (res && res.ok) { try { const c = await caches.open(CACHE); c.put(req, res.clone()); } catch (_) {} }
      return res;
    } catch (_) {
      // オフライン：キャッシュ→無ければトップ
      const cached = await caches.match(req);
      return cached || (await caches.match('/index.html')) || Response.error();
    }
  })());
});
