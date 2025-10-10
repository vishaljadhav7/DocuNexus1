
import {
  ArrowRight,
} from "lucide-react";

import { Link } from "react-router-dom";


export const Footer = () => {
  return (   
  <footer className="py-16 bg-gray-900 text-gray-300">
     <div className="container px-6 mx-auto max-w-5xl">
       <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
         <div className="space-y-4">
           <h3 className="text-xl font-semibold text-white mb-4">
             AI Contracts
           </h3>
           <p className="text-sm">
             Empowering teams with intelligent contract solutions that save
             time and reduce risk.
           </p>
           <div className="flex gap-4 pt-4">
             {[
               {
                 name: "twitter",
                 icon: <ArrowRight className="w-5 h-5 text-white" />,
               },
               {
                 name: "linkedin",
                 icon: <ArrowRight className="w-5 h-5 text-white" />,
               },
               {
                 name: "facebook",
                 icon: <ArrowRight className="w-5 h-5 text-white" />,
               },
             ].map((social) => (
               <Link
                 key={social.name}
                 to="/"
                 className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors"
               >
                 <span className="sr-only">{social.name}</span>
                 {social.icon}
               </Link>
             ))}
           </div>
         </div>
         <div>
           <h3 className="text-lg font-semibold text-white mb-4">
             Product
           </h3>
           <ul className="space-y-3 text-sm">
             {["Features", "Pricing", "Use Cases", "Security"].map(
               (item) => (
                 <li key={item}>
                   <Link
                     to="/"
                     className="hover:text-white transition-colors"
                   >
                     {item}
                   </Link>
                 </li>
               )
             )}
           </ul>
         </div>
         <div>
           <h3 className="text-lg font-semibold text-white mb-4">
             Company
           </h3>
           <ul className="space-y-3 text-sm">
             {["About", "Blog", "Careers", "Contact"].map((item) => (
               <li key={item}>
                 <Link
                   to="/"
                   className="hover:text-white transition-colors"
                 >
                   {item}
                 </Link>
               </li>
             ))}
           </ul>
         </div>
         <div>
           <h3 className="text-lg font-semibold text-white mb-4">
             Get in Touch
           </h3>
           <ul className="space-y-3 text-sm">
             <li className="flex items-center gap-3">
               <svg
                 className="w-4 h-4"
                 fill="none"
                 stroke="currentColor"
                 viewBox="0 0 24 24"
               >
                 <path
                   strokeLinecap="round"
                   strokeLinejoin="round"
                   strokeWidth="2"
                   d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                 />
               </svg>
               <span>hello@aicontracts.com</span>
             </li>
             <li className="flex items-center gap-3">
               <svg
                 className="w-4 h-4"
                 fill="none"
                 stroke="currentColor"
                 viewBox="0 0 24 24"
               >
                 <path
                   strokeLinecap="round"
                   strokeLinejoin="round"
                   strokeWidth="2"
                   d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                 />
               </svg>
               <span>+1 (555) 987-6543</span>
             </li>
             <li className="flex items-center gap-3">
               <svg
                 className="w-4 h-4"
                 fill="none"
                 stroke="currentColor"
                 viewBox="0 0 24 24"
               >
                 <path
                   strokeLinecap="round"
                   strokeLinejoin="round"
                   strokeWidth="2"
                   d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                 />
                 <path
                   strokeLinecap="round"
                   strokeLinejoin="round"
                   strokeWidth="2"
                   d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                 />
               </svg>
               <span>123 AI Street, San Francisco, CA</span>
             </li>
           </ul>
         </div>
       </div>
       <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center gap-4">
         <p className="text-sm">
           © {new Date().getFullYear()} AI Contracts. All rights reserved.
         </p>
         <div className="flex gap-6">
           <Link
             to="/"
             className="text-sm hover:text-white transition-colors"
           >
             Privacy Policy
           </Link>
           <Link
             to="/"
             className="text-sm hover:text-white transition-colors"
           >
             Terms of Service
           </Link>
           <Link
             to="/"
             className="text-sm hover:text-white transition-colors"
           >
             Cookie Policy
           </Link>
         </div>
       </div>
     </div>
   </footer>

  )
}
 