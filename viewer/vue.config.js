const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.module
      .rule('raw')
      .test(/\.mustache$/)
      .use('raw-loader')
      .loader('raw-loader')
      .end();
  }
});
