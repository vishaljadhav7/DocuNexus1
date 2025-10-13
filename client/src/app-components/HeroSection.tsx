import {
  ArrowRight,
  Sparkles,
  Star,
  User,
  Clock,
  Upload,
  Search,
  FileText,
  Shield,
  AlertCircle,
  ChevronRight,
  BarChart2,
  FileCheck,
  AlertTriangle
} from "lucide-react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button"
import { Link } from "react-router-dom";
import { Header, Footer } from "./index";


export const HeroSection = () => {
  const features = [
    {
      title: "Smart Analysis",
      desc: "Get AI-driven insights in seconds",
      color: "from-blue-100 to-blue-50",
      icon: <Sparkles className="w-5 h-5 text-blue-600" />,
    },
    {
      title: "Risk Detection",
      desc: "Instantly identify potential issues",
      color: "from-teal-100 to-teal-50",
      icon: <Shield className="w-5 h-5 text-teal-600" />,
    },
    {
      title: "Time Efficiency",
      desc: "Reduce review time by up to 90%",
      color: "from-purple-100 to-purple-50",
      icon: <Clock className="w-5 h-5 text-purple-600" />,
    },
  ];

  const testimonials = [
    {
      quote:
        "This platform transformed our workflow, saving hours on every contract review.",
      author: "Emma T.",
      position: "General Counsel",
      company: "LegalTech Inc.",
      icon: <User className="w-10 h-10 text-indigo-600" />,
    },
    {
      quote:
        "The AI insights have helped us identify critical issues we would have missed otherwise.",
      author: "Michael R.",
      position: "Contract Manager",
      company: "Enterprise Solutions",
      icon: <User className="w-10 h-10 text-indigo-600" />,
    },
  ];

  const companies = ["Notion", "Dribble", "Dropbox"];

  return (
    <>
    <Header/>
    <div className="min-h-screen bg-gray-50 font-sans ">
      <main>
        {/* Hero Section */}
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="py-20 md:py-32 bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100"
        >
          <div className="container px-6 mx-auto max-w-5xl">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              {/* Hero intro */}
              <div className="text-center lg:text-left">
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="inline-flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm mb-6 border border-gray-200"
                >
                  <Sparkles className="w-4 h-4 text-indigo-500" />
                  <span className="text-sm font-medium text-gray-700">Powered by AI</span>
                </motion.div>
                <h1 className="text-4xl md:text-5xl font-semibold tracking-tight mb-6 text-gray-900">
                  Simplify Contracts with <span className="text-indigo-600">AI Precision</span>
                </h1>
                <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto lg:mx-0">
                  Review smarter, reduce risks, and save time with intelligent contract analysis built for your team.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                  <Link to="/sign-up">
                    <Button
                      size="lg"
                      className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg px-8 py-3 shadow-md transition-transform hover:scale-105"
                    >
                      Try for Free <ArrowRight className="ml-2 w-5 h-5" />
                    </Button>
                  </Link>
                  <Button
                    size="lg"
                    variant="outline"
                    className="border-gray-300 bg-white hover:bg-gray-50 text-gray-700 font-medium rounded-lg px-8 py-3 shadow-md transition-transform hover:scale-105"
                  >
                    Watch Demo
                  </Button>
                </div>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                  className="mt-12"
                >
                  <p className="text-sm text-gray-500 mb-4">Trusted by leading companies</p>
                  <div className="flex flex-wrap gap-6 justify-center lg:justify-start">
                    {companies.map((company, index) => (
                      <span key={index} className="text-gray-500 font-medium hover:text-gray-700 transition-colors">
                        {company}
                      </span>
                    ))}
                  </div>
                </motion.div>
              </div>

              {/* Contract card */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="relative hidden md:block"
              >
                <div className="relative bg-white rounded-2xl shadow-2xl overflow-hidden border border-gray-100 p-8">
                  {/* Gradient header bar with enhanced design */}
                  <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500"></div>

                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="bg-indigo-50 p-1.5 rounded-md">
                          <FileText className="w-5 h-5 text-indigo-600" />
                        </div>
                        <span className="font-semibold text-gray-900">Contract Analysis</span>
                      </div>
                      <div className="flex items-center gap-2 bg-green-50 px-3 py-1 rounded-full border border-green-100">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-sm text-green-700 font-medium">Processing</span>
                      </div>
                    </div>

                    {/* Document sections with improved visual design */}
                    <div className="space-y-4">
                      <div className="h-8 bg-gray-100 rounded-md w-full flex items-center px-3">
                        <div className="w-4 h-4 bg-indigo-200 rounded-full mr-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-1/3"></div>
                      </div>
                      <div className="h-8 bg-gray-100 rounded-md w-3/4 flex items-center px-3">
                        <div className="w-4 h-4 bg-green-200 rounded-full mr-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-1/4"></div>
                      </div>
                      <div className="h-8 bg-gray-100 rounded-md w-5/6 flex items-center px-3">
                        <div className="w-4 h-4 bg-amber-200 rounded-full mr-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-2/5"></div>
                      </div>
                      <div className="h-8 bg-gray-100 rounded-md w-2/3 flex items-center px-3">
                        <div className="w-4 h-4 bg-red-200 rounded-full mr-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-1/4"></div>
                      </div>
                    </div>

                    {/* Enhanced alert cards */}
                    <div className="flex items-center gap-3 bg-indigo-50 p-4 rounded-lg border border-indigo-100">
                      <div className="bg-white p-1.5 rounded-full shadow-sm">
                        <AlertCircle className="text-indigo-600 w-5 h-5 flex-shrink-0" />
                      </div>
                      <div>
                        <div className="text-sm font-semibold text-gray-900">Risk detected in Section 3.2</div>
                        <div className="text-xs text-gray-500">Liability clause needs review</div>
                      </div>
                      <div className="ml-auto bg-indigo-100 rounded-full p-1">
                        <ChevronRight className="w-4 h-4 text-indigo-600" />
                      </div>
                    </div>

                    <div className="flex items-center gap-3 bg-green-50 p-4 rounded-lg border border-green-100">
                      <div className="bg-white p-1.5 rounded-full shadow-sm">
                        <Shield className="text-green-600 w-5 h-5 flex-shrink-0" />
                      </div>
                      <div>
                        <div className="text-sm font-semibold text-gray-900">Compliant with regulations</div>
                        <div className="text-xs text-gray-500">All required clauses present</div>
                      </div>
                      <div className="ml-auto bg-green-100 rounded-full p-1">
                        <ChevronRight className="w-4 h-4 text-green-600" />
                      </div>
                    </div>

                    {/* Enhanced footer */}
                    <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
                      <div className="text-sm text-gray-500 flex items-center gap-1.5">
                        <Clock className="w-4 h-4 text-gray-400" />
                        Analysis complete: 2 min ago
                      </div>
                      <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-4">
                        View Report
                      </Button>
                    </div>
                  </div>
                </div>

                {/* Enhanced floating cards */}
                <div className="absolute -bottom-6 -left-6 bg-white p-4 rounded-lg shadow-lg border border-gray-100 flex items-center gap-3">
                  <div className="bg-red-50 p-1.5 rounded-full">
                    <AlertTriangle className="text-red-500 w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-900">Risk detected</div>
                    <div className="text-xs text-gray-500">Section 3.2</div>
                  </div>
                </div>

                <div className="absolute -top-4 -right-4 bg-white p-4 rounded-lg shadow-lg border border-gray-100">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-sm font-semibold text-gray-900">Analysis complete</span>
                  </div>
                </div>

                {/* Additional floating elements */}
                <div className="absolute top-1/3 -right-5 bg-white p-3 rounded-lg shadow-lg border border-gray-100">
                  <div className="flex flex-col items-center gap-1">
                    <BarChart2 className="text-indigo-600 w-5 h-5" />
                    <span className="text-xs font-semibold text-gray-900">3 Insights</span>
                  </div>
                </div>

                <div className="absolute top-1/4 -left-5 bg-white p-3 rounded-lg shadow-lg border border-gray-100">
                  <div className="flex flex-col items-center gap-1">
                    <FileCheck className="text-green-600 w-5 h-5" />
                    <span className="text-xs font-semibold text-gray-900">Verified</span>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </motion.section>

        {/* Features Section */}
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="py-20 bg-gradient-to-br from-gray-50 to-blue-50"
        >
          <div className="container px-6 mx-auto max-w-5xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-semibold mb-4 text-gray-900">
                Why Teams Choose Us
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Discover how our AI transforms contract management.
              </p>
            </motion.div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="p-6 rounded-xl bg-white shadow-sm hover:shadow-md transition-shadow border border-gray-100"
                >
                  <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-gray-900">
                    {feature.title}
                  </h3>
                  <p className="text-base text-gray-600">{feature.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.section>

        {/* How It Works Section */}
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="py-20 bg-white"
        >
          <div className="container px-6 mx-auto max-w-5xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-semibold mb-4 text-gray-900">
                How It Works
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Three simple steps to revolutionize your contract reviews.
              </p>
            </motion.div>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  step: "01",
                  title: "Upload",
                  desc: "Upload your contract document in any format",
                  icon: <Upload className="w-8 h-8 text-indigo-600" />,
                },
                {
                  step: "02",
                  title: "Analyze",
                  desc: "Our AI engine analyzes the entire document",
                  icon: <Search className="w-8 h-8 text-indigo-600" />,
                },
                {
                  step: "03",
                  title: "Review",
                  desc: "Get detailed insights and recommendations",
                  icon: <FileText className="w-8 h-8 text-indigo-600" />,
                },
              ].map((item, index) => (
                <motion.div
                  key={item.step}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="text-center"
                >
                  <div className="flex justify-center mb-4">{item.icon}</div>
                  <div className="bg-indigo-50 text-indigo-600 font-semibold text-lg w-12 h-12 rounded-full flex items-center justify-center mb-4 mx-auto">
                    {item.step}
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-gray-900">
                    {item.title}
                  </h3>
                  <p className="text-base text-gray-600">{item.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.section>

        {/* Testimonials Section */}
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="py-20 bg-gradient-to-br from-gray-50 to-indigo-50"
        >
          <div className="container px-6 mx-auto max-w-5xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-semibold mb-4 text-gray-900">
                Trusted by Professionals
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Hear from teams who’ve transformed their workflow.
              </p>
            </motion.div>
            <div className="grid md:grid-cols-2 gap-8">
              {testimonials.map((testimonial, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100"
                >
                  <div className="flex justify-start mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className="w-5 h-5 text-yellow-400 fill-current"
                      />
                    ))}
                  </div>
                  <p className="text-base text-gray-600 italic mb-4">
                    {testimonial.quote} 
                  </p>
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center">
                      {testimonial.icon}
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">
                        {testimonial.author}
                      </div>
                      <div className="text-sm text-gray-500">
                        {testimonial.position}, {testimonial.company}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.section>

        {/* CTA Section */}
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="py-20 bg-gradient-to-r from-indigo-600 via-blue-600 to-purple-600 text-white"
        >
          <div className="container px-6 mx-auto max-w-5xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-semibold mb-4">
                Get Started Today
              </h2>
              <p className="text-lg mb-8 text-indigo-100">
                Join thousands of teams optimizing contracts with AI. Try it
                free.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/sign-up">
                  <Button
                    size="lg"
                    className="bg-white text-indigo-600 hover:bg-gray-50 font-medium rounded-lg px-8 py-3 shadow-md transition-transform hover:scale-105"
                  >
                    Try for Free <ArrowRight className="ml-2 w-5 h-5" />
                  </Button>
                </Link>
                <Link to="/">
                  <Button
                    size="lg"
                    variant="outline"
                    className="border-white/30 bg-transparent hover:bg-white/10 text-white font-medium rounded-lg px-8 py-3 transition-transform hover scale-105"
                  >
                    Contact Sales
                  </Button>
                </Link>
              </div>
            </motion.div>
          </div>
        </motion.section>

        {/* Footer */}
        <Footer/>
      </main>
    </div>
    </>
  );
}
