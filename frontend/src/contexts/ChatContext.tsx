import React, { createContext, useContext, useState, useEffect, useRef, ReactNode } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  type: 'text' | 'voice' | 'system';
  metadata?: {
    language?: string;
    confidence?: number;
    audioUrl?: string;
    voice_ready?: string[];
    intent?: string;
    suggestions?: string[];
  };
}

interface ChatContextType {
  messages: Message[];
  isLoading: boolean;
  sendMessage: (text: string, language: string) => Promise<void>;
  clearMessages: () => void;
  isConnected: boolean;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const { user } = useAuth();

  // Mock AI responses for demonstration
  const mockAIResponses = {
    'crop advice': 'आपकी मिट्टी और मौसम के अनुसार, इस सीजन में गेहूं, सरसों या चना की खेती अच्छी रहेगी। मैं आपको विस्तृत जानकारी दे सकता हूं।',
    'loan help': 'कृषि ऋण के लिए आप PM-Kisan योजना, KCC कार्ड या बैंक ऋण का लाभ उठा सकते हैं। क्या आप किसी विशेष योजना के बारे में जानना चाहते हैं?',
    'market prices': 'आज के मंडी भाव: गेहूं ₹2,100-2,300/quintal, धान ₹1,800-2,000/quintal, मक्का ₹1,500-1,700/quintal। क्या आप किसी विशेष फसल का भाव जानना चाहते हैं?',
    'risk alert': 'आपके क्षेत्र में अगले 3 दिनों में बारिश की संभावना है। फसल सुरक्षा के लिए उचित उपाय करें।',
    'farming calendar': 'इस महीने के लिए: गेहूं की बुवाई का सही समय है, सरसों की कटाई करें, और नई फसलों की योजना बनाएं।',
    'local schemes': 'आपके राज्य में कई सरकारी योजनाएं उपलब्ध हैं: मिट्टी स्वास्थ्य कार्ड, फसल बीमा, और सब्सिडी। क्या आप किसी विशेष योजना के बारे में जानना चाहते हैं?'
  };

  useEffect(() => {
    // Add welcome message when component mounts
    addMessage({
      id: Date.now().toString(),
      text: `नमस्ते ${user?.name || 'किसान'}! मैं KrishiMitra आपकी कैसे मदद कर सकता हूं? बोलकर अपना सवाल पूछें - फसल, ऋण, मंडी भाव, मौसम या सरकारी योजनाओं के बारे में।`,
      sender: 'ai',
      timestamp: new Date(),
      type: 'system',
      metadata: {
        voice_ready: [`नमस्ते ${user?.name || 'किसान'}! मैं KrishiMitra आपकी कैसे मदद कर सकता हूं?`, "बोलकर अपना सवाल पूछें - फसल, ऋण, मंडी भाव, मौसम या सरकारी योजनाओं के बारे में।"],
        intent: 'welcome',
        suggestions: ['फसल की सलाह लें', 'ऋण की जानकारी लें', 'मंडी भाव जानें', 'मौसम की जानकारी लें']
      }
    });
  }, []); // Only run once on mount

  useEffect(() => {
    // Only try to connect if we have a user or are in anonymous mode
    if (user || true) { // Always try to connect, even anonymously
      console.log('Attempting WebSocket connection...');
      connectWebSocket();
    } else {
      console.log('No user available, using mock responses');
    }

    return () => {
      console.log('Cleaning up WebSocket connection...');
      if (wsRef.current) {
        // Only close if the connection is actually open or connecting
        if (wsRef.current.readyState === WebSocket.OPEN || wsRef.current.readyState === WebSocket.CONNECTING) {
          wsRef.current.close(1000, 'Component unmounting');
        }
      }
    };
  }, []); // Remove user dependency to prevent reconnection loops

  const connectWebSocket = () => {
    try {
      // Close existing connection if any
      if (wsRef.current) {
        if (wsRef.current.readyState === WebSocket.OPEN || wsRef.current.readyState === WebSocket.CONNECTING) {
          console.log('Closing existing WebSocket connection...');
          wsRef.current.close(1000, 'Reconnecting');
        }
      }

      const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';
      const clientId = user?.id || 'anonymous';
      
      console.log(`Connecting to WebSocket: ${wsUrl}/${clientId}`);
      wsRef.current = new WebSocket(`${wsUrl}/${clientId}`);
      
      wsRef.current.onopen = () => {
        console.log('✅ WebSocket connected successfully');
        setIsConnected(true);
      };
      
      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 WebSocket message received:', data);
          handleWebSocketMessage(data);
        } catch (error) {
          console.error('❌ Error parsing WebSocket message:', error);
        }
      };
      
