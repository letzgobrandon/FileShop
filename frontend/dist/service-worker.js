importScripts("/precache-manifest.201b6769cb069ce3e01de9e3fcf0f8ff.js", "https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

workbox.setConfig({
  debug: false
});

workbox.core.setCacheNameDetails({
  prefix: "fileshop"
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */

self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

// Cache images:
workbox.routing.registerRoute(
    /\.(?:png|gif|jpg|jpeg|svg)$/,
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: "images",
        plugins: [
            new workbox.expiration.Plugin({
                maxEntries: 60,
                maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
            })
        ]
    })
);

// Cache Google fonts:
workbox.routing.registerRoute(
    new RegExp("https://fonts.(?:googleapis|gstatic).com/(.*)"),
    new workbox.strategies.CacheFirst({
        cacheName: "googleapis",
        plugins: [
            new workbox.expiration.Plugin({
                maxEntries: 30,
                maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
            })
        ]
    })
);

// Cache Google fonts:
workbox.routing.registerRoute(
    new RegExp("https://fonts.(?:googleapis|gstatic).com/(.*)"),
    new workbox.strategies.CacheFirst({
        cacheName: "googleapis",
        plugins: [
            new workbox.expiration.Plugin({
                maxEntries: 30,
                maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
            })
        ]
    })
);

workbox.routing.registerNavigationRoute(workbox.precaching.getCacheKeyForURL("index.html"));

