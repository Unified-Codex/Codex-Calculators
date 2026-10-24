/* Riven Calculator offline cache. Bump CACHE_VERSION for every public release.
   Always upload index.html, manifest.json, sw.js and icons together. */
const CACHE_VERSION='v3.6';
const SHELL_CACHE=`riven-calculator-shell-${CACHE_VERSION}`;
const FONT_CACHE='riven-calculator-google-fonts-v1';
const APP_SHELL=['./','./index.html','./manifest.json','./icons/icon-192.png','./icons/icon-512.png','./icons/apple-touch-icon.png'];
const APP_INDEX=new URL('./index.html',self.registration.scope).href;
const APP_ORIGIN=new URL(self.registration.scope).origin;

self.addEventListener('install',event=>{
  event.waitUntil((async()=>{
    const cache=await caches.open(SHELL_CACHE);
    await cache.addAll(APP_SHELL.map(path=>new Request(new URL(path,self.registration.scope).href,{cache:'reload'})));
    // Do not skipWaiting automatically during an active session: a user may be editing a Riven.
  })());
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
});

// Pages are fetched from GitHub whenever online and fall back to cached HTML offline.
async function servePage(request){
  const controller=new AbortController();
  const timer=setTimeout(()=>controller.abort(),5000);
  try{
    const result=await fetch(request,{cache:'no-store',signal:controller.signal});
    if(!result.ok)throw new Error('Navigation unavailable');
    // A storage quota error must not break the online calculator.
    try{const cache=await caches.open(SHELL_CACHE);await cache.put(APP_INDEX,result.clone());}catch(e){}
    return result;
  }catch(error){
    return (await caches.match(APP_INDEX))||new Response('Offline files are not yet available. Reconnect and open the calculator once.',{
      status:503,headers:{'Content-Type':'text/plain;charset=utf-8'}
    });
  }finally{clearTimeout(timer);}
}
async function serveShellAsset(request){
  const cache=await caches.open(SHELL_CACHE);
  const stored=await cache.match(request);
  if(stored)return stored;
  try{
    const response=await fetch(request);
    if(response.ok){try{await cache.put(request,response.clone());}catch(e){}}
    return response;
  }catch(error){return Response.error();}
}
async function serveGoogleFont(request){
  const cache=await caches.open(FONT_CACHE);
  const stored=await cache.match(request);
  if(stored)return stored;
  try{
    const response=await fetch(request);
    if(response.ok||response.type==='opaque'){try{await cache.put(request,response.clone());}catch(e){}}
    return response;
  }catch(error){return Response.error();}
}
self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  if((url.hostname==='fonts.googleapis.com'||url.hostname==='fonts.gstatic.com')){
    event.respondWith(serveGoogleFont(req));
    return;
  }
  if(url.origin!==APP_ORIGIN||!url.pathname.startsWith(new URL(self.registration.scope).pathname))return;
  if(req.mode==='navigate'){
    event.respondWith(servePage(req));
    return;
  }
  event.respondWith(serveShellAsset(req));
});
