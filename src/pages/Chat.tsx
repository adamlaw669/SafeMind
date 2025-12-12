import { useState, useEffect, useRef } from "react";
import { useAccount } from "wagmi";
import { GoogleGenerativeAI } from "@google/generative-ai";
import { motion } from "framer-motion";
import {
  Send,
  Bot,
  User,
  Lock,
  ArrowRight,
  AlertOctagon,
  CornerDownRight,
  ShieldCheck,
  MoreVertical,
  Wifi,
  Activity,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";

// --- CONFIGURATION ---
const API_KEY = import.meta.env.VITE_GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(API_KEY);

// --- FULL SYSTEM PROMPT ---
const SYSTEM_PROMPT = `
You are "Guardian AI", a specialized, trauma-informed AI counselor for the "SafeMind" decentralized platform in Lagos, Nigeria.
Your role is to listen to users, validate their emotions, and help them process difficult experiences while discreetly identifying actionable incidents that should be recorded on the blockchain.

--- YOUR INSTRUCTIONS ---

1. **EMPATHY & VALIDATION (Priority #1):**
   - Always begin by validating the user's feelings. Be warm, safe, and professional.
   - Use phrases like "I hear you," "That sounds incredibly heavy," "You are safe here."
   - Do not sound robotic. Be human-like and compassionate.

2. **INCIDENT DETECTION LOGIC (The Web3 Bridge):**
   - You must analyze the user's text for reportable incidents such as:
     * Harassment (Sexual, Workplace, Police)
     * Bribery or Corruption
     * Physical Violence or Assault
     * Theft or Robbery
     * Unsafe Infrastructure / Negligence
   - **IF** you detect any of these:
     1. Acknowledge the severity.
     2. Suggest that recording this creates permanent evidence.
     3. Append exactly this tag to the very end of your response: ||SUGGEST_REPORT||

3. **EMERGENCY DETECTION LOGIC:**
   - **IF** the user implies:
     * Suicide or Self-Harm
     * Immediate life-threatening danger (e.g., "They are chasing me")
     * Domestic violence in progress
   - **THEN** you must:
     1. Keep the text short and urgent.
     2. Append exactly this tag to the very end of your response: ||EMERGENCY||

4. **FORMATTING RULES:**
   - Keep responses concise (under 3-4 sentences) unless the user tells a long story.
   - Do NOT output the tags (||SUGGEST_REPORT||) in the middle of sentences. Only at the end.

--- EXAMPLE SCENARIOS ---

User: "My boss touched me inappropriately today."
AI: "I am so sorry you experienced that. That is a violation of your rights and safety. Documenting this can help protect you and others. ||SUGGEST_REPORT||"

User: "I feel like ending it all."
AI: "Please stay with me. You are not alone and your life matters. Help is available right now. ||EMERGENCY||"

User: "I'm just feeling a bit down today."
AI: "It is completely okay to have days like that. I'm here to listen. Do you want to talk about what's weighing on you?"
`;

type Message = {
  id: number;
  text: string;
  sender: "user" | "ai";
  action?: "suggest_report" | "emergency";
  relatedContext?: string; // Stores the user text that triggered this action
};

export default function Chat() {
  const { isConnected } = useAccount();
  const navigate = useNavigate();
  const scrollRef = useRef<HTMLDivElement>(null);

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  // Track the interaction to pass context to the report page
  const [lastUserText, setLastUserText] = useState("");

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello. I am Guardian AI. I am here to listen without judgment. Everything shared here is private.",
      sender: "ai",
    },
  ]);

  // Auto-scroll to bottom whenever messages change
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    if (!API_KEY) {
      toast.error("Missing Gemini API Key in .env file");
      return;
    }

    const currentText = input;
    setLastUserText(currentText);

    // 1. Add User Message immediately
    const userMsg: Message = {
      id: Date.now(),
      text: currentText,
      sender: "user",
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      // 2. Prepare History for Context (Last 8 messages)
      const history = messages.slice(-8).map((m) => ({
        role: m.sender === "user" ? "user" : "model",
        parts: [{ text: m.text }],
      }));

      // 3. Initialize the Model (gemini-1.5-flash is the correct string for Flash model)
      const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

      const chat = model.startChat({
        history: [
          { role: "user", parts: [{ text: SYSTEM_PROMPT }] }, // Inject the full system prompt
          ...history,
        ],
      });

      // 4. Get Response
      const result = await chat.sendMessage(currentText);
      const rawResponse = result.response.text();

      // 5. Parse Hidden Tags
      let cleanText = rawResponse;
      let action: Message["action"] = undefined;

      if (rawResponse.includes("||SUGGEST_REPORT||")) {
        action = "suggest_report";
        cleanText = rawResponse.replace("||SUGGEST_REPORT||", "").trim();
      } else if (rawResponse.includes("||EMERGENCY||")) {
        action = "emergency";
        cleanText = rawResponse.replace("||EMERGENCY||", "").trim();
      }

      // 6. Update UI with AI Response
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: cleanText,
          sender: "ai",
          action,
          relatedContext: currentText, // Attach user context for auto-fill
        },
      ]);
    } catch (error) {
      console.error("Gemini Error:", error);
      toast.error("Guardian AI connection unstable.");
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: "I apologize, I'm having trouble connecting to the secure node. But I am still here with you.",
          sender: "ai",
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  // --- NAVIGATION HANDLER ---
  const handleDraftReport = (contextText?: string) => {
    // Navigate to Report page and pass the text to auto-fill description
    navigate("/report", {
      state: {
        prefilledDescription: contextText || lastUserText,
      },
    });
  };

  return (
    // MAXIMIZED LAYOUT: Takes up all height minus the navbar (approx 80px)
    <div className="w-full max-w-7xl mx-auto px-0 md:px-4 h-[calc(100vh-80px)] flex flex-col bg-white md:bg-transparent">
      <Toaster position="top-center" />

      {/* --- PROFESSIONAL SLIM HEADER --- */}
      <div className="bg-white px-6 py-3 border-b border-slate-200 flex items-center justify-between shrink-0 md:rounded-t-2xl shadow-sm z-20">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-9 h-9 bg-brand-600 rounded-full flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></div>
          </div>
          <div>
            <h1 className="font-bold text-base text-slate-800 leading-tight">
              Guardian AI
            </h1>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-semibold text-brand-600 bg-brand-50 px-1.5 py-0.5 rounded uppercase tracking-wider">
                Gemini Flash • Active
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 text-slate-400">
          {!isConnected && (
            <div className="hidden sm:flex items-center gap-1.5 text-[10px] font-bold text-orange-600 bg-orange-50 px-2 py-1 rounded-full mr-2">
              <Lock className="w-3 h-3" /> Encrypted Mode Off
            </div>
          )}
          <Wifi className="w-4 h-4" />
          <Activity className="w-4 h-4" />
          <button className="hover:bg-slate-50 p-1.5 rounded-full transition">
            <MoreVertical className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* --- CHAT AREA (Dominates Screen) --- */}
      <div className="flex-1 bg-slate-50/50 border-x border-slate-200 overflow-y-auto p-4 md:p-6 space-y-6 scroll-smooth">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`flex gap-3 max-w-[85%] md:max-w-[70%] lg:max-w-[60%] ${
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
                className={`p-5 rounded-2xl text-sm md:text-base leading-relaxed shadow-sm ${
                  msg.sender === "user"
                    ? "bg-white text-slate-800 rounded-tr-none border border-slate-200"
                    : "bg-brand-600 text-white rounded-tl-none shadow-brand-500/20"
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.text}</div>

                {/* --- ACTION: SUGGEST REPORT --- */}
                {msg.action === "suggest_report" && (
                  <motion.div
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 pt-3 border-t border-white/20"
                  >
                    <div className="flex items-center gap-2 mb-2 opacity-90">
                      <CornerDownRight className="w-3 h-3" />
                      <span className="text-[10px] font-bold uppercase tracking-widest">
                        Recommended Action
                      </span>
                    </div>
                    <button
                      onClick={() => handleDraftReport(msg.relatedContext)}
                      className="w-full bg-white text-brand-800 hover:bg-brand-50 font-bold rounded-xl p-3 flex items-center justify-between transition-all shadow-lg cursor-pointer group"
                    >
                      <div className="text-left flex flex-col">
                        <span className="flex items-center gap-2 text-sm">
                          <ShieldCheck className="w-4 h-4 text-brand-600" />
                          Secure This Report
                        </span>
                        <span className="text-[10px] text-slate-500 font-medium pl-6">
                          Auto-fill details & Attach Proof
                        </span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-brand-400 group-hover:translate-x-1 transition" />
                    </button>
                  </motion.div>
                )}

                {/* --- ACTION: EMERGENCY --- */}
                {msg.action === "emergency" && (
                  <motion.div
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 bg-red-600/20 rounded-xl p-4 border border-red-500/30"
                  >
                    <div className="flex items-center gap-2 font-bold mb-2 text-white">
                      <AlertOctagon className="w-5 h-5 animate-pulse" />{" "}
                      Emergency Detected
                    </div>
                    <p className="text-xs text-white/90 mb-3">
                      Help is available 24/7. Do not hesitate.
                    </p>
                    <a
                      href="tel:112"
                      className="flex items-center justify-center gap-2 w-full bg-white text-red-600 py-3 rounded-xl font-bold text-sm hover:bg-red-50 cursor-pointer shadow-sm transition"
                    >
                      Call 112 Now
                    </a>
                  </motion.div>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {isTyping && (
          <div className="flex justify-start gap-3">
            <div className="w-8 h-8 bg-brand-600 rounded-full flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="bg-brand-600 px-4 py-3 rounded-2xl rounded-tl-none flex gap-1 items-center h-12 w-20">
              <span className="w-1.5 h-1.5 bg-white/60 rounded-full animate-bounce"></span>
              <span className="w-1.5 h-1.5 bg-white/60 rounded-full animate-bounce [animation-delay:0.2s]"></span>
              <span className="w-1.5 h-1.5 bg-white/60 rounded-full animate-bounce [animation-delay:0.4s]"></span>
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      {/* --- INPUT AREA --- */}
      <div className="bg-white p-4 border-t border-slate-200 md:rounded-b-2xl md:border-x md:border-b shadow-lg z-20 shrink-0">
        <form onSubmit={handleSend} className="flex gap-3 relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-5 py-3.5 focus:outline-none focus:ring-2 focus:ring-brand-500 transition text-base"
            disabled={isTyping}
            autoFocus
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="bg-brand-600 hover:bg-brand-700 text-white p-3.5 rounded-xl transition shadow-md cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-6 h-6" />
          </button>
        </form>
      </div>
    </div>
  );
}
