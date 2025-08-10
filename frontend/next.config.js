module.exports = {
  reactStrictMode: true,
  // Enable environment variables
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000',
    MAPBOX_API_KEY: process.env.MAPBOX_API_KEY || '',
  },
  // Configure webpack
  webpack: (config, { isServer }) => {
    // Fixes npm packages that depend on `fs` module
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    return config;
  },
};