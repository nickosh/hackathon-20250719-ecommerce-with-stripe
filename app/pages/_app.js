import Layout from "@/components/Layout"
import "@/styles/globals.css"
import { CartProvider } from "use-shopping-cart"
import React from "react"

export default function App({ Component, pageProps }) {
  return (
    <CartProvider
      mode="payment"
      cartMode="client-only"
      stripe={process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY}
      successUrl={`${process.env.NEXT_PUBLIC_SITE_URL}/success`}
      cancelUrl={`${process.env.NEXT_PUBLIC_SITE_URL}/?success=false`}
      currency="JPY"
      allowedCountries={["JP"]}
      shouldPersist={true}
    >
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </CartProvider>
  )
}
