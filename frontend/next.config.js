/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/backend/:path*",
        destination: "https://ai-cloud-log-analyzer.onrender.com/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
