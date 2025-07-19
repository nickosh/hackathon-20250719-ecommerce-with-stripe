let mockRedirectToCheckout // ← just a declaration, no initial value

jest.mock("@stripe/stripe-js", () => {
  const fn = jest.fn() // create the spy
  mockRedirectToCheckout = fn // assign to outer scope

  return {
    loadStripe: () => Promise.resolve({ redirectToCheckout: fn }),
  }
})

/* ---------- 3.  Mock use-shopping-cart ---------- */
const mockCart = {
  cartCount: 1,
  cartDetails: {
    price_abc123: {
      id: "price_abc123",
      name: "Test Product",
      price: 1000,
      quantity: 1,
      currency: "USD",
    },
  },
}
jest.mock("use-shopping-cart", () => ({
  useShoppingCart: () => mockCart,
}))

/* ---------- 4.  Mock global fetch BEFORE component import ---------- */
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ sessionId: "mock_session_id" }),
  })
)

/* ---------- 5.  NOW import React / RTL / component ---------- */
import React from "react"
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import CheckoutButton from "../../components/CheckoutButton"

/* ---------- 6.  Tests ---------- */
describe("CheckoutButton", () => {
  beforeEach(() => jest.clearAllMocks())

  it("shows error when cart is empty", async () => {
    mockCart.cartCount = 0
    render(<CheckoutButton />)

    fireEvent.click(screen.getByRole("button"))
    await waitFor(() =>
      expect(
        screen.getByText("Please add some items to your cart")
      ).toBeInTheDocument()
    )
  })

  it("redirects to Stripe when cart has items", async () => {
    mockCart.cartCount = 1
    render(<CheckoutButton />)

    fireEvent.click(screen.getByRole("button"))
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled()
      expect(mockRedirectToCheckout).toHaveBeenCalledWith({
        sessionId: "mock_session_id",
      })
    })
  })

  it("disables button when cart has more than 20 items", () => {
    mockCart.cartCount = 21
    render(<CheckoutButton />)

    expect(screen.getByRole("button")).toBeDisabled()
    expect(
      screen.getByText("You cannot have more than 20 items")
    ).toBeInTheDocument()
  })
})
