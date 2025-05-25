import React from 'react';
import { Link } from 'react-router-dom';

interface HeaderProps {
  isAuthenticated?: boolean;
  cartItemCount?: number;
}

const Header: React.FC<HeaderProps> = ({ isAuthenticated = false, cartItemCount = 0 }) => {
  return (
    <header className="bg-white shadow-md py-4 sticky top-0 z-50">
      <div className="container mx-auto px-6 flex items-center justify-between">
        <div className="text-xl font-bold text-orange-700">
          <Link to="/">HandcraftHeritage</Link>
        </div>
        <nav className="hidden lg:flex space-x-10">
          <Link to="/" className="text-gray-600 hover:text-orange-700">Home</Link>
          <Link to="/categories" className="text-gray-600 hover:text-orange-700">Categories</Link>
          <Link to="/artisans" className="text-gray-600 hover:text-orange-700">Artisans</Link>
          <Link to="/stories" className="text-gray-600 hover:text-orange-700">Cultural Stories</Link>
          <Link to="/how-it-works" className="text-gray-600 hover:text-orange-700">How It Works</Link>
        </nav>
        <div className="flex items-center space-x-4">
          <button className="text-gray-600 hover:text-orange-700">
            <i className="fas fa-search text-lg"></i>
          </button>
          <Link to="/cart" className="text-gray-600 hover:text-orange-700 relative">
            <i className="fas fa-shopping-cart text-lg"></i>
            {cartItemCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-orange-700 rounded-full w-5 h-5 flex items-center justify-center text-white text-xs">
                {cartItemCount}
              </span>
            )}
          </Link>
          {isAuthenticated ? (
            <Link to="/profile" className="text-gray-600 hover:text-orange-700">
              <i className="fas fa-user text-lg"></i>
            </Link>
          ) : (
            <Link to="/login" className="hidden md:block bg-orange-700 hover:bg-orange-800 text-white py-2 px-4 rounded-md">
              Sign In
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
