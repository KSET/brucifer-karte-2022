module.exports = {
  transpileDependencies: true,

  chainWebpack: config => {
    config.module
      .rule('html')
      .test(/\.html$/)
      .use('html-loader')
      .loader('html-loader')
      .tap(options => {
        return {
          ...options,
          minimize: false, // You can set this to true if you want to minify HTML files
        };
      });
  },
};

