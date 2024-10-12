import theme from './theme.js';

export default {
  server: {
    host: '0.0.0.0',
    port: 3001,
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'pdp-frontend',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [// https://go.nuxtjs.dev/chakra
  '@chakra-ui/nuxt', // https://go.nuxtjs.dev/emotion
  '@nuxtjs/emotion', // 新增 @nuxtjs/proxy 模組
  '@nuxtjs/proxy', '@nuxt/ui'],

  // 配置 Chakra UI 主題
  chakra: {
    extendTheme: theme, // 這裡引用 theme.js 並擴展主題設定
  },

  // 代理設置
  proxy: {
    '/rp/': {
      target: "https://de.yuntech.poc.com:3443", // 你的 API 目標 URL
      secure: false, // 在開發環境中忽略 SSL 憑證
      changeOrigin: true, // 避免 CORS 問題
      pathRewrite: { '^/api/': '/' }, // 選擇性地重寫 URL 路徑
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
};