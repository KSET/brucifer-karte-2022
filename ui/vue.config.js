const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    // emit .wasm as a plain file (used for the QR decoder) instead of a webpack wasm module
    config.module.rule('wasm').test(/\.wasm$/).type('asset/resource')
  }
})
