import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FinanceGPT - AI-Powered Financial Analysis",
  description: "Advanced financial analysis platform powered by AI, real-time data, and comprehensive market insights",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50`}>
        {/* Simple Top Navigation Bar */}
        <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              {/* Logo */}
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">F</span>
                </div>
                <span className="font-bold text-gray-900 text-lg">FinanceGPT</span>
              </div>
              
              {/* Navigation Links */}
              <nav className="hidden md:flex space-x-8">
                <a href="#dashboard" className="text-gray-700 hover:text-blue-600 font-medium">Dashboard</a>
                <a href="#analysis" className="text-gray-700 hover:text-blue-600 font-medium">Analysis</a>
                <a href="#sentiment" className="text-gray-700 hover:text-blue-600 font-medium">Sentiment</a>
                <a href="#fundamentals" className="text-gray-700 hover:text-blue-600 font-medium">Fundamentals</a>
              </nav>
              
              {/* Action Button */}
              <div>
                <button className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-colors">
                  Get Started
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main>
          {children}
        </main>
      </body>
    </html>
  );
}
