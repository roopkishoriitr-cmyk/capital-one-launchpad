import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Mic, MicOff, Phone, PhoneOff, Video, VideoOff, Settings, MessageSquare,
  User, Bot, Volume2, VolumeX, Camera, CameraOff, MoreVertical, Minimize2, Maximize2
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { toast } from 'react-hot-toast';

const Chat: React.FC = () => {
  const { user } = useAuth();
  const [selectedLanguage, setSelectedLanguage] = useState('hi');
  
  // Video call states
  const [isVideoOn, setIsVideoOn] = useState(true);
  const [isAudioOn, setIsAudioOn] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showControls, setShowControls] = useState(true);
  const [isKrishiMitraSpeaking, setIsKrishiMitraSpeaking] = useState(false);
  const [currentSpeaker, setCurrentSpeaker] = useState<'farmer' | 'krishimitra' | null>(null);
  const [realtimeSession, setRealtimeSession] = useState<any>(null);
  const [isRealtimeActive, setIsRealtimeActive] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const krishiMitraVideoRef = useRef<HTMLVideoElement>(null);

  // Languages
  const languages = [
    { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
    { code: 'bn', name: 'বাংলা', flag: '🇮🇳' },
    { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
    { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
    { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
    { code: 'gu', name: 'ગુજરાતી', flag: '🇮🇳' },
    { code: 'pa', name: 'ਪੰਜਾਬੀ', flag: '🇮🇳' },
    { code: 'or', name: 'ଓଡ଼ିଆ', flag: '🇮🇳' },
    { code: 'ml', name: 'മലയാളം', flag: '🇮🇳' },
    { code: 'kn', name: 'ಕನ್ನಡ', flag: '🇮🇳' },
    { code: 'en', name: 'English', flag: '🇮🇳' }
  ];

  const startRealtimeSession = async () => {
    try {
      setIsLoading(true);
      toast.success('🔄 KrishiMitra Realtime session शुरू हो रहा है...');
      
      console.log('🎤 Starting realtime session...');
      console.log('📝 Language:', selectedLanguage);
      console.log('👤 User ID:', user?.id);
      
      const response = await fetch('/api/v1/voice/realtime/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          voice: 'alloy', 
          language: selectedLanguage, 
          user_id: user?.id,
          farmer_context: {
            location: "Punjab, India",
            crops: ["wheat", "rice", "cotton"],
            experience: "15 years",
            land_size: "10 acres",
            current_concerns: ["loan repayment", "crop selection", "market prices"]
          }
        }),
      });

      console.log('📡 Response status:', response.status);
      console.log('📡 Response headers:', response.headers);

      if (!response.ok) { 
        const errorText = await response.text();
        console.error('❌ Response error:', errorText);
        throw new Error(`Failed to create realtime session: ${response.status} ${errorText}`); 
      }

      const sessionData = await response.json();
      console.log('✅ Session data received:', sessionData);
      
      setRealtimeSession(sessionData);
      setIsRealtimeActive(true);
      setCurrentSpeaker('krishimitra');
      setIsKrishiMitraSpeaking(true);
      
      toast.success('✅ KrishiMitra Realtime session सक्रिय है! अब आप बोल सकते हैं।');
      
      // Simulate KrishiMitra speaking
      setTimeout(() => {
        setIsKrishiMitraSpeaking(false);
        setCurrentSpeaker(null);
      }, 3000);
      
    } catch (error) {
      console.error('❌ Error starting realtime session:', error);
      toast.error('❌ Realtime session शुरू करने में समस्या। कृपया फिर से कोशिश करें।');
    } finally {
      setIsLoading(false);
    }
  };

  const stopRealtimeSession = () => {
    console.log('🛑 Stopping realtime session...');
    setRealtimeSession(null);
    setIsRealtimeActive(false);
    setCurrentSpeaker(null);
    setIsKrishiMitraSpeaking(false);
    toast.success('🛑 KrishiMitra Realtime session बंद हो गया है।');
  };

  // Video call controls
  const toggleVideo = () => setIsVideoOn(!isVideoOn);
  const toggleAudio = () => setIsMuted(!isMuted);
  const toggleFullscreen = () => setIsFullscreen(!isFullscreen);

  return (
    <div className={`min-h-screen bg-gradient-to-br from-green-50 to-blue-50 ${isFullscreen ? 'fixed inset-0 z-50' : ''}`}>
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">KrishiMitra Voice Call</h1>
                <p className="text-sm text-gray-500">
                  {isRealtimeActive ? '🟢 Realtime Active' : '🔴 Realtime Inactive'}
                  {realtimeSession && ` • Session: ${realtimeSession.session_id?.slice(-8)}`}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                {languages.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
              
              <button
                onClick={toggleFullscreen}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                {isFullscreen ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Video Call Interface */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-200px)]">
          
          {/* Farmer's Video Panel */}
          <div className="relative bg-gray-900 rounded-xl overflow-hidden shadow-2xl">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center text-white">
                <User className="w-24 h-24 mx-auto mb-4 opacity-50" />
                <p className="text-lg font-semibold">{user?.name || 'किसान'}</p>
                <p className="text-sm opacity-75">आपका वीडियो</p>
              </div>
            </div>
            
            {/* Speaking indicator */}
            {currentSpeaker === 'farmer' && (
              <div className="absolute top-4 left-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm animate-pulse">
                🗣️ बोल रहे हैं
              </div>
            )}
            
            {/* Audio indicator */}
            {isMuted && (
              <div className="absolute top-4 right-4 bg-gray-800 text-white px-3 py-1 rounded-full text-sm">
                🔇 म्यूट
              </div>
            )}
          </div>

          {/* KrishiMitra's Video Panel */}
          <div className="relative bg-gray-900 rounded-xl overflow-hidden shadow-2xl">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center text-white">
                <Bot className="w-24 h-24 mx-auto mb-4 opacity-50" />
                <p className="text-lg font-semibold">KrishiMitra AI</p>
                <p className="text-sm opacity-75">AI सहायक</p>
              </div>
            </div>
            
            {/* AI Status */}
            <div className="absolute top-4 right-4 flex space-x-2">
              <div className={`px-3 py-1 rounded-full text-sm ${
                isRealtimeActive 
                  ? 'bg-blue-500 text-white animate-pulse' 
                  : 'bg-green-500 text-white'
              }`}>
                {isRealtimeActive ? '🔄 Realtime' : 'AI सक्रिय'}
              </div>
            </div>
            
            {/* Speaking indicator */}
            {isKrishiMitraSpeaking && (
              <div className="absolute bottom-4 left-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm animate-pulse">
                🗣️ बोल रहा है
              </div>
            )}
          </div>
        </div>

        {/* Control Panel */}
        <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between">
            
            {/* Left Controls */}
            <div className="flex items-center space-x-4">
              <button onClick={toggleAudio} className={`p-4 rounded-full transition-all duration-200 ${isMuted ? 'bg-red-500 text-white hover:bg-red-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
                {isMuted ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
              </button>
              
              <button onClick={toggleVideo} className={`p-4 rounded-full transition-all duration-200 ${!isVideoOn ? 'bg-red-500 text-white hover:bg-red-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
                {isVideoOn ? <Video className="w-6 h-6" /> : <VideoOff className="w-6 h-6" />}
              </button>
            </div>

            {/* Center - Call Controls */}
            <div className="flex items-center space-x-4">
              <button 
                onClick={stopRealtimeSession} 
                disabled={!isRealtimeActive}
                className={`p-4 rounded-full transition-colors ${
                  isRealtimeActive 
                    ? 'bg-red-500 text-white hover:bg-red-600' 
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                <PhoneOff className="w-6 h-6" />
              </button>
              
              <button 
                onClick={startRealtimeSession} 
                disabled={isRealtimeActive || isLoading}
                className={`p-4 rounded-full transition-colors ${
                  isRealtimeActive || isLoading
                    ? 'bg-green-600 text-white cursor-not-allowed' 
                    : 'bg-green-500 text-white hover:bg-green-600'
                }`}
              >
                {isLoading ? (
                  <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Phone className="w-6 h-6" />
                )}
              </button>
            </div>

            {/* Right Controls */}
            <div className="flex items-center space-x-4">
              <button className="p-4 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors">
                <Settings className="w-6 h-6" />
              </button>
              
              <button className="p-4 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors">
                <MoreVertical className="w-6 h-6" />
              </button>
            </div>
          </div>

          {/* Status Information */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {isRealtimeActive ? '🎤 Voice Session Active' : '📞 Start Voice Session'}
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                {isRealtimeActive 
                  ? 'KrishiMitra is ready to help you with farming advice. Speak naturally!'
                  : 'Click the green phone button to start a voice conversation with KrishiMitra.'
                }
              </p>
              
              {realtimeSession && (
                <div className="bg-gray-50 rounded-lg p-4 text-left">
                  <h4 className="font-medium text-gray-900 mb-2">Session Details:</h4>
                  <div className="text-sm text-gray-600 space-y-1">
                    <p><strong>Session ID:</strong> {realtimeSession.session_id}</p>
                    <p><strong>Model:</strong> {realtimeSession.model}</p>
                    <p><strong>Voice:</strong> {realtimeSession.voice}</p>
                    <p><strong>Language:</strong> {realtimeSession.language}</p>
                    <p><strong>Status:</strong> {realtimeSession.status}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-white border-t mt-6">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between text-sm text-gray-500">
            <span>Powered by KrishiMitra AI</span>
            <span>OpenAI Realtime API • Voice-First AI Assistant</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
