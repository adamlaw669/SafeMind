import { useState } from 'react';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { BrainCircuit, Menu, X, LayoutDashboard } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  // User-facing links
  const userLinks = [
    { name: 'Home', path: '/' },
    { name: 'Report Incident', path: '/report' },
    { name: 'AI Companion', path: '/chat' },
  ];

  return (
    <nav className="sticky top-0 z-[50] w-full bg-white/90 backdrop-blur-xl border-b border-slate-200/60 shadow-sm transition-all h-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
        <div className="flex justify-between h-full items-center">
          
          {/* LOGO */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="relative flex items-center justify-center w-9 h-9 bg-brand-600 rounded-lg shadow-md group-hover:bg-brand-700 transition">
              <BrainCircuit className="text-white w-5 h-5" />
            </div>
            <span className="text-lg font-black tracking-tight text-slate-900">SafeMind</span>
          </Link>

          {/* DESKTOP NAV */}
          <div className="hidden md:flex items-center gap-1">
            {userLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${
                  isActive(link.path)
                    ? 'text-brand-700 bg-brand-50'
                    : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                {link.name}
              </Link>
            ))}
            
            {/* Divider */}
            <div className="h-6 w-px bg-slate-200 mx-2"></div>

            {/* NGO Portal Link (Distinct) */}
            <Link
                to="/dashboard"
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold border transition-all ${
                  isActive('/dashboard')
                    ? 'bg-slate-800 text-white border-slate-800 shadow-md'
                    : 'bg-white text-slate-700 border-slate-200 hover:border-slate-400'
                }`}
            >
                <LayoutDashboard className="w-4 h-4" />
                Agency Portal
            </Link>
          </div>

          {/* WALLET & MOBILE TOGGLE */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:block">
               <ConnectButton showBalance={false} accountStatus="avatar" />
            </div>

            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-2 rounded-lg bg-slate-100 text-slate-600"
            >
              {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* MOBILE MENU */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden border-b border-slate-200 bg-white overflow-hidden absolute w-full left-0 top-20 shadow-xl"
          >
            <div className="px-4 py-6 space-y-3">
              {userLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="block px-4 py-3 rounded-lg text-base font-bold text-slate-600 hover:bg-slate-50"
                >
                  {link.name}
                </Link>
              ))}
              <Link
                  to="/dashboard"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="block px-4 py-3 rounded-lg text-base font-bold bg-slate-800 text-white"
              >
                  Agency Portal
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}