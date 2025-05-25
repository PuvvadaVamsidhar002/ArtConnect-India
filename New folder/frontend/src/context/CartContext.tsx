import React, { createContext, useContext, useState, ReactNode } from 'react';

// Define the shape of the cart item
interface CartItem {
  productId: string;
  partnerId: string;
  name: string;
  price: number;
  quantity: number;
  image?: string;
}

// Define the shape of the cart context
interface CartContextType {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (productId: string, partnerId: string) => void;
  updateQuantity: (productId: string, partnerId: string, quantity: number) => void;
  clearCart: () => void;
  totalItems: number;
  totalPrice: number;
}

// Create the context with a default value
const CartContext = createContext<CartContextType | undefined>(undefined);

// Provider component
export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>([]);

  // Add an item to the cart
  const addItem = (item: CartItem) => {
    setItems(prevItems => {
      // Check if item already exists in cart
      const existingItemIndex = prevItems.findIndex(
        i => i.productId === item.productId && i.partnerId === item.partnerId
      );

      if (existingItemIndex >= 0) {
        // Update quantity if item exists
        const updatedItems = [...prevItems];
        updatedItems[existingItemIndex].quantity += item.quantity;
        return updatedItems;
      } else {
        // Add new item if it doesn't exist
        return [...prevItems, item];
      }
    });
  };

  // Remove an item from the cart
  const removeItem = (productId: string, partnerId: string) => {
    setItems(prevItems => 
      prevItems.filter(item => 
        !(item.productId === productId && item.partnerId === partnerId)
      )
    );
  };

  // Update the quantity of an item
  const updateQuantity = (productId: string, partnerId: string, quantity: number) => {
    if (quantity <= 0) {
      removeItem(productId, partnerId);
      return;
    }

    setItems(prevItems => 
      prevItems.map(item => 
        item.productId === productId && item.partnerId === partnerId
          ? { ...item, quantity }
          : item
      )
    );
  };

  // Clear the cart
  const clearCart = () => {
    setItems([]);
  };

  // Calculate total items in cart
  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);

  // Calculate total price
  const totalPrice = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  // Context value
  const value = {
    items,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    totalItems,
    totalPrice
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

// Custom hook to use the cart context
export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
