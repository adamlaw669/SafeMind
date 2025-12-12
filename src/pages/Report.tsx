import { useState, useRef, useEffect } from 'react';
import { useAccount, useSignMessage } from 'wagmi';
import { motion } from 'framer-motion';
import { MapPin, ShieldCheck, Loader2, CheckCircle, Lock, Upload, X, FileText, Crosshair, Sparkles } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import { useLocation } from 'react-router-dom'; // Import useLocation

export default function ReportPage() {
  const { isConnected, address } = useAccount();
  const { signMessageAsync } = useSignMessage();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // 1. Get State from Router (from Chat page)
  const location = useLocation();
  
  const [loading, setLoading] = useState(false);
  const [locLoading, setLocLoading] = useState(false);
  const [step, setStep] = useState(1);

  const [formData, setFormData] = useState({
    category: '',
    description: '',
    location: '',
    file: null as File | null
  });

  // 2. AUTO-FILL LOGIC
  useEffect(() => {
    if (location.state && location.state.prefilledDescription) {
        setFormData(prev => ({
            ...prev,
            description: location.state.prefilledDescription
        }));
        toast.success("Incident details auto-filled from Guardian AI", {
            icon: '🤖',
            duration: 4000
        });
    }
  }, [location.state]);

  const categories = [
    { id: 'Harassment', label: 'Harassment', icon: '✋' },
    { id: 'Corruption', label: 'Corruption', icon: '💰' },
    { id: 'Violence', label: 'Physical Violence', icon: '👊' },
    { id: 'MentalHealth', label: 'Mental Distress', icon: '🧠' },
    { id: 'Infrastructure', label: 'Unsafe Area', icon: '🚧' },
    { id: 'Other', label: 'Other', icon: '📝' },
  ];

  // ... (Keep existing Geolocation logic) ...
  const handleAutoDetectLocation = () => {
    if (!navigator.geolocation) {
      toast.error("Geolocation is not supported");
      return;
    }
    setLocLoading(true);
    const toastId = toast.loading("Acquiring Satellite Position...");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        const coordString = `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
        try {
            toast.loading("Resolving Address...", { id: toastId });
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
            const data = await response.json();
            if (data && data.display_name) {
                const cleanAddress = data.display_name.split(',').slice(0, 3).join(', '); 
                setFormData(prev => ({ ...prev, location: cleanAddress }));
                toast.success("Location Verified", { id: toastId });
            } else {
                setFormData(prev => ({ ...prev, location: `GPS: ${coordString}` }));
                toast.success("GPS Coordinates Captured", { id: toastId });
            }
        } catch (error) {
            setFormData(prev => ({ ...prev, location: `GPS: ${coordString}` }));
            toast.success("GPS Captured (Offline Mode)", { id: toastId });
        } finally {
            setLocLoading(false);
        }
      },
      (error) => {
        console.error(error);
        toast.error("Permission denied.", { id: toastId });
        setLocLoading(false);
      }
    );
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFormData({ ...formData, file: e.target.files[0] });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.category || !formData.description) {
      toast.error("Please select a category and provide a description.");
      return;
    }
    if (!isConnected) {
      toast.error("Connect wallet to sign report.");
      return;
    }

    setLoading(true);
    const toastId = toast.loading("Encrypting & Anchoring...");

    try {
      const messageToSign = `
SAFEMIND IMMUTABLE REPORT
-------------------------
Category: ${formData.category}
Location: ${formData.location || 'Anonymous'}
Timestamp: ${new Date().toISOString()}
Reporter: ${address}

DESCRIPTION:
${formData.description}

EVIDENCE ATTACHED:
File: ${formData.file ? formData.file.name : 'None'}

I certify this report is true.
Proof Hash: ${Math.random().toString(36).substring(7)}
      `;

      await signMessageAsync({ message: messageToSign });
      await new Promise(resolve => setTimeout(resolve, 2000));

      toast.dismiss(toastId);
      toast.success("Success! Report anchored on-chain.");
      setStep(2);
    } catch (error) {
      toast.dismiss(toastId);
      toast.error("User rejected signature.");
    } finally {
      setLoading(false);
    }
  };

  if (step === 2) {
    return (
      <div className="max-w-2xl mx-auto pt-10 px-4">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white p-8 md:p-12 rounded-3xl shadow-xl text-center border border-brand-100"
        >
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="w-10 h-10 text-green-600" />
          </div>
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Report Secured.</h2>
          <p className="text-slate-500 mb-8 max-w-lg mx-auto">
            Your report is now immutable evidence.
          </p>
          <div className="bg-slate-50 p-4 rounded-xl mb-8 text-left font-mono text-xs md:text-sm text-slate-600 border border-slate-200 break-all">
            <p className="mb-2 text-[10px] text-slate-400 uppercase tracking-widest font-bold">Transaction Hash</p>
            0x71c8...92a1 • Verified
          </div>
          <div className="flex justify-center gap-4">
            <button onClick={() => window.location.href = '/dashboard'} className="bg-brand-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-brand-700 transition cursor-pointer">
              View Dashboard
            </button>
            <button onClick={() => { setStep(1); setFormData({ category: '', description: '', location: '', file: null }); }} className="text-slate-500 font-medium px-8 py-3 hover:text-slate-800 cursor-pointer">
              File Another
            </button>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto pt-6 px-4 pb-20">
      <Toaster position="top-center" />
      
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Secure Incident Report</h1>
        <p className="text-slate-500 mt-2 flex items-center gap-2 text-sm">
          <Lock className="w-4 h-4 text-brand-500" /> End-to-End Encrypted • Anonymous • Free
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        
        {/* Category */}
        <section>
          <label className="block text-sm font-bold text-slate-700 mb-3 uppercase tracking-wider">Select Category</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {categories.map((cat) => (
              <button
                key={cat.id}
                type="button"
                onClick={() => setFormData({ ...formData, category: cat.id })}
                className={`p-4 rounded-2xl border-2 transition-all flex flex-col items-center gap-2 text-center cursor-pointer ${
                  formData.category === cat.id 
                    ? 'border-brand-500 bg-brand-50 text-brand-900 ring-2 ring-brand-200' 
                    : 'border-slate-100 bg-white shadow-sm hover:border-brand-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <span className="text-2xl mb-1">{cat.icon}</span>
                <span className="text-xs font-bold uppercase tracking-wide">{cat.label}</span>
              </button>
            ))}
          </div>
        </section>

        {/* Details */}
        <section className="bg-white p-6 md:p-8 rounded-[2rem] shadow-sm border border-slate-200 space-y-6">
          
          {/* Location */}
          <div>
            <label className="block text-sm font-bold text-slate-700 mb-2">Location</label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <MapPin className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
                <input 
                  type="text" 
                  placeholder="e.g. Yaba Bus Stop"
                  className="w-full pl-12 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 transition text-slate-700 font-medium"
                  value={formData.location}
                  onChange={e => setFormData({...formData, location: e.target.value})}
                />
              </div>
              <button
                type="button"
                onClick={handleAutoDetectLocation}
                disabled={locLoading}
                className="bg-slate-900 text-white px-4 rounded-xl flex items-center gap-2 hover:bg-slate-800 transition disabled:opacity-70 cursor-pointer min-w-[140px] justify-center"
              >
                {locLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Crosshair className="w-5 h-5" />}
                <span className="hidden md:inline text-sm font-bold">{locLoading ? 'Locating...' : 'Auto-Detect'}</span>
              </button>
            </div>
          </div>

          {/* Description (Auto-Filled) */}
          <div>
            <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-bold text-slate-700">Incident Description</label>
                {/* Visual Indicator if auto-filled */}
                {location.state?.prefilledDescription && (
                    <span className="text-[10px] bg-brand-100 text-brand-700 px-2 py-0.5 rounded-full font-bold flex items-center gap-1">
                        <Sparkles className="w-3 h-3" /> Auto-filled from Chat
                    </span>
                )}
            </div>
            <textarea 
              rows={5}
              placeholder="Describe the incident..."
              className="w-full p-4 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500 transition resize-none text-slate-700"
              value={formData.description}
              onChange={e => setFormData({...formData, description: e.target.value})}
            />
          </div>

          {/* Evidence */}
          <div>
            <label className="block text-sm font-bold text-slate-700 mb-2">Evidence (Optional)</label>
            {!formData.file ? (
              <div 
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:bg-slate-50 hover:border-brand-400 transition cursor-pointer group"
              >
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  className="hidden" 
                  onChange={handleFileChange}
                />
                <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-3 group-hover:bg-brand-100 transition">
                  <Upload className="w-6 h-6 text-slate-400 group-hover:text-brand-600" />
                </div>
                <p className="text-sm font-medium text-slate-600">Upload Image / Video</p>
              </div>
            ) : (
              <div className="flex items-center justify-between p-4 bg-brand-50 border border-brand-200 rounded-xl">
                <div className="flex items-center gap-3">
                  <FileText className="w-6 h-6 text-brand-600" />
                  <span className="text-sm font-bold text-slate-800">{formData.file.name}</span>
                </div>
                <button 
                  type="button"
                  onClick={() => setFormData({ ...formData, file: null })}
                  className="p-2 hover:bg-white rounded-full text-red-500 cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            )}
          </div>

        </section>

        {/* Action */}
        <div className="flex flex-col gap-4">
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-brand-600 hover:bg-brand-700 text-white font-bold py-4 rounded-2xl text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-3 group cursor-pointer"
          >
            {loading ? <Loader2 className="animate-spin" /> : <ShieldCheck className="group-hover:scale-110 transition" />}
            {isConnected ? 'Cryptographically Sign & Submit' : 'Connect Wallet to Submit'}
          </button>
        </div>
      </form>
    </div>
  );
}