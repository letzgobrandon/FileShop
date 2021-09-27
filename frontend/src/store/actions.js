export default {
    updateSidebarState({commit}, value) {
        commit('UPDATE_SIDEBAR_STATE', value)
    },
    updateSiteTitle(t, value) {
        document.title = `${value} | FileShop`
    },
    updateHeaderTitle({commit}, value) {
        commit('UPDATE_HEADER_TITLE', value)
    },
    updateHeaderSide({commit}, value) {
        commit('UPDATE_HEADER_SIDE', value)
    },
    updateServiceWorker({commit}, registration){
        commit('SET_SERVICE_WORKER', registration)
      },
}