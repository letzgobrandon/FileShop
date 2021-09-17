const { InjectManifest } = require("workbox-webpack-plugin");

module.exports = {
  publicPath: '/',
  devServer: {
    disableHostCheck: true
  },

  pwa: {
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      swSrc: "src/service-worker.js",
    }
  }

}
