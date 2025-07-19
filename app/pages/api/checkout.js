import Stripe from "stripe"

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: "2023-10-16",
})

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST")
    return res.status(405).end("Method Not Allowed")
  }

  try {
    const { cartDetails } = req.body

    if (!cartDetails || typeof cartDetails !== "object") {
      return res.status(400).json({ error: "Invalid cart" })
    }

    const line_items = Object.values(cartDetails).map((item) => ({
      price_data: {
        currency: "jpy",
        product_data: {
          name: item.name,
        },
        unit_amount: item.price, // JPY unit (e.g. 500 = ¥500)
      },
      quantity: item.quantity,
    }))

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      line_items,
      mode: "payment",
      success_url: `${process.env.NEXT_PUBLIC_SITE_URL}/success`,
      cancel_url: `${process.env.NEXT_PUBLIC_SITE_URL}/cancel`,
    })

    return res.status(200).json({ sessionId: session.id })
  } catch (error) {
    console.error("Stripe error:", error)
    return res.status(500).json({ error: "Internal Server Error" })
  }
}
