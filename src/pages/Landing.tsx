import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shield,  Activity, ArrowRight, Zap, Globe, Server } from 'lucide-react';

export default function Landing() {
  return (
    <div className="relative overflow-hidden w-full">
      
      {/* --- BACKGROUND EFFECTS --- */}
      {/* Mint Gradient Blob */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[700px] bg-gradient-to-b from-brand-50 to-transparent pointer-events-none -z-10" />
      {/* Glowing Orb Right */}
      <div className="absolute top-20 right-0 w-96 h-96 bg-brand-200/40 rounded-full blur-[100px] -z-10" />
      {/* Glowing Orb Left */}
      <div className="absolute top-40 left-0 w-72 h-72 bg-purple-200/30 rounded-full blur-[80px] -z-10" />

      {/* --- 1. LIVE SYSTEM TICKER --- */}
      <div className="bg-slate-900 text-white text-[10px] md:text-xs font-medium py-2.5 overflow-hidden border-b border-slate-800">
        <div className="flex items-center justify-center gap-6 md:gap-12 opacity-90">
          <span className="flex items-center gap-2 text-green-400">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            System Operational
          </span>
          <span className="hidden sm:flex items-center gap-2">
            <Shield className="w-3 h-3 text-brand-400" /> 
            14 Reports Secured on Blockchain Today
          </span>
          <span className="flex items-center gap-2">
            <Activity className="w-3 h-3 text-brand-400" /> 
            Live Nodes: Lagos, Abuja, Port Harcourt
          </span>
        </div>
      </div>

      {/* --- 2. HERO SECTION --- */}
      <section className="pt-16 pb-20 md:pt-24 md:pb-32 px-4 max-w-7xl mx-auto text-center relative z-10">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-white/60 backdrop-blur-sm border border-brand-200 rounded-full px-4 py-1.5 shadow-sm mb-8 hover:bg-white/80 transition cursor-default">
            <span className="text-xs font-bold text-brand-700 tracking-wide uppercase">Lagos Impact Hackathon 2025 • SDG 16</span>
          </div>

          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-black text-slate-900 tracking-tight mb-6 leading-[1.1]">
            Report Injustice. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 to-teal-400">
              Recover Safely.
            </span>
          </h1>
          
          {/* Subheadline */}
          <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto mb-10 leading-relaxed font-light">
            The first decentralized platform for anonymous reporting and mental wellness. 
            We use <span className="font-semibold text-slate-900">Ethereum</span> to ensure your story is immutable, uncensorable, and heard.
          </p>
          
          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link 
              to="/report" 
              className="w-full sm:w-auto bg-slate-900 text-white px-8 py-4 rounded-2xl text-lg font-bold shadow-xl hover:shadow-2xl hover:bg-slate-800 transition transform hover:-translate-y-1 flex items-center justify-center gap-3 group"
            >
              <Shield className="w-5 h-5 text-brand-400 group-hover:scale-110 transition" />
              Start Anonymous Report
            </Link>
            <Link 
              to="/dashboard" 
              className="w-full sm:w-auto bg-white text-slate-700 border border-slate-200 px-8 py-4 rounded-2xl text-lg font-bold hover:bg-slate-50 transition flex items-center justify-center gap-2 group"
            >
              <Activity className="w-5 h-5 text-slate-400 group-hover:text-brand-500 transition" />
              View Public Data
            </Link>
          </div>

          {/* Tech Stack / Trust */}
          <div className="mt-16 pt-8 border-t border-brand-100/50 flex flex-col items-center">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-6">Secured By Decentralized Tech</p>
            <div className="flex flex-wrap justify-center gap-8 md:gap-16 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
               <div className="flex items-center gap-2 font-bold text-slate-700 text-lg"><Globe className="w-5 h-5"/> Ethereum</div>
               <div className="flex items-center gap-2 font-bold text-slate-700 text-lg"><Server className="w-5 h-5"/> IPFS Storage</div>
               <div className="flex items-center gap-2 font-bold text-slate-700 text-lg"><Zap className="w-5 h-5"/> WalletConnect</div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* --- 3. HOW IT WORKS --- */}
      <section className="py-24 bg-white relative">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900">How SafeMind Protects You</h2>
            <p className="text-slate-500 mt-3 text-lg">Advanced cryptography, simple human experience.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 relative">
            {/* Connecting Line (Desktop Only) */}
            <div className="hidden md:block absolute top-12 left-20 right-20 h-0.5 bg-gradient-to-r from-brand-100 via-purple-100 to-brand-100 -z-10" />

            {/* Step 1 */}
            <motion.div 
              whileHover={{ y: -5 }}
              className="bg-white p-8 rounded-[2rem] border border-slate-100 shadow-xl shadow-slate-200/50 relative"
            >
              <div className="w-14 h-14 bg-brand-50 rounded-2xl flex items-center justify-center mb-6 text-2xl font-bold text-brand-600 border border-brand-100 mx-auto md:mx-0">
                1
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Connect Wallet</h3>
              <p className="text-slate-500 leading-relaxed">
                No email. No phone number. Your wallet address is your only identity. This guarantees <strong className="text-brand-600">100% anonymity</strong> from the start.
              </p>
            </motion.div>

            {/* Step 2 */}
            <motion.div 
              whileHover={{ y: -5 }}
              className="bg-white p-8 rounded-[2rem] border border-slate-100 shadow-xl shadow-slate-200/50 relative"
            >
              <div className="w-14 h-14 bg-purple-50 rounded-2xl flex items-center justify-center mb-6 text-2xl font-bold text-purple-600 border border-purple-100 mx-auto md:mx-0">
                2
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Submit & Sign</h3>
              <p className="text-slate-500 leading-relaxed">
                Fill the secure form. Your wallet <strong className="text-purple-600">cryptographically signs</strong> the data, anchoring an immutable proof on-chain.
              </p>
            </motion.div>

            {/* Step 3 */}
            <motion.div 
              whileHover={{ y: -5 }}
              className="bg-white p-8 rounded-[2rem] border border-slate-100 shadow-xl shadow-slate-200/50 relative"
            >
              <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center mb-6 text-2xl font-bold text-blue-600 border border-blue-100 mx-auto md:mx-0">
                3
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Verified Impact</h3>
              <p className="text-slate-500 leading-relaxed">
                Agencies receive verified reports. Our AI updates the <strong className="text-blue-600">Public Heatmap</strong>, helping NGOs deploy resources instantly.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* --- 4. CALL TO ACTION (Bottom) --- */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto bg-slate-900 rounded-[2.5rem] p-10 md:p-20 text-center relative overflow-hidden shadow-2xl">
          {/* Decorative glowing orb */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-brand-500/20 rounded-full blur-[100px] pointer-events-none" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500/20 rounded-full blur-[100px] pointer-events-none" />
          
          <div className="relative z-10">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              Build a Safer Lagos.
            </h2>
            <p className="text-slate-300 text-lg mb-10 max-w-xl mx-auto">
              Whether you are a victim, an observer, or an NGO, your participation creates the data we need for policy change.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/report" className="bg-brand-500 text-white px-8 py-4 rounded-2xl font-bold hover:bg-brand-400 transition shadow-lg shadow-brand-500/25">
                Report Incident Now
              </Link>
              <a href="mailto:partners@safemind.ng" className="text-white px-8 py-4 rounded-2xl font-bold border border-slate-700 hover:bg-slate-800 transition flex items-center justify-center gap-2">
                For Government & NGOs <ArrowRight className="w-4 h-4"/>
              </a>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}