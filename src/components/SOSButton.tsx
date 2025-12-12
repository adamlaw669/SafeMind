/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from 'react';
import { PhoneCall, X, AlertOctagon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SOSButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating Button (Visible on ALL Pages) */}
      <div className="fixed bottom-6 right-6 z-[100]">
        <button
          onClick={() => setIsOpen(true)}
          className="group flex items-center gap-3 bg-emergency-600 hover:bg-emergency-500 text-white pl-4 pr-6 py-4 rounded-full shadow-2xl transition-all hover:scale-105 active:scale-95 border-4 border-white ring-4 ring-emergency-600/30 cursor-pointer"
        >
          <div className="relative">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-white opacity-75"></span>
            <PhoneCall className="relative h-6 w-6" />
          </div>
          <div className="text-left leading-tight">
            <span className="block font-black tracking-wider text-sm">SOS HELP</span>
            <span className="block text-[10px] opacity-90 font-medium">No Wallet Needed</span>
          </div>
        </button>
      </div>

      {/* The Emergency Modal */}
      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-[101] flex items-end sm:items-center justify-center p-4 sm:p-6">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm"
            />

            {/* Modal Content */}
            <motion.div
              initial={{ y: "100%", opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: "100%", opacity: 0 }}
              className="relative w-full max-w-md bg-white rounded-3xl shadow-2xl overflow-hidden"
            >
              <div className="bg-emergency-600 p-6 text-white text-center relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10"></div>
                
                <button 
                  onClick={() => setIsOpen(false)}
                  className="absolute top-4 right-4 p-2 bg-white/20 rounded-full hover:bg-white/30 transition cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>

                <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4 backdrop-blur-md border border-white/30">
                  <AlertOctagon className="w-8 h-8 text-white" />
                </div>
                <h2 className="text-2xl font-bold">Emergency Mode</h2>
                <p className="text-emergency-100 text-sm mt-1">
                  These calls are free and do not require internet or wallet connection.
                </p>
              </div>

              <div className="p-6 space-y-3 bg-slate-50">
                <a href="tel:112" className="flex items-center justify-between w-full bg-white border border-slate-200 p-4 rounded-xl shadow-sm hover:border-emergency-500 hover:shadow-md transition group">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-emergency-50 rounded-full flex items-center justify-center group-hover:bg-emergency-100 transition">
                      <PhoneCall className="w-5 h-5 text-emergency-600" />
                    </div>
                    <div className="text-left">
                      <h3 className="font-bold text-slate-800">Lagos Emergency</h3>
                      <p className="text-xs text-slate-500">For Ambulance, Fire, Police</p>
                    </div>
                  </div>
                  <span className="text-xl font-bold text-slate-900">112</span>
                </a>

                <a href="tel:08000333333" className="flex items-center justify-between w-full bg-white border border-slate-200 p-4 rounded-xl shadow-sm hover:border-purple-500 hover:shadow-md transition group">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-purple-50 rounded-full flex items-center justify-center group-hover:bg-purple-100 transition">
                      <Shield className="w-5 h-5 text-purple-600" />
                    </div>
                    <div className="text-left">
                      <h3 className="font-bold text-slate-800">Domestic Violence</h3>
                      <p className="text-xs text-slate-500">Lagos DSVRT Team</p>
                    </div>
                  </div>
                  <span className="text-sm font-bold text-purple-700 bg-purple-50 px-3 py-1 rounded-full">Call Now</span>
                </a>

                <button 
                  onClick={() => setIsOpen(false)}
                  className="w-full py-4 text-slate-400 font-medium text-sm hover:text-slate-600 cursor-pointer"
                >
                  Cancel and Return to App
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}

// Icon helper
function Shield(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
  );
}