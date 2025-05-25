import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { productService, qrCodeService, partnerService } from '../services/api';
import { useCart } from '../context/CartContext';

interface ProductPageParams {
  id: string;
}

const ProductPage: React.FC = () => {
  const { id } = useParams<ProductPageParams>();
  const [product, setProduct] = useState<any>(null);
  const [partners, setPartners] = useState<any[]>([]);
  const [selectedPartner, setSelectedPartner] = useState<any>(null);
  const [quantity, setQuantity] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>('description');
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('');
  const [showTransparency, setShowTransparency] = useState<boolean>(false);
  const [transparencyData, setTransparencyData] = useState<any>(null);
  
  const { addItem } = useCart();

  useEffect(() => {
    const fetchProductData = async () => {
      try {
        setLoading(true);
        
        // Fetch product details
        const productData = await productService.getProductById(id);
        setProduct(productData);
        
        // Fetch partners offering this product
        const partnersData = await partnerService.getPartnersByProduct(id);
        setPartners(partnersData.partners || []);
        
        // Set default selected partner (lowest price)
        if (partnersData.partners && partnersData.partners.length > 0) {
          const sortedPartners = [...partnersData.partners].sort((a, b) => a.price - b.price);
          setSelectedPartner(sortedPartners[0]);
        }
        
        // Get QR code URL
        const qrUrl = qrCodeService.getProductQRCode(id);
        setQrCodeUrl(qrUrl);
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching product data:', err);
        setError('Failed to load product data. Please try again later.');
        setLoading(false);
      }
    };

    if (id) {
      fetchProductData();
    }
  }, [id]);

  const handlePartnerChange = (partnerId: string) => {
    const partner = partners.find(p => p.PARTNER_ID === partnerId);
    setSelectedPartner(partner);
  };

  const handleQuantityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setQuantity(parseInt(e.target.value));
  };

  const handleAddToCart = () => {
    if (product && selectedPartner) {
      addItem({
        productId: product.PRODUCT_ID,
        partnerId: selectedPartner.PARTNER_ID,
        name: product.NAME,
        price: selectedPartner.PRICE,
        quantity: quantity,
        image: `/products/${product.PRODUCT_ID}.jpg`
      });
      
      // Show confirmation message (could use a toast notification here)
      alert('Product added to cart!');
    }
  };

  const handleShowTransparency = async () => {
    try {
      if (!transparencyData) {
        const data = await qrCodeService.getTransparencyData(id);
        setTransparencyData(data);
      }
      setShowTransparency(true);
    } catch (err) {
      console.error('Error fetching transparency data:', err);
      alert('Failed to load transparency data. Please try again later.');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-700"></div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="container mx-auto px-6 py-12">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error || 'Product not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Breadcrumb */}
      <div className="bg-white py-4 shadow-sm">
        <div className="container mx-auto px-6">
          <nav className="text-sm">
            <ol className="list-none p-0 flex">
              <li className="flex items-center">
                <Link to="/" className="text-gray-600 hover:text-orange-700">Home</Link>
                <svg className="h-4 w-4 mx-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </li>
              <li className="flex items-center">
                <Link to="/categories" className="text-gray-600 hover:text-orange-700">Categories</Link>
                <svg className="h-4 w-4 mx-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </li>
              <li className="text-gray-800 font-medium">{product.NAME}</li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Product Details */}
      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Product Images */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="mb-4 h-96 overflow-hidden rounded-lg">
              <img 
                src={`/products/${product.PRODUCT_ID}.jpg`} 
                alt={product.NAME} 
                className="w-full h-full object-contain"
              />
            </div>
            <div className="grid grid-cols-4 gap-2">
              <div className="h-24 border rounded cursor-pointer hover:border-orange-700">
                <img 
                  src={`/products/${product.PRODUCT_ID}.jpg`} 
                  alt={product.NAME} 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="h-24 border rounded cursor-pointer hover:border-orange-700">
                <img 
                  src={`/products/${product.PRODUCT_ID}_2.jpg`} 
                  alt={product.NAME} 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="h-24 border rounded cursor-pointer hover:border-orange-700">
                <img 
                  src={`/products/${product.PRODUCT_ID}_3.jpg`} 
                  alt={product.NAME} 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="h-24 border rounded cursor-pointer hover:border-orange-700">
                <img 
                  src={`/products/${product.PRODUCT_ID}_4.jpg`} 
                  alt={product.NAME} 
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>

          {/* Product Info */}
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">{product.NAME}</h1>
            
            <div className="flex items-center mb-4">
              <Link to={`/artisans/${product.ARTISAN_ID}`} className="text-orange-700 hover:text-orange-800">
                By {product.ARTISAN_NAME}
              </Link>
              <span className="mx-2 text-gray-400">|</span>
              <span className="text-gray-600">{product.REGION_NAME}, {product.STATE}</span>
            </div>
            
            {selectedPartner && (
              <div className="text-2xl font-bold text-orange-700 mb-6">
                ₹{selectedPartner.PRICE.toLocaleString()}
              </div>
            )}
            
            <div className="mb-6">
              <p className="text-gray-700">{product.DESCRIPTION}</p>
            </div>
            
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Materials</h3>
              <p className="text-gray-700">{product.MATERIALS}</p>
            </div>
            
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Dimensions</h3>
              <p className="text-gray-700">{product.DIMENSIONS}</p>
            </div>
            
            {/* Partner Selection */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Select Partner Website</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {partners.map(partner => (
                  <div 
                    key={partner.PARTNER_ID}
                    className={`border rounded-lg p-4 cursor-pointer ${
                      selectedPartner && selectedPartner.PARTNER_ID === partner.PARTNER_ID 
                        ? 'border-orange-700 bg-orange-50' 
                        : 'border-gray-200 hover:border-orange-700'
                    }`}
                    onClick={() => handlePartnerChange(partner.PARTNER_ID)}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <h4 className="font-medium">{partner.NAME}</h4>
                        <div className="flex items-center mt-1">
                          <div className="flex">
                            {[...Array(5)].map((_, i) => (
                              <svg 
                                key={i}
                                className={`h-4 w-4 ${i < Math.floor(partner.RATING) ? 'text-yellow-400' : 'text-gray-300'}`}
                                fill="currentColor"
                                viewBox="0 0 20 20"
                              >
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                              </svg>
                            ))}
                          </div>
                          <span className="text-sm text-gray-600 ml-1">({partner.REVIEW_COUNT})</span>
                        </div>
                      </div>
                      <div className="text-lg font-bold text-orange-700">
                        ₹{partner.PRICE.toLocaleString()}
                      </div>
                    </div>
                    <div className="mt-2 text-sm text-gray-600">
                      <div>Shipping: ₹{partner.SHIPPING_FEE.toLocaleString()}</div>
                      <div>Delivery: {partner.ESTIMATED_DELIVERY}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Quantity Selection */}
            <div className="mb-6">
              <label htmlFor="quantity" className="block text-lg font-semibold mb-2">
                Quantity
              </label>
              <select
                id="quantity"
                value={quantity}
                onChange={handleQuantityChange}
                className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                  <option key={num} value={num}>
                    {num}
                  </option>
                ))}
              </select>
            </div>
            
            {/* Add to Cart Button */}
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 mb-8">
              <button
                onClick={handleAddToCart}
                disabled={!selectedPartner}
                className="bg-orange-700 hover:bg-orange-800 text-white py-3 px-6 rounded-md font-medium flex-1 disabled:opacity-50"
              >
                Add to Cart
              </button>
              <button
                onClick={handleShowTransparency}
                className="border border-orange-700 text-orange-700 hover:bg-orange-50 py-3 px-6 rounded-md font-medium"
              >
                View Transparency
              </button>
            </div>
            
            {/* QR Code */}
            <div className="flex items-center space-x-4 mb-6">
              <div className="w-24 h-24 border rounded-md overflow-hidden">
                <img src={qrCodeUrl} alt="Product QR Code" className="w-full h-full object-cover" />
              </div>
              <div>
                <h3 className="font-semibold">Scan for Authenticity</h3>
                <p className="text-sm text-gray-600">
                  Scan this QR code to verify product authenticity and see artisan details
                </p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Product Tabs */}
        <div className="mt-12">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8">
              <button
                onClick={() => setActiveTab('description')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'description'
                    ? 'border-orange-700 text-orange-700'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Description
              </button>
              <button
                onClick={() => setActiveTab('cultural_story')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'cultural_story'
                    ? 'border-orange-700 text-orange-700'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Cultural Story
              </button>
              <button
                onClick={() => setActiveTab('artisan')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'artisan'
                    ? 'border-orange-700 text-orange-700'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Artisan
              </button>
            </nav>
          </div>
          
          <div className="py-6">
            {activeTab === 'description' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">Product Description</h3>
                <p className="text-gray-700 mb-4">{product.DESCRIPTION}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                  <div>
                    <h4 className="font-semibold mb-2">Materials</h4>
                    <p className="text-gray-700">{product.MATERIALS}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">Dimensions</h4>
                    <p className="text-gray-700">{product.DIMENSIONS}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">Weight</h4>
                    <p className="text-gray-700">{product.WEIGHT}</p>
                  </div>
                  {product.IS_GI_TAGGED && (
                    <div>
                      <h4 className="font-semibold mb-2">GI Tagged</h4>
                      <p className="text-gray-700">This product has Geographical Indication (GI) tag, certifying its origin and quality.</p>
                    </div>
                  )}
                </div>
              </div>
            )}
            
            {activeTab === 'cultural_story' && (
              <div>
                <h3 className="text-xl font-semibold mb-4">{product.STORY_TITLE || 'Cultural Significance'}</h3>
                <p className="text-gray-700 mb-4">{product.STORY_CONTENT || 'Cultural story content not available.'}</p>
                
                {product.HISTORY && (
                  <div className="mt-6">
                    <h4 className="font-semibold mb-2">Historical Background</h4>
                    <p className="text-gray-700">{product.HISTORY}</p>
                  </div>
                )}
                
                {product.CULTURAL_SIGNIFICANCE && (
                  <div className="mt-6">
                    <h4 className="font-semibold mb-2">Cultural Significance</h4>
                    <p className="text-gray-700">{product.CULTURAL_SIGNIFICANCE}</p>
                  </div>
                )}
              </div>
            )}
            
            {activeTab === 'artisan' && (
              <div>
                <div className="flex flex-col md:flex-row">
                  <div className="md:w-1/4 mb-6 md:mb-0">
                    <div className="w-48 h-48 rounded-full overflow-hidden mx-auto">
                      <img 
                        src={product.ARTISAN_IMAGE_URL || '/default-artisan.jpg'} 
                        alt={product.ARTISAN_NAME} 
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                  <div className="md:w-3/4 md:pl-8">
                    <h3 className="text-xl font-semibold mb-2">{product.ARTISAN_NAME}</h3>
                    <p className="text-gray-600 mb-4">{product.CRAFT_TYPE} Artisan from {product.ARTISAN_LOCATION}</p>
                    
                    <p className="text-gray-700 mb-6">{product.ARTISAN_BIO || 'Artisan bio not available.'}</p>
                    
                    <Link 
                      to={`/artisans/${product.ARTISAN_ID}`}
                      className="text-orange-700 hover:text-orange-800 font-medium"
                    >
                      View Artisan Profile
                    </Link>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Transparency Modal */}
      {showTransparency && transparencyData && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Product Transparency</h2>
                <button 
                  onClick={() => setShowTransparency(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-lg font-semibold mb-4">Product Details</h3>
                  <div className="space-y-3">
                    <div>
                      <span className="font-medium">Name:</span> {transparencyData.PRODUCT_NAME}
                    </div>
                    <div>
                      <span className="font-medium">Materials:</span> {transparencyData.MATERIALS}
                    </div>
                    <div>
                      <span className="font-medium">Region:</span> {transparencyData.region.name}, {transparencyData.region.state}
                    </div>
                    {transparencyData.gi_tag && (
                      <div>
                        <span className="font-medium">GI Tag:</span> {transparencyData.gi_tag.name}
                      </div>
                    )}
                  </div>
                  
                  <h3 className="text-lg font-semibold mt-6 mb-4">Artisan Information</h3>
                  <div className="space-y-3">
                    <div>
                      <span className="font-medium">Name:</span> {transparencyData.artisan.name}
                    </div>
                    <div>
                      <span className="font-medium">Location:</span> {transparencyData.artisan.location}
                    </div>
                    <div>
                      <span className="font-medium">Craft:</span> {transparencyData.artisan.craft_type}
                    </div>
                    <div>
                      <span className="font-medium">Years Active:</span> {transparencyData.artisan.years_active}
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold mb-4">Pricing Transparency</h3>
                  
                  {transparencyData.partners && transparencyData.partners.map((partner, index) => (
                    <div key={index} className="mb-6 p-4 border rounded-lg">
                      <h4 className="font-medium mb-2">{partner.name}</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Product Price:</span>
                          <span>₹{partner.price.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Platform Fee ({partner.revenue_sharing.platform_fee_percentage}%):</span>
                          <span>₹{partner.revenue_sharing.platform_fee.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between font-medium">
                          <span>Artisan Earnings ({partner.revenue_sharing.artisan_revenue_percentage}%):</span>
                          <span>₹{partner.revenue_sharing.artisan_revenue.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between text-sm text-gray-600 pt-2 border-t">
                          <span>Shipping Fee:</span>
                          <span>₹{partner.shipping_fee.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
                    <h4 className="font-medium mb-2">Our Commitment</h4>
                    <p className="text-sm">
                      We ensure that 80-90% of the product price goes directly to the artisans and local partners, 
                      supporting traditional craftsmanship and sustainable livelihoods.
                    </p>
                  </div>
                </div>
              </div>
              
              {transparencyData.cultural_story && (
                <div className="mt-8">
                  <h3 className="text-lg font-semibold mb-4">Cultural Story</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    {transparencyData.cultural_story.title && (
                      <h4 className="font-medium mb-2">{transparencyData.cultural_story.title}</h4>
                    )}
                    {transparencyData.cultural_story.content && (
                      <p className="mb-4">{transparencyData.cultural_story.content}</p>
                    )}
                    {transparencyData.cultural_story.history && (
                      <div className="mt-4">
                        <h5 className="font-medium mb-1">Historical Background</h5>
                        <p>{transparencyData.cultural_story.history}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              <div className="mt-8 flex justify-end">
                <button 
                  onClick={() => setShowTransparency(false)}
                  className="bg-orange-700 hover:bg-orange-800 text-white py-2 px-4 rounded-md"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductPage;
