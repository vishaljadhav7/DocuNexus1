import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";


export function Header() {


  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md shadow-sm"
    >
      <div className="container mx-auto px-6 max-w-5xl h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center transition-transform group-hover:scale-110">
            <span className="text-white font-semibold text-xl">D</span>
          </div>
          <span className="text-xl font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors">
            DocuNexus
          </span>
        </Link>

        <div className="flex items-center gap-8">
          <Link to="/sign-in">
            <Button
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg px-6 py-2 shadow-md transition-transform hover:scale-105"
            >
              Sign In
            </Button>
          </Link>
        </div>
      </div>
    </motion.header>
  );
}