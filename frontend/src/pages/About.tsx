import React from 'react';
import { motion } from 'framer-motion';
import { 
  Leaf, 
  Brain, 
  Users, 
  Globe, 
  Shield, 
  Award,
  Phone,
  Mail,
  MapPin,
  Github,
  Twitter
} from 'lucide-react';
import Layout from '../components/Layout';

const About: React.FC = () => {
  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI-Powered Insights",
      description: "Advanced machine learning algorithms provide personalized farming recommendations and financial advice."
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: "Multi-Language Support",
      description: "Available in 10 Indian languages to ensure accessibility for farmers across the country."
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Secure & Private",
      description: "Your data is protected with enterprise-grade security and privacy measures."
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Community Driven",
      description: "Built with input from farmers, agricultural experts, and financial institutions."
    }
  ];

  const team = [
    {
      name: "AI & ML Team",
      role: "Machine Learning Engineers",
      description: "Developing intelligent algorithms for crop recommendations and financial analysis."
    },
    {
      name: "Agricultural Experts",
      role: "Domain Specialists",
      description: "Providing expertise in farming practices, crop management, and agricultural economics."
    },
    {
      name: "Financial Advisors",
      role: "Banking & Finance",
      description: "Ensuring accurate financial advice and loan optimization strategies."
    },
    {
      name: "User Experience",
      role: "Design & Development",
      description: "Creating intuitive interfaces that work seamlessly across devices and languages."
    }
  ];

  const stats = [
    { label: "Farmers Served", value: "10,000+" },
    { label: "Languages Supported", value: "10" },
    { label: "AI Agents", value: "5" },
    { label: "Success Rate", value: "95%" }
  ];

  return (
    <Layout title="About">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6">
            <Leaf className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            About KrishiSampann
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Empowering Indian farmers with AI-driven insights for better farming decisions, 
            financial planning, and market opportunities.
          </p>
        </motion.div>

        {/* Mission Statement */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg p-8 text-white mb-16"
        >
          <h2 className="text-2xl font-bold mb-4">Our Mission</h2>
          <p className="text-lg text-green-100">
            "Be it the seed in your hand or the loan on your head — both must be nurtured wisely to bear fruit."
          </p>
          <p className="text-green-100 mt-4">
            We believe that every farmer deserves access to intelligent, personalized advice that can transform 
            their farming practices and financial well-being. KrishiSampann bridges the gap between traditional 
            farming wisdom and modern technology.
          </p>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16"
        >
          {stats.map((stat, index) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">{stat.value}</div>
              <div className="text-gray-600">{stat.label}</div>
            </div>
          ))}
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <div key={feature.title} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="text-green-500 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Team */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Our Team</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {team.map((member, index) => (
              <div key={member.name} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-1">{member.name}</h3>
                <p className="text-green-600 font-medium mb-3">{member.role}</p>
                <p className="text-gray-600">{member.description}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Technology Stack */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Technology</h2>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Frontend</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• React with TypeScript</li>
                  <li>• Tailwind CSS</li>
                  <li>• Framer Motion</li>
                  <li>• Progressive Web App</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Backend</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• FastAPI (Python)</li>
                  <li>• PostgreSQL Database</li>
                  <li>• Redis Caching</li>
                  <li>• WebSocket Support</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">AI/ML</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• Large Language Models</li>
                  <li>• Multi-Agent System</li>
                  <li>• Voice Processing</li>
                  <li>• Vector Embeddings</li>
                </ul>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Contact */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-8"
        >
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">Get in Touch</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Phone className="w-5 h-5 text-green-500" />
                  <span className="text-gray-600">+91 1800-KRISHI</span>
                </div>
                <div className="flex items-center space-x-3">
                  <Mail className="w-5 h-5 text-green-500" />
                  <span className="text-gray-600">support@krishisampann.com</span>
                </div>
                <div className="flex items-center space-x-3">
                  <MapPin className="w-5 h-5 text-green-500" />
                  <span className="text-gray-600">Mumbai, Maharashtra, India</span>
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Follow Us</h3>
              <div className="flex space-x-4">
                <button className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
                  <Github className="w-5 h-5 text-gray-600" />
                </button>
                <button className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
                  <Twitter className="w-5 h-5 text-gray-600" />
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default About;
