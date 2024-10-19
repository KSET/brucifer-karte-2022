const { defineConfig } = require('@vue/cli-service');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,

  configureWebpack: {
    plugins: [
      // Copy the game files from src/assets/igrica to dist/igrica
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.resolve(__dirname, 'src/assets/igrica'),
            to: 'igrica',
          },
        ],
      }),
    ],
    module: {
      rules: [
        // Use file-loader for HTML files in the igrica directory
        {
          test: /\.html$/,
          include: path.resolve(__dirname, 'src/assets/igrica'),
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'igrica',
          },
        },
      ],
    },
  },

  chainWebpack: config => {
    // Exclude the 'igrica' directory from Webpack's processing
    config.module
      .rule('exclude-igrica')
      .test(() => true)
      .pre()
      .include.add(path.resolve(__dirname, 'src/assets/igrica'))
      .end()
      .use('null-loader')
      .loader('null-loader')
      .end();
  },
});
