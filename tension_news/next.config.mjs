/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ["serpapi.com", "encrypted-tbn0.gstatic.com"],
  },
  experimental: {
    typedRoutes: true,
  },
};

export default nextConfig;
