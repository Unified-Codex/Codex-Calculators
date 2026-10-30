/* Riven Calculator offline app. Bump CACHE_VERSION on each public release.
 * Offline HTML must be cached even when a nonessential icon fails to load. */
const CACHE_VERSION='v6.0-closest-two';
const SHELL_CACHE=`riven-calculator-shell-${CACHE_VERSION}-share-once-v1`;
const FONT_CACHE='riven-calculator-google-fonts-v1';
const APP_INDEX=new URL('./index.html',self.registration.scope).href;
const APP_ORIGIN=new URL(self.registration.scope).origin;
const OPTIONAL_ASSETS=['./','./manifest.json','./icon-192.png','./icon-512.png','./apple-touch-icon.png','./favicon-32.png','./tool-riven.png','./tool-duplicate.png','./tool-relic.png','./tool-nightwave.png'];

async function precacheCore(){
  const cache=await caches.open(SHELL_CACHE);
  // A single successful navigation is sufficient for a fully functional offline
  // calculator. Never make this dependent on manifest or icon availability.
  const response=await fetch(new Request(APP_INDEX,{cache:'reload'}));
  if(!response.ok)throw new Error(`Unable to cache the calculator: HTTP ${response.status}`);
  await cache.put(APP_INDEX,response);
  // A missing optional asset must not abort service-worker installation.
  await Promise.allSettled(OPTIONAL_ASSETS.map(async path=>{
    const url=new URL(path,self.registration.scope).href;
    const result=await fetch(new Request(url,{cache:'reload'}));
    if(result.ok)await cache.put(url,result);
  }));
}

self.addEventListener('install',event=>{
  event.waitUntil(precacheCore());
  // Keep an existing active session in place until the user accepts an update.
});
self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(key=>key.startsWith('riven-calculator-shell-')&&key!==SHELL_CACHE).map(key=>caches.delete(key)));
    await self.clients.claim();
  })());
});
self.addEventListener('message',event=>{
  if(event.data?.type==='SKIP_WAITING')self.skipWaiting();
  if(event.data?.type==='GET_VERSION')event.ports?.[0]?.postMessage({type:'RIVEN_SW_VERSION',version:CACHE_VERSION});
  if(event.data?.type==='CHECK_OFFLINE_READY'){
    event.waitUntil((async()=>{
      const cached=await caches.match(APP_INDEX);
      event.source?.postMessage({type:'OFFLINE_READY',ready:!!cached});
    })());
  }
});

// Network-first when connected. Fall back to the known-good, precached HTML
// for *any* navigation under this GitHub Pages project path, including / and
// /index.html. A timeout avoids a long hang on flaky phone networks.
async function servePage(request){
  const controller=new AbortController();
  const timer=setTimeout(()=>controller.abort(),3500);
  try{
    const result=await fetch(request,{cache:'no-store',signal:controller.signal});
    if(!result.ok)throw new Error('Navigation unavailable');
    try{
      const cache=await caches.open(SHELL_CACHE);
      await cache.put(APP_INDEX,result.clone());
    }catch(e){/* An exhausted device cache must not break online use. */}
    return result;
  }catch(error){
    return (await caches.match(APP_INDEX))||new Response('Offline copy not ready. Reconnect and open the calculator once.',{
      status:503,headers:{'Content-Type':'text/plain;charset=utf-8'}
    });
  }finally{clearTimeout(timer);}
}
async function serveShellAsset(request){
  const cached=await caches.match(request);
  if(cached)return cached;
  try{
    const response=await fetch(request);
    if(response.ok){
      try{const cache=await caches.open(SHELL_CACHE);await cache.put(request,response.clone());}catch(e){}
    }
    return response;
  }catch(error){return Response.error();}
}
async function serveGoogleFont(request){
  const cache=await caches.open(FONT_CACHE);
  const cached=await cache.match(request);
  if(cached)return cached;
  try{
    const response=await fetch(request);
    if(response.ok||response.type==='opaque'){
      try{await cache.put(request,response.clone());}catch(e){}
    }
    return response;
  }catch(error){return Response.error();}
}
self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  if(url.hostname==='fonts.googleapis.com'||url.hostname==='fonts.gstatic.com'){
    event.respondWith(serveGoogleFont(req));
    return;
  }
  if(url.origin!==APP_ORIGIN||!url.pathname.startsWith(new URL(self.registration.scope).pathname))return;
  if(req.mode==='navigate')event.respondWith(servePage(req));
  else event.respondWith(serveShellAsset(req));
});
