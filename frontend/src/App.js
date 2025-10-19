import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Globe, ArrowUpDown, Copy, Share2, Sun, Moon, BarChart3, Zap, History, 
  Sparkles, Mic, MicOff, Settings, ChevronDown, Check, Loader2, TrendingUp, 
  Clock, Star, Download, Upload, MoreHorizontal, Volume2, VolumeX, BookOpen, 
  Target, Layers, Palette, Shield, Zap as Lightning, User, Bell, Search,
  Languages, RefreshCw, FileText, Image, Video, Music, File, FolderOpen,
  Plus, Minus, Edit3, Trash2, Heart, Bookmark, ExternalLink, Maximize2,
  Minimize2, RotateCcw, Save, Send, Filter, SortAsc, Grid, List, Eye,
  EyeOff, Lock, Unlock, CheckCircle, XCircle, AlertCircle, Info,
  Home, Menu, X, ChevronLeft, ChevronRight, Play, Pause, Stop,
  Calendar, Tag, Users, HelpCircle, MessageSquare, Phone, Mail,
  Github, Twitter, Linkedin, Facebook, Instagram, Youtube, Twitch,
  Coffee, Gift, Award, Trophy, Medal, Crown, Diamond, Star as StarIcon,
  LogOut
} from 'lucide-react';

// Animation variants
const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: "easeOut" }
};

const staggerChildren = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

// Premium Components
const GlassButton = ({ children, variant = 'primary', size = 'md', className = '', onClick, disabled = false, ...props }) => {
  const variants = {
    primary: 'bg-indigo-600/90 hover:bg-indigo-700/90 text-white backdrop-blur-sm shadow-lg hover:shadow-xl',
    secondary: 'bg-white/80 hover:bg-white/90 text-slate-700 backdrop-blur-sm shadow-sm hover:shadow-md border border-white/20',
    ghost: 'hover:bg-white/50 text-slate-600 dark:text-slate-400 backdrop-blur-sm',
    glass: 'bg-white/20 hover:bg-white/30 text-slate-700 dark:text-slate-300 backdrop-blur-md border border-white/30',
    danger: 'bg-red-500/90 hover:bg-red-600/90 text-white backdrop-blur-sm shadow-lg hover:shadow-xl',
    success: 'bg-green-500/90 hover:bg-green-600/90 text-white backdrop-blur-sm shadow-lg hover:shadow-xl',
    warning: 'bg-yellow-500/90 hover:bg-yellow-600/90 text-white backdrop-blur-sm shadow-lg hover:shadow-xl',
    info: 'bg-blue-500/90 hover:bg-blue-600/90 text-white backdrop-blur-sm shadow-lg hover:shadow-xl'
  };
  
  const sizes = {
    sm: 'px-3 py-2 text-sm font-medium',
    md: 'px-4 py-2.5 text-sm font-medium',
    lg: 'px-6 py-3 text-base font-medium',
    xl: 'px-8 py-4 text-lg font-medium'
  };
  
  return (
    <motion.button
      className={`inline-flex items-center justify-center rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed ${variants[variant]} ${sizes[size]} ${className}`}
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </motion.button>
  );
};

const GlassInput = ({ className = '', ...props }) => (
  <input
    className={`w-full px-4 py-3 bg-white/60 dark:bg-slate-800/60 backdrop-blur-sm border border-white/30 dark:border-slate-700/30 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-500 dark:placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all duration-300 font-medium ${className}`}
    {...props}
  />
);

const GlassTextarea = ({ className = '', ...props }) => (
  <textarea
    className={`w-full px-4 py-3 bg-white/60 dark:bg-slate-800/60 backdrop-blur-sm border border-white/30 dark:border-slate-700/30 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-500 dark:placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all duration-300 resize-none font-medium ${className}`}
    {...props}
  />
);

const GlassSelect = ({ children, className = '', ...props }) => (
  <select
    className={`w-full px-4 py-3 bg-white/60 dark:bg-slate-800/60 backdrop-blur-sm border border-white/30 dark:border-slate-700/30 rounded-xl text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all duration-300 font-medium ${className}`}
    {...props}
  >
    {children}
  </select>
);