      wsRef.current.onclose = (event) => {
        console.log(`🔌 WebSocket disconnected - Code: ${event.code}, Reason: ${event.reason}`);
        setIsConnected(false);
        
        // Only attempt to reconnect if it wasn't a clean close
        if (event.code !== 1000) {
          console.log('🔄 Attempting to reconnect in 3 seconds...');
          setTimeout(() => {
            if (wsRef.current?.readyState === WebSocket.CLOSED) {
              connectWebSocket();
            }
          }, 3000);
        }
      };
      
      wsRef.current.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        setIsConnected(false);
      };
    } catch (error) {
      console.error('❌ Error connecting to WebSocket:', error);
      setIsConnected(false);
    }
  };

  const handleWebSocketMessage = (data: any) => {
    // Handle KrishiMitra response format
    if (data.text) {
      addMessage({
        id: Date.now().toString(),
        text: data.text,
        sender: 'ai',
        timestamp: new Date(),
        type: 'text',
        metadata: {
          language: data.language,
          confidence: data.confidence,
          voice_ready: data.voice_ready,
          intent: data.intent,
          suggestions: data.suggestions
        }
      });
    } else if (data.type === 'error') {
      addMessage({
        id: Date.now().toString(),
        text: 'माफ़ करें, कुछ गलत हो गया। कृपया फिर से कोशिश करें।',
        sender: 'ai',
        timestamp: new Date(),
        type: 'system'
      });
    }
  };

  const addMessage = (message: Message) => {
    setMessages(prev => [...prev, message]);
  };

  const sendMessage = async (text: string, language: string) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
      type: 'text',
      metadata: { language }
    };

    addMessage(userMessage);
    setIsLoading(true);

    try {
      // Try WebSocket first if available
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          message: text,
          language,
          user_id: user?.id
        }));
      } else {
        // Fallback to mock responses
        await sendMockResponse(text, language);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      addMessage({
        id: (Date.now() + 1).toString(),
        text: 'माफ़ करें, कुछ गलत हो गया। कृपया फिर से कोशिश करें।',
        sender: 'ai',
        timestamp: new Date(),
        type: 'system'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const sendMockResponse = async (text: string, language: string) => {
    // Simulate KrishiMitra processing delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    // Generate contextual response
    let response = '';
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('crop') || lowerText.includes('फसल')) {
      response = mockAIResponses['crop advice'];
    } else if (lowerText.includes('loan') || lowerText.includes('ऋण') || lowerText.includes('कर्ज')) {
      response = mockAIResponses['loan help'];
    } else if (lowerText.includes('market') || lowerText.includes('मंडी') || lowerText.includes('भाव')) {
      response = mockAIResponses['market prices'];
    } else if (lowerText.includes('risk') || lowerText.includes('जोखिम') || lowerText.includes('मौसम')) {
      response = mockAIResponses['risk alert'];
    } else if (lowerText.includes('calendar') || lowerText.includes('कैलेंडर')) {
      response = mockAIResponses['farming calendar'];
    } else if (lowerText.includes('scheme') || lowerText.includes('योजना')) {
      response = mockAIResponses['local schemes'];
    } else {
      // Generic response
      response = 'आपका सवाल बहुत अच्छा है! मैं आपकी मदद करने की कोशिश करूंगा। क्या आप किसी विशेष विषय के बारे में जानना चाहते हैं?';
    }
    
    addMessage({
      id: Date.now().toString(),
      text: response,
      sender: 'ai',
      timestamp: new Date(),
      type: 'text',
      metadata: { language }
    });
  };

  const sendMessageViaAPI = async (text: string, language: string) => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/chat/send`, {
        message: text,
        language,
        user_id: user?.id
      });
      
      if (response.data.success) {
        addMessage({
          id: Date.now().toString(),
          text: response.data.response,
          sender: 'ai',
          timestamp: new Date(),
          type: 'text',
          metadata: { language }
        });
      }
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  };

  const clearMessages = () => {
    setMessages([]);
  };

  const value: ChatContextType = {
    messages,
    isLoading,
    sendMessage,
    clearMessages,
    isConnected
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};
