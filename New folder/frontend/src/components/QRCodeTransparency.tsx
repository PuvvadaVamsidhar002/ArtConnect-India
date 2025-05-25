import React, { useState, useEffect } from 'react';
import { qrCodeService } from '../services/api';

interface QRCodeTransparencyProps {
  productId: string;
}

const QRCodeTransparency: React.FC<QRCodeTransparencyProps> = ({ productId }) => {
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('');
  const [transparencyData, setTransparencyData] = useState<any>(null);
  const [showTransparency, setShowTransparency] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Get QR code URL
    const qrUrl = qrCodeService.getProductQRCode(productId);
    setQrCodeUrl(qrUrl);
  }, [productId]);

  const handleShowTransparency = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (!transparencyData) {
        const data = await qrCodeService.getTransparencyData(productId);
        setTransparencyData(data);
      }
      
      setShowTransparency(true);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching transparency data:', err);
      setError('Failed to load transparency data. Please try again later.');
      setLoading(false);
    }
  };

  return (
    <div>
      {/* QR Code Display */}
      <div className="flex items-center space-x-4 mb-6">
        <div className="w-24 h-24 border rounded-md overflow-hidden">
          {qrCodeUrl ? (
            <img src={qrCodeUrl} alt="Product QR Code" className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full bg-gray-100 flex items-center justify-center">
              <span className="text-gray-400">QR Code</span>
            </div>
          )}
        </div>
        <div>
          <h3 className="font-semibold">Scan for Authenticity</h3>
          <p className="text-sm text-gray-600">
            Scan this QR code to verify product authenticity and see artisan details
          </p>
          <button
            onClick={handleShowTransparency}
            disabled={loading}
            className="mt-2 text-orange-700 hover:text-orange-800 text-sm font-medium"
          >
            {loading ? 'Loading...' : 'View Transparency Details'}
          </button>
          {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
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

export default QRCodeTransparency;
