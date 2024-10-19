// vue.config.js
const { defineConfig } = require('@vue/cli-service');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,

  configureWebpack: {
    plugins: [
      // Copy the game files from src/assets/igrica to dist/assets/igrica
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.resolve(__dirname, 'src/assets/igrica'),
            to: 'assets/igrica',
            noErrorOnMissing: true, // Prevent errors if the source folder is missing
          },
        ],
      }),
    ],
  },

  chainWebpack: config => {
    const igricaPath = path.resolve(__dirname, 'src/assets/igrica');

    // Exclude the 'igrica' directory from default asset processing rules
    config.module.rule('images').exclude.add(igricaPath).end();
    config.module.rule('media').exclude.add(igricaPath).end();
    config.module.rule('fonts').exclude.add(igricaPath).end();
    config.module.rule('svg').exclude.add(igricaPath).end();

    // Create a new rule to handle files in 'igrica' directory without processing
    config.module
      .rule('copy-igrica')
      .test(/\.(html|js|json|data|mem|wasm|png|jpe?g|gif|mp3|ogg|wav|mp4|webm|css)$/i)
      .include.add(igricaPath)
      .end()
      .type('asset/resource')
      .set('generator', {
        filename: 'assets/igrica/[name][ext]',
      });
  },
});
