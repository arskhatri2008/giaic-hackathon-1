const path = require('path');

module.exports = function (context, options) {
  return {
    name: 'docusaurus-plugin-chatbot',

    getClientModules() {
      return [path.resolve(__dirname, './client-module.js')];
    },

    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@site/src/components/Chatbot': path.resolve(__dirname, '../../components/Chatbot'),
          },
        },
      };
    },
  };
};