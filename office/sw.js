self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>self.clients.claim());
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(u.pathname.endsWith('office-status.json')||u.pathname.endsWith('office-history.jsonl'))return; // 常に最新
  e.respondWith(caches.open('kinoko-v1').then(c=>c.match(e.request).then(r=>{
    const f=fetch(e.request).then(res=>{if(res.ok)c.put(e.request,res.clone());return res;}).catch(()=>r);
    return r||f;
  })));
});
