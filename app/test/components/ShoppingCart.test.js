import React from "react"
import { render, screen } from "@testing-library/react"
import ShoppingCart from "../../components/ShoppingCart"

const mockUseShoppingCartDefault = {
  shouldDisplayCart: true,
  cartCount: 1,
  cartDetails: {
    price_abc123: {
      id: "price_abc123",
      name: "Test Item",
      quantity: 2,
      price: 500,
      currency: "JPY",
    },
  },
}

const mockUseShoppingCartEmpty = {
  shouldDisplayCart: true,
  cartCount: 0,
  cartDetails: {},
}

const mockUseShoppingCartHidden = {
  shouldDisplayCart: false,
  cartCount: 1,
  cartDetails: {
    price_abc123: {
      id: "price_abc123",
      name: "Hidden Item",
      quantity: 1,
      price: 100,
      currency: "JPY",
    },
  },
}

jest.mock("../../components/CartItem", () => ({ item }) => (
  <div data-testid="cart-item">{item.name}</div>
))
jest.mock("../../components/CheckoutButton", () => () => (
  <button>Mock Checkout</button>
))

// Mock module factory
jest.mock("use-shopping-cart", () => ({
  useShoppingCart: jest.fn(),
}))

// Get the mocked function
import { useShoppingCart } from "use-shopping-cart"

describe("ShoppingCart", () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it("renders cart items and total correctly when cart has items", () => {
    useShoppingCart.mockReturnValue(mockUseShoppingCartDefault)
    render(<ShoppingCart />)

    expect(screen.getByTestId("cart-item")).toHaveTextContent("Test Item")
    expect(screen.getByText("Total: ￥1000(2)")).toBeInTheDocument()
    expect(screen.getByText("Mock Checkout")).toBeInTheDocument()
  })

  it("renders empty cart message when cart is empty", () => {
    useShoppingCart.mockReturnValue(mockUseShoppingCartEmpty)
    render(<ShoppingCart />)

    expect(
      screen.getByText("You have no items in your cart")
    ).toBeInTheDocument()
  })

  it("hides the cart when shouldDisplayCart is false", () => {
    useShoppingCart.mockReturnValue(mockUseShoppingCartHidden)
    const { container } = render(<ShoppingCart />)

    expect(container.firstChild).toHaveClass("opacity-0")
  })
})
