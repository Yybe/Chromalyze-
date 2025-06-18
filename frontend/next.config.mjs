/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  webpack: (config, { isServer }) => {
    // Fix for prop-types and react-dropzone compatibility
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      path: false,
      crypto: false,
    };

    return config;
  }
}

export default nextConfig