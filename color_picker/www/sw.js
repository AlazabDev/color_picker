const CACHE_NAME = 'azab-color-picker-v1.0.0';
const RUNTIME_CACHE = 'runtime-cache-v1';

// قائمة الملفات المطلوب حفظها في الكاش
const STATIC_CACHE_URLS = [
    '/color-picker',
    '/assets/color_picker/css/color_picker.css',
    '/assets/color_picker/js/color_picker.js',
    '/assets/color_picker/img/icon-192.png',
    '/assets/color_picker/img/icon-512.png',
    '/manifest.json',
    // إضافة الخطوط والمكتبات المطلوبة
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// تثبيت Service Worker
self.addEventListener('install', event => {
    console.log('🔧 تثبيت Service Worker...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('📦 حفظ الملفات في الكاش...');
                return cache.addAll(STATIC_CACHE_URLS);
            })
            .then(() => {
                console.log('✅ تم تثبيت Service Worker بنجاح');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('❌ فشل في تثبيت Service Worker:', error);
            })
    );
});

// تفعيل Service Worker
self.addEventListener('activate', event => {
    console.log('🚀 تفعيل Service Worker...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
                            console.log('🗑️ حذف كاش قديم:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('✅ تم تفعيل Service Worker بنجاح');
                return self.clients.claim();
            })
    );
});

// التعامل مع طلبات الشبكة
self.addEventListener('fetch', event => {
    // تجاهل طلبات غير HTTP
    if (!event.request.url.startsWith('http')) return;
    
    // تجاهل طلبات POST/PUT/DELETE
    if (event.request.method !== 'GET') return;
    
    event.respondWith(
        caches.match(event.request)
            .then(cachedResponse => {
                // إذا وجد في الكاش، أرجعه
                if (cachedResponse) {
                    console.log('📱 تحميل من الكاش:', event.request.url);
                    return cachedResponse;
                }
                
                // إلا فجلبه من الشبكة
                return fetch(event.request)
                    .then(response => {
                        // تحقق من صحة الاستجابة
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        
                        // احفظ نسخة في الكاش للمرة القادمة
                        const responseToCache = response.clone();
                        caches.open(RUNTIME_CACHE)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            });
                        
                        return response;
                    })
                    .catch(error => {
                        console.error('❌ فشل في جلب البيانات:', error);
                        
                        // إرجاع صفحة أوفلاين إذا كانت متاحة
                        if (event.request.destination === 'document') {
                            return caches.match('/offline.html');
                        }
                        
                        throw error;
                    });
            })
    );
});

// رسائل من التطبيق الرئيسي
self.addEventListener('message', event => {
    switch (event.data.type) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
            
        case 'GET_VERSION':
            event.ports[0].postMessage({
                type: 'VERSION',
                version: CACHE_NAME
            });
            break;
            
        case 'CLEAR_CACHE':
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => caches.delete(cacheName))
                );
            }).then(() => {
                event.ports[0].postMessage({
                    type: 'CACHE_CLEARED'
                });
            });
            break;
    }
});

// إشعارات الدفع (اختيارية)
self.addEventListener('push', event => {
    if (!event.data) return;
    
    const data = event.data.json();
    const options = {
        body: data.body || 'رسالة جديدة من منتقي الألوان',
        icon: '/assets/color_picker/img/icon-192.png',
        badge: '/assets/color_picker/img/icon-72.png',
        dir: 'rtl',
        lang: 'ar',
        vibrate: [200, 100, 200],
        data: data,
        actions: [
            {
                action: 'open',
                title: 'فتح التطبيق',
                icon: '/assets/color_picker/img/icon-96.png'
            },
            {
                action: 'close',
                title: 'إغلاق'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title || 'منتقي الألوان', options)
    );
});

// التعامل مع النقر على الإشعارات
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'open' || !event.action) {
        event.waitUntil(
            clients.openWindow('/color-picker')
        );
    }
});
