// vue.config.js
const { defineConfig } = require('@vue/cli-service');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,

  chainWebpack: config => {
    config.module
      .rule('assets')
      .test(/\.(html|js|png|jpg|gif|mp3|json|txt)$/)
      .use('file-loader')
      .loader('file-loader')
      .tap(options => {
        return {
          ...options,
          name: 'assets/[name].[hash:8].[ext]',
        };
      });
  },
});
