import { useState, useEffect, useRef } from "react";
import { useAccount } from "wagmi";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { motion } from "framer-motion";
import {
  Send,
  Bot,
  User,
  // Lock, 
  ArrowRight,
  AlertOctagon,
  // CornerDownRight, 
  ShieldCheck,
  MoreVertical,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";

// --- CONFIG ---
const API_KEY = import.meta.env.VITE_GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(API_KEY);

const SYSTEM_PROMPT = `
You are "Guardian AI", a professional trauma-informed assistant for "SafeMind".
1. Validate feelings briefly.
2. If the user describes a crime/harassment/injustice, append "||SUGGEST_REPORT||".
3. If immediate danger, append "||EMERGENCY||".
4. Keep responses concise and professional.
`;

type Message = {
  id: number;
  text: string;
  sender: "user" | "ai";
  action?: "suggest_report" | "emergency";
  relatedContext?: string;
};

export default function Chat() {
  const { isConnected } = useAccount();
  const navigate = useNavigate();
  const scrollRef = useRef<HTMLDivElement>(null);

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [lastUserText, setLastUserText] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello. I am Guardian AI. I am here to listen. Everything shared here is private.",
      sender: "ai",
    },
  ]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    if (!API_KEY) {
      toast.error("API Key missing");
      return;
    }

    const currentText = input;
    setLastUserText(currentText);

    const userMsg: Message = {
      id: Date.now(),
      text: currentText,
      sender: "user",
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const history = messages.slice(-6).map((m) => ({
        role: m.sender === "user" ? "user" : "model",
        parts: [{ text: m.text }],
      }));

      const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
      const chat = model.startChat({
        history: [
          { role: "user", parts: [{ text: SYSTEM_PROMPT }] },
          ...history,
        ],
      });

      const result = await chat.sendMessage(currentText);
      const rawResponse = result.response.text();

      let cleanText = rawResponse;
      let action: Message["action"] = undefined;

      if (rawResponse.includes("||SUGGEST_REPORT||")) {
        action = "suggest_report";
        cleanText = rawResponse.replace("||SUGGEST_REPORT||", "").trim();
      } else if (rawResponse.includes("||EMERGENCY||")) {
        action = "emergency";
        cleanText = rawResponse.replace("||EMERGENCY||", "").trim();
      }

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: cleanText,
          sender: "ai",
          action,
          relatedContext: currentText,
        },
      ]);
    } catch (error) {
      toast.error("Connection unstable");
    } finally {
      setIsTyping(false);
    }
  };

  const handleDraftReport = (contextText?: string) => {
    navigate("/report", {
      state: { prefilledDescription: contextText || lastUserText },
    });
  };

  return (
    // MAXIMIZED LAYOUT: Fixed height relative to navbar (approx 80px)
    <div className="w-full max-w-7xl mx-auto px-0 md:px-4 h-[calc(100vh-80px)] flex flex-col bg-white md:bg-transparent">
      <Toaster position="top-center" />

      {/* --- PROFESSIONAL HEADER (Slim) --- */}
      <div className="bg-white px-6 py-3 border-b border-slate-200 flex items-center justify-between shrink-0 md:rounded-t-2xl shadow-sm z-20">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-brand-600 rounded-full flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-base text-slate-800 leading-tight">
              Guardian AI
            </h1>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
                Online • Encrypted
              </span>
            </div>
          </div>
        </div>
        <button className="text-slate-400 hover:text-slate-600">
          <MoreVertical className="w-5 h-5" />
        </button>
      </div>

      {/* --- CHAT AREA (Fills Space) --- */}
      <div className="flex-1 bg-slate-50 border-x border-slate-200 overflow-y-auto p-4 md:p-6 space-y-6 scroll-smooth">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`flex gap-3 max-w-[85%] md:max-w-[70%] ${
                msg.sender === "user" ? "flex-row-reverse" : "flex-row"
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center mt-1 ${
                  msg.sender === "user"
                    ? "bg-white border border-slate-200"
                    : "bg-brand-600 text-white"
                }`}
              >
                {msg.sender === "user" ? (
                  <User className="w-4 h-4 text-slate-400" />
                ) : (
                  <Bot className="w-5 h-5" />
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={`p-4 rounded-2xl text-sm md:text-base leading-relaxed shadow-sm ${
                  msg.sender === "user"
                    ? "bg-white text-slate-800 rounded-tr-none border border-slate-200"
                    : "bg-brand-600 text-white rounded-tl-none"
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.text}</div>

                {/* Report Action */}
                {msg.action === "suggest_report" && (
                  <motion.div
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 pt-3 border-t border-white/20"
                  >
                    <button
                      onClick={() => handleDraftReport(msg.relatedContext)}
                      className="w-full bg-white text-brand-800 hover:bg-brand-50 font-bold rounded-xl p-3 flex items-center justify-between transition-all shadow-sm cursor-pointer"
                    >
                      <div className="text-left flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4 text-brand-600" />
                        <span className="text-sm">Draft Secure Report</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-brand-400" />
                    </button>
                  </motion.div>
                )}

                {/* Emergency Action */}
                {msg.action === "emergency" && (
                  <motion.div
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-3 bg-red-600/20 rounded-lg p-3 border border-red-500/30"
                  >
                    <a
                      href="tel:112"
                      className="flex items-center justify-center gap-2 w-full bg-white text-red-600 py-2 rounded-lg font-bold text-xs hover:bg-red-50 cursor-pointer"
                    >
                      <AlertOctagon className="w-4 h-4" /> Call 112
                    </a>
                  </motion.div>
                )}
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex gap-3">
            <div className="w-8 h-8 bg-brand-600 rounded-full flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="bg-brand-600 px-4 py-3 rounded-2xl rounded-tl-none flex gap-1 items-center">
              <span className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-white/60 rounded-full animate-bounce [animation-delay:0.2s]"></span>
              <span className="w-2 h-2 bg-white/60 rounded-full animate-bounce [animation-delay:0.4s]"></span>
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      {/* --- INPUT AREA --- */}
      <div className="bg-white p-4 border-t border-slate-200 md:rounded-b-2xl md:border-x md:border-b shadow-lg z-20 shrink-0">
        <form onSubmit={handleSend} className="flex gap-2 relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-500 transition"
            disabled={isTyping}
            autoFocus
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="bg-brand-600 hover:bg-brand-700 text-white p-3 rounded-xl transition shadow-md cursor-pointer"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
