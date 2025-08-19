import React from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Calendar, 
  MapPin, 
  DollarSign, 
  AlertTriangle,
  BarChart3,
  Users,
  Leaf
} from 'lucide-react';
import Layout from '../components/Layout';
import { useAuth } from '../contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const stats = [
    {
      title: 'Total Crops',
      value: '3',
      change: '+1',
      icon: <Leaf className="w-6 h-6" />,
      color: 'bg-green-500'
    },
    {
      title: 'Active Loans',
      value: '₹45,000',
      change: '-₹5,000',
      icon: <DollarSign className="w-6 h-6" />,
      color: 'bg-blue-500'
    },
    {
      title: 'Weather Alert',
      value: '1',
      change: 'New',
      icon: <AlertTriangle className="w-6 h-6" />,
      color: 'bg-yellow-500'
    },
    {
      title: 'Market Trend',
      value: '↗️',
      change: '+12%',
      icon: <TrendingUp className="w-6 h-6" />,
      color: 'bg-purple-500'
    }
  ];

  const quickActions = [
    {
      title: 'Check Market Prices',
      description: 'Get latest mandi prices for your crops',
      icon: <BarChart3 className="w-5 h-5" />,
      action: () => console.log('Market prices')
    },
    {
      title: 'Weather Forecast',
      description: 'View 7-day weather forecast',
      icon: <MapPin className="w-5 h-5" />,
      action: () => console.log('Weather forecast')
    },
    {
      title: 'Loan Status',
      description: 'Check your loan repayment status',
      icon: <DollarSign className="w-5 h-5" />,
      action: () => console.log('Loan status')
    },
    {
      title: 'Crop Calendar',
      description: 'View farming calendar and reminders',
      icon: <Calendar className="w-5 h-5" />,
      action: () => console.log('Crop calendar')
    }
  ];

  return (
    <Layout title="Dashboard">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            नमस्ते {user?.name || 'किसान'}!
          </h1>
          <p className="text-gray-600">
            आज का सारांश और आपकी फसल की जानकारी
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-sm text-green-600">{stat.change}</p>
                </div>
                <div className={`${stat.color} text-white p-3 rounded-lg`}>
                  {stat.icon}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              {quickActions.map((action, index) => (
                <motion.button
                  key={action.title}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={action.action}
                  className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors text-left"
                >
                  <div className="text-gray-600">{action.icon}</div>
                  <div>
                    <p className="font-medium text-gray-900">{action.title}</p>
                    <p className="text-sm text-gray-600">{action.description}</p>
                  </div>
                </motion.button>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">Wheat crop updated</p>
                  <p className="text-xs text-gray-600">2 hours ago</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">Loan payment received</p>
                  <p className="text-xs text-gray-600">1 day ago</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">Weather alert issued</p>
                  <p className="text-xs text-gray-600">2 days ago</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Insights */}
        <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-6 text-white">
          <h3 className="text-lg font-semibold mb-2">AI Insights</h3>
          <p className="text-green-100 mb-4">
            आपकी गेहूं की फसल के लिए मौसम अनुकूल है। अगले सप्ताह में सिंचाई की आवश्यकता हो सकती है।
          </p>
          <button className="bg-white text-green-600 px-4 py-2 rounded-lg font-medium hover:bg-green-50 transition-colors">
            और जानकारी प्राप्त करें
          </button>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
