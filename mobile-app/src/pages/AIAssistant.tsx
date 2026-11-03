import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Send,
  ArrowRight,
  RefreshCw,
  Copy,
  Check,
  Download,
  ExternalLink,
  Calculator,
  BookOpen,
  X,
  Smile,
  Paperclip,
  Mic,
  Settings,
  Sparkles,
  Leaf,
  ShieldCheck,
  CheckCheck,
  Terminal,
} from 'lucide-react';
import { ChatMessage, AssistantEngineStatus } from '../types';
import { assistantService } from '../services/assistantService';
import { authService } from '../services/authService';

// Zero-dependency Rich Code & Markdown renderer
const RenderMarkdown: React.FC<{ content: string }> = ({ content }) => {
  const lines = content.split('\n');
  const elements: React.ReactNode[] = [];

  let inTable = false;
  let tableRows: string[][] = [];
  let inCodeBlock = false;
  let codeBlockLang = '';
  let codeBlockLines: string[] = [];

  const flushTable = () => {
    if (tableRows.length > 0) {
      const header = tableRows[0];
      const body = tableRows.slice(1).filter((r) => !r.every((c) => c.match(/^[:\-\s]+$/)));
      elements.push(
        <div key={`table-${elements.length}`} className="my-3 overflow-x-auto rounded-xl border border-gray-200 shadow-2xs">
          <table className="min-w-full divide-y divide-gray-200 text-xs">
            <thead className="bg-gray-100/90 font-bold text-gray-700">
              <tr>
                {header.map((col, idx) => (
                  <th key={idx} className="px-3 py-2 text-left">{col.trim()}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 bg-white">
              {body.map((row, rIdx) => (
                <tr key={rIdx} className={rIdx % 2 === 0 ? 'bg-white' : 'bg-gray-50/60'}>
                  {row.map((cell, cIdx) => (
                    <td key={cIdx} className="px-3 py-2 text-gray-800 font-mono text-[11px] sm:text-xs">{cell.trim()}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      tableRows = [];
    }
    inTable = false;
  };

  const flushCodeBlock = () => {
    if (inCodeBlock) {
      const codeString = codeBlockLines.join('\n');
      elements.push(
        <CodeBlockViewer
          key={`code-${elements.length}`}
          language={codeBlockLang || 'code'}
          code={codeString}
        />
      );
      codeBlockLines = [];
      inCodeBlock = false;
      codeBlockLang = '';
    }
  };

  const formatInline = (text: string): React.ReactNode => {
    // 1. Links [text](url)
    const linkRegex = /\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g;
    const parts: React.ReactNode[] = [];
    let lastIndex = 0;
    let match;

    while ((match = linkRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push(formatFormatting(text.substring(lastIndex, match.index)));
      }
      parts.push(
        <a
          key={`link-${match.index}`}
          href={match[2]}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[#027eb5] hover:text-[#005c4b] underline font-semibold inline-flex items-center gap-0.5"
        >
          {match[1]}
          <ExternalLink className="w-2.5 h-2.5 inline" />
        </a>
      );
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < text.length) {
      parts.push(formatFormatting(text.substring(lastIndex)));
    }
    return parts.length > 0 ? parts : text;
  };

  const formatFormatting = (raw: string): React.ReactNode => {
    // Inline code `code`
    const codeRegex = /`([^`]+)`/g;
    const segments: React.ReactNode[] = [];
    let cur = 0;
    let cm;

    while ((cm = codeRegex.exec(raw)) !== null) {
      if (cm.index > cur) {
        segments.push(formatBold(raw.substring(cur, cm.index)));
      }
      segments.push(
        <code key={`inline-code-${cm.index}`} className="px-1.5 py-0.5 mx-0.5 rounded bg-gray-100 text-[#005c4b] font-mono text-[11px] font-bold border border-gray-200">
          {cm[1]}
        </code>
      );
      cur = cm.index + cm[0].length;
    }
    if (cur < raw.length) {
      segments.push(formatBold(raw.substring(cur)));
    }
    return segments;
  };

  const formatBold = (raw: string): React.ReactNode => {
    // Bold **text**
    const boldRegex = /\*\*([^*]+)\*\*/g;
    const pieces: React.ReactNode[] = [];
    let last = 0;
    let m;
    while ((m = boldRegex.exec(raw)) !== null) {
      if (m.index > last) pieces.push(raw.substring(last, m.index));
      pieces.push(<strong key={m.index} className="font-bold text-gray-950">{m[1]}</strong>);
      last = m.index + m[0].length;
    }
    if (last < raw.length) pieces.push(raw.substring(last));
    return pieces;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Fenced Code Block start / end
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        flushCodeBlock();
      } else {
        if (inTable) flushTable();
        inCodeBlock = true;
        codeBlockLang = line.trim().replace('```', '').trim();
      }
      continue;
    }

    if (inCodeBlock) {
      codeBlockLines.push(line);
      continue;
    }

    // Markdown Table row
    if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
      inTable = true;
      const cols = line.trim().split('|').slice(1, -1);
      tableRows.push(cols);
      continue;
    } else if (inTable) {
      flushTable();
    }

    // Section Headings
    if (line.startsWith('### ')) {
      const heading = line.replace('### ', '');
      elements.push(
        <div key={`h3-${i}`} className="mt-3.5 mb-1.5 flex items-center gap-2">
          <span className="w-1.5 h-4 rounded-full bg-gradient-to-b from-[#00d2ff] to-[#9d4edd]"></span>
          <h4 className="text-xs sm:text-sm font-extrabold text-[#111b21] tracking-tight">{heading}</h4>
        </div>
      );
      continue;
    }

    if (line.startsWith('## ')) {
      const heading = line.replace('## ', '');
      elements.push(
        <h3 key={`h2-${i}`} className="text-sm sm:text-base font-extrabold text-[#111b21] mt-3 mb-1">
          {heading}
        </h3>
      );
      continue;
    }

    // Unordered Bullet
    if (line.trim().startsWith('• ') || line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
      const text = line.trim().replace(/^[•\-\*]\s+/, '');
      elements.push(
        <div key={`li-${i}`} className="flex items-start gap-2 my-1 text-xs sm:text-sm text-gray-800 pl-1 leading-relaxed">
          <span className="text-[#00a884] font-bold mt-1 text-[10px]">●</span>
          <div className="flex-1">{formatInline(text)}</div>
        </div>
      );
      continue;
    }

    // Ordered List
    const numMatch = line.trim().match(/^(\d+)\.\s+(.*)$/);
    if (numMatch) {
      elements.push(
        <div key={`ol-${i}`} className="flex items-start gap-2 my-1 text-xs sm:text-sm text-gray-800 pl-1 leading-relaxed">
          <span className="w-4 h-4 rounded-full bg-emerald-100 text-[#005c4b] font-bold text-[10px] flex items-center justify-center shrink-0 mt-0.5">
            {numMatch[1]}
          </span>
          <div className="flex-1">{formatInline(numMatch[2])}</div>
        </div>
      );
      continue;
    }

    // Empty lines
    if (!line.trim()) {
      elements.push(<div key={`sp-${i}`} className="h-1.5" />);
      continue;
    }

    // Standard paragraph
    elements.push(
      <p key={`p-${i}`} className="text-xs sm:text-sm text-gray-800 leading-relaxed">
        {formatInline(line)}
      </p>
    );
  }

  if (inTable) flushTable();
  if (inCodeBlock) flushCodeBlock();

  return <div className="space-y-1">{elements}</div>;
};

// Sleek Code Block Viewer with Copy Button
const CodeBlockViewer: React.FC<{ language: string; code: string }> = ({ language, code }) => {
  const [copied, setCopied] = useState(false);

  const handleCopyCode = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-2.5 rounded-xl overflow-hidden bg-[#1e1e1e] border border-gray-800 text-gray-200 text-xs shadow-md">
      <div className="flex items-center justify-between px-3.5 py-1.5 bg-[#2d2d2d] border-b border-gray-700/60 text-[11px] font-mono">
        <span className="text-cyan-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
          <Terminal className="w-3 h-3 text-cyan-400" />
          {language || 'code'}
        </span>
        <button
          onClick={handleCopyCode}
          className="flex items-center gap-1 text-gray-400 hover:text-white transition-colors"
        >
          {copied ? (
            <>
              <Check className="w-3 h-3 text-emerald-400" />
              <span className="text-emerald-400 font-semibold text-[10px]">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3 h-3" />
              <span className="text-[10px]">Copy code</span>
            </>
          )}
        </button>
      </div>
      <pre className="p-3.5 overflow-x-auto font-mono text-[11px] leading-relaxed text-gray-100">
        <code>{code}</code>
      </pre>
    </div>
  );
};

export const AIAssistant: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome-meta-ai',
      sender: 'assistant',
      content:
        "### 1. Direct Answer\n" +
        "Hello! I am your **AGRO AI Assistant**. 🚀\n\n" +
        "### 2. Ask Me Anything!\n" +
        "• **Programming & Coding**: Python algorithms, JavaScript, SQL queries, debugging & web dev.\n" +
        "• **Mathematics & Calculations**: Percentage calculations, algebra, formulas, and farm math.\n" +
        "• **Agricultural Sciences**: general crop and soil guidance, symptom screening, IPM concepts, and farm calculations. Confirm high-impact field decisions with local agricultural experts.\n" +
        "• **World Knowledge & STEM**: Physics, aerodynamics, biographies (Elon Musk, Abdul Kalam), and astronomy.\n" +
        "• **Daily Life & Cooking**: Authentic recipes (Paneer Butter Masala, Masala Chai), habits, and health.\n\n" +
        "How can I help you right now?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      category: 'general',
      suggestedQuestions: [
        'Write python code to reverse a string',
        'What is 15% of 800?',
        'Who is Elon Musk?',
        'How do I identify and manage Tomato Early Blight with IPM?',
      ],
    },
  ]);

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [engineStatus, setEngineStatus] = useState<AssistantEngineStatus | null>(null);
  const [sessionId, setSessionId] = useState<string>(() => `wa-session-${Date.now()}`);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [showCalculatorModal, setShowCalculatorModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [canConfigureAI, setCanConfigureAI] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [showAttachmentMenu, setShowAttachmentMenu] = useState(false);

  const chatBottomRef = useRef<HTMLDivElement>(null);

  const quickPrompts = [
    { label: '💻 Reverse a String in Python', query: 'Write a python function to reverse a string with tests' },
    { label: '🧮 15% of 800 Calculation', query: 'What is 15% of 800?' },
    { label: '🚀 Who is Elon Musk?', query: 'Who is Elon Musk and what are his major achievements?' },
    { label: '✈️ How Airplanes Fly', query: 'Explain how airplanes generate lift and fly' },
    { label: '🍲 Paneer Butter Masala', query: 'How to make authentic restaurant-style Paneer Butter Masala?' },
    { label: '🌾 Tomato Early Blight IPM', query: 'How do I identify and manage Tomato Early Blight with IPM?' },
    { label: '🧪 NPK 120:60:40 Dosage', query: 'Calculate NPK fertilizer requirement for 1 hectare wheat (120:60:40)' },
    { label: '🪨 Black Vertisol Soil Guide', query: 'What are suitable crops and soil amendments for Black Soil?' },
  ];

  const quickEmojis = ['🌱', '🌾', '💡', '🧮', '💻', '🔬', '🍲', '🍎', '🚀', '⚡', '📊', '🧪'];

  useEffect(() => {
    assistantService.getEngineStatus().then((status) => setEngineStatus(status));
    authService.getCurrentUser().then((user) => setCanConfigureAI(user?.role === 'admin')).catch(() => setCanConfigureAI(false));
  }, []);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (userText: string) => {
    if (!userText.trim() || loading) return;

    setShowEmojiPicker(false);
    setShowAttachmentMenu(false);

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      content: userText.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await assistantService.sendMessage(userText, messages, sessionId);
      if (response.sessionId) {
        setSessionId(response.sessionId);
      }

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        content: response.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        category: response.category,
        evidenceSources: response.evidenceSources,
        suggestedQuestions: response.suggestedQuestions,
        calculatorData: response.calculatorData,
        modelProvider: response.modelProvider,
        relatedAction: response.relatedAction,
        savedToAccount: response.savedToAccount,
        persistenceMessage: response.persistenceMessage,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        sender: 'assistant',
        content: `I could not get a response from the AGRO AI backend: ${err?.message || 'Unknown connection error'}. Please check the connection and try again. This message is not an AI-generated answer and has not been saved as a successful response.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        category: 'general',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = async () => {
    await assistantService.clearSession(sessionId);
    const newSid = `wa-session-${Date.now()}`;
    setSessionId(newSid);
    setMessages([
      {
        id: `reset-${Date.now()}`,
        sender: 'assistant',
        content:
          "### 1. Direct Answer\nChat cleared! I am your AGRO AI Assistant, ready to answer questions on programming, mathematics, science, cooking, or evidence-based agricultural advice.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        category: 'general',
      },
    ]);
  };

  const handleCopy = (msgId: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(msgId);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const handleExportAdvisory = (msg: ChatMessage) => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    let advisoryContent = `# AGRO AI Assistant Report\nGenerated: ${new Date().toLocaleString()}\nCategory: ${msg.category || 'General'}\n\n`;
    advisoryContent += msg.content + '\n\n';

    if (msg.evidenceSources && msg.evidenceSources.length > 0) {
      advisoryContent += `## Authoritative Sources & Citations\n`;
      msg.evidenceSources.forEach((src, idx) => {
        advisoryContent += `${idx + 1}. **${src.title}**\n   Organization: ${src.organization} (${src.year})\n   URL: ${src.url}\n\n`;
      });
    }

    const blob = new Blob([advisoryContent], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `agro_ai_response_${timestamp}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-[#f0f2f5] flex flex-col justify-between">
      {/* WhatsApp Chat Outer Card */}
      <div className="max-w-5xl mx-auto w-full flex-1 flex flex-col my-3 sm:my-5 px-2 sm:px-4">
        
        {/* WhatsApp & AGRO AI Header Bar */}
        <div className="bg-[#005c4b] text-white px-4 py-3 sm:px-5 sm:py-3.5 rounded-t-2xl shadow-md flex items-center justify-between gap-3">
          {/* Avatar and Agent Info */}
          <div className="flex items-center gap-3">
            {/* AGRO AI Glowing Iridescent Ring Avatar */}
            <div className="relative flex items-center justify-center w-11 h-11 rounded-full p-[2.5px] bg-gradient-to-tr from-[#00d2ff] via-[#3a7bd5] via-[#a17fe0] to-[#f857a6] shadow-md">
              <div className="w-full h-full bg-[#111b21] rounded-full flex items-center justify-center overflow-hidden">
                <div className="w-5 h-5 rounded-full bg-gradient-to-tr from-[#00d2ff] via-[#a17fe0] to-[#f857a6] blur-[1px] opacity-90"></div>
              </div>
              <span className="absolute bottom-0 right-0 w-3 h-3 bg-emerald-400 border-2 border-[#005c4b] rounded-full animate-pulse"></span>
            </div>

            <div>
              <div className="flex items-center gap-1.5 flex-wrap">
                <h1 className="text-base sm:text-lg font-bold text-white flex items-center gap-1">
                  AGRO AI
                  <span className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-blue-500 text-white text-[10px] shadow-xs">
                    ✓
                  </span>
                </h1>
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-white/15 text-white/90 font-medium">
                  AGRICULTURE ASSISTANT
                </span>
              </div>
              <p className="text-xs text-emerald-100 flex items-center gap-1.5 font-normal">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-300"></span>
                {engineStatus?.badge || 'Checking assistant status'} • crop care, soil, pests and farming guidance
              </p>
            </div>
          </div>

          {/* Action Icons Bar (WhatsApp Header Right) */}
          <div className="flex items-center gap-1.5 sm:gap-2">
            <button
              onClick={() => setShowCalculatorModal(true)}
              title="Agricultural Calculators"
              className="p-2 sm:px-3 sm:py-1.5 rounded-full sm:rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <Calculator className="w-4 h-4" />
              <span className="hidden sm:inline">Calculators</span>
            </button>

            {canConfigureAI && <button
              onClick={() => setShowSettingsModal(true)}
              title="AI Model Settings"
              className="p-2 sm:px-3 sm:py-1.5 rounded-full sm:rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <Settings className="w-4 h-4" />
              <span className="hidden sm:inline">Settings</span>
            </button>}

            <button
              onClick={handleClearChat}
              title="New Conversation"
              className="p-2 rounded-full hover:bg-white/20 text-white/90 hover:text-white transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Quick Suggestion Chips Carousel */}
        <div className="bg-[#e9edef] px-3 py-2 border-x border-gray-300 flex items-center gap-2 overflow-x-auto scrollbar-none text-xs">
          <span className="text-[11px] font-bold text-gray-500 whitespace-nowrap flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-[#00a884]" /> Ask AGRO AI:
          </span>
          {quickPrompts.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(p.query)}
              className="px-3 py-1 rounded-full bg-white border border-gray-300 hover:border-[#00a884] hover:bg-[#d9fdd3]/40 text-[#111b21] font-medium whitespace-nowrap transition-all shadow-2xs text-[11px]"
            >
              {p.label}
            </button>
          ))}
        </div>

        {/* WhatsApp Chat Window with authentic doodle background */}
        <div className="whatsapp-chat-bg border-x border-b border-gray-300 shadow-md flex-1 flex flex-col min-h-[550px] max-h-[720px] rounded-b-2xl overflow-hidden relative">
          
          {/* Scrollable Message History */}
          <div className="flex-1 p-3 sm:p-5 overflow-y-auto space-y-4">
            
            {/* Centered WhatsApp Encryption Security Pill */}
            <div className="flex justify-center my-1">
              <div className="px-3 py-1.5 bg-[#ffeecd] border border-[#f5c368]/50 text-[#54656f] text-[11px] rounded-lg shadow-2xs max-w-md text-center flex items-center gap-1.5 font-medium">
                <ShieldCheck className="w-3.5 h-3.5 text-[#b28212] shrink-0" />
                <span>Evidence-based AI reasoning active. Zero personal data leakage.</span>
              </div>
            </div>

            {/* Centered Date Badge */}
            <div className="flex justify-center my-2">
              <span className="px-3 py-1 bg-white/90 text-gray-500 text-[10px] font-bold rounded-lg shadow-2xs uppercase tracking-wider">
                Today
              </span>
            </div>

            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} w-full`}
              >
                {/* Bubble Container */}
                <div
                  className={`relative p-3.5 sm:p-4 rounded-2xl text-xs sm:text-sm leading-relaxed space-y-2 max-w-[92%] sm:max-w-[82%] shadow-[0_1px_0.5px_rgba(11,20,26,0.13)] ${
                    msg.sender === 'user'
                      ? 'bg-[#d9fdd3] text-[#111b21] rounded-tr-xs'
                      : 'bg-white text-[#111b21] rounded-tl-xs border border-gray-200/60'
                  }`}
                >
                  {/* AGRO AI Header within bot bubble */}
                  {msg.sender === 'assistant' && (
                    <div className="flex items-center justify-between pb-1.5 border-b border-gray-100 mb-1">
                      <div className="flex items-center gap-1.5">
                        <div className="w-4 h-4 rounded-full p-[1px] bg-gradient-to-tr from-[#00d2ff] via-[#9d4edd] to-[#f857a6]">
                          <div className="w-full h-full bg-white rounded-full"></div>
                        </div>
                        <span className="font-extrabold text-xs bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600">
                          AGRO AI
                        </span>
                      </div>
                      {msg.category && (
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 text-[#005c4b] font-bold uppercase tracking-wider">
                          {msg.category}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Message Body */}
                  {msg.sender === 'user' ? (
                    <div className="whitespace-pre-wrap font-medium text-[13px] sm:text-sm">{msg.content}</div>
                  ) : (
                    <RenderMarkdown content={msg.content} />
                  )}

                  {msg.sender === 'assistant' && msg.persistenceMessage && (
                    <p className={`pt-1 text-[10px] ${msg.savedToAccount ? 'text-emerald-700' : 'text-amber-700'}`}>
                      {msg.persistenceMessage}
                    </p>
                  )}

                  {/* WhatsApp Interactive Receipt for Calculator Data */}
                  {msg.sender === 'assistant' && msg.calculatorData && (
                    <div className="p-3 bg-[#f0f9f6] border border-[#a3e2cd] rounded-xl space-y-2 text-xs">
                      <div className="flex items-center gap-1.5 font-bold text-[#005c4b]">
                        <Calculator className="w-3.5 h-3.5 text-[#00a884]" />
                        <span>Execution Calculation Receipt</span>
                      </div>
                      {msg.calculatorData.fertilizers && (
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-center">
                          {msg.calculatorData.fertilizers.map((f: any, fIdx: number) => (
                            <div key={fIdx} className="p-2 bg-white rounded-lg border border-[#a3e2cd] shadow-2xs">
                              <span className="text-[10px] text-gray-500 block truncate">{f.name.split('(')[0]}</span>
                              <span className="text-sm font-extrabold text-[#005c4b] block">{f.quantityKg} kg</span>
                              <span className="text-[10px] text-gray-400 block">{f.bags} bags</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* WhatsApp Link Preview Style Citation Cards */}
                  {msg.sender === 'assistant' && msg.evidenceSources && msg.evidenceSources.length > 0 && (
                    <div className="pt-2.5 border-t border-gray-100 space-y-1.5">
                      <div className="flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider text-[#005c4b]">
                        <BookOpen className="w-3 h-3 text-[#00a884]" />
                        <span>Authoritative Sources & Reference Citations</span>
                      </div>
                      <div className="grid grid-cols-1 gap-1.5">
                        {msg.evidenceSources.map((src, sIdx) => (
                          <a
                            key={sIdx}
                            href={src.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2 rounded-xl bg-gray-50 border border-gray-200 hover:border-[#00a884] hover:bg-[#d9fdd3]/20 transition-all flex items-start justify-between gap-2 text-left"
                          >
                            <div className="space-y-0.5">
                              <span className="inline-block px-1.5 py-0.2 rounded bg-emerald-100 text-[#005c4b] font-bold text-[9px] uppercase">
                                {src.organization} ({src.year})
                              </span>
                              <p className="text-xs font-bold text-[#111b21] hover:text-[#005c4b] leading-tight">
                                {src.title}
                              </p>
                              <span className="text-[9px] text-gray-400 font-mono truncate block max-w-xs">
                                {src.url}
                              </span>
                            </div>
                            <ExternalLink className="w-3.5 h-3.5 text-gray-400 shrink-0 mt-1" />
                          </a>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Contextual Follow-up Quick Reply Pills */}
                  {msg.sender === 'assistant' && msg.suggestedQuestions && msg.suggestedQuestions.length > 0 && (
                    <div className="pt-2 space-y-1.5">
                      <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">
                        Quick Questions:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {msg.suggestedQuestions.map((sq, sqIdx) => (
                          <button
                            key={sqIdx}
                            onClick={() => handleSend(sq)}
                            className="px-2.5 py-1 rounded-full bg-white border border-gray-300 hover:border-[#00a884] hover:bg-[#d9fdd3]/50 text-[11px] text-[#111b21] font-medium text-left transition-all shadow-2xs flex items-center gap-1"
                          >
                            <Sparkles className="w-2.5 h-2.5 text-[#00a884]" />
                            {sq}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Message Bottom Row: Action Buttons & WhatsApp Double Blue Check */}
                  <div className="pt-1.5 flex items-center justify-between gap-2 flex-wrap text-[10px]">
                    {msg.sender === 'assistant' ? (
                      <div className="flex items-center gap-1.5">
                        <button
                          onClick={() => handleCopy(msg.id, msg.content)}
                          className="px-2 py-0.5 rounded bg-gray-100 hover:bg-gray-200 text-gray-600 font-medium transition-colors"
                        >
                          {copiedId === msg.id ? (
                            <span className="text-emerald-700 font-bold flex items-center gap-0.5">
                              <Check className="w-2.5 h-2.5" /> Copied
                            </span>
                          ) : (
                            <span className="flex items-center gap-0.5">
                              <Copy className="w-2.5 h-2.5" /> Copy
                            </span>
                          )}
                        </button>

                        <button
                          onClick={() => handleExportAdvisory(msg)}
                          className="px-2 py-0.5 rounded bg-gray-100 hover:bg-gray-200 text-gray-600 font-medium transition-colors flex items-center gap-0.5"
                        >
                          <Download className="w-2.5 h-2.5" /> Export .MD
                        </button>

                        {msg.relatedAction && (
                          <Link
                            to={msg.relatedAction.route}
                            className="px-2.5 py-0.5 rounded bg-[#00a884] hover:bg-[#008f6f] text-white font-bold transition-colors flex items-center gap-1 shadow-2xs"
                          >
                            <span>{msg.relatedAction.label}</span>
                            <ArrowRight className="w-2.5 h-2.5" />
                          </Link>
                        )}
                      </div>
                    ) : (
                      <div></div>
                    )}

                    {/* WhatsApp Timestamp + Double Blue Checkmark */}
                    <div className="flex items-center gap-1 ml-auto text-gray-500 font-mono text-[10px]">
                      <span>{msg.timestamp}</span>
                      {msg.sender === 'user' && (
                        <CheckCheck className="w-3.5 h-3.5 text-[#53bdeb] inline" />
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* AGRO AI Typing Indicator */}
            {loading && (
              <div className="flex justify-start">
                <div className="p-3.5 rounded-2xl rounded-tl-xs bg-white border border-gray-200 text-[#111b21] text-xs flex items-center gap-2 shadow-[0_1px_0.5px_rgba(11,20,26,0.13)]">
                  <div className="flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-[#00a884] animate-bounce"></span>
                    <span className="w-2 h-2 rounded-full bg-[#00a884] animate-bounce [animation-delay:0.2s]"></span>
                    <span className="w-2 h-2 rounded-full bg-[#00a884] animate-bounce [animation-delay:0.4s]"></span>
                  </div>
                  <span className="text-gray-500 font-medium ml-1">AGRO AI is thinking...</span>
                </div>
              </div>
            )}
            <div ref={chatBottomRef} />
          </div>

          {/* Quick Emoji Tray Popover */}
          {showEmojiPicker && (
            <div className="bg-white border-t border-gray-200 p-2.5 flex items-center gap-2 overflow-x-auto shadow-md">
              <span className="text-[11px] font-bold text-gray-400 whitespace-nowrap">Insert Emoji:</span>
              {quickEmojis.map((emoji, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setInput((prev) => prev + emoji);
                    setShowEmojiPicker(false);
                  }}
                  className="text-lg hover:scale-125 transition-transform p-1"
                >
                  {emoji}
                </button>
              ))}
            </div>
          )}

          {/* Attachment Quick Menu */}
          {showAttachmentMenu && (
            <div className="bg-white border-t border-gray-200 p-3 grid grid-cols-2 sm:grid-cols-4 gap-2 shadow-lg animate-in slide-in-from-bottom-2">
              <button
                onClick={() => {
                  setShowAttachmentMenu(false);
                  setShowCalculatorModal(true);
                }}
                className="p-2.5 rounded-xl border border-gray-200 hover:border-[#00a884] hover:bg-[#d9fdd3]/30 text-left flex items-center gap-2.5 transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-emerald-100 text-[#005c4b] flex items-center justify-center font-bold">
                  <Calculator className="w-4 h-4" />
                </div>
                <div>
                  <span className="font-bold text-xs text-[#111b21] block">Calculators</span>
                  <span className="text-[10px] text-gray-500 block">NPK, Seeds, Drip</span>
                </div>
              </button>

              <Link
                to="/production/crop"
                className="p-2.5 rounded-xl border border-gray-200 hover:border-[#00a884] hover:bg-[#d9fdd3]/30 text-left flex items-center gap-2.5 transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center font-bold">
                  <Leaf className="w-4 h-4" />
                </div>
                <div>
                  <span className="font-bold text-xs text-[#111b21] block">Crop Health</span>
                  <span className="text-[10px] text-gray-500 block">Diagnose 39 Diseases</span>
                </div>
              </Link>

              <Link
                to="/production/soil"
                className="p-2.5 rounded-xl border border-gray-200 hover:border-[#00a884] hover:bg-[#d9fdd3]/30 text-left flex items-center gap-2.5 transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-orange-100 text-orange-800 flex items-center justify-center font-bold">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <span className="font-bold text-xs text-[#111b21] block">Soil Analysis</span>
                  <span className="text-[10px] text-gray-500 block">Classification & pH</span>
                </div>
              </Link>

              <Link
                to="/nutrition"
                className="p-2.5 rounded-xl border border-gray-200 hover:border-[#00a884] hover:bg-[#d9fdd3]/30 text-left flex items-center gap-2.5 transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-emerald-100 text-[#005c4b] flex items-center justify-center font-bold">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div>
                  <span className="font-bold text-xs text-[#111b21] block">Better Nutrition</span>
                  <span className="text-[10px] text-gray-500 block">7-Day Diet Planner</span>
                </div>
              </Link>
            </div>
          )}

          {/* WhatsApp Bottom Input Bar */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend(input);
            }}
            className="p-2.5 sm:p-3 bg-[#f0f2f5] border-t border-gray-200 flex items-center gap-2"
          >
            {/* Emoji Button */}
            <button
              type="button"
              onClick={() => {
                setShowEmojiPicker((p) => !p);
                setShowAttachmentMenu(false);
              }}
              className="p-2 rounded-full hover:bg-gray-200 text-gray-500 transition-colors"
              title="Emoji Tray"
            >
              <Smile className="w-5 h-5" />
            </button>

            {/* Paperclip Button */}
            <button
              type="button"
              onClick={() => {
                setShowAttachmentMenu((p) => !p);
                setShowEmojiPicker(false);
              }}
              className="p-2 rounded-full hover:bg-gray-200 text-gray-500 transition-colors"
              title="Attachments & Tools"
            >
              <Paperclip className="w-5 h-5" />
            </button>

            {/* Pill-shaped Input Field */}
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask AGRO AI anything... (coding, math, farming, science, recipes, life)"
              className="flex-1 px-4 py-2.5 bg-white rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#00a884] text-xs sm:text-sm text-[#111b21] shadow-2xs placeholder-gray-400"
            />

            {/* Mic / Voice Placeholder */}
            <button
              type="button"
              onClick={() => {
                setInput((prev) => (prev ? prev : 'How do I identify and manage Tomato Early Blight with IPM?'));
              }}
              className="p-2 rounded-full hover:bg-gray-200 text-gray-500 transition-colors hidden sm:block"
              title="Voice Input (Auto-fill Sample)"
            >
              <Mic className="w-5 h-5" />
            </button>

            {/* Circular WhatsApp Green Send Button */}
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="w-10 h-10 sm:w-11 sm:h-11 rounded-full bg-[#00a884] hover:bg-[#008f6f] text-white flex items-center justify-center shadow-md active:scale-95 transition-all disabled:opacity-40 disabled:pointer-events-none"
              title="Send Message"
            >
              <Send className="w-4 h-4 sm:w-5 sm:h-5 ml-0.5" />
            </button>
          </form>
        </div>
      </div>

      {/* Interactive Farm Calculator Modal */}
      {showCalculatorModal && (
        <FarmCalculatorModal
          onClose={() => setShowCalculatorModal(false)}
          onInsertPrompt={(prompt) => {
            setShowCalculatorModal(false);
            handleSend(prompt);
          }}
        />
      )}

      {/* AI Model Settings Modal */}
      {showSettingsModal && (
        <AIModelSettingsModal
          currentStatus={engineStatus}
          onClose={() => setShowSettingsModal(false)}
          onStatusUpdated={(newStatus) => setEngineStatus(newStatus)}
        />
      )}
    </div>
  );
};

// Interactive Farm Calculator Drawer Modal
const FarmCalculatorModal: React.FC<{
  onClose: () => void;
  onInsertPrompt: (prompt: string) => void;
}> = ({ onClose, onInsertPrompt }) => {
  const [activeTab, setActiveTab] = useState<'npk' | 'seed' | 'irrigation' | 'economics'>('npk');

  // NPK form state
  const [targetN, setTargetN] = useState('120');
  const [targetP, setTargetP] = useState('60');
  const [targetK, setTargetK] = useState('40');
  const [area, setArea] = useState('1');
  const [unit, setUnit] = useState('ha');

  // Seed rate form state
  const [rowSpacing, setRowSpacing] = useState('60');
  const [plantSpacing, setPlantSpacing] = useState('20');
  const [seedArea, setSeedArea] = useState('1');

  // Irrigation form state
  const [eto, setEto] = useState('4.5');
  const [kc, setKc] = useState('1.15');
  const [irrigArea, setIrrigArea] = useState('4047');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-xl border border-gray-200 space-y-4">
        <div className="flex items-center justify-between border-b pb-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-[#005c4b] flex items-center justify-center">
              <Calculator className="w-5 h-5 text-[#00a884]" />
            </div>
            <div>
              <h3 className="font-extrabold text-gray-900 text-sm sm:text-base">Farm & Engineering Calculators</h3>
              <p className="text-[11px] text-gray-500">Deterministic AST mathematical solvers with ICAR formulas</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tabs */}
        <div className="grid grid-cols-4 gap-1 p-1 bg-gray-100 rounded-xl text-xs font-bold text-gray-600">
          <button
            onClick={() => setActiveTab('npk')}
            className={`py-1.5 rounded-lg transition-all ${activeTab === 'npk' ? 'bg-white text-[#005c4b] shadow-2xs font-extrabold' : 'hover:text-gray-900'}`}
          >
            NPK Dose
          </button>
          <button
            onClick={() => setActiveTab('seed')}
            className={`py-1.5 rounded-lg transition-all ${activeTab === 'seed' ? 'bg-white text-[#005c4b] shadow-2xs font-extrabold' : 'hover:text-gray-900'}`}
          >
            Seed Rate
          </button>
          <button
            onClick={() => setActiveTab('irrigation')}
            className={`py-1.5 rounded-lg transition-all ${activeTab === 'irrigation' ? 'bg-white text-[#005c4b] shadow-2xs font-extrabold' : 'hover:text-gray-900'}`}
          >
            Irrigation
          </button>
          <button
            onClick={() => setActiveTab('economics')}
            className={`py-1.5 rounded-lg transition-all ${activeTab === 'economics' ? 'bg-white text-[#005c4b] shadow-2xs font-extrabold' : 'hover:text-gray-900'}`}
          >
            Economics
          </button>
        </div>

        {/* Tab 1: NPK */}
        {activeTab === 'npk' && (
          <div className="space-y-3 text-xs">
            <p className="text-gray-500">Calculate exact Urea, DAP, and MOP bags accounting for dual-nutrient contribution:</p>
            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="font-bold text-gray-700 block mb-1">Target N (kg)</label>
                <input
                  type="number"
                  value={targetN}
                  onChange={(e) => setTargetN(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
              <div>
                <label className="font-bold text-gray-700 block mb-1">Target P₂O₅ (kg)</label>
                <input
                  type="number"
                  value={targetP}
                  onChange={(e) => setTargetP(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
              <div>
                <label className="font-bold text-gray-700 block mb-1">Target K₂O (kg)</label>
                <input
                  type="number"
                  value={targetK}
                  onChange={(e) => setTargetK(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="font-bold text-gray-700 block mb-1">Area Size</label>
                <input
                  type="number"
                  value={area}
                  onChange={(e) => setArea(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
              <div>
                <label className="font-bold text-gray-700 block mb-1">Area Unit</label>
                <select
                  value={unit}
                  onChange={(e) => setUnit(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl bg-white"
                >
                  <option value="ha">Hectares (ha)</option>
                  <option value="acre">Acres</option>
                </select>
              </div>
            </div>
            <button
              onClick={() => onInsertPrompt(`Calculate NPK fertilizer dosage for ${area} ${unit} with target ${targetN}:${targetP}:${targetK}`)}
              className="w-full py-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white font-bold rounded-xl shadow-sm transition-colors text-xs flex items-center justify-center gap-1.5"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Insert Fertilizer Math to Chat</span>
            </button>
          </div>
        )}

        {/* Tab 2: Seed Rate */}
        {activeTab === 'seed' && (
          <div className="space-y-3 text-xs">
            <p className="text-gray-500">Calculate required plant population and seed quantity factoring seed utility:</p>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="font-bold text-gray-700 block mb-1">Row Spacing (cm)</label>
                <input
                  type="number"
                  value={rowSpacing}
                  onChange={(e) => setRowSpacing(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
              <div>
                <label className="font-bold text-gray-700 block mb-1">Plant Spacing (cm)</label>
                <input
                  type="number"
                  value={plantSpacing}
                  onChange={(e) => setPlantSpacing(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
            </div>
            <div>
              <label className="font-bold text-gray-700 block mb-1">Area (hectares)</label>
              <input
                type="number"
                value={seedArea}
                onChange={(e) => setSeedArea(e.target.value)}
                className="w-full px-3 py-2 border rounded-xl"
              />
            </div>
            <button
              onClick={() => onInsertPrompt(`Calculate seed rate and plant population for ${seedArea} ha with ${rowSpacing} cm row spacing and ${plantSpacing} cm plant spacing`)}
              className="w-full py-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white font-bold rounded-xl shadow-sm transition-colors text-xs flex items-center justify-center gap-1.5"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Insert Seed Rate Math to Chat</span>
            </button>
          </div>
        )}

        {/* Tab 3: Irrigation */}
        {activeTab === 'irrigation' && (
          <div className="space-y-3 text-xs">
            <p className="text-gray-500">Calculate daily crop water demand (ETc) and drip irrigation runtime:</p>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="font-bold text-gray-700 block mb-1">ETo (mm/day)</label>
                <input
                  type="number"
                  value={eto}
                  onChange={(e) => setEto(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
              <div>
                <label className="font-bold text-gray-700 block mb-1">Crop Kc Factor</label>
                <input
                  type="number"
                  value={kc}
                  onChange={(e) => setKc(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl"
                />
              </div>
            </div>
            <div>
              <label className="font-bold text-gray-700 block mb-1">Field Area (m²)</label>
              <input
                type="number"
                value={irrigArea}
                onChange={(e) => setIrrigArea(e.target.value)}
                className="w-full px-3 py-2 border rounded-xl"
              />
            </div>
            <button
              onClick={() => onInsertPrompt(`Calculate daily drip irrigation runtime for ${irrigArea} m2 with ETo ${eto} mm/day and Kc ${kc}`)}
              className="w-full py-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white font-bold rounded-xl shadow-sm transition-colors text-xs flex items-center justify-center gap-1.5"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Insert Irrigation Math to Chat</span>
            </button>
          </div>
        )}

        {/* Tab 4: Economics */}
        {activeTab === 'economics' && (
          <div className="space-y-3 text-xs">
            <p className="text-gray-500">Calculate comprehensive farm economics, gross margin, net profit, and BCR:</p>
            <button
              onClick={() => onInsertPrompt(`Calculate cost of cultivation, net profit, and benefit-cost ratio (BCR) for wheat with 45 quintals expected yield and MSP of ₹2275/Q`)}
              className="w-full py-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white font-bold rounded-xl shadow-sm transition-colors text-xs flex items-center justify-center gap-1.5"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Insert Farm Economics Math to Chat</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

// Interactive AI Model Settings Modal
const AIModelSettingsModal: React.FC<{
  currentStatus: AssistantEngineStatus | null;
  onClose: () => void;
  onStatusUpdated: (status: AssistantEngineStatus) => void;
}> = ({ currentStatus, onClose, onStatusUpdated }) => {
  const [provider, setProvider] = useState<string>(currentStatus?.provider || 'offline');
  const [model, setModel] = useState<string>(currentStatus?.model || '');
  const [apiKey, setApiKey] = useState<string>('');
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  const handleSave = async () => {
    setSaving(true);
    setNotice(null);
    try {
      if (provider === 'offline' || provider === 'none') {
        const res = await assistantService.resetConfig();
        onStatusUpdated(res);
        setNotice('Switched the assistant to offline mode. Answers may be limited without a configured provider.');
      } else {
        if (!apiKey.trim()) {
          setNotice('Please provide a valid API key for live provider.');
          setSaving(false);
          return;
        }
        const res = await assistantService.updateConfig(provider, model || undefined, apiKey);
        onStatusUpdated(res);
        setNotice(`Successfully connected to ${provider.toUpperCase()} live LLM!`);
      }
      setTimeout(() => {
        onClose();
      }, 1200);
    } catch (err: any) {
      setNotice(err.message || 'Failed to update configuration.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-in fade-in">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-xl border border-gray-200 space-y-4">
        <div className="flex items-center justify-between border-b pb-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-[#005c4b] flex items-center justify-center">
              <Settings className="w-5 h-5 text-[#00a884]" />
            </div>
            <div>
              <h3 className="font-extrabold text-gray-900 text-sm sm:text-base">AI Model Configuration</h3>
              <p className="text-[11px] text-gray-500">Configure a provider or use the backend offline mode</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-3 text-xs">
          <div>
            <label className="font-bold text-gray-700 block mb-1">Select AI Provider</label>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="w-full px-3 py-2 border rounded-xl bg-white font-medium text-gray-800"
            >
              <option value="offline">Autonomous Offline Engine (Zero Key Required • Recommended)</option>
              <option value="groq">Groq (Ultra-Fast Llama-3.1-8B)</option>
              <option value="gemini">Google Gemini (Gemini 1.5 Flash)</option>
              <option value="openai">OpenAI (GPT-4o Mini)</option>
            </select>
          </div>

          {provider !== 'offline' && provider !== 'none' && (
            <div className="space-y-2">
              <div>
                <label className="font-bold text-gray-700 block mb-1">Model Name (Optional)</label>
                <input
                  type="text"
                  placeholder="e.g. llama-3.1-8b-instant, gemini-1.5-flash"
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl font-mono text-xs"
                />
              </div>
              <div>
                <label className="font-bold text-gray-700 block mb-1">API Key</label>
                <input
                  type="password"
                  placeholder={`Enter your ${provider.toUpperCase()} API key`}
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  className="w-full px-3 py-2 border rounded-xl font-mono text-xs"
                />
              </div>
              <p className="text-[10px] text-gray-400">
                Your key is stored strictly in-memory during this session and never logged to external disks.
              </p>
            </div>
          )}

          {notice && (
            <div className="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px] font-semibold">
              {notice}
            </div>
          )}

          <div className="pt-2 flex items-center justify-end gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-gray-600 hover:bg-gray-100 font-semibold"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="px-5 py-2 rounded-xl bg-[#00a884] hover:bg-[#008f6f] text-white font-bold shadow-sm transition-colors disabled:opacity-50 flex items-center gap-1.5"
            >
              {saving ? 'Saving...' : 'Apply Configuration'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
