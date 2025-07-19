import { useState } from "react"
import { useShoppingCart } from "use-shopping-cart"
import { loadStripe } from "@stripe/stripe-js"
import React from "react"
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY)

export default function CheckoutButton() {
  const [status, setStatus] = useState("idle")
  const { cartCount, cartDetails } = useShoppingCart()

  const handleClick = async (event) => {
    event.preventDefault()

    if (!cartCount || cartCount === 0) {
      setStatus("no-items")
      return
    }

    setStatus("loading")

    try {
      const response = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cartDetails }),
      })

      if (!response.ok) throw new Error("Failed to create session")

      const { sessionId } = await response.json()
      const stripe = await stripePromise

      if (stripe && sessionId) {
        await stripe.redirectToCheckout({ sessionId })
      } else {
        setStatus("redirect-error")
      }
    } catch (err) {
      console.error("Stripe Redirect Error:", err)
      setStatus("redirect-error")
    }
  }

  return (
    <article className="mt-3 flex flex-col">
      <div className="text-red-700 text-xs mb-3 h-5 text-center">
        {cartCount > 20
          ? "You cannot have more than 20 items"
          : status === "redirect-error"
          ? "Unable to redirect to Stripe checkout page"
          : status === "no-items"
          ? "Please add some items to your cart"
          : null}
      </div>
      <button
        onClick={handleClick}
        className="bg-emerald-50 hover:bg-emerald-500 hover:text-white transition-colors duration-500 text-emerald-500 py-3 px-5 rounded-md w-100 disabled:bg-slate-300 disabled:cursor-not-allowed disabled:text-white"
        disabled={cartCount > 20 || status === "no-items"}
      >
        {status !== "loading" ? "Proceed to checkout" : "Loading..."}
      </button>
    </article>
  )
}
