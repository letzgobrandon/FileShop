/* eslint-disable no-console */

import { register } from 'register-service-worker'

if (process.env.NODE_ENV === 'production') {
    register(`${process.env.BASE_URL}service-worker.js`, {
        ready () {
            console.log(
                'App is being served from cache by a service worker.\n' +
                'For more details, visit https://goo.gl/AFskqB'
            )
        },
        registered (registration) {
            console.log('Service worker has been registered.')
            window.dispatchEvent(new CustomEvent('swRegistered', {
                "detail": {registration: registration}
            }))
        },
        cached (registration) {
            console.log('Content has been cached for offline use.')
            window.dispatchEvent(new CustomEvent('swRegistered', {
                "detail": {registration: registration}
            }))
        },
        updatefound () {
            console.log('New update is downloading.')
        },
        updated (registration) {
            window.dispatchEvent(new CustomEvent('swUpdateAvailable', {
                "detail": {worker: registration.waiting}
            }))
        },
        offline () {
            console.log('No internet connection found. App is running in offline mode.')
        },
        error (error) {
            console.error('Error during service worker registration:', error)
        }
    })
    var refreshing;
    navigator.serviceWorker.addEventListener("controllerchange", function() {
        console.log("Activating new version")
        if(refreshing) return

        window.location.reload()
        refreshing = true
    })
}
