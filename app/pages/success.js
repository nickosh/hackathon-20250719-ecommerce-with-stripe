import { useEffect } from 'react';
import { useShoppingCart } from 'use-shopping-cart';

export default function Success() {
  const { clearCart } = useShoppingCart();

  useEffect(() => {
    // Clear the cart when component mounts
    clearCart();
  }, [clearCart]);

  return (
    <div className="text-center p-8">
      <h1 className="text-xl mb-4">Thank you for your purchase! 🛍️</h1>
      <p className="text-green-600 mb-4">Your order has been successfully processed.</p>
      <a href="/" className="inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
        Return to Home
      </a>
    </div>
  );
}