import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface User {
  id: string;
  phone_number: string;
  name: string;
  language: string;
  state: string;
  district: string;
  village: string;
  land_area: number;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (phoneNumber: string, name: string, language: string, state: string, district: string, village: string, landArea: number) => Promise<void>;
  logout: () => void;
  register: (userData: Omit<User, 'id' | 'created_at'>) => Promise<void>;
  updateUser: (userData: Partial<User>) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored user data on app load
    const storedUser = localStorage.getItem('krishisampann_user');
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        setUser(userData);
      } catch (error) {
        console.error('Error parsing stored user data:', error);
        localStorage.removeItem('krishisampann_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (
    phoneNumber: string,
    name: string,
    language: string,
    state: string,
    district: string,
    village: string,
    landArea: number
  ) => {
    try {
      setIsLoading(true);
      
      // Check if user exists
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/users/phone/${phoneNumber}`);
      
      if (response.data) {
        // User exists, update with new data
        const updatedUser = await axios.put(`${process.env.REACT_APP_API_URL}/api/v1/users/${response.data.id}`, {
          name,
          language,
          state,
          district,
          village,
          land_area: landArea
        });
        
        setUser(updatedUser.data);
        localStorage.setItem('krishisampann_user', JSON.stringify(updatedUser.data));
      } else {
        // User doesn't exist, create new user
        const newUser = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/users/register`, {
          phone_number: phoneNumber,
          name,
          language,
          state,
          district,
          village,
          land_area: landArea
        });
        
        setUser(newUser.data);
        localStorage.setItem('krishisampann_user', JSON.stringify(newUser.data));
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: Omit<User, 'id' | 'created_at'>) => {
    try {
      setIsLoading(true);
      
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/users/register`, userData);
      
      setUser(response.data);
      localStorage.setItem('krishisampann_user', JSON.stringify(response.data));
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateUser = async (userData: Partial<User>) => {
    if (!user) throw new Error('No user logged in');
    
    try {
      setIsLoading(true);
      
      const response = await axios.put(`${process.env.REACT_APP_API_URL}/api/v1/users/${user.id}`, userData);
      
      const updatedUser = { ...user, ...response.data };
      setUser(updatedUser);
      localStorage.setItem('krishisampann_user', JSON.stringify(updatedUser));
    } catch (error) {
      console.error('Update user error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('krishisampann_user');
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    register,
    updateUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
