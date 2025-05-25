import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { productService, artisanService } from '../services/api';

// Hero section component
const Hero: React.FC = () => {
  return (
    <section className="relative bg-cover bg-center h-96" style={{ backgroundImage: "url('/hero-bg.jpg')" }}>
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="container mx-auto px-6 h-full flex items-center justify-center relative z-10">
        <div className="text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">Discover India's Authentic Handicrafts</h1>
          <p className="text-xl text-white mb-8">Connecting artisans with global customers through transparent, ethical marketplace</p>
          <div className="flex justify-center">
            <Link to="/categories" className="bg-orange-700 hover:bg-orange-800 text-white py-3 px-6 rounded-md mr-4">
              Explore Products
            </Link>
            <Link to="/artisans" className="bg-transparent border-2 border-white text-white py-3 px-6 rounded-md hover:bg-white hover:text-gray-800">
              Meet Artisans
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

// Category card component
interface CategoryCardProps {
  id: string;
  name: string;
  image: string;
  productCount: number;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ id, name, image, productCount }) => {
  return (
    <Link to={`/categories/${id}`} className="group">
      <div className="rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300">
        <div className="h-48 overflow-hidden">
          <img 
            src={image} 
            alt={name} 
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
        <div className="p-4 bg-white">
          <h3 className="text-lg font-semibold text-gray-800">{name}</h3>
          <p className="text-sm text-gray-600">{productCount} products</p>
        </div>
      </div>
    </Link>
  );
};

// Featured product card component
interface ProductCardProps {
  id: string;
  name: string;
  image: string;
  price: number;
  artisanName: string;
  region: string;
}

const ProductCard: React.FC<ProductCardProps> = ({ id, name, image, price, artisanName, region }) => {
  return (
    <Link to={`/products/${id}`} className="group">
      <div className="rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300">
        <div className="h-56 overflow-hidden">
          <img 
            src={image} 
            alt={name} 
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
        <div className="p-4 bg-white">
          <h3 className="text-lg font-semibold text-gray-800 group-hover:text-orange-700 transition-colors">{name}</h3>
          <p className="text-orange-700 font-medium mt-1">₹{price.toLocaleString()}</p>
          <div className="flex justify-between mt-2 text-sm text-gray-600">
            <span>By {artisanName}</span>
            <span>{region}</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

// Artisan card component
interface ArtisanCardProps {
  id: string;
  name: string;
  image: string;
  craft: string;
  location: string;
}

const ArtisanCard: React.FC<ArtisanCardProps> = ({ id, name, image, craft, location }) => {
  return (
    <Link to={`/artisans/${id}`} className="group">
      <div className="rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 bg-white">
        <div className="h-48 overflow-hidden">
          <img 
            src={image || '/default-artisan.jpg'} 
            alt={name} 
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-800 group-hover:text-orange-700 transition-colors">{name}</h3>
          <p className="text-sm text-gray-600 mt-1">{craft}</p>
          <p className="text-sm text-gray-600 mt-1">{location}</p>
        </div>
      </div>
    </Link>
  );
};

// Cultural story card component
interface StoryCardProps {
  title: string;
  excerpt: string;
  image: string;
}

const StoryCard: React.FC<StoryCardProps> = ({ title, excerpt, image }) => {
  return (
    <div className="rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 bg-white">
      <div className="h-48 overflow-hidden">
        <img 
          src={image} 
          alt={title} 
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        <p className="text-sm text-gray-600 mt-2 line-clamp-3">{excerpt}</p>
        <button className="mt-3 text-orange-700 hover:text-orange-800 font-medium">
          Read More
        </button>
      </div>
    </div>
  );
};

// Main HomePage component
const HomePage: React.FC = () => {
  const [featuredProducts, setFeaturedProducts] = useState<any[]>([]);
  const [featuredArtisans, setFeaturedArtisans] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Sample categories data (would come from API in production)
  const categories = [
    { id: '1', name: 'Textiles', image: '/category-textiles.jpg', productCount: 245 },
    { id: '2', name: 'Pottery', image: '/category-pottery.jpg', productCount: 189 },
    { id: '3', name: 'Woodwork', image: '/category-woodwork.jpg', productCount: 156 },
    { id: '4', name: 'Metalwork', image: '/category-metalwork.jpg', productCount: 132 },
    { id: '5', name: 'Jewelry', image: '/category-jewelry.jpg', productCount: 210 },
    { id: '6', name: 'Paintings', image: '/category-paintings.jpg', productCount: 98 }
  ];

  // Sample cultural stories data (would come from API in production)
  const culturalStories = [
    {
      title: 'The Art of Madhubani Painting',
      excerpt: 'Originating in the Mithila region of Bihar, Madhubani painting is characterized by geometric patterns, mythological motifs, and vibrant colors. Learn about its rich history and cultural significance.',
      image: '/story-madhubani.jpg'
    },
    {
      title: 'Pashmina: The Royal Fabric',
      excerpt: 'Discover the intricate process behind creating authentic Pashmina shawls from Kashmir, a craft that has been passed down through generations for over 600 years.',
      image: '/story-pashmina.jpg'
    },
    {
      title: 'Bronze Casting of Swamimalai',
      excerpt: 'The ancient lost-wax technique of bronze casting practiced in Swamimalai, Tamil Nadu, dates back to the Chola period. Explore how artisans keep this tradition alive today.',
      image: '/story-bronze.jpg'
    }
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch featured products
        const productsResponse = await productService.getProducts(1, 8);
        setFeaturedProducts(productsResponse.products || []);
        
        // Fetch featured artisans
        const artisansResponse = await artisanService.getArtisans(1, 4);
        setFeaturedArtisans(artisansResponse.artisans || []);
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching homepage data:', err);
        setError('Failed to load data. Please try again later.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <Hero />
      
      {/* Categories Section */}
      <section className="py-12 bg-white">
        <div className="container mx-auto px-6">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800">Explore Categories</h2>
            <Link to="/categories" className="text-orange-700 hover:text-orange-800 font-medium">
              View All Categories
            </Link>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map(category => (
              <CategoryCard 
                key={category.id}
                id={category.id}
                name={category.name}
                image={category.image}
                productCount={category.productCount}
              />
            ))}
          </div>
        </div>
      </section>
      
      {/* Featured Products Section */}
      <section className="py-12 bg-gray-50">
        <div className="container mx-auto px-6">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800">Featured Products</h2>
            <Link to="/products" className="text-orange-700 hover:text-orange-800 font-medium">
              View All Products
            </Link>
          </div>
          
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-700"></div>
            </div>
          ) : error ? (
            <div className="text-center text-red-600 py-8">{error}</div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {featuredProducts.map(product => (
                <ProductCard 
                  key={product.PRODUCT_ID}
                  id={product.PRODUCT_ID}
                  name={product.NAME}
                  image={`/products/${product.PRODUCT_ID}.jpg`}
                  price={product.PRICE}
                  artisanName={product.ARTISAN_NAME}
                  region={product.REGION_NAME}
                />
              ))}
            </div>
          )}
        </div>
      </section>
      
      {/* Transparency Banner */}
      <section className="py-12 bg-orange-700 text-white">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="md:w-1/2 mb-8 md:mb-0">
              <h2 className="text-3xl font-bold mb-4">Transparency in Every Product</h2>
              <p className="text-lg mb-6">
                Every product features a QR code that reveals the artisan's story, pricing breakdown, 
                and authenticity verification. We believe in fair trade and ethical practices.
              </p>
              <Link to="/how-it-works" className="bg-white text-orange-700 hover:bg-gray-100 py-3 px-6 rounded-md font-medium">
                Learn How It Works
              </Link>
            </div>
            <div className="md:w-1/3">
              <img src="/qr-code-demo.png" alt="QR Code Transparency" className="rounded-lg shadow-lg" />
            </div>
          </div>
        </div>
      </section>
      
      {/* Featured Artisans Section */}
      <section className="py-12 bg-white">
        <div className="container mx-auto px-6">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800">Meet Our Artisans</h2>
            <Link to="/artisans" className="text-orange-700 hover:text-orange-800 font-medium">
              View All Artisans
            </Link>
          </div>
          
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-700"></div>
            </div>
          ) : error ? (
            <div className="text-center text-red-600 py-8">{error}</div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {featuredArtisans.map(artisan => (
                <ArtisanCard 
                  key={artisan.ARTISAN_ID}
                  id={artisan.ARTISAN_ID}
                  name={artisan.NAME}
                  image={artisan.IMAGE_URL || '/default-artisan.jpg'}
                  craft={artisan.CRAFT_TYPE}
                  location={artisan.LOCATION}
                />
              ))}
            </div>
          )}
        </div>
      </section>
      
      {/* Cultural Stories Section */}
      <section className="py-12 bg-gray-50">
        <div className="container mx-auto px-6">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800">Cultural Stories</h2>
            <Link to="/stories" className="text-orange-700 hover:text-orange-800 font-medium">
              View All Stories
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {culturalStories.map((story, index) => (
              <StoryCard 
                key={index}
                title={story.title}
                excerpt={story.excerpt}
                image={story.image}
              />
            ))}
          </div>
        </div>
      </section>
      
      {/* Newsletter Section */}
      <section className="py-12 bg-gray-800 text-white">
        <div className="container mx-auto px-6">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-4">Join Our Newsletter</h2>
            <p className="text-lg mb-8">
              Subscribe to receive updates on new artisans, products, and cultural stories.
            </p>
            <form className="flex flex-col md:flex-row justify-center">
              <input 
                type="email" 
                placeholder="Your email address" 
                className="px-4 py-3 md:w-96 rounded-md md:rounded-r-none mb-4 md:mb-0 focus:outline-none text-gray-800"
              />
              <button 
                type="submit" 
                className="bg-orange-700 hover:bg-orange-800 px-6 py-3 rounded-md md:rounded-l-none font-medium"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