const GlassSwitch = ({ checked, onChange, className = '', ...props }) => (
  <motion.button
    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500/20 backdrop-blur-sm ${
      checked ? 'bg-indigo-600/90' : 'bg-slate-300/80 dark:bg-slate-600/80'
    } ${className}`}
    onClick={() => onChange(!checked)}
    whileTap={{ scale: 0.95 }}
    {...props}
  >
    <motion.span
      className="inline-block h-4 w-4 transform rounded-full bg-white shadow-lg"
      animate={{ x: checked ? 24 : 4 }}
      transition={{ type: "spring", stiffness: 500, damping: 30 }}
    />
  </motion.button>
);

// Main App Component
const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('de');
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [autoDetect, setAutoDetect] = useState(true);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [history, setHistory] = useState([]);
  const [usageStats, setUsageStats] = useState({ used: 1250, limit: 10000 });
  const [selectedModel, setSelectedModel] = useState('premium');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [fullscreenMode, setFullscreenMode] = useState(false);
  const [favorites, setFavorites] = useState([]);
  const [recentFiles, setRecentFiles] = useState([]);
  const [notifications, setNotifications] = useState([
    { id: 1, message: "Translation completed successfully", type: "success", time: "2 min ago" },
    { id: 2, message: "New model available", type: "info", time: "1 hour ago" },
    { id: 3, message: "Usage limit warning", type: "warning", time: "3 hours ago" }
  ]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [currentPage, setCurrentPage] = useState('translate');
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'de', name: 'German', flag: '🇩🇪' },
    { code: 'fr', name: 'French', flag: '🇫🇷' },
    { code: 'es', name: 'Spanish', flag: '🇪🇸' },
    { code: 'it', name: 'Italian', flag: '🇮🇹' },
    { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
    { code: 'ru', name: 'Russian', flag: '🇷🇺' },
    { code: 'ja', name: 'Japanese', flag: '🇯🇵' },
    { code: 'ko', name: 'Korean', flag: '🇰🇷' },
    { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
    { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
    { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  ];

  const models = [
    { id: 'standard', name: 'Standard', description: 'Fast & reliable', price: 'Free' },
    { id: 'premium', name: 'Premium', description: 'Enhanced accuracy', price: '$9.99/mo' },
    { id: 'pro', name: 'Pro', description: 'Domain-specific', price: '$19.99/mo' },
  ];

  // Theme effect
  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDarkMode);
  }, [isDarkMode]);

  // Audio level simulation
  useEffect(() => {
    if (isRecording) {
      const interval = setInterval(() => {
        setAudioLevel(Math.random() * 100);
      }, 100);
      return () => clearInterval(interval);
    }
  }, [isRecording]);

  // Translation function with optimizations
  const handleTranslate = async () => {
    if (!sourceText.trim()) return;
    
    setIsTranslating(true);
    
    try {
      const startTime = Date.now();
      
      const response = await fetch('http://localhost:8000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: sourceText,
          source_language: sourceLang,
          target_language: targetLang,
          max_length: 50,  // Balanced for speed and quality
          beam_size: 1,    // Greedy decoding for speed
        }),
      });
      
      const data = await response.json();
      const translationTime = Date.now() - startTime;
      
      setTranslatedText(data.translated_text);
      
      // Add to history
      const newTranslation = {
        id: Date.now().toString(),
        sourceText,
        translatedText: data.translated_text,
        sourceLang,
        targetLang,
        timestamp: new Date(),
        processingTime: translationTime,
      };
      setHistory(prev => [newTranslation, ...prev.slice(0, 19)]);
      
      // Add notification with timing info
      addNotification(`Translation completed in ${translationTime}ms!`, "success");
      
    } catch (error) {
      console.error('Translation error:', error);
      setTranslatedText('Translation failed. Please try again.');
      addNotification("Translation failed. Please try again.", "error");
    } finally {
      setIsTranslating(false);
    }
  };

  const handleSwapLanguages = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
    setSourceText(translatedText);
    setTranslatedText(sourceText);
    addNotification("Languages swapped successfully!", "info");
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(translatedText);
    addNotification("Text copied to clipboard!", "success");
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: 'Translation',
        text: `${sourceText} → ${translatedText}`,
      });
    } else {
      navigator.clipboard.writeText(`${sourceText} → ${translatedText}`);
      addNotification("Translation shared to clipboard!", "info");
    }
  };

  const handleFavorite = (item) => {
    const favoriteItem = {
      id: Date.now().toString(),
      ...item,
      timestamp: new Date()
    };
    setFavorites(prev => [favoriteItem, ...prev.slice(0, 19)]);
    addNotification("Added to favorites!", "success");
  };

  const removeFavorite = (id) => {
    setFavorites(prev => prev.filter(item => item.id !== id));
    addNotification("Removed from favorites!", "info");
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileItem = {
        id: Date.now().toString(),
        name: file.name,
        size: file.size,
        type: file.type,
        timestamp: new Date()
      };
      setRecentFiles(prev => [fileItem, ...prev.slice(0, 9)]);
      addNotification(`File "${file.name}" uploaded successfully!`, "success");
    }
  };

  const handleVoiceInput = () => {
    setIsListening(!isListening);
    setIsRecording(!isRecording);
    if (!isListening) {
      addNotification("Voice input started", "info");
      // Simulate voice input
      setTimeout(() => {
        setSourceText(prev => prev + " Hello, this is a voice input test. ");
        setIsListening(false);
        setIsRecording(false);
        addNotification("Voice input completed", "success");
      }, 3000);
        } else {
      addNotification("Voice input stopped", "info");
    }
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      const filteredHistory = history.filter(item => 
        item.sourceText.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.translatedText.toLowerCase().includes(searchQuery.toLowerCase())
      );
      addNotification(`Found ${filteredHistory.length} results for "${searchQuery}"`, "info");
    }
  };

  const addNotification = (message, type) => {
    const newNotification = {
      id: Date.now(),
      message,
      type,
      time: "Just now"
    };
    setNotifications(prev => [newNotification, ...prev.slice(0, 9)]);
  };

  const clearHistory = () => {
    setHistory([]);
    addNotification("History cleared!", "info");
  };

  const exportHistory = () => {
    const dataStr = JSON.stringify(history, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'translation-history.json';
    link.click();
    addNotification("History exported successfully!", "success");
  };

  const handleNewTranslation = () => {
    setSourceText('');
    setTranslatedText('');
    addNotification("New translation started!", "info");
  };

  const handleUpgrade = () => {
    addNotification("Redirecting to upgrade page...", "info");
    // Simulate upgrade process
    setTimeout(() => {
      addNotification("Upgrade completed! Welcome to Premium!", "success");
    }, 2000);
  };

  const handleSettings = () => {
    setShowAdvanced(!showAdvanced);
    addNotification("Settings toggled!", "info");
  };

  const handleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setFullscreenMode(true);
      addNotification("Entered fullscreen mode", "info");
    } else {
      document.exitFullscreen();
      setFullscreenMode(false);
      addNotification("Exited fullscreen mode", "info");
    }
  };

  const handleThemeToggle = () => {
    setIsDarkMode(!isDarkMode);
    addNotification(`Switched to ${!isDarkMode ? 'dark' : 'light'} mode`, "info");
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
    addNotification(`Switched to ${page} page`, "info");
  };

  const handleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

  const handleNotificationClick = (id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  };

  return (
    <div className={`min-h-screen transition-colors duration-700 ${
      isDarkMode 
        ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900' 
        : 'bg-gradient-to-br from-slate-50 via-white to-gray-50'
    }`}>
      
      {/* Beautiful Enhanced Header */}
      <motion.header 
        className="sticky top-0 z-50 bg-gradient-to-r from-white/95 via-slate-50/95 to-white/95 dark:from-slate-900/95 dark:via-slate-800/95 dark:to-slate-900/95 backdrop-blur-2xl border-b-2 border-gradient-to-r from-indigo-200/60 via-blue-200/60 to-indigo-200/60 dark:from-slate-600/60 dark:via-slate-500/60 dark:to-slate-600/60 shadow-2xl"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        <div className="w-full px-8">
          <div className="flex items-center justify-between h-20">
            
            {/* Left: Logo + Title + Navigation */}
            <motion.div 
              className="flex items-center space-x-6"
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.1 }}
            >
              <div className="w-14 h-14 bg-gradient-to-br from-indigo-600 via-blue-600 to-purple-600 rounded-3xl flex items-center justify-center shadow-2xl border-3 border-white/30 dark:border-slate-600/40 hover:shadow-3xl transition-all duration-300">
                <Globe className="w-8 h-8 text-white drop-shadow-lg" />
              </div>
              <div className="space-y-1">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-blue-600 dark:from-indigo-400 dark:to-blue-400 bg-clip-text text-transparent">
                  LinguaFlow Pro
              </h1>
                <p className="text-sm text-slate-500 dark:text-slate-400 font-medium">Enterprise Translation Platform</p>
              </div>
              
              {/* Navigation */}
              <nav className="hidden md:flex items-center space-x-8">
                <button 
                  onClick={() => handlePageChange('translate')}
                  className={`px-6 py-3 rounded-2xl font-semibold transition-all duration-300 border-2 ${
                    currentPage === 'translate' 
                      ? 'bg-gradient-to-r from-indigo-100 to-blue-100 dark:from-indigo-900/40 dark:to-blue-900/40 text-indigo-700 dark:text-indigo-300 border-indigo-300/60 dark:border-indigo-600/60 shadow-lg' 
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100/60 dark:hover:bg-slate-800/60 border-slate-200/40 dark:border-slate-700/40 hover:border-slate-300/60 dark:hover:border-slate-600/60 hover:shadow-md'
                  }`}
                >
                  Translate
                </button>
                <button 
                  onClick={() => handlePageChange('batch')}
                  className={`px-6 py-3 rounded-2xl font-semibold transition-all duration-300 border-2 ${
                    currentPage === 'batch' 
                      ? 'bg-gradient-to-r from-indigo-100 to-blue-100 dark:from-indigo-900/40 dark:to-blue-900/40 text-indigo-700 dark:text-indigo-300 border-indigo-300/60 dark:border-indigo-600/60 shadow-lg' 
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100/60 dark:hover:bg-slate-800/60 border-slate-200/40 dark:border-slate-700/40 hover:border-slate-300/60 dark:hover:border-slate-600/60 hover:shadow-md'
                  }`}
                >
                  Batch
                </button>
                <button 
                  onClick={() => handlePageChange('history')}
                  className={`px-6 py-3 rounded-2xl font-semibold transition-all duration-300 border-2 ${
                    currentPage === 'history' 
                      ? 'bg-gradient-to-r from-indigo-100 to-blue-100 dark:from-indigo-900/40 dark:to-blue-900/40 text-indigo-700 dark:text-indigo-300 border-indigo-300/60 dark:border-indigo-600/60 shadow-lg' 
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100/60 dark:hover:bg-slate-800/60 border-slate-200/40 dark:border-slate-700/40 hover:border-slate-300/60 dark:hover:border-slate-600/60 hover:shadow-md'
                  }`}
                >
                  History
                </button>
                <button 
                  onClick={() => handlePageChange('analytics')}
                  className={`font-medium transition-colors ${currentPage === 'analytics' ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'}`}
                >
                  Analytics
                </button>
              </nav>
            </motion.div>
            
            {/* Enhanced Right Controls */}
            <motion.div 
              className="flex items-center space-x-6"
              initial={{ x: 20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              {/* Enhanced Search */}
              <div className="hidden lg:flex items-center space-x-3">
                <GlassInput 
                  placeholder="Search translations..." 
                  className="w-72 border-2 border-slate-300/60 dark:border-slate-600/60 rounded-2xl shadow-lg focus:shadow-xl px-6 py-3" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <GlassButton 
                  variant="ghost" 
                  size="sm" 
                  onClick={handleSearch}
                  className="p-3 border-2 border-slate-300/60 dark:border-slate-600/60 rounded-2xl shadow-lg hover:shadow-xl"
                >
                  <Search className="w-5 h-5" />
                </GlassButton>
              </div>
              
              {/* Enhanced Model Selector */}
              <GlassSelect 
                value={selectedModel} 
                onChange={(e) => setSelectedModel(e.target.value)}
                className="w-40 text-sm border-2 border-slate-300/60 dark:border-slate-600/60 rounded-2xl shadow-lg px-4 py-3 font-semibold"
              >
                {models.map(model => (
                  <option key={model.id} value={model.id}>
                    {model.name}
                  </option>
                ))}
              </GlassSelect>
              
              {/* Notifications */}
              <div className="relative">
                <GlassButton 
                  variant="ghost" 
                  size="sm" 
                  className="p-2"
                  onClick={() => setShowNotifications(!showNotifications)}
                >
                  <Bell className="w-5 h-5" />
                  {notifications.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {notifications.length}
                    </span>
                  )}
                </GlassButton>
                
                {/* Notifications Dropdown */}
                <AnimatePresence>
                  {showNotifications && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="absolute right-0 top-12 w-80 bg-white/90 dark:bg-slate-800/90 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-xl shadow-xl p-4 z-50"
                    >
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-slate-900 dark:text-slate-100">Notifications</h3>
                        <GlassButton variant="ghost" size="sm" onClick={() => setNotifications([])}>
                          <Trash2 className="w-4 h-4" />
                        </GlassButton>
                      </div>
                      <div className="space-y-2 max-h-64 overflow-y-auto">
                        {notifications.map(notif => (
                          <motion.div
                            key={notif.id}
                            className="p-3 bg-slate-50/50 dark:bg-slate-700/50 rounded-lg cursor-pointer hover:bg-slate-100/50 dark:hover:bg-slate-600/50 transition-colors"
                            onClick={() => handleNotificationClick(notif.id)}
                          >
                            <div className="flex items-start space-x-2">
                              <div className={`w-2 h-2 rounded-full mt-2 ${
                                notif.type === 'success' ? 'bg-green-500' :
                                notif.type === 'error' ? 'bg-red-500' :
                                notif.type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                              }`} />
                              <div className="flex-1">
                                <p className="text-sm text-slate-900 dark:text-slate-100">{notif.message}</p>
                                <p className="text-xs text-slate-500 dark:text-slate-400">{notif.time}</p>
                              </div>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              
              {/* Fullscreen Toggle */}
              <GlassButton 
                variant="ghost" 
                size="sm" 
                className="p-2"
                onClick={handleFullscreen}
              >
                {fullscreenMode ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
              </GlassButton>
              
              {/* Enhanced Theme Toggle */}
              <GlassButton
                variant="ghost"
                size="sm"
                onClick={handleThemeToggle}
                className="p-3 border-2 border-slate-300/60 dark:border-slate-600/60 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300"
              >
                {isDarkMode ? <Sun className="w-6 h-6" /> : <Moon className="w-6 h-6" />}
              </GlassButton>
              
              {/* User Menu */}
              <div className="relative">
                <GlassButton 
                  variant="ghost" 
                  size="sm" 
                  className="p-2"
                  onClick={handleUserMenu}
                >
                  <User className="w-5 h-5" />
                </GlassButton>
                
                {/* User Menu Dropdown */}
                <AnimatePresence>
                  {showUserMenu && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="absolute right-0 top-12 w-48 bg-white/90 dark:bg-slate-800/90 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-xl shadow-xl p-2 z-50"
                    >
                      <div className="space-y-1">
                        <GlassButton variant="ghost" className="w-full justify-start">
                          <User className="w-4 h-4 mr-2" />
                          Profile
                        </GlassButton>
                        <GlassButton variant="ghost" className="w-full justify-start">
                          <Settings className="w-4 h-4 mr-2" />
                          Settings
                        </GlassButton>
                        <GlassButton variant="ghost" className="w-full justify-start">
                          <HelpCircle className="w-4 h-4 mr-2" />
                          Help
                        </GlassButton>
                        <div className="border-t border-slate-200/50 dark:border-slate-700/50 my-2" />
                        <GlassButton variant="danger" className="w-full justify-start">
                          <LogOut className="w-4 h-4 mr-2" />
                          Sign Out
                        </GlassButton>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.header>

      {/* Full-Width Main Content */}
      <main className="w-full">
        <div className="flex">
          
          {/* Enhanced Sidebar */}
          <motion.aside 
            className={`${sidebarOpen ? 'w-80' : 'w-16'} transition-all duration-300 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-r-2 border-slate-300/60 dark:border-slate-600/60 min-h-screen shadow-xl`}
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6 }}
          >
            <div className="p-6">
              {/* Sidebar Toggle */}
              <div className="flex justify-between items-center mb-6">
                {sidebarOpen && <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Tools</h2>}
                <GlassButton 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="p-2"
                >
                  {sidebarOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                </GlassButton>
              </div>

              {sidebarOpen && (
                <div className="space-y-6">
                  {/* Quick Actions */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Quick Actions</h3>
                    <GlassButton variant="secondary" className="w-full justify-start" onClick={handleNewTranslation}>
                      <FileText className="w-4 h-4 mr-2" />
                      New Translation
                    </GlassButton>
                    <GlassButton variant="secondary" className="w-full justify-start" onClick={() => document.getElementById('file-upload').click()}>
                      <Upload className="w-4 h-4 mr-2" />
                      Upload File
                    </GlassButton>
                    <GlassButton variant="secondary" className="w-full justify-start" onClick={() => handlePageChange('history')}>
                      <History className="w-4 h-4 mr-2" />
                      View History
                    </GlassButton>
                    <GlassButton variant="secondary" className="w-full justify-start" onClick={exportHistory}>
                      <Download className="w-4 h-4 mr-2" />
                      Export History
                    </GlassButton>
                  </div>

                  {/* Voice Input */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Voice Input</h3>
                    <div className="p-4 bg-slate-50/50 dark:bg-slate-800/50 rounded-xl">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Voice Input</span>
                        <GlassSwitch checked={isListening} onChange={handleVoiceInput} />
                      </div>
                      {isRecording && (
                        <div className="flex items-center space-x-2">
                          <div className="flex space-x-1">
                            {[...Array(5)].map((_, i) => (
                              <motion.div
                                key={i}
                                className="w-1 bg-indigo-500 rounded-full"
                                animate={{ height: [4, 20, 4] }}
                                transition={{ duration: 0.5, repeat: Infinity, delay: i * 0.1 }}
                              />
                            ))}
                          </div>
                          <span className="text-xs text-slate-500 dark:text-slate-400">Listening...</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Recent Files */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Recent Files</h3>
                      <GlassButton variant="ghost" size="sm" onClick={() => setRecentFiles([])}>
                        <Trash2 className="w-3 h-3" />
                      </GlassButton>
                    </div>
                    {recentFiles.length === 0 ? (
                      <p className="text-sm text-slate-500 dark:text-slate-400">No recent files</p>
                    ) : (
                      <div className="space-y-2 max-h-32 overflow-y-auto scrollbar-premium">
                        {recentFiles.map((file, index) => (
                          <div key={file.id} className="flex items-center space-x-2 p-2 bg-slate-50/50 dark:bg-slate-800/50 rounded-lg hover:bg-slate-100/50 dark:hover:bg-slate-700/50 transition-colors">
                            <File className="w-4 h-4 text-slate-500" />
                            <span className="text-sm text-slate-600 dark:text-slate-400 truncate flex-1">{file.name}</span>
                            <GlassButton variant="ghost" size="sm" onClick={() => setRecentFiles(prev => prev.filter(f => f.id !== file.id))}>
                              <X className="w-3 h-3" />
                            </GlassButton>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Favorites */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Favorites</h3>
                      <GlassButton variant="ghost" size="sm" onClick={() => setFavorites([])}>
                        <Trash2 className="w-3 h-3" />
                      </GlassButton>
                    </div>
                    {favorites.length === 0 ? (
                      <p className="text-sm text-slate-500 dark:text-slate-400">No favorites yet</p>
                    ) : (
                      <div className="space-y-2 max-h-32 overflow-y-auto scrollbar-premium">
                        {favorites.map((item, index) => (
                          <div key={item.id} className="flex items-center space-x-2 p-2 bg-slate-50/50 dark:bg-slate-800/50 rounded-lg hover:bg-slate-100/50 dark:hover:bg-slate-700/50 transition-colors">
                            <Heart className="w-4 h-4 text-red-500" />
                            <span className="text-sm text-slate-600 dark:text-slate-400 truncate flex-1">{item.sourceText}</span>
                            <GlassButton variant="ghost" size="sm" onClick={() => removeFavorite(item.id)}>
                              <X className="w-3 h-3" />
                            </GlassButton>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Statistics */}
                  <div className="space-y-2">
                    <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Statistics</h3>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="text-center p-3 bg-slate-50/50 dark:bg-slate-800/50 rounded-lg">
                        <div className="text-lg font-bold text-slate-900 dark:text-slate-100">{history.length}</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Translations</div>
                      </div>
                      <div className="text-center p-3 bg-slate-50/50 dark:bg-slate-800/50 rounded-lg">
                        <div className="text-lg font-bold text-slate-900 dark:text-slate-100">{favorites.length}</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Favorites</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </motion.aside>

          {/* Main Content Area */}
          <div className="flex-1 p-6">
            <motion.div 
              className="grid grid-cols-1 xl:grid-cols-3 gap-6"
              variants={staggerChildren}
              initial="initial"
              animate="animate"
            >
              
              {/* Translation Interface */}
              <div className="xl:col-span-2 space-y-6">
                
                {/* Main Translation Card */}
                <motion.div
                  className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-2 border-slate-200/60 dark:border-slate-700/60 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500 p-10"
                  variants={fadeInUp}
                >
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100 mb-2">
                        Translate Text
                      </h2>
                      <p className="text-slate-500 dark:text-slate-400">
                        Enter your text and select languages to translate
                      </p>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      <GlassSwitch checked={autoDetect} onChange={setAutoDetect} />
                      <span className="text-sm text-slate-600 dark:text-slate-400 font-semibold">
                        Auto-detect
                </span>
              </div>
            </div>

                  {/* Enhanced Language Selection */}
                  <div className="grid md:grid-cols-3 gap-12 mb-12">
                    <div className="space-y-4">
                      <label className="block text-sm font-bold text-slate-800 dark:text-slate-200 mb-6 uppercase tracking-wider">
                        Source Language
                      </label>
                      <div className="relative p-2">
                        <GlassSelect 
                          value={sourceLang} 
                          onChange={(e) => setSourceLang(e.target.value)}
                          className="w-full border-3 border-slate-300/70 dark:border-slate-600/70 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 px-6 py-4 text-lg font-semibold"
                        >
                          {languages.map(lang => (
                            <option key={lang.code} value={lang.code}>
                              {lang.flag} {lang.name}
                            </option>
                          ))}
                        </GlassSelect>
                      </div>
                    </div>
                    
                    <div className="flex items-end justify-center">
                      <motion.button
                        className="p-6 bg-gradient-to-br from-indigo-500 to-blue-500 hover:from-indigo-600 hover:to-blue-600 text-white border-3 border-indigo-400/50 dark:border-indigo-300/50 rounded-3xl transition-all duration-300 shadow-2xl hover:shadow-3xl backdrop-blur-sm"
                        onClick={handleSwapLanguages}
                        whileHover={{ scale: 1.1, rotate: 180 }}
                        whileTap={{ scale: 0.9 }}
                      >
                        <ArrowUpDown className="w-8 h-8" />
                      </motion.button>
            </div>

                    <div className="space-y-4">
                      <label className="block text-sm font-bold text-slate-800 dark:text-slate-200 mb-6 uppercase tracking-wider">
                        Target Language
                      </label>
                      <div className="relative p-2">
                        <GlassSelect 
                          value={targetLang} 
                          onChange={(e) => setTargetLang(e.target.value)}
                          className="w-full border-3 border-slate-300/70 dark:border-slate-600/70 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 px-6 py-4 text-lg font-semibold"
                        >
                          {languages.map(lang => (
                            <option key={lang.code} value={lang.code}>
                              {lang.flag} {lang.name}
                            </option>
                          ))}
                        </GlassSelect>
                      </div>
                </div>
              </div>
              
                  {/* Text Areas */}
                  <div className="grid md:grid-cols-2 gap-6 mb-8">
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 uppercase tracking-wide">
                        Source text
                      </label>
                      <div className="relative">
                        <GlassTextarea
                          value={sourceText}
                          onChange={(e) => setSourceText(e.target.value)}
                          placeholder="Enter text to translate..."
                          className="h-48 text-base leading-relaxed border-2 border-slate-300/60 dark:border-slate-600/60 rounded-2xl shadow-lg focus:shadow-xl transition-all duration-300"
                        />
                        <div className="absolute bottom-3 right-3 flex space-x-2">
                          <motion.button
                            className={`p-2 rounded-lg transition-colors backdrop-blur-sm ${
                              isListening 
                                ? 'bg-red-100/80 text-red-600 dark:bg-red-900/20 dark:text-red-400' 
                                : 'hover:bg-white/50 dark:hover:bg-slate-800/50 text-slate-500'
                            }`}
                            onClick={handleVoiceInput}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                          >
                            {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                          </motion.button>
                        </div>
                </div>
              </div>
              
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 uppercase tracking-wide">
                        Translation
                      </label>
                      <div className="relative">
                        <GlassTextarea
                          value={translatedText}
                          readOnly
                          placeholder="Translation will appear here..."
                          className="h-48 text-base leading-relaxed bg-slate-50/60 dark:bg-slate-800/60 border-2 border-slate-300/60 dark:border-slate-600/60 rounded-2xl shadow-lg"
                        />
                        {translatedText && (
                          <AnimatePresence>
                            <motion.div 
                              className="absolute bottom-3 right-3 flex space-x-2"
                              initial={{ opacity: 0, scale: 0.8 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ duration: 0.3 }}
                            >
                              <motion.button 
                                className="p-2 hover:bg-white/50 dark:hover:bg-slate-800/50 rounded-lg transition-colors text-slate-500 backdrop-blur-sm"
                                onClick={handleCopy}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                              >
                                <Copy className="w-4 h-4" />
                              </motion.button>
                              <motion.button 
                                className="p-2 hover:bg-white/50 dark:hover:bg-slate-800/50 rounded-lg transition-colors text-slate-500 backdrop-blur-sm"
                                onClick={handleShare}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                              >
                                <Share2 className="w-4 h-4" />
                              </motion.button>
                              <motion.button 
                                className="p-2 hover:bg-white/50 dark:hover:bg-slate-800/50 rounded-lg transition-colors text-slate-500 backdrop-blur-sm"
                                onClick={() => handleFavorite({ sourceText, translatedText, sourceLang, targetLang })}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                              >
                                <Heart className="w-4 h-4" />
                              </motion.button>
                            </motion.div>
                          </AnimatePresence>
                        )}
              </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center justify-between">
                    <motion.button
                      onClick={handleTranslate}
                      disabled={!sourceText.trim() || isTranslating}
                      className="inline-flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white font-bold rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed text-lg backdrop-blur-sm border-2 border-indigo-500/20 hover:border-indigo-400/40"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {isTranslating ? (
                        <>
                          <motion.div
                            className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                          />
                          <span>Translating...</span>
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-5 h-5" />
                          <span>Translate</span>
                        </>
                      )}
                    </motion.button>
                    
                    <div className="flex items-center space-x-3">
                      <GlassButton
                        variant="ghost"
                        size="md"
                        onClick={handleSettings}
                        className="flex items-center space-x-2"
                      >
                        <Settings className="w-4 h-4" />
                        <span>Advanced</span>
                      </GlassButton>
                      
                      <input
                        type="file"
                        accept=".txt,.doc,.docx,.pdf"
                        onChange={handleFileUpload}
                        className="hidden"
                        id="file-upload"
                      />
                      <label htmlFor="file-upload">
                        <GlassButton variant="secondary" size="md" className="flex items-center space-x-2">
                          <Upload className="w-4 h-4" />
                          <span>Upload</span>
                        </GlassButton>
                      </label>
                    </div>
                  </div>

                  {/* Advanced Options */}
                  <AnimatePresence>
                    {showAdvanced && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className="mt-8 pt-8 border-t border-slate-200/50 dark:border-slate-700/50"
                      >
                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 uppercase tracking-wide">
                              Model
                            </label>
                            <GlassSelect value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
                              {models.map(model => (
                                <option key={model.id} value={model.id}>
                                  {model.name} - {model.description} ({model.price})
                                </option>
                              ))}
                            </GlassSelect>
                          </div>
                          <div>
                            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 uppercase tracking-wide">
                              Quality
                            </label>
                            <GlassSelect>
                              <option>Balanced</option>
                              <option>Speed</option>
                              <option>Accuracy</option>
                            </GlassSelect>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>

                {/* Batch Upload Card */}
                <motion.div
                  className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-2 border-slate-200/60 dark:border-slate-700/60 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500 p-6"
                  variants={fadeInUp}
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
                      Batch Translation
                    </h3>
                    <GlassButton variant="secondary" size="sm" onClick={() => document.getElementById('csv-upload').click()}>
                      <Upload className="w-4 h-4 mr-2" />
                      Upload CSV
                    </GlassButton>
                  </div>
                  <div className="border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-2xl p-8 text-center hover:border-indigo-400 dark:hover:border-indigo-500 transition-colors duration-300">
                    <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/20 rounded-xl flex items-center justify-center mx-auto mb-4">
                      <Upload className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
                    </div>
                    <p className="text-slate-600 dark:text-slate-400 font-semibold">
                      Upload a CSV file to translate multiple texts at once
                    </p>
                  </div>
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="csv-upload"
                  />
                </motion.div>
              </div>

              {/* Right Column - Analytics & History */}
              <div className="space-y-6">
                
                {/* Usage Analytics */}
                <motion.div
                  className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-2 border-slate-200/60 dark:border-slate-700/60 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500 p-6"
                  variants={fadeInUp}
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
                      Usage Analytics
                    </h3>
                    <div className="p-2 bg-indigo-100 dark:bg-indigo-900/20 rounded-lg">
                      <BarChart3 className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                    </div>
                  </div>
                  
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between text-sm mb-3">
                        <span className="text-slate-600 dark:text-slate-400 font-semibold">Characters used</span>
                        <span className="font-bold text-slate-900 dark:text-slate-100">
                          {usageStats.used.toLocaleString()} / {usageStats.limit.toLocaleString()}
                        </span>
                      </div>
                      <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
                        <motion.div
                          className="bg-gradient-to-r from-indigo-500 to-blue-500 h-2 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${(usageStats.used / usageStats.limit) * 100}%` }}
                          transition={{ duration: 2, ease: "easeOut" }}
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-3">
                      <div className="text-center p-4 bg-slate-50/50 dark:bg-slate-800/50 rounded-xl">
                        <div className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-1">24</div>
                        <div className="text-sm text-slate-500 dark:text-slate-400 font-semibold">Today</div>
                      </div>
                      <div className="text-center p-4 bg-slate-50/50 dark:bg-slate-800/50 rounded-xl">
                        <div className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-1">156</div>
                        <div className="text-sm text-slate-500 dark:text-slate-400 font-semibold">This Week</div>
                      </div>
                    </div>
                    
                    <GlassButton variant="glass" className="w-full" onClick={handleUpgrade}>
                      <Lightning className="w-4 h-4 mr-2" />
                      Upgrade Plan
                    </GlassButton>
                  </div>
                </motion.div>

                {/* Recent History */}
                <motion.div
                  className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-2 border-slate-200/60 dark:border-slate-700/60 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500 p-6"
                  variants={fadeInUp}
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
                      Recent Translations
                    </h3>
                    <div className="flex items-center space-x-2">
                      <div className="p-2 bg-green-100 dark:bg-green-900/20 rounded-lg">
                        <History className="w-5 h-5 text-green-600 dark:text-green-400" />
                      </div>
                      <GlassButton variant="ghost" size="sm" onClick={clearHistory}>
                        <Trash2 className="w-4 h-4" />
                      </GlassButton>
                    </div>
                  </div>
                  
                  <div className="space-y-3 max-h-96 overflow-y-auto scrollbar-premium">
                    {history.length === 0 ? (
                      <div className="text-center py-8">
                        <div className="w-12 h-12 bg-slate-100 dark:bg-slate-800 rounded-xl flex items-center justify-center mx-auto mb-4">
                          <Clock className="w-6 h-6 text-slate-400" />
                        </div>
                        <p className="text-slate-500 dark:text-slate-400 font-semibold">
                          No recent translations
                        </p>
                      </div>
                    ) : (
                      history.map((item, index) => (
                        <motion.div
                          key={item.id}
                          className="p-4 bg-slate-50/50 dark:bg-slate-800/50 rounded-xl cursor-pointer hover:bg-slate-100/50 dark:hover:bg-slate-700/50 transition-all duration-300 border border-slate-200/50 dark:border-slate-700/50"
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.3, delay: index * 0.1 }}
                          whileHover={{ scale: 1.01 }}
                          onClick={() => {
                            setSourceText(item.sourceText);
                            setTranslatedText(item.translatedText);
                            setSourceLang(item.sourceLang);
                            setTargetLang(item.targetLang);
                          }}
                        >
                          <div className="flex items-start justify-between">
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate mb-1">
                                {item.sourceText}
                              </p>
                              <p className="text-sm text-slate-600 dark:text-slate-400 truncate">
                                {item.translatedText}
                              </p>
                            </div>
                            <div className="flex items-center space-x-2 ml-3">
                              <span className="text-xs text-slate-500 dark:text-slate-400 bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded-lg font-semibold">
                                {item.sourceLang}→{item.targetLang}
                              </span>
                            </div>
                          </div>
                        </motion.div>
                      ))
                    )}
                  </div>
                </motion.div>

                {/* Settings */}
                <motion.div
                  className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-2 border-slate-200/60 dark:border-slate-700/60 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500 p-6"
                  variants={fadeInUp}
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
                      Settings
                    </h3>
                    <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
                      <Settings className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                    </div>
                  </div>
                  
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                          Auto-detect language
                        </p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          Automatically detect source language
                        </p>
                      </div>
                      <GlassSwitch checked={autoDetect} onChange={setAutoDetect} />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                          Show advanced options
                        </p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          Display model selector and BLEU metrics
                        </p>
                      </div>
                      <GlassSwitch checked={showAdvanced} onChange={setShowAdvanced} />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                          Dark mode
                        </p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          Switch between light and dark themes
                        </p>
                      </div>
                      <GlassSwitch checked={isDarkMode} onChange={setIsDarkMode} />
                    </div>
                  </div>
                </motion.div>
              </div>
            </motion.div>
            </div>
          </div>
        </main>

      {/* Amazing Footer */}
      <motion.footer 
        className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-t border-slate-200/50 dark:border-slate-700/50 mt-16"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            
            {/* Company Info */}
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                  <Globe className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100">LinguaFlow Pro</h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Enterprise Translation Platform</p>
                </div>
              </div>
              <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                Enterprise-grade GPU-optimized translation platform powered by RTX 5060 Ti. 
                Sub-2-second responses with professional reliability for global businesses.
              </p>
              <div className="flex items-center space-x-4">
                <GlassButton variant="ghost" size="sm" className="p-2">
                  <Github className="w-5 h-5" />
                </GlassButton>
                <GlassButton variant="ghost" size="sm" className="p-2">
                  <Twitter className="w-5 h-5" />
                </GlassButton>
                <GlassButton variant="ghost" size="sm" className="p-2">
                  <Linkedin className="w-5 h-5" />
                </GlassButton>
                <GlassButton variant="ghost" size="sm" className="p-2">
                  <Facebook className="w-5 h-5" />
                </GlassButton>
              </div>
            </div>

            {/* Features */}
            <div className="space-y-4">
              <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Features</h4>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">Real-time Translation</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">Voice Input</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">Batch Processing</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">History & Favorites</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">API Access</span>
                </div>
              </div>
            </div>

            {/* Support */}
            <div className="space-y-4">
              <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Support</h4>
              <div className="space-y-2">
                <GlassButton variant="ghost" className="w-full justify-start">
                  <HelpCircle className="w-4 h-4 mr-2" />
                  Help Center
                </GlassButton>
                <GlassButton variant="ghost" className="w-full justify-start">
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Contact Us
                </GlassButton>
                <GlassButton variant="ghost" className="w-full justify-start">
                  <Phone className="w-4 h-4 mr-2" />
                  Phone Support
                </GlassButton>
                <GlassButton variant="ghost" className="w-full justify-start">
                  <Mail className="w-4 h-4 mr-2" />
                  Email Support
                </GlassButton>
                <GlassButton variant="ghost" className="w-full justify-start">
                  <BookOpen className="w-4 h-4 mr-2" />
                  Documentation
                </GlassButton>
              </div>
            </div>

            {/* Newsletter */}
            <div className="space-y-4">
              <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Stay Updated</h4>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Get the latest updates, tips, and new features delivered to your inbox.
              </p>
              <div className="space-y-3">
                <GlassInput placeholder="Enter your email" />
                <GlassButton variant="primary" className="w-full">
                  <Mail className="w-4 h-4 mr-2" />
                  Subscribe
                </GlassButton>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="w-4 h-4 text-green-500" />
                <span className="text-xs text-slate-500 dark:text-slate-400">
                  We respect your privacy. Unsubscribe anytime.
                </span>
              </div>
            </div>
          </div>

          {/* Bottom Section */}
          <div className="border-t border-slate-200/50 dark:border-slate-700/50 mt-12 pt-8">
            <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
              <div className="flex items-center space-x-6">
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  © 2024 Translate Pro. All rights reserved.
                </p>
                <div className="flex items-center space-x-4">
                  <GlassButton variant="ghost" size="sm">
                    Privacy Policy
                  </GlassButton>
                  <GlassButton variant="ghost" size="sm">
                    Terms of Service
                  </GlassButton>
                  <GlassButton variant="ghost" size="sm">
                    Cookie Policy
                  </GlassButton>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <StarIcon className="w-4 h-4 text-yellow-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">4.9/5 Rating</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Users className="w-4 h-4 text-blue-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">10K+ Users</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Award className="w-4 h-4 text-purple-500" />
                  <span className="text-sm text-slate-600 dark:text-slate-400">Award Winning</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.footer>
      </div>
  );
};

export default App;