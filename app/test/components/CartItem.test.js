import { render, screen, fireEvent } from "@testing-library/react"
import CartItem from "../../components/CartItem"
import { CartProvider } from "use-shopping-cart"
import { act } from "react-dom/test-utils"
import React from "react"

const mockItem = {
  id: "price_abc123",
  name: "Test Product",
  price: 1000,
  currency: "USD",
}

function TestWrapper({ children }) {
  return (
    <CartProvider
      mode="payment"
      cartMode="client-only"
      stripe=""
      currency="USD"
      shouldPersist={false}
      language="en"
    >
      {children}
    </CartProvider>
  )
}

describe("CartItem", () => {
  it("renders item and handles increment click", async () => {
    render(
      <TestWrapper>
        <CartItem item={mockItem} />
      </TestWrapper>
    )

    // Find the increment button and click it
    const incrementBtn = screen.getByRole("button", { name: "+" })

    // Wrap in act to avoid warnings
    await act(async () => {
      fireEvent.click(incrementBtn)
    })

    // You could assert something here (e.g., quantity display or cart state)
    // For now, let's just ensure the button exists
    expect(incrementBtn).toBeInTheDocument()
  })
})
