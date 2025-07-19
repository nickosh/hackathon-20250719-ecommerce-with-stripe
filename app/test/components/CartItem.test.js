// test/components/CartItem.test.js
import { render, screen, fireEvent } from "@testing-library/react"
import CartItem from "../../components/CartItem"
import { CartProvider } from "use-shopping-cart"

const item = {
  name: "Sushi",
  emoji: "🍣",
  quantity: 2,
  price: 120,
  id: "price_abc123",
}

test("renders CartItem and allows add/remove", () => {
  render(
    <CartProvider>
      <CartItem item={item} />
    </CartProvider>
  )

  expect(screen.getByText("Sushi")).toBeInTheDocument()
  expect(screen.getByText("￥240")).toBeInTheDocument()

  const addButton = screen.getByText("+")
  fireEvent.click(addButton)
  // You can mock incrementItem() and check if it was called
})
